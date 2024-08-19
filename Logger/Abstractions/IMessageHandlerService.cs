using Logger.Model;
using System.Xml.Serialization;

namespace Logger.Abstractions
{
    public interface IMessageHandlerService
    {
        void LogMessage(LogMessage message);
        public void LogLoggerMessage(LogType type, string message);
    }
}