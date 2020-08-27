import logging
import threading
import signal

from datetime import datetime
from proton.handlers import MessagingHandler
from proton.reactor import Container

import common

"""
This AMQP receiver application, receives messages, with an expected
body and properties sizes (if not met a message will be logged).
After `reconnect_after` (or CLIENT_RECONNECT_AFTER env) messages
have been received, the receiver will recycle its connection.

When executed, it will spawn multiple processes based on provided `--processes`
(or CLIENT_PROCESSES env).

You can execute it using CLI arguments, or setting environment variables.
Run with `--help` for more info.
"""

# public receiver variables (initialized after parsing)
interrupted = False
expected_body_size = 0
expected_properties_size = 0


class Receiver(MessagingHandler, threading.Thread):
    def __init__(self, opts):
        super(Receiver, self).__init__(auto_accept=True, auto_settle=True)
        threading.Thread.__init__(self)
        self.host = opts.host
        self.port = opts.port
        self.address = opts.address
        self.reconnect_after = opts.reconnect_after
        self.container = None
        self._receiver = None
        self._url = "amqp://%s:%s/%s" % (self.host, self.port, self.address)
        self._next_task = None
        # internal stats
        self._received = 0
        self._elapsed_times = list()

    def run(self):
        while not interrupted:
            logging.info("starting receiver container")
            self.container = Container(self)
            self.container.run()
            logging.warning("receiver container stopped [interrupted = %s]" % interrupted)

    def interrupt(self):
        if self._receiver:
            self._receiver.close()
            self.container.stop()

    def on_start(self, event):
        self.create_receiver(event)

    def create_receiver(self, event):
        if self._receiver is not None:
            logging.info("closing receiver")
            self._receiver.close()
            if event.connection:
                event.connection.close()
            self._reset_stats()
        logging.info("creating receiver")
        self._receiver = event.container.create_receiver(self._url)

    def on_message(self, event):
        self._received += 1
        msg = event.message
        body_size = len(msg.body)
        prop_size = 0

        elapsed_ms = -1
        if msg.properties:
            # calculate elapsed time based on incoming time property
            if "time" in msg.properties:
                before_request = datetime.now()
                # request
                now = common.get_current_time_iso()
                after_request = datetime.now()
                request_elapsed = after_request - before_request
                request_elapsed_ms = int(request_elapsed.total_seconds()*1000)

                time_sent = msg.properties['time']  # ISO Format
                elapsed = datetime.fromisoformat(now) - datetime.fromisoformat(time_sent)
                elapsed_ms = int(elapsed.total_seconds()*1000)
                # store elapsed time in ms
                self._elapsed_times.append(elapsed_ms - request_elapsed_ms)

            prop_size = sum([len(k)+len(msg.properties[k]) for k in msg.properties])

        logging.info("received [body:%d, properties:%d] - elapsed (ms): %d" % (body_size, prop_size, elapsed_ms))
        if expected_body_size != body_size:
            logging.error("incorrect body has been received [size: %d - expected size: %d]" % (
                body_size, expected_body_size))
        if expected_properties_size != prop_size:
            logging.error("incorrect properties has been received [size: %d - expected size: %d]" % (
                prop_size, expected_properties_size))
        if self._received == self.reconnect_after:
            logging.info("recycling receiver connection")
            self.create_receiver(event)

    def _reset_stats(self):
        self._received = 0
        self._e2e_times = list()


# Main flow for sender app
if __name__ == "__main__":
    parsed_opts, args = common.parse_opts(False)

    # same message body and properties will be used by all sender instances
    expected_body_size = parsed_opts.message_size
    expected_properties_size = parsed_opts.properties_size

    # initializing logging
    common.initialize_logging(parsed_opts.log_level)

    # list of spawned sender processes
    processes = list()

    # Interrupts all running senders
    def interrupt_handler(sig, f):
        global interrupted
        interrupted = True
        for receiver in processes:
            receiver.interrupt()

    # Capturing SIGINT
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)

    # spawning receiver threads
    for i in range(parsed_opts.processes):
        r = Receiver(parsed_opts)
        processes.append(r)
        r.start()

    # waiting on all threads to finish
    for t in processes:
        t.join()

    print("Exiting")
