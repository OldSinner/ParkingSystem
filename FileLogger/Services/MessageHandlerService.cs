using FileLogger.Abstractions;
using Serilog;
using Serilog.Context;

namespace FileLogger.Services
{
    class MessageHandlerService : IMessageHandlerService
    {
        private readonly LoggerConfiguration loggerConfiguration;

        public MessageHandlerService(LoggerConfiguration loggerConfiguration)
        {
            this.loggerConfiguration = loggerConfiguration;
        }
        public void SendMessage()
        {
            var logger = loggerConfiguration.CreateLogger();
            logger.Information("No contextual properties");
            using (LogContext.PushProperty("Service", 1))
            {
                logger.Information("Carries property A = 1");
            }
            logger.Information("ok");
        }
    }
}