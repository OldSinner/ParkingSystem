import pika
from Communication.CommunicationModels import *
from Communication.Logger import LoggerClass
from Helpers.const import *
from Configuration.Configuration import *


class BrokerReceiver:
    """
    A class to receive messages from a message broker and process them.

    This class establishes a connection to a message broker and listens for events
    related to gate operations. It processes incoming messages using a callback function.

    Args:
        detector: The detector instance used for processing.
        config (MQConfiguration): Configuration settings for the message queue.
        logger (LoggerClass): Logger instance for logging events.

    Methods:
        Dispose: Closes the connection to the message broker.
        callback: Processes incoming messages from the message broker.
        Consume: Starts consuming messages from the message broker.
    """

    def __init__(self, detector, config: MQConfiguration, logger: LoggerClass):
        """
        Initializes the BrokerReceiver with the specified detector, configuration, and logger.

        This constructor sets up the necessary components for the BrokerReceiver, including
        establishing a connection to the message broker using the provided configuration.

        Args:
        detector: The detector instance used for processing.
        config (MQConfiguration): Configuration settings for the message queue.
        logger (LoggerClass): Logger instance for logging events.
        """
        self.detector = detector
        self.config = config
        self.Logger = logger
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.config.url)
        )

    def Dispose(self):
        self.connection.close()

    def _callback(self, ch, method, properties, body):
        response = GateEvent(body)
        print(response)

    def Consume(self):
        """
        Starts consuming messages from the message broker.

        This method sets up the necessary channel and queue for receiving messages related
        to gate events. It begins listening for messages and processes them using the specified
        callback function.
        Raises:
            Exception: If there is an error during the setup or consumption of messages.
        """
        try:
            channel = self.connection.channel()
            channel.exchange_declare(
                exchange=self.config.gate_event_queue, exchange_type="fanout"
            )
            result = channel.queue_declare(queue="", exclusive=True)
            queue_name = result.method.queue
            channel.queue_bind(exchange=self.config.gate_event_queue, queue=queue_name)
            channel.basic_consume(
                queue=queue_name, on_message_callback=self._callback, auto_ack=True
            )
            self.Logger.LogInfo("BrokerReceiver.Consume", "start_consuming")
            channel.start_consuming()
        except Exception as ex:
            self.Logger.LogErr("BrokerReceiver.Consume", ex)
