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

import org.apache.camel.Exchange;
import org.apache.camel.Processor;
import org.apache.camel.builder.RouteBuilder;

import java.util.concurrent.atomic.AtomicLong;

/**
 * Produces messages to a pre-defined AMQP endpoing (amqp.timedsender.to.queue property) at
 * a fixed rate defined by property "amqp.timedsender.period".
 */
public class TimedSender extends RouteBuilder {

    AtomicLong messageCount = new AtomicLong();

    public void configure() throws Exception {

        from("timer://timedSender?fixedRate=true&period={{amqp.timedsender.period}}")
                .process(new Processor() {
                    public void process(Exchange exchange) throws Exception {
                        exchange.getIn().setBody(String.format("Generated message body with ID %s",
                                messageCount.incrementAndGet()));
                    }
                })
                .log("Sending message to: {{amqp.timedsender.to.queue}}")
                .bean("msgLogger", "logAmqpMessageInfo")
                .to("amqp:queue:{{amqp.timedsender.to.queue}}")
        ;

    }
}
