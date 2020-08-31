import logging
import threading
import signal
import os

from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

import common

"""
This AMQP sender application, sends one message, with a pre-defined
body and properties sizes, every `interval_delay` (or CLIENT_INTERVAL_SECONDS
env) seconds. After `reconnect_after` (or CLIENT_RECONNECT_AFTER env) messages
have been accepted, the sender will recycle its connection.

When executed, it will spawn multiple threads based on provided `--processes`
(or CLIENT_PROCESSES env).

You can execute it using CLI arguments, or setting environment variables.
Run with `--help` for more info.
"""

# public sender variables (initialized after parsing)
message_body = ""
interrupted = False


class Sender(MessagingHandler, threading.Thread):
    def __init__(self, opts):
        super(Sender, self).__init__()
        threading.Thread.__init__(self)
        self.host = opts.host
        self.port = opts.port
        self.address = opts.address
        self.interval_delay = opts.interval_delay
        self.reconnect_after = opts.reconnect_after
        self.ttl = opts.ttl
        self.container = None
        self._sender = None
        self._url = "amqp://%s:%s/%s" % (self.host, self.port, self.address)
        self._next_task = None
        # internal stats
        self._sent = 0
        self._accepted = 0
        self._released = 0
        self._rejected = 0

    def run(self):
        while not interrupted:
            logging.info("starting sender container")
            self.container = Container(self)
            self.container.run()
            logging.error("sender container stopped [interrupted = %s]" % interrupted)

    def interrupt(self):
        if self._sender:
            logging.info("sender has been interrupted")
            self._sender.close()
            self.container.stop()

    def on_start(self, event):
        self.create_sender(event)

    def create_sender(self, event):
        if self._sender is not None:
            logging.info("closing sender")
            self._sender.close()
            if event.connection:
                event.connection.close()
            self._reset_stats()
        logging.info("creating sender")
        self._sender = event.container.create_sender(self._url)

    # def on_unhandled(self, method, *args):
    #     logging.error("on_unhandled - method: %s - args: %s", method, args)

    def on_sendable(self, event):
        if self._sender.credit > 0 and self._next_task is None:
            props = common.generate_application_properties(parsed_opts.properties_size)
            msg = Message(id="%s-%d" % (os.getpid(), self._sent + 1),
                          properties=props,
                          body=message_body,
                          ttl=self.ttl,
                          durable=True)
            self._sender.send(msg)
            self._sent += 1
            if self.interval_delay > 0:
                logging.debug("delaying %d secs [credit=%d]" % (self.interval_delay, self._sender.credit))
                self._next_task = event.reactor.schedule(self.interval_delay, self)

    def on_timer_task(self, event):
        logging.debug("tick")
        self._next_task = None
        self.on_sendable(event)

    def on_accepted(self, event):
        self._accepted += 1
        if self._accepted == self.reconnect_after:
            logging.info("recycling sender connection")
            self.create_sender(event)

    def on_released(self, event):
        self._released += 1
        logging.warning("message released [%s]" % event.delivery.tag)

    def on_rejected(self, event):
        self._rejected += 1
        logging.warning("message rejected [%s]" % event.delivery.tag)

    def _reset_stats(self):
        self._sent = 0
        self._accepted = 0
        self._released = 0
        self._rejected = 0


# Main flow for sender app
if __name__ == "__main__":

    # parsing arguments
    parsed_opts, args = common.parse_opts(True)

    # same message body will be used by all sender instances
    message_body = common.generate_message_body(parsed_opts.message_size, "abcdedfgijklmnopqrstuvwxyz0123456789")

    # initializing logging
    common.initialize_logging(parsed_opts.log_level)

    # list of spawned sender processes
    processes = list()

    # Interrupts all running senders
    def interrupt_handler(sig, f):
        global interrupted
        interrupted = True
        for sender in processes:
            sender.interrupt()

    # Capturing SIGINT
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)

    # spawning sender threads
    for i in range(parsed_opts.processes):
        s = Sender(parsed_opts)
        processes.append(s)
        s.start()

    # waiting on all threads to finish
    for t in processes:
        t.join()

    print("Exiting")
