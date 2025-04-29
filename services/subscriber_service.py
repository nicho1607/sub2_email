import pika
from config.rabbitmq_config import RabbitMQConfig
from domain.models import PreInscripcion
from infrastructure.email_service import EmailService

class SubscriberService:
    def __init__(self):
        self.config = RabbitMQConfig()
        self.email_service = EmailService()
    
    def callback(self, ch, method, properties, body):
        try:
            mensaje = body.decode('utf-8')
            print(f"Suscriptor 2 recibió el mensaje: {mensaje}")
            
            # Procesar el mensaje
            data = PreInscripcion.from_json(mensaje)
            email_body = PreInscripcion.to_email_body(data)
            
            # Enviar correo
            if self.email_service.send_email(email_body):
                print("Correo enviado exitosamente a Yilbertarboleda@gmail.com")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print("Fallo al enviar correo")
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                
        except Exception as e:
            print(f"Error procesando mensaje: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    
    def start(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.config.host,
                port=self.config.port,
                virtual_host=self.config.virtual_host,
                credentials=self.config.credentials
            )
        )
        
        channel = connection.channel()
        channel.exchange_declare(
            exchange=self.config.exchange,
            exchange_type='topic',
            durable=True
        )
        
        channel.queue_declare(
            queue=self.config.queue_name,
            durable=True,
            exclusive=False
        )
        
        channel.queue_bind(
            exchange=self.config.exchange,
            queue=self.config.queue_name,
            routing_key=self.config.routing_key
        )
        
        channel.basic_consume(
            queue=self.config.queue_name,
            on_message_callback=self.callback,
            auto_ack=False
        )
        
        print("Esperando mensajes... Presiona CTRL+C para salir.")
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print("Detenido por el usuario")
            connection.close()