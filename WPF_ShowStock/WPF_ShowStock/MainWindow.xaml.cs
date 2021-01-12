using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Emgu.CV;
using Emgu.CV.CvEnum;
using Emgu.CV.Structure;
using myEmguLibrary;
using Point = System.Drawing.Point;

namespace WPF_ShowStock
{
    /// <summary>
    /// MainWindow.xaml 的互動邏輯
    /// </summary>
    public partial class MainWindow : Window
    {


        public MainWindow()
        {
            InitializeComponent();

        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            Mat mat = new Mat(500, 500, DepthType.Cv8U, 3);

            myChart chart = new myChart();
            myChart.Table table = new myChart.Table();
            table.rect_outerBox = new System.Drawing.Rectangle(10, 10, 480, 480);
            table.rect_innerBox = new System.Drawing.Rectangle(30, 30, 440, 440);
            table.row_count = 3;
            table.column_count = 4;
            chart.drawTable(mat, table);

            myChart.Value value = new myChart.Value();
            value.col = 2;
            value.row = 3;
            chart.drawValue(mat,table,value);

            //Random rnd = new Random();
            //Task.Run(() =>
            //{
            //    while (true)
            //    {
            //        MyInvoke.setToZero(ref mat);
            //        CvInvoke.Circle(mat, new Point((int)(rnd.NextDouble() * 500.0), (int)(rnd.NextDouble() * 500.0)), 5, new MCvScalar(200, 200, 200), -1);
            //        this.Dispatcher.Invoke((Action)(() => { image_main.Source = MyInvoke.MatToBitmap(mat); }));
            //    }

            //});
            image_main.Source = MyInvoke.MatToBitmap(mat);



        }
    }
}
