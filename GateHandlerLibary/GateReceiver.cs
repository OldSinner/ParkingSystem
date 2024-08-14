using System.Text;
using System.Threading.Channels;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace GateHandlerLibary
{
    public class GateReceiver : IDisposable
    {
        private const string OPEN_GATE_QUEUE = "OPEN_GATE_1";
        private const string HOST = "localhost";

        private IConnection? Connection { get; set; }
        private IModel? Channel { get; set; } = null;
        public EventingBasicConsumer? eventingBasicConsumer { get; private set; }

        public void TryToConnect()
        {
            var factory = new ConnectionFactory { HostName = HOST };
            Connection = factory.CreateConnection();
            Channel = Connection.CreateModel();
            Channel.QueueDeclare(queue: OPEN_GATE_QUEUE,
                                 durable: false,
                                 exclusive: false,
                                 autoDelete: false,
                                 arguments: null);
            eventingBasicConsumer = new EventingBasicConsumer(Channel);
            Channel.BasicConsume(OPEN_GATE_QUEUE, false, eventingBasicConsumer);
        }
        public bool IsConnected => Connection?.IsOpen ?? false;
        public GateReceiver()
        {
            
        }
        public void Dispose()
        {
            Channel?.Close();
            Connection?.Close();
        }
    }
}
