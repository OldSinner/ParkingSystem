using FileLogger.Abstractions;
using Microsoft.Extensions.Configuration;
using RabbitMQ.Client;
namespace FileLogger.Services
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
            messageHandlerService.LogFileLoggerMessage(LogType.Information, "Connecting to Mq");
            ConnectionFactory connection = new ConnectionFactory
            {
                UserName = configuration.GetSection("mqUsername").Value,
                Password = configuration.GetSection("mqPassword").Value,
                HostName = configuration.GetSection("mqUrl").Value,
                DispatchConsumersAsync = true
            };
            connection.DispatchConsumersAsync = true;
            var channel = connection.CreateConnection();
            messageHandlerService.LogFileLoggerMessage(LogType.Information, "Connection Created");
            return channel;
        }
    }
}
