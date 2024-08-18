using FileLogger.Abstractions;
using FileLogger.Services;
using Serilog.Core;

namespace Microsoft.Extensions.DependencyInjection
{
    public static class ServiceCollectionExtension
    {
        public static IServiceCollection AddFileLoggerServices(this IServiceCollection services, Logger logger)
        {
            services.AddSingleton<IMessageHandlerService, MessageHandlerService>();
            services.AddSingleton<IRabbitMqService, RabbitMqService>();
            services.AddSingleton<ILoggerService, LoggerService>();
            services.AddSingleton<Logger>(logger);
            return services;
        }
    }
}
