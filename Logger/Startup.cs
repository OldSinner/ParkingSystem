using Logger.Abstractions;
using Logger.Services;
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

        var logger = new LoggerConfiguration()
            .Enrich.FromLogContext()
            .WriteTo.Console(outputTemplate: config.GetSection("LogOutputFormat").Value ?? string.Empty).CreateLogger();

        ServiceCollection services = new();
        services.AddSingleton<IConfiguration>(config);
        services.AddLoggerServices(logger);
        Provider = services.BuildServiceProvider();
    }

    public async Task RunAsync()
    {
        var logger = Provider.GetService<IMessageHandlerService>()!;

        logger.LogLoggerMessage(LogType.Information, "Starting Logger...");
        try
        {
            var service = Provider.GetService<ILoggerService>();
            if (service != null)
            {
                var cts = new CancellationTokenSource();
                var token = cts.Token;
                await service.StartConsumeLogs(token);
                service.Dispose();
            }
            logger.LogLoggerMessage(LogType.Information, "Closing Logger...");
        }
        catch (Exception ex)
        {
            logger.LogLoggerMessage(LogType.Error, ex.Message);
        }

    }
}