using Logger.Abstractions;
using Logger.Model;
using Microsoft.Extensions.Configuration;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Data.Common;
using System.Reflection;
using System.Text.Json;
using System.Threading.Channels;

namespace Logger.Services
{
    class LoggerService : ILoggerService
    {
        private readonly IMessageHandlerService messageHandlerService;
        private readonly IRabbitMqService rabbitMqService;
        private IConnection connection;
        private IModel model;
        private string queueName = "User";
        public LoggerService(IMessageHandlerService messageHandlerService, IRabbitMqService rabbitMqService, IConfiguration configuration)
        {
            this.messageHandlerService = messageHandlerService ?? throw new ArgumentNullException(nameof(messageHandlerService));
            this.rabbitMqService = rabbitMqService;

            var exchangeName = configuration.GetSection("logsExchange").Value ?? string.Empty;
            ConnectToMq(rabbitMqService, exchangeName);
        }

        private void ConnectToMq(IRabbitMqService rabbitMqService, string exchangeName)
        {
            connection = rabbitMqService.CreateChannel();
            model = connection.CreateModel();

            messageHandlerService.LogLoggerMessage(LogType.Information, $"Create Exchange \"{exchangeName}\"");
            model.ExchangeDeclare(exchange: exchangeName, type: ExchangeType.Fanout);

            messageHandlerService.LogLoggerMessage(LogType.Information, $"Binding Queue");
            queueName = model.QueueDeclare().QueueName;
            model.QueueBind(queue: queueName,
                      exchange: exchangeName,
                      routingKey: "");
        }

        public async Task StartConsumeLogs(CancellationToken token)
        {
            messageHandlerService.LogLoggerMessage(LogType.Information, "Start Consume Logs");
            var consumer = new AsyncEventingBasicConsumer(model);
            consumer.Received += async (ch, ea) =>
            {
                var body = ea.Body.ToArray();
                var text = System.Text.Encoding.UTF8.GetString(body);
                try
                {
                    var log = JsonSerializer.Deserialize<LogMessage>(text);
                    if (log != null)
                    {
                        messageHandlerService.LogMessage(log);
                    }
                    else
                    {
                        throw new InvalidOperationException("Cannot deserialize");
                    }
                }
                catch (Exception ex)
                {
                    LogErrorEmptyOrCannotParse(ex);
                }

                await Task.CompletedTask;
            };
            model.BasicConsume(queueName, false, consumer);
            await Task.Run(() => token.WaitHandle.WaitOne());

            messageHandlerService.LogLoggerMessage(LogType.Information, "Stoping Consume Logs");
            await Task.CompletedTask;
        }
        public void LogErrorEmptyOrCannotParse(Exception ex) => messageHandlerService.LogLoggerMessage(LogType.Error, ex.Message);

        public void Dispose()
        {
            if (model.IsOpen)
                model.Close();
            if (connection.IsOpen)
                connection.Close();
        }
    }
}