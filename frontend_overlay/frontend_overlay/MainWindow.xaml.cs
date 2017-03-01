using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Interop;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;


namespace frontend_overlay
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    /// 

    public partial class MainWindow : Window
    {
        public String gameString = "";
        WindowInteropHelper wih;
        SimpleHTTPServer httpServer;
        int gameStrLines = 0;

        public MainWindow()
        {
            InitializeComponent();
            this.Topmost = true;
            System.Windows.Threading.DispatcherTimer dispatcherTimer = new System.Windows.Threading.DispatcherTimer();
            dispatcherTimer.Tick += new EventHandler(dispatcherTimer_Tick);
            dispatcherTimer.Interval = new TimeSpan(0, 0, 1);
            dispatcherTimer.Start();
            
            wih = new WindowInteropHelper(this);
            httpServer = new SimpleHTTPServer( 8053, this);
        }

        void updateWindowSize()
        {
            int extendedStyle = Util.GetWindowLong(wih.Handle, Util.GWL_EXSTYLE);
            Util.SetWindowLong(wih.Handle, Util.GWL_EXSTYLE, extendedStyle | Util.WS_EX_TRANSPARENT);
            // code goes here
            IntPtr hwnd = Util.FindWindow("PPSSPPWnd", (string)null);
            IntPtr hwndForegroundWindow = Util.GetForegroundWindow();
            if ((hwnd == null) || (hwnd != hwndForegroundWindow))
            {
                this.Topmost = false;
                return;
            }
            this.Topmost = true;
            Util.RECT rct;
            if (!Util.GetWindowRect(hwnd, out rct))
            {
                return;
            }
            double heightFactor = 1;
            if (heightFactor < gameStrLines)
            {
                heightFactor = gameStrLines;
            }
            if (heightFactor > 9)
            {
                heightFactor = 9;
            }
            int height = (int) ((rct.Bottom - rct.Top) * 0.1 * heightFactor);
            rct.Bottom -= 10;
            rct.Top = rct.Bottom - height;
            rct.Left += 10;
            rct.Right -= 10;
            Util.SetWindowPos(wih.Handle, IntPtr.Zero, rct.Left, rct.Top, rct.Right - rct.Left, rct.Bottom - rct.Top, Util.SetWindowPosFlags.SWP_SHOWWINDOW);

        }
        private void dispatcherTimer_Tick(object sender, EventArgs e)
        {
            updateWindowSize();
        }

        public void handleNewGameStr(String gameStr)
        {
            
            this.Dispatcher.Invoke(new Action(() =>
            {
                Console.WriteLine(gameStr);
                gameStrLines = gameStr.Split('\n').Length;
                textBlock.Text = gameStr;
                updateWindowSize();
            }));
        }

        private void handleClosed(object sender, EventArgs e)
        {
            httpServer.Stop();
        }
    }
}
