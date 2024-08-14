using GateHandlerLibary;
using RabbitMQ.Client.Events;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Channels;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.Tab;

namespace GateHandlerUI
{
    public partial class GateHandlerMainWindow : Form
    {
        public GatesHandler gateHandler { get; set; } = null!;
        public GateHandlerMainWindow()
        {
            InitializeComponent();
        }

        private void LoadGatesStatus(object sender, GateEventArg? e)
        {
            var gate = gateHandler.Gates.First();
            Gate_1_Button.Invoke(() =>
            {
            Gate_1_Button.Text = gate.GateOpened ? "Otwarta" : "Zamknięta";
            });
        }

        private void GateHandlerMainWindow_Load(object sender, EventArgs e)
        {
            gateHandler = new GatesHandler();
            LoadGatesStatus(this, null);
            gateHandler.GateChanged += LoadGatesStatus;

            Gate_1_Button.Text = "Zamknięta";
            try
            {
                rabbitStatusBox.Text = gateHandler.IsConnected() ? "Połączono" : "Nie połączono";
            }
            catch (Exception ex)
            {
                rabbitStatusBox.Text = ex.Message;
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            if (gateHandler != null)
            {
                rabbitStatusBox.Text = gateHandler.IsConnected() ? "Połączono" : "Nie połączono";
            }
            else
            {
                rabbitStatusBox.Text = "Utracono connectora";
            }
        }

        private void Gate_1_Button_Click(object sender, EventArgs e)
        {
           
        }
    }
}
