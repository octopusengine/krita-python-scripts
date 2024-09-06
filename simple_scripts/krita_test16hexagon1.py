import krita as k
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QColorDialog, QDialogButtonBox
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QImage
from PyQt5.QtCore import QPointF, QByteArray, Qt
import math

# Basic class for the settings dialog
class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Hexagon Settings')
        layout = QVBoxLayout()

        # Hexagon width (in pixels)
        self.label_width = QLabel('Hexagon Width (px):')
        self.spin_width = QSpinBox()
        self.spin_width.setMinimum(10)
        self.spin_width.setMaximum(200)
        self.spin_width.setValue(50)

        # Spacing between hexagons (in pixels)
        self.label_spacing = QLabel('Spacing between hexagons (px):')
        self.spin_spacing = QSpinBox()
        self.spin_spacing.setMinimum(0)
        self.spin_spacing.setMaximum(100)
        self.spin_spacing.setValue(10)

        # Button to select color
        self.label_color = QLabel('Hexagon Color:')
        self.button_color = QPushButton('Choose Color')
        self.button_color.clicked.connect(self.choose_color)
        self.color = QColor(0, 0, 0)  # Default black color

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_width)
        layout.addWidget(self.spin_width)
        layout.addWidget(self.label_spacing)
        layout.addWidget(self.button_color)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    # Function to choose the color for hexagons
    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

# Function to calculate the hexagon points
def create_hexagon(center, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        x = center.x() + size * math.cos(angle_rad)
        y = center.y() + size * math.sin(angle_rad)
        points.append(QPointF(x, y))
    return points

# Function to draw hexagons on the canvas
def draw_hexagons(hex_width, hex_color, spacing):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Hexagons", "paintlayer")
    doc.rootNode().addChildNode(new_layer, None)

    # Set the new layer as active
    doc.setActiveNode(new_layer)

    # Get the width and height of the document
    width = doc.width()
    height = doc.height()

    # Create a QImage for drawing
    image = QImage(width, height, QImage.Format_ARGB32)
    image.fill(Qt.transparent)  # Set the background to transparent

    # Create QPainter for drawing on the QImage
    painter = QPainter(image)
    painter.setPen(QPen(hex_color))  # Set the pen with hexagon color
    painter.setBrush(QBrush(hex_color))  # Set the brush with hexagon color

    # Calculate the height of a hexagon
    hex_height = math.sqrt(3) * hex_width / 2  # Height of a regular hexagon

    # Start drawing hexagons row by row
    y_position = 0
    row = 0
    while y_position < height:
        x_position = 0 if row % 2 == 0 else hex_width / 2  # Offset for even rows
        while x_position < width:
            # Calculate the center of the hexagon
            center = QPointF(x_position + hex_width / 2, y_position + hex_height / 2)
            # Get the hexagon points
            hexagon_points = create_hexagon(center, hex_width / 2)
            # Draw the hexagon
            painter.drawPolygon(hexagon_points)
            x_position += hex_width + spacing  # Move to the next hexagon in the row

        y_position += hex_height + spacing  # Move to the next row
        row += 1

    # Release the painter to free memory
    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert the image data to QByteArray

    # Set the modified pixel data back to the new layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw hexagons
def main():
    dialog = SettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the settings from the user
        hex_width = dialog.spin_width.value()
        hex_color = dialog.color
        spacing = dialog.spin_spacing.value()

        # Draw hexagons based on user settings
        draw_hexagons(hex_width, hex_color, spacing)

# Run the main function
main()
