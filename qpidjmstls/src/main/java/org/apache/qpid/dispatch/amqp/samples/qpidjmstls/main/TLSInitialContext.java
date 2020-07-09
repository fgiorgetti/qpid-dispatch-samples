package org.apache.qpid.dispatch.amqp.samples.qpidjmstls.main;

import javax.naming.InitialContext;
import javax.naming.NamingException;
import java.io.IOException;
import java.io.InputStream;
import java.net.URLEncoder;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.TreeMap;

public class TLSInitialContext {

    public static final String INITIAL_CONTEXT = "org.apache.qpid.jms.jndi.JmsInitialContextFactory";
    public static final String CONFIG_FILE = "/config.properties";

    private static final TreeMap<String, String> defaultProperties = new TreeMap<String, String>();

    public static final String LOOKUP_CONNECTION_FACTORY = "amqpFactory";
    public static final String LOOKUP_QUEUE = "myQueueLookup";

    private static final String KEY_SCHEME = "scheme";
    private static final String KEY_HOST = "host";
    private static final String KEY_PORT = "port";
    private static final String KEY_QUEUE = "queue";

    static {
        defaultProperties.put("transport.keyStoreLocation", "client.keystore");
        defaultProperties.put("transport.keyStorePassword", "12345");
        defaultProperties.put("transport.verifyHost", "false");
        defaultProperties.put("transport.keyAlias", "client");
        defaultProperties.put("transport.trustAll", "true");
    }

    public static InitialContext generateInitialContext() throws IOException, NamingException {

        // Loading config.properties resource (internal properties)
        Properties internalProp = new Properties();

        InputStream configStream = TLSInitialContext.class.getResourceAsStream(CONFIG_FILE);
        internalProp.load(configStream);

        // Preparing the connectionFactory
        StringBuilder cf = new StringBuilder();
        cf.append(internalProp.getProperty(KEY_SCHEME, "amqps"));
        cf.append("://");
        cf.append(internalProp.getProperty(KEY_HOST, "127.0.0.1"));
        cf.append(":");
        cf.append(internalProp.getProperty(KEY_PORT, "5671"));

        boolean first = true;
        for (Entry<String, String> entry: defaultProperties.entrySet()) {
            cf.append(first? "?":"&");
            first = false;
            cf.append(URLEncoder.encode(entry.getKey(), "UTF-8"));
            cf.append("=");
            cf.append(URLEncoder.encode(internalProp.getProperty(entry.getKey(), entry.getValue()), "UTF-8"));
        }

        // p is properties to initial InitialContext
        Properties p = new Properties();

        // Default options
        p.put("java.naming.factory.initial", INITIAL_CONTEXT);
        p.put("connectionfactory.amqpFactory", cf.toString());
        p.put("queue.myQueueLookup", internalProp.getProperty(KEY_QUEUE, "queue"));

        //System.out.println(p);
        return new InitialContext(p);

    }

}
