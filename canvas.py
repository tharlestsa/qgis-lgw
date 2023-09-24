from qgis.gui import QgsMapCanvas
from qgis.PyQt.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout
class CustomMapCanvas(QgsMapCanvas):
    def __init__(self, parent=None):
        super(CustomMapCanvas, self).__init__(parent)

        # Create a loading label
        self.loadingLabel = QLabel("Loading...", self)
        self.loadingLabel.setStyleSheet("background-color: white; padding: 5px;")
        self.loadingLabel.setAlignment(Qt.AlignCenter)


        # Position it in the center
        layout = QVBoxLayout(self)
        layout.addWidget(self.loadingLabel)

        # Connect the renderComplete signal to hide the loading label
        self.renderComplete.connect(self.hideLoading)

    def showLoading(self):
        self.loadingLabel.show()

    def hideLoading(self):
        self.loadingLabel.hide()
