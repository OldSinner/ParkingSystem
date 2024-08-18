using FileLogger.Abstractions;
using Microsoft.Extensions.Configuration;
using RabbitMQ.Client;
namespace FileLogger.Services
{
    public class RabbitMqService : IRabbitMqService
    {
        private readonly IConfiguration configuration;

        public RabbitMqService(IConfiguration configuration)
        {
            this.configuration = configuration;
        }
        public IConnection CreateChannel()
        {
            ConnectionFactory connection = new ConnectionFactory
            {
                UserName = configuration.GetSection("mqUsername").Value,
                Password = configuration.GetSection("mqPassword").Value,
                HostName = configuration.GetSection("mqUrl").Value,
                DispatchConsumersAsync = true
            };
            connection.DispatchConsumersAsync = true;
            var channel = connection.CreateConnection();
            return channel;
        }
    }
}
