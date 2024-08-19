using Logger.Abstractions;
using Logger.Model;
using Serilog;
using Serilog.Context;
using System.Diagnostics;
using System.Reflection;

namespace Logger.Services
{
    class MessageHandlerService : IMessageHandlerService
    {
        private readonly ILogger logger;

        public MessageHandlerService(ILogger logger)
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
        }

        public void LogLoggerMessage(LogType type, string message)
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

        private static void Send(LogMessage message, ILogger logger)
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