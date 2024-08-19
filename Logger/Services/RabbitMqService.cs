using Logger.Abstractions;
using Microsoft.Extensions.Configuration;
using RabbitMQ.Client;
namespace Logger.Services
{
    public class RabbitMqService : IRabbitMqService
    {
        private readonly IConfiguration configuration;
        private readonly IMessageHandlerService messageHandlerService;

        public RabbitMqService(IConfiguration configuration, IMessageHandlerService messageHandlerService)
        {
            this.configuration = configuration;
            this.messageHandlerService = messageHandlerService;
        }
        public IConnection CreateChannel()
        {
            messageHandlerService.LogLoggerMessage(LogType.Information, "Connecting to Mq");
            ConnectionFactory connection = new ConnectionFactory
            {
                UserName = configuration.GetSection("mqUsername").Value,
                Password = configuration.GetSection("mqPassword").Value,
                HostName = configuration.GetSection("mqUrl").Value,
                DispatchConsumersAsync = true
            };
            // Remove this line as it's redundant
            // connection.DispatchConsumersAsync = true;
            var channel = connection.CreateConnection();
            messageHandlerService.LogLoggerMessage(LogType.Information, "Connection Created");
            return channel;
        }
    }
}
