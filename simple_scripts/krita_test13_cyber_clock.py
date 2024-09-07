import krita as k
import math
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QColorDialog, QDialogButtonBox
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PyQt5.QtCore import Qt, QPointF, QByteArray

# Basic class for the settings dialog
class ConcentricCirclesLinesDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Concentric Circles and Lines Settings')
        layout = QVBoxLayout()

        # Circle distance input
        self.label_circle_distance = QLabel('Circle Distance:')
        self.spin_circle_distance = QSpinBox()
        self.spin_circle_distance.setMinimum(10)
        self.spin_circle_distance.setMaximum(100)
        self.spin_circle_distance.setValue(50)

        # Number of lines (N)
        self.label_N = QLabel('Number of Lines (N):')
        self.spin_N = QSpinBox()
        self.spin_N.setMinimum(0)
        self.spin_N.setMaximum(120)
        self.spin_N.setValue(6)

        # Line thickness input
        self.label_thickness = QLabel('Line Thickness:')
        self.spin_thickness = QSpinBox()
        self.spin_thickness.setMinimum(1)
        self.spin_thickness.setMaximum(10)
        self.spin_thickness.setValue(2)

        # Line and circle color selection
        self.label_color = QLabel('Line and Circle Color:')
        self.button_color = QPushButton('Choose Color')
        self.button_color.clicked.connect(self.choose_color)
        self.color = QColor(0, 0, 0)  # Default black color

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_circle_distance)
        layout.addWidget(self.spin_circle_distance)
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

# Function to draw concentric circles and full-span lines
def draw_concentric_circles_lines(circle_distance, N, line_thickness, color):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Concentric Circles and Lines", "paintlayer")
    doc.rootNode().addChildNode(new_layer, None)
    doc.setActiveNode(new_layer)

    # Get the width and height of the document
    width = doc.width()
    height = doc.height()

    # Calculate the center of the document
    center_x = width / 2
    center_y = height / 2

    # Create a QImage to draw on
    image = QImage(width, height, QImage.Format_ARGB32)
    image.fill(Qt.transparent)  # Set the background to transparent

    # Create a QPainter to draw on the QImage
    painter = QPainter(image)
    pen = QPen(color)
    pen.setWidth(line_thickness)
    painter.setPen(pen)

    # Draw concentric circles
    radius = circle_distance
    while radius < min(width, height) / 2:
        painter.drawEllipse(QPointF(center_x, center_y), radius, radius)
        radius += circle_distance

    # Draw lines from edge to edge through the center
    if N > 0:
        angle_step = 360 / N  # Step size for angle in degrees

        for i in range(N):
            angle = i * angle_step
            radians = math.radians(angle)

            # Calculate the intersection points on the edges of the canvas
            x_start = center_x + math.cos(radians) * (width / 2)
            y_start = center_y - math.sin(radians) * (height / 2)  # Invert y due to coordinate system

            x_end = center_x + math.cos(radians + math.pi) * (width / 2)  # Extend to the opposite side
            y_end = center_y - math.sin(radians + math.pi) * (height / 2)  # Continue to opposite side

            # Draw the line from one edge through the center to the opposite edge
            painter.drawLine(QPointF(x_start, y_start), QPointF(x_end, y_end))

    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert to QByteArray

    # Set the modified pixel data back to the layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw concentric circles and full-span lines
def main():
    # Open the settings dialog
    dialog = ConcentricCirclesLinesDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the user-selected settings
        circle_distance = dialog.spin_circle_distance.value()
        N = dialog.spin_N.value()
        line_thickness = dialog.spin_thickness.value()
        color = dialog.color

        # Draw the concentric circles and lines based on the settings
        draw_concentric_circles_lines(circle_distance, N, line_thickness, color)

# Run the main function
main()
