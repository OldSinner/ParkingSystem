public class Program
{
    private async static Task Main(string[] args)
    {
        var Startup = new Startup();
        Startup.BuildServices();
        await Startup.RunAsync();
    }
}