import krita as k
import random
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QCheckBox, QPushButton, QColorDialog, QDialogButtonBox
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PyQt5.QtCore import Qt, QPointF, QByteArray

# Basic class for the settings dialog
class MikadoDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Mikado Line Settings')
        layout = QVBoxLayout()

        # N input (number of lines)
        self.label_N = QLabel('Number of Lines (N):')
        self.spin_N = QSpinBox()
        self.spin_N.setMinimum(10)
        self.spin_N.setMaximum(2000)
        self.spin_N.setValue(200)

        # Lx and Ly input (length of lines)
        self.label_Lx = QLabel('Length X (Lx):')
        self.spin_Lx_min = QSpinBox()
        self.spin_Lx_min.setMinimum(10)
        self.spin_Lx_min.setMaximum(1000)
        self.spin_Lx_min.setValue(100)  # Default

        self.spin_Lx_max = QSpinBox()
        self.spin_Lx_max.setMinimum(10)
        self.spin_Lx_max.setMaximum(1000)
        self.spin_Lx_max.setValue(500)  # Default

        self.label_Ly = QLabel('Length Y (Ly):')
        self.spin_Ly_min = QSpinBox()
        self.spin_Ly_min.setMinimum(10)
        self.spin_Ly_min.setMaximum(1000)
        self.spin_Ly_min.setValue(100)  # Default

        self.spin_Ly_max = QSpinBox()
        self.spin_Ly_max.setMinimum(10)
        self.spin_Ly_max.setMaximum(1000)
        self.spin_Ly_max.setValue(500)  # Default

        # Random color checkbox
        self.checkbox_random_color = QCheckBox('Random Colors')
        self.checkbox_random_color.setChecked(False)

        # Line thickness input
        self.label_thickness = QLabel('Line Thickness:')
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
        layout.addWidget(self.label_N)
        layout.addWidget(self.spin_N)
        layout.addWidget(self.label_Lx)
        layout.addWidget(self.spin_Lx_min)
        layout.addWidget(self.spin_Lx_max)
        layout.addWidget(self.label_Ly)
        layout.addWidget(self.spin_Ly_min)
        layout.addWidget(self.spin_Ly_max)
        layout.addWidget(self.checkbox_random_color)
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

# Function to draw random lines with positive or negative lengths
def draw_mikado_lines(N, Lx_min, Lx_max, Ly_min, Ly_max, random_color, line_thickness, color):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Mikado Lines", "paintlayer")
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
    pen.setWidth(line_thickness)
    painter.setPen(pen)

    # Draw N random lines
    for _ in range(N):
        # Generate random start point
        x_start = random.randint(0, width)
        y_start = random.randint(0, height)

        # Generate random lengths with positive or negative values
        Lx = random.randint(Lx_min, Lx_max)
        Ly = random.randint(Ly_min, Ly_max)

        # Determine if the length should be negative
        if random.randint(0, 1) == 1:
            Lx = -Lx
        if random.randint(0, 1) == 1:
            Ly = -Ly

        # Generate random end point
        x_end = x_start + Lx
        y_end = y_start + Ly

        # Randomize color if needed
        if random_color:
            line_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            pen.setColor(line_color)
            painter.setPen(pen)

        # Draw the line
        painter.drawLine(QPointF(x_start, y_start), QPointF(x_end, y_end))

    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert to QByteArray

    # Set the modified pixel data back to the layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw random lines
def main():
    # Open the settings dialog
    dialog = MikadoDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the user-selected settings
        N = dialog.spin_N.value()
        Lx_min = dialog.spin_Lx_min.value()
        Lx_max = dialog.spin_Lx_max.value()
        Ly_min = dialog.spin_Ly_min.value()
        Ly_max = dialog.spin_Ly_max.value()
        random_color = dialog.checkbox_random_color.isChecked()
        line_thickness = dialog.spin_thickness.value()
        color = dialog.color

        # Draw the random lines based on the settings
        draw_mikado_lines(N, Lx_min, Lx_max, Ly_min, Ly_max, random_color, line_thickness, color)

# Run the main function
main()
