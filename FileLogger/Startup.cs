using FileLogger.Abstractions;
using FileLogger.Services;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using System.Text.Json;

public class Startup
{
    public ServiceProvider Provider { get; set; } = null!;
    public void BuildServices()
    {
        var config = new ConfigurationBuilder()
        .AddJsonFile("appsettings.json", optional: false)
        .Build();

        ServiceCollection services = new();
        services.AddSingleton<IMessageHandlerService, MessageHandlerService>();
        services.AddSingleton<LoggerConfiguration>(new LoggerConfiguration()
            .Enrich.FromLogContext()
            .WriteTo.Console(outputTemplate: config.GetSection("LogOutputFormat").Value ?? string.Empty)
        );
        Provider = services.BuildServiceProvider();
    }

    public Task RunAsync()
    {
        var service = Provider.GetService<IMessageHandlerService>();
        if (service != null)
        {
            service.LogMessage(new FileLogger.Model.LogMessage
            {
                Action = "Test-Send",
                LogType = LogType.Information,
                Message = JsonSerializer.Serialize(new { a = 1, b = 3 }),
                Service = "Test",
                Version = "1.2"
            });
        }
        return Task.CompletedTask;
    }
}