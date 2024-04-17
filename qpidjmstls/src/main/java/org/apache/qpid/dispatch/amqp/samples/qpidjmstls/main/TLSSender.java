package org.apache.qpid.dispatch.amqp.samples.qpidjmstls.main;

/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 */
import jakarta.jms.*;
import javax.naming.InitialContext;

public class TLSSender {

    private static final int DEFAULT_COUNT = 10;
    private static final int DELIVERY_MODE = DeliveryMode.NON_PERSISTENT;

    public static void main(String[] args) throws Exception {

        int count = DEFAULT_COUNT;
        if (args.length == 0) {
            System.out.println("Sending up to " + count + " messages.");
            System.out.println("Specify a message count as the program argument if you wish to send a different amount.");
        } else {
            count = Integer.parseInt(args[0]);
            System.out.println("Sending up to " + count + " messages.");
        }

        // Generating InitialContext based on config.properties
        // TODO If args informed, use it over config.properites
        InitialContext context = TLSInitialContext.generateInitialContext();

        // Creating connection factory (based on generated info)
        ConnectionFactory factory = (ConnectionFactory) context.lookup(TLSInitialContext.LOOKUP_CONNECTION_FACTORY);

        // Destination queue
        Destination queue = (Destination) context.lookup(TLSInitialContext.LOOKUP_QUEUE);

        // Connecting to broker
        Connection connection = factory.createConnection(System.getProperty("USER"), System.getProperty("PASSWORD"));
        connection.start();

        // Creating a session
        Session session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

        // Create producer and start sending
        MessageProducer messageProducer = session.createProducer(queue);

        long start = System.currentTimeMillis();
        for (int i = 1; i <= count; i++) {
            TextMessage message = session.createTextMessage("Text!");
            messageProducer.send(message, DELIVERY_MODE, Message.DEFAULT_PRIORITY, Message.DEFAULT_TIME_TO_LIVE);

            if (i % 100 == 0) {
                System.out.println("Sent message " + i);
            }
        }

        long finish = System.currentTimeMillis();
        long taken = finish - start;
        System.out.println("Sent " + count + " messages in " + taken + "ms");

        connection.close();

    }

}
