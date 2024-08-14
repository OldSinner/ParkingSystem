namespace GateHandlerLibary.Models
{
    public record ActionRequested
    {
        public ActionType Action { get; set; } 
        public string ReplyTo { get; set; } = string.Empty;
    }
}
