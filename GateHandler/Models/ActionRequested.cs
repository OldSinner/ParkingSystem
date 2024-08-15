namespace GateHandler.Models
{
    public record ActionRequested
    {
        public ActionRq Action { get; set; }
        public DateTime RequestDate { get; set; }
    }
}
