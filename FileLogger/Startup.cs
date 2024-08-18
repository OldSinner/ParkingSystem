using FileLogger.Abstractions;
using FileLogger.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using Serilog.Core;
using System.Text.Json;

public class Startup
{
    public ServiceProvider Provider { get; set; } = null!;
    public void BuildServices()
    {
        var config = new ConfigurationBuilder()
        .AddJsonFile("appsettings.json", optional: false)
        .AddJsonFile("appsettings.development.json", optional: false)

        .Build();

        ServiceCollection services = new();
        services.AddSingleton<IConfiguration>(config);
        services.AddSingleton<IMessageHandlerService, MessageHandlerService>();
        services.AddSingleton<IRabbitMqService, RabbitMqService>();
        services.AddSingleton<ILoggerService, LoggerService>();
        services.AddSingleton<Logger>(new LoggerConfiguration()
            .Enrich.FromLogContext()
            .WriteTo.Console(outputTemplate: config.GetSection("LogOutputFormat").Value ?? string.Empty).CreateLogger()
        );
        Provider = services.BuildServiceProvider();
    }

    public async Task RunAsync()
    {
        var service = Provider.GetService<ILoggerService>();
        if (service != null)
        {
            var cts = new CancellationTokenSource();
            var token = cts.Token;
            await service.StartConsumeLogs(token);
            service.Dispose();
        }
    }
}