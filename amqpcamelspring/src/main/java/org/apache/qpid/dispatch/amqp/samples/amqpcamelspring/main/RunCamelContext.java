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
package org.apache.qpid.dispatch.amqp.samples.amqpcamelspring.main;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.spring.Main;
import org.apache.camel.spring.SpringCamelContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

/**
 * Provides mechanisms to load the camel context from an XML file and
 * allows an implementing class to define which Route to run.
 */
public abstract class RunCamelContext {

    protected ClassPathXmlApplicationContext applicationContext;
    protected SpringCamelContext camelContext;
    protected Main camelMain;

    public void runCamel(String[] args) throws Exception {

        // Loading context from XML
        applicationContext = new ClassPathXmlApplicationContext("/camel-context.xml");
        camelContext = new SpringCamelContext(applicationContext);

        // Defining loaded context
        camelMain = new Main();
        camelMain.setApplicationContext(applicationContext);

        // Adding routes manually
        camelMain.addRouteBuilder(getRoute());

        // Starting camel
        camelMain.run(args);

    }

    /**
     * Must return the only Route that will be executed.
     * @return RouteBuilder
     */
    public abstract RouteBuilder getRoute();

}
