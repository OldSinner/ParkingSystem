using Logger.Abstractions;
using Logger.Model;
using FluentAssertions;
using Microsoft.Extensions.DependencyInjection;

namespace Logger.Tests
{
    public class MessageHandlerServiceTests
    {
        IServiceProvider _serviceProvider;
        public MessageHandlerServiceTests()
        {
            _serviceProvider = TestHelper.BuildSerivceProvider();
        }

        [Fact]
        public void LogLoggerMessageTest()
        {
            var service = _serviceProvider.GetService<IMessageHandlerService>();
            service.Should().NotBeNull();

            var action = () => { service!.LogLoggerMessage(LogType.Information, "UNIT-TEST"); };
            action.Should().NotThrow();
        }

        [Fact]
        public void LogLogMessageTest()
        {
            var service = _serviceProvider.GetService<IMessageHandlerService>();
            service.Should().NotBeNull();

            var log = new LogMessage
            {
                Action = "Unit-Test",
                LogType = LogType.Debug,
                Message = "Unit-Test",
                Service = "Unit-Test",
                Version = "1.0.0"
            };

            var action = () => { service!.LogMessage(log); };
            action.Should().NotThrow();
        }
    }
}
