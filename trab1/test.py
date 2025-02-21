import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout (vertical)
        main_layout = QVBoxLayout(self)

        # Top section (horizontal layout)
        top_layout = QHBoxLayout()
        top_label = QLabel("Top Section", self)
        top_button = QPushButton("Top Button", self)
        top_layout.addWidget(top_label)
        top_layout.addWidget(top_button)

        # Middle section (grid layout)
        grid_layout = QGridLayout()
        grid_label1 = QLabel("Grid Label 1", self)
        grid_label2 = QLabel("Grid Label 2", self)
        grid_button1 = QPushButton("Grid Button 1", self)
        grid_button2 = QPushButton("Grid Button 2", self)

        grid_layout.addWidget(grid_label1, 0, 0)
        grid_layout.addWidget(grid_button1, 0, 1)
        grid_layout.addWidget(grid_label2, 1, 0)
        grid_layout.addWidget(grid_button2, 1, 1)

        # Bottom section (just a label)
        bottom_label = QLabel("Bottom Section", self)

        # Add layouts to the main layout
        main_layout.addLayout(top_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(bottom_label)

        # Set the main window properties
        self.setWindowTitle("Multiple Layouts Example")
        self.resize(500, 300)

        # Show the window
        self.setLayout(main_layout)
        self.show()

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())

