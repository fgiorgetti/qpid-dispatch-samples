from docker.io/library/openjdk:11.0.15-jdk as builder

WORKDIR /app
COPY . .
RUN apt update && apt -y install maven && mvn clean package

from docker.io/library/openjdk:11.0.15-jre

WORKDIR /app
COPY --from=builder /app/amqpcamelspring/target/amqp-camel-spring-1.0-SNAPSHOT.jar /app/qpidjmstls/target/qpid-jms-tls-1.0-SNAPSHOT.jar .

CMD ["java", "-cp", "amqp-camel-spring-1.0-SNAPSHOT.jar", "org.apache.qpid.dispatch.amqp.samples.amqpcamelspring.main.TimedSenderMain"]
