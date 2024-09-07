import krita as k
import random
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QDialogButtonBox, QColorDialog
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PyQt5.QtCore import Qt, QPointF, QByteArray

# Basic class for the settings dialog
class NoiseLinesDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Noise Lines Settings')
        layout = QVBoxLayout()

        # Direction selection (Horizontal or Vertical)
        self.label_direction = QLabel('Direction:')
        self.combo_direction = QComboBox()
        self.combo_direction.addItems(['Horizontal', 'Vertical'])

        # R input (random range)
        self.label_R = QLabel('R (Random Range):')
        self.spin_R = QSpinBox()
        self.spin_R.setMinimum(0)
        self.spin_R.setMaximum(50)
        self.spin_R.setValue(3)

        # S input (step size)
        self.label_S = QLabel('S (Step Size):')
        self.spin_S = QSpinBox()
        self.spin_S.setMinimum(0)
        self.spin_S.setMaximum(50)
        self.spin_S.setValue(5)

        # N input (number of lines)
        self.label_N = QLabel('N (Number of Lines):')
        self.spin_N = QSpinBox()
        self.spin_N.setMinimum(1)
        self.spin_N.setMaximum(100)
        self.spin_N.setValue(10)

        # Line thickness input
        self.label_thickness = QLabel('Line Thickness (px):')
        self.spin_thickness = QSpinBox()
        self.spin_thickness.setMinimum(1)
        self.spin_thickness.setMaximum(10)
        self.spin_thickness.setValue(2)

        # Line color selection
        self.label_color = QLabel('Line Color:')
        self.button_color = QPushButton('Choose Color')
        self.button_color.clicked.connect(self.choose_color)
        self.color = QColor(0, 0, 0)  # Default black color

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_direction)
        layout.addWidget(self.combo_direction)
        layout.addWidget(self.label_R)
        layout.addWidget(self.spin_R)
        layout.addWidget(self.label_S)
        layout.addWidget(self.spin_S)
        layout.addWidget(self.label_N)
        layout.addWidget(self.spin_N)
        layout.addWidget(self.label_thickness)
        layout.addWidget(self.spin_thickness)
        layout.addWidget(self.label_color)
        layout.addWidget(self.button_color)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

# Function to draw noisy lines
def draw_noise_lines(direction, R, S, N, thickness, color):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Noise Lines", "paintlayer")
    doc.rootNode().addChildNode(new_layer, None)
    doc.setActiveNode(new_layer)

    # Get the width and height of the document
    width = doc.width()
    height = doc.height()

    # Create a QImage to draw on
    image = QImage(width, height, QImage.Format_ARGB32)
    image.fill(Qt.transparent)  # Set the background to transparent

    # Create a QPainter to draw on the QImage
    painter = QPainter(image)
    pen = QPen(color)
    pen.setWidth(thickness)
    painter.setPen(pen)

    # Draw N noisy lines
    for _ in range(N):
        if direction == 'Horizontal':
            # Initial starting point
            y = random.randint(0, height)
            x = 0

            points = [QPointF(x, y)]
            # Create a noisy horizontal line
            while x < width:
                x += S
                y += random.randint(-R, R)
                points.append(QPointF(x, y))

            # Draw the polyline
            painter.drawPolyline(*points)

        elif direction == 'Vertical':
            # Initial starting point
            x = random.randint(0, width)
            y = 0

            points = [QPointF(x, y)]
            # Create a noisy vertical line
            while y < height:
                y += S
                x += random.randint(-R, R)
                points.append(QPointF(x, y))

            # Draw the polyline
            painter.drawPolyline(*points)

    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert to QByteArray

    # Set the modified pixel data back to the layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw noisy lines
def main():
    # Open the settings dialog
    dialog = NoiseLinesDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the user-selected settings
        direction = dialog.combo_direction.currentText()
        R = dialog.spin_R.value()
        S = dialog.spin_S.value()
        N = dialog.spin_N.value()
        thickness = dialog.spin_thickness.value()
        color = dialog.color

        # Draw the noisy lines based on the settings
        draw_noise_lines(direction, R, S, N, thickness, color)

# Run the main function
main()
