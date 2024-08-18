using RabbitMQ.Client;

namespace FileLogger.Abstractions
{
    public interface IRabbitMqService
    {
        IConnection CreateChannel();
    }
}
