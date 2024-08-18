﻿
using FileLogger.Abstractions;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Serilog;
using Serilog.Core;

namespace FileLogger.Tests
{
    public static class TestHelper
    {
        public static IServiceProvider BuildSerivceProvider()
        {
            var config = new ConfigurationBuilder()
            .AddJsonFile("appsettings.json", optional: false)
            .AddJsonFile("appsettings.development.json", optional: false)
            .Build();

            var logger = new LoggerConfiguration()
                .Enrich.FromLogContext()
                .WriteTo.Console(outputTemplate: config.GetSection("LogOutputFormat").Value ?? string.Empty).CreateLogger();

            ServiceCollection services = new();
            services.AddSingleton<IConfiguration>(config);
            services.AddFileLoggerServices(logger);
            return services.BuildServiceProvider();
        }
    }
}
