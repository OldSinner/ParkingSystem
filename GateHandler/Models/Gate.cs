namespace GateHandler.Models
{
    public class Gate
    {
        public int GateNumber { get; set; }
        public string GateFlow { get; set; } = string.Empty;
        public bool GateOpened { get; set; }
    }
}
