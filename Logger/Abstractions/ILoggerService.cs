namespace Logger.Abstractions
{
    public interface ILoggerService : IDisposable
    {
        Task StartConsumeLogs(CancellationToken token);
    }
}
