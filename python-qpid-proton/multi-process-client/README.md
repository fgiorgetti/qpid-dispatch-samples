# multi-process-client

AMQP multi-process-client provides a sender and a receiver application
that are able to spawn multiple processes.

These applications are build for a very specific scenario, so they share
some common features:

* Dynamic number of processes to be spawned
* Reconnect rate (after X messages received or sent) 
* Delay between each sent message (sender only)
* Use pre-defined sizes for message body and properties

## Sender usage

```
$ python sender.py --help
Usage: sender.py [options]

Options:
  -h, --help            show this help message and exit
  --host=HOST           The AMQP host to connect (or set AMQP_HOST env var)
  --port=PORT           AMQP port to connect (or set AMQP_PORT env var)
  --address=ADDRESS     Address to send messages to (or set AMQP_ADDRESS env
                        var)
  --processes=PROCESSES
                        number of processes to spawn (or set CLIENT_PROCESSES
                        env var)
  --message-size=MESSAGE_SIZE
                        size of message body (or set CLIENT_MESSAGE_SIZE env
                        var)
  --properties-size=PROPERTIES_SIZE
                        size of application properties (or set
                        CLIENT_PROPERTIES_SIZE env var)
  --reconnect-after=RECONNECT_AFTER
                        after a given number of messages delivered the sender
                        will recycle its connection (or set
                        CLIENT_RECONNECT_AFTER env var)
  --interval-delay=INTERVAL_DELAY
                        delay in seconds between sending cycle (or set
                        CLIENT_INTERVAL_DELAY env var)
  --ttl=TTL             ttl in milliseconds (or set CLIENT_TTL env var)
  --log-level=LOG_LEVEL
                        logging level (or set LOG_LEVEL env var)
```

## Receiver usage

```
$ python receiver.py --help

Options:
  -h, --help            show this help message and exit
  --host=HOST           The AMQP host to connect (or set AMQP_HOST env var)
  --port=PORT           AMQP port to connect (or set AMQP_PORT env var)
  --address=ADDRESS     receive messages from
  --processes=PROCESSES
                        number of processes to spawn (or set CLIENT_PROCESSES
                        env var)
  --message-size=MESSAGE_SIZE
                        size of message body (or set CLIENT_MESSAGE_SIZE env
                        var)
  --properties-size=PROPERTIES_SIZE
                        size of application properties (or set
                        CLIENT_PROPERTIES_SIZE env var)
  --reconnect-after=RECONNECT_AFTER
                        receiver
  --log-level=LOG_LEVEL
                        logging level (or set LOG_LEVEL env var)
```

## Running through a container

When running in a container, you can also specify an extra environment
variable, which is the `CLIENT_APP`. By default, it is set to `sender.py`
but you can set it to `receiver.py` if you want to run the receiver.

Examples:

### Sender in a container

```
docker run --rm --name sender -e AMQP_HOST=172.17.0.1 fgiorgetti/multi-process-client:latest
```

### Receiver in a container

```
docker run --rm --name receiver -e AMQP_HOST=172.17.0.1 -e CLIENT_APP=receiver.py fgiorgetti/multi-process-client:latest
```
