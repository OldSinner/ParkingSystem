namespace Logger.Model
{
    public class LogMessage
    {
        public LogType LogType { get; set; }
        public string Message { get; set; } = string.Empty;
        public string Action { get; set; } = string.Empty;
        public string Version { get; set; } = "0.0.0";
        public string Service { get; set; } = string.Empty;
    }

}
