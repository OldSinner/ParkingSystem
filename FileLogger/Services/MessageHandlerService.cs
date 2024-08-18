using FileLogger.Abstractions;
using FileLogger.Model;
using Serilog;
using Serilog.Context;
using Serilog.Core;

namespace FileLogger.Services
{
    class MessageHandlerService : IMessageHandlerService
    {
        private readonly LoggerConfiguration loggerConfiguration;

        public MessageHandlerService(LoggerConfiguration loggerConfiguration)
        {
            this.loggerConfiguration = loggerConfiguration;
        }
        public void LogMessage(LogMessage message)
        {
            var logger = loggerConfiguration.CreateLogger();
            logger.Information("No contextual properties");
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