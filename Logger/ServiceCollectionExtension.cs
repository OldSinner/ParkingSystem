using Logger.Abstractions;
using Logger.Services;

namespace Microsoft.Extensions.DependencyInjection
{
    public static class ServiceCollectionExtension
    {
        public static IServiceCollection AddLoggerServices(this IServiceCollection services, Serilog.Core.Logger logger)
        {
            services.AddSingleton<IMessageHandlerService, MessageHandlerService>();
            services.AddSingleton<IRabbitMqService, RabbitMqService>();
            services.AddSingleton<ILoggerService, LoggerService>();
            services.AddSingleton<Serilog.Core.Logger>(logger);
            return services;
        }
    }
}
