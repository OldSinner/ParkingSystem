using FileLogger.Abstractions;
using FileLogger.Services;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;

public class Startup
{
    public ServiceProvider Provider { get; set; } = null!;
    public void BuildServices()
    {
        ServiceCollection services = new();
        services.AddSingleton<ILoggerFactory>(LoggerFactory.Create(builder => builder.AddConsole()));
        services.AddSingleton<IMessageHandlerService, MessageHandlerService>();
        Provider = services.BuildServiceProvider();
    }

    public Task RunAsync()
    {
        var serv = Provider.GetService<IMessageHandlerService>();
        serv.SendMessage();
        return Task.CompletedTask;
    }
}