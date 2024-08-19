using RabbitMQ.Client;

namespace Logger.Abstractions
{
    public interface IRabbitMqService
    {
        IConnection CreateChannel();
    }
}
