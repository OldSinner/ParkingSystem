using GateHandler.Models;
using RabbitMQ.Client.Events;
using System.Text.Json;
using System.Text;

namespace GateHandler
{
    public class GatesHandler : IDisposable
    {
        public ActionReceiver ActionReceiver { get; set; } = new ActionReceiver();
        public List<Gate> Gates { get; set; } = [];
        public delegate void GateChangedHandler(object sender, GateEventArg e);
        public event GateChangedHandler GateChanged;

        public bool IsConnected() => ActionReceiver.IsConnected;
        public GatesHandler()
        {
            ActionReceiver.TryToConnect();
            ActionReceiver.eventingBasicConsumer!.Received += DecodedMessage;
            Gates.Add(new Gate
            {
                GateFlow = "IN",
                GateNumber = 1,
                GateOpened = false
            });
        }
        private void DecodedMessage(object? sender, BasicDeliverEventArgs e)
        {
            var requested = JsonSerializer.Deserialize<ActionRequested>(Encoding.UTF8.GetString(e.Body.ToArray()));
            switch (requested.Action)
            {
                case ActionRq.NONE:
                    break;
                case ActionRq.OPENGATE:
                    OpenGate(requested);
                    break;
                case ActionRq.CLOSEGATE:
                    break;

            }
        }

        private void OpenGate(ActionRequested req)
        {
            var gate = Gates.First();
            gate.GateOpened = true;
            GateChanged?.Invoke(this, new GateEventArg
            {
                Action = req.Action,
                Success = true
            });
        }

        public void Dispose() => ActionReceiver.Dispose();
    }

    public class GateEventArg
    {
        public ActionRq Action { get; set; }
        public bool Success { get; set; }
    }
}
