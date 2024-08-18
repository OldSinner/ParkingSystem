using Microsoft.Extensions.DependencyInjection;

public class Startup
{
    public ServiceProvider Provider { get; set; } = null!;
    public void BuildServices()
    {
        ServiceCollection services = new();
        Provider = services.BuildServiceProvider();
    }

    public Task RunAsync()
    {
        return Task.CompletedTask;
    }
}