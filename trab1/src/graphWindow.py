##################### Graph Window

class graphWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
         # Set title
        self.setWindowTitle('Graph')

        # Set Size
        self.setGeometry(500, 500, 720, 420)

        self.graphPlot = pyqtgraph.PlotWidget()
        self.setCentralWidget(self.graphPlot)
        self.graphPlot.setBackground("w")
        self.xs = []
        self.ys = []
        self.graphPlot.setTitle("Title")
        self.graphPlot.setLabel("left", "Y")
        self.graphPlot.setLabel("bottom", "X")
        self.line = self.graphPlot.plot(self.xs, self.ys)

    def addDataPoint(self,x,y):
        self.xs.append(x)
        self.ys.append(y)
        self.line.setData(self.xs, self.ys)
    
    def clearGraph(self):
        self.xs = []
        self.ys = []
        self.line.setData(self.xs, self.ys)