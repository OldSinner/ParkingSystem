namespace GateHandlerUI
{
    partial class GateHandlerMainWindow
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            components = new System.ComponentModel.Container();
            Gate_1_Button = new Button();
            label1 = new Label();
            label2 = new Label();
            rabbitStatusBox = new TextBox();
            timer1 = new System.Windows.Forms.Timer(components);
            SuspendLayout();
            // 
            // Gate_1_Button
            // 
            Gate_1_Button.Location = new Point(12, 12);
            Gate_1_Button.Name = "Gate_1_Button";
            Gate_1_Button.Size = new Size(198, 35);
            Gate_1_Button.TabIndex = 0;
            Gate_1_Button.Text = "Otwarta";
            Gate_1_Button.UseVisualStyleBackColor = true;
            Gate_1_Button.Click += Gate_1_Button_Click;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(216, 22);
            label1.Name = "label1";
            label1.Size = new Size(85, 15);
            label1.TabIndex = 1;
            label1.Text = "Status Bramy 1";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(12, 302);
            label2.Name = "label2";
            label2.Size = new Size(99, 15);
            label2.TabIndex = 2;
            label2.Text = "RabbitMQ Status:";
            // 
            // rabbitStatusBox
            // 
            rabbitStatusBox.Location = new Point(117, 299);
            rabbitStatusBox.Name = "rabbitStatusBox";
            rabbitStatusBox.ReadOnly = true;
            rabbitStatusBox.Size = new Size(100, 23);
            rabbitStatusBox.TabIndex = 3;
            // 
            // timer1
            // 
            timer1.Interval = 2000;
            timer1.Tick += timer1_Tick;
            // 
            // GateHandlerMainWindow
            // 
            AutoScaleDimensions = new SizeF(7F, 15F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(490, 326);
            Controls.Add(rabbitStatusBox);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(Gate_1_Button);
            Name = "GateHandlerMainWindow";
            Text = "Gate Handler";
            Load += GateHandlerMainWindow_Load;
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Button Gate_1_Button;
        private Label label1;
        private Label label2;
        private TextBox rabbitStatusBox;
        private System.Windows.Forms.Timer timer1;
    }
}