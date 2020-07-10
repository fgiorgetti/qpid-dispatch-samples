DOCKER := docker
IMAGE_AMQPCAMELSPRING := docker.io/fgiorgetti/amqpcamelspring:1.0

docker-build:
	$(DOCKER) build -t $(IMAGE_AMQPCAMELSPRING) -f Dockerfile-amqpcamelspring .
