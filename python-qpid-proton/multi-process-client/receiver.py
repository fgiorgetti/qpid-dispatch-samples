from proton.handlers import MessagingHandler
from proton.reactor import Container
from proton import Message
import common
import logging
import optparse
import socket
import os
import multiprocessing

"""

"""

# public receiver variables (initialized after parsing)
expected_body = ""
expected_properties = dict()
expected_body_size = 0
expected_properties_size = 0


class Receiver(MessagingHandler):
    def __init__(self, opts):
        super(Receiver, self).__init__()
        self.host = opts.host
        self.port = opts.port
        self.address = opts.address
        self.reconnect_after = opts.reconnect_after
        self.container = Container(self)
        self._receiver = None
        self._url = "amqp://%s:%s/%s" % (self.host, self.port, self.address)
        self._next_task = None
        # internal stats
        self._received = 0

    def on_start(self, event):
        self.create_receiver(event)

    def create_receiver(self, event):
        if self._receiver is not None:
            logging.info("closing receiver")
            self._receiver.close()
            event.connection.close()
            self._reset_stats()
        logging.info("creating receiver")
        self._receiver = event.container.create_receiver(self._url)

    def on_message(self, event):
        self._received += 1
        msg = event.message
        body_size = len(msg.body)
        prop_size = sum([len(k)+len(msg.properties[k]) for k in msg.properties])
        logging.debug("received [body:%d, properties:%d]" % (body_size, prop_size))
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


# Main flow for sender app
if __name__ == "__main__":
    parsed_opts, args = common.parse_opts(False)

    # same message body and properties will be used by all sender instances
    expected_body = common.generate_message_body(parsed_opts.message_size, "abcdedfgijklmnopqrstuvwxyz0123456789")
    expected_body_size = parsed_opts.message_size
    expected_properties = common.generate_application_properties(parsed_opts.properties_size)
    expected_properties_size = parsed_opts.properties_size

    # initializing logging
    common.initialize_logging(parsed_opts.log_level)

    # list of spawned sender processes
    processes = list()

    # spawning receiver processes
    for i in range(parsed_opts.processes):
        proc = multiprocessing.Process(target=Container(Receiver(parsed_opts)).run)
        proc.start()
        processes.append(proc)

    # waiting on all processes to finish
    for proc in processes:
        proc.join()

    print("Exiting")
