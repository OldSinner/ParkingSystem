using FileLogger.Model;
using System.Xml.Serialization;

namespace FileLogger.Abstractions
{
    public interface IMessageHandlerService
    {
        void LogMessage(LogMessage message);
        public void LogFileLoggerMessage(LogType type, string message, string method);
    }
}