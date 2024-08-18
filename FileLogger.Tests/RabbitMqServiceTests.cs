using FileLogger.Abstractions;
using FluentAssertions;
using Microsoft.Extensions.DependencyInjection;

namespace FileLogger.Tests
{
    public class RabbitMqServiceTests
    {
        IServiceProvider _serviceProvider;
        public RabbitMqServiceTests()
        {
            _serviceProvider = TestHelper.BuildSerivceProvider();
        }

        [Fact]
        public void RabbitMqShouldCreateConnect()
        {
            var service = _serviceProvider.GetService<IRabbitMqService>();
            service.Should().NotBeNull();

            var model = service!.CreateChannel();
            model.Should().NotBeNull();
        }

    }
}
