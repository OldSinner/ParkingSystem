namespace GateHandlerLibary.Models
{
    public class GateEvent
    {
        public bool Success { get; set; }
        public string Error { get; set; } = string.Empty;
        public ActionType ActionType { get; set; }
        public int Action { get; set; }
        public string Body { get; set; } = string.Empty;
        public DateTime EventOccuredDate { get; set; }
    }
}
