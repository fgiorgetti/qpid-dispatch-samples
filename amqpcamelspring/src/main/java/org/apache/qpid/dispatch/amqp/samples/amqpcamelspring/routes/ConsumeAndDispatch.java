/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.qpid.dispatch.amqp.samples.amqpcamelspring.routes;

import org.apache.camel.ExchangePattern;
import org.apache.camel.LoggingLevel;
import org.apache.camel.builder.RouteBuilder;

import javax.jms.JMSException;

/**
 * Defines a Camel Route that consumes messages from a pre-defined queue (amqp.consumeanddispatch.from.queue property)
 * and then forwards the received message to another AMQP endpoint (amqp.consumeanddispatch.to.queue property).
 *
 * JMSExceptions are handled and just an error message will be logged in case something wrong occurs.
 */
public class ConsumeAndDispatch extends RouteBuilder {

    /**
     * Defines the main route
     * @throws Exception
     */
    public void configure() throws Exception {

        // Configuring exception handlers
        configureExceptionHandling();

        // Main Route
        from("amqp:queue:{{amqp.consumeanddispatch.from.queue}}?disableReplyTo=True")
            .log("Message received from: {{amqp.consumeanddispatch.from.queue}}")
            .bean("msgLogger", "logAmqpMessageInfo")
            .log("Forwarding message to: {{amqp.consumeanddispatch.to.queue}}")
            .to(ExchangePattern.InOnly, "amqp:queue:{{amqp.consumeanddispatch.to.queue}}")
        ;

    }

    /**
     * Exception handling
     */
    private void configureExceptionHandling() {
        onException(JMSException.class)
            .continued(true)
            .log(LoggingLevel.ERROR, "A JMSException has be thrown: ${exception.message}")
        ;
    }

}
