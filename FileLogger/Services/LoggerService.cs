using FileLogger.Abstractions;
using FileLogger.Model;
using Microsoft.Extensions.Configuration;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Data.Common;
using System.Text.Json;
using System.Threading.Channels;

namespace FileLogger.Services
{
    class LoggerService : ILoggerService
    {
        private readonly IMessageHandlerService messageHandlerService;
        private readonly IRabbitMqService rabbitMqService;
        private readonly IConnection connection;
        private readonly IModel model;
        private string queueName = "User";
        public LoggerService(IMessageHandlerService messageHandlerService,IRabbitMqService rabbitMqService, IConfiguration configuration)
        {
            this.messageHandlerService = messageHandlerService ?? throw new ArgumentNullException(nameof(messageHandlerService));
            this.rabbitMqService = rabbitMqService;
            var exchangeName = configuration.GetSection("logsExchange").Value ?? string.Empty;
            connection = rabbitMqService.CreateChannel();
            model = connection.CreateModel();
            model.ExchangeDeclare(exchange: exchangeName, type: ExchangeType.Fanout);
            queueName = model.QueueDeclare().QueueName;
            model.QueueBind(queue: queueName,
                      exchange: exchangeName,
                      routingKey: "");
        }

        public async Task StartConsumeLogs()
        {
            var consumer = new AsyncEventingBasicConsumer(model);
            consumer.Received += async (ch, ea) =>
            {
                var body = ea.Body.ToArray();
                var text = System.Text.Encoding.UTF8.GetString(body);
                var log = JsonSerializer.Deserialize<LogMessage>(text);
                await Task.CompletedTask;
            };
            model.BasicConsume(queueName, false, consumer);
            await Task.CompletedTask;
        }

        public void Dispose()
        {
            if (model.IsOpen)
                model.Close();
            if (connection.IsOpen)
                connection.Close();
        }
    }
}