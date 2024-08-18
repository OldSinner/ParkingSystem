namespace FileLogger.Abstractions
{
    public interface ILoggerService : IDisposable
    {
        Task StartConsumeLogs();
    }
}
