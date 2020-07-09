# AMQP Camel Spring

Provides three simple clients implemented using Apache Camel and Spring Framework to exchange messages.

## Pre-requisites

Before running the samples, make sure you have an AMQP Server running (default: 127.0.0.1:5672).

## Configuration

You can customize default configuration used by the internal clients by modifying the ```camel.properties``` file.
It can be modified inside the project itself, or you can override it by installing a copy of it
into /etc/qpid-dispatch-samples/amqpcamelspring/camel.properties.

## Clients

### TimedSender

It uses Camel timer to send generated messages at a fixed rate.
By default, it will produce messages to: "prefix.queue1" queue.

### ConsumeAndDispatch

This client provides a consumer endpoint that receive messages from "prefix.queue1"
and then it forwards the received message to another AMQP endpoint "prefix.queue2" (addresses can be customized).

### SimpleConsumer

Simply consumes messages from "prefix.queue2".

## Running the samples

The client applications will run indefinitely (till you manually stop them), and can be executed by running:

```mvn exec:java -P <ProfileName>```

You must replace the ```<ProfileName>``` to be used with any of:

- TimedSender
- ConsumeAndDispatch
- SimpleConsumer
