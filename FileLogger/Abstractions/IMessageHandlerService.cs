using FileLogger.Model;

namespace FileLogger.Abstractions
{
    public interface IMessageHandlerService
    {
        void LogMessage(LogMessage message);
    }
}