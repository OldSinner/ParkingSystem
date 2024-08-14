using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading.Channels;
using GateHandlerLibary.Models;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace GateHandlerLibary
{
    public class ActionReceiver : IDisposable
    {
        private const string GATE_HANDLER_QUEUE = "GATE_HANDLER";
        private const string HOST = "localhost";

        private IConnection? Connection { get; set; }
        public IModel? Channel { get; set; } = null;
        public EventingBasicConsumer? eventingBasicConsumer { get; private set; }

        public void TryToConnect()
        {
            var factory = new ConnectionFactory { HostName = HOST };
            Connection = factory.CreateConnection();
            Channel = Connection.CreateModel();
            Channel.QueueDeclare(queue: GATE_HANDLER_QUEUE,
                                 durable: false,
                                 exclusive: false,
                                 autoDelete: false,
                                 arguments: null);
            eventingBasicConsumer = new EventingBasicConsumer(Channel);
            Channel.BasicConsume(GATE_HANDLER_QUEUE, false, eventingBasicConsumer);
        }

        

        public bool IsConnected => Connection?.IsOpen ?? false;
        public ActionReceiver()
        {
            
        }
        public void Dispose()
        {
            Channel?.Close();
            Connection?.Close();
        }
    }
}
