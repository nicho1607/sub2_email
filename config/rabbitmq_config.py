import pika

class RabbitMQConfig:
    def __init__(self):
        self.host = "moose-01.rmq.cloudamqp.com"
        self.port = 5672
        self.virtual_host = "pmvmwhnl"
        self.credentials = pika.PlainCredentials("pmvmwhnl", "D6sgX6xS_iAplcdiNbWeHe3ZWITrVGY2")
        self.exchange = "universidad"
        self.routing_key = "preinscripcion.*"
        self.queue_name = "Sub2"