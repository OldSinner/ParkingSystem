using FileLogger.Abstractions;
using Microsoft.Extensions.Logging;

namespace FileLogger.Services
{
    class MessageHandlerService : IMessageHandlerService
    {
        private readonly ILoggerFactory logger;

        public MessageHandlerService(ILoggerFactory logger)
        {
            this.logger = logger;
        }
        public void SendMessage()
        {
            var log = logger.CreateLogger("Test");
            log.LogInformation("Siemanooo!");
        }
    }
}