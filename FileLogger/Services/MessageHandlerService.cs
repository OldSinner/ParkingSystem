using FileLogger.Abstractions;
using FileLogger.Model;
using Serilog;
using Serilog.Context;
using Serilog.Core;
using System.Diagnostics;
using System.Reflection;

namespace FileLogger.Services
{
    class MessageHandlerService : IMessageHandlerService
    {
        private readonly Logger logger;

        public MessageHandlerService(Logger logger)
        {
            this.logger = logger;
        }
        public void LogMessage(LogMessage message)
        {
            using (LogContext.PushProperty("Service", message.Service))
            {
                using (LogContext.PushProperty("Version", message.Version))
                {
                    using (LogContext.PushProperty("Action", message.Action))
                    {
                        Send(message, logger);
                    }
                }
            }
            logger.Dispose();
        }

        public void LogFileLoggerMessage(LogType type, string message)
        {
            StackTrace stackTrace = new StackTrace();
            var method = stackTrace?.GetFrame(1)?.GetMethod()?.Name ?? "Not Deterimated";
            var name = Assembly.GetExecutingAssembly().GetName();
            var log = new LogMessage()
            {
                LogType = type,
                Message = message,
                Action = method,
                Service = name.Name ?? "ServiceNotDetected",
                Version = name.Version?.ToString() ?? "0.0.0."
            };
            LogMessage(log);
        }

        private static void Send(LogMessage message, Logger logger)
        {
            switch (message.LogType)
            {
                case LogType.Information:
                    logger.Information($"{message.Message}");
                    break;
                case LogType.Warning:
                    logger.Warning($"{message.Message}");
                    break;
                case LogType.Error:
                    logger.Error($"{message.Message}");
                    break;
                case LogType.Debug:
                    logger.Debug($"{message.Message}");
                    break;
                default:
                    break;
            }
        }
    }
}