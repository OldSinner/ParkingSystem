using GateHandlerLibary;
using RabbitMQ.Client.Events;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace GateHandlerUI
{
    public partial class GateHandlerMainWindow : Form
    {
        private bool Gate1Open = false;
        public GateReceiver? gateReceiver { get; set; }
        public GateHandlerMainWindow()
        {
            InitializeComponent();
        }

        private void GateHandlerMainWindow_Load(object sender, EventArgs e)
        {
            Gate_1_Button.Text = "Zamknięta";
            gateReceiver = new GateReceiver();
            try
            {
                gateReceiver.TryToConnect();
                rabbitStatusBox.Text = gateReceiver.IsConnected ? "Połączono" : "Nie połączono";
            }
            catch (Exception ex)
            {
                rabbitStatusBox.Text = ex.Message;
            }
            gateReceiver!.eventingBasicConsumer!.Received += ReceivedOpenCommand;
        }
        private void ReceivedOpenCommand(object? sender, BasicDeliverEventArgs e)
        {
            if (!Gate1Open)
            {
                Gate_1_Button.Invoke(new Action(() =>
                {
                    Gate_1_Button.Text = "Otwarta";
                }));
                Gate1Open = true;
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (gateReceiver != null)
            {
                rabbitStatusBox.Text = gateReceiver.IsConnected ? "Połączono" : "Nie połączono";
            }
            else
            {
                rabbitStatusBox.Text = "Utracono connectora";
            }
        }

        private void Gate_1_Button_Click(object sender, EventArgs e)
        {
            if (!Gate1Open)
            {
                Gate_1_Button.Text = "Otwarta";
                Gate1Open = true;
            }
            else
            {
                Gate_1_Button.Text = "Zamknięta";
                Gate1Open = true;
            }
        }
    }
}
