using Logger.Abstractions;
using Logger.Services;
using Serilog;

namespace Microsoft.Extensions.DependencyInjection
{
    public static class ServiceCollectionExtension
    {
        public static IServiceCollection AddLoggerServices(this IServiceCollection services, ILogger logger)
        {
            services.AddSingleton<IMessageHandlerService, MessageHandlerService>();
            services.AddSingleton<IRabbitMqService, RabbitMqService>();
            services.AddSingleton<ILoggerService, LoggerService>();
            services.AddSingleton<ILogger>(logger);
            return services;
        }
    }
}
