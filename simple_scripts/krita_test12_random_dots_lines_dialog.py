import krita as k
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QColorDialog, QDialogButtonBox
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QImage
from PyQt5.QtCore import QPoint, QByteArray, Qt
import random

# Basic class for the settings dialog
class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Points and Lines Settings')
        layout = QVBoxLayout()

        # Number of points input
        self.label_points = QLabel('Number of Points:')
        self.spin_points = QSpinBox()
        self.spin_points.setMinimum(2)  # Minimum of 2 points
        self.spin_points.setMaximum(1000)  # Maximum of 1000 points
        self.spin_points.setValue(100)  # Default value of 100 points

        # Button to select color for points
        self.label_color_points = QLabel('Points Color:')
        self.button_color_points = QPushButton('Choose Points Color')
        self.button_color_points.clicked.connect(self.choose_color_points)
        self.color_points = QColor(255, 0, 0)  # Default red color for points

        # Button to select color for lines
        self.label_color_lines = QLabel('Lines Color:')
        self.button_color_lines = QPushButton('Choose Lines Color')
        self.button_color_lines.clicked.connect(self.choose_color_lines)
        self.color_lines = QColor(128, 128, 128)  # Default gray color for lines

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)  # Action for OK
        self.buttons.rejected.connect(self.reject)  # Action for Cancel

        # Add all widgets to the layout
        layout.addWidget(self.label_points)
        layout.addWidget(self.spin_points)
        layout.addWidget(self.label_color_points)
        layout.addWidget(self.button_color_points)
        layout.addWidget(self.label_color_lines)
        layout.addWidget(self.button_color_lines)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    # Function to choose the color for points
    def choose_color_points(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_points = color  # Set the selected color for points

    # Function to choose the color for lines
    def choose_color_lines(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_lines = color  # Set the selected color for lines

# Function to draw points and lines
def draw_points_and_lines(points_count, color_points, color_lines):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer for points and lines
    new_layer = doc.createNode("Points and Lines", "paintlayer")
    doc.rootNode().addChildNode(new_layer, None)

    # Set the new layer as the active layer
    doc.setActiveNode(new_layer)

    # Get the width and height of the document
    width = doc.width()
    height = doc.height()

    # Create a QImage for drawing
    image = QImage(width, height, QImage.Format_ARGB32)
    image.fill(Qt.transparent)  # Set the background to transparent

    # Create a QPainter for drawing on the QImage
    painter = QPainter(image)

    # Set the pen for drawing lines (with the selected color and 3px width)
    pen_line = QPen(color_lines)
    pen_line.setWidth(3)  # Set the line width to 3px
    painter.setPen(pen_line)

    # List to store the generated points
    points = []

    # Generate and draw the points
    for i in range(points_count):
        x_pos = random.randint(0, width)
        y_pos = random.randint(0, height)
        point = QPoint(x_pos, y_pos)
        points.append(point)

        if i > 0:
            # Draw a line connecting the current point with the previous one
            painter.drawLine(points[i - 1], points[i])

    # Set the pen and brush for drawing circles (points)
    pen_circle = QPen(Qt.NoPen)  # No outline for circles
    brush_circle = QBrush(color_points)  # Fill the circles with the selected color
    painter.setPen(pen_circle)
    painter.setBrush(brush_circle)

    # Draw circles for each point
    for point in points:
        painter.drawEllipse(point, 10, 10)  # Draw a circle with a 21px diameter (radius 10)

    # Release the painter to free memory
    painter.end()

    # Convert the QImage to a QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert the image data to QByteArray

    # Set the modified pixel data back to the new layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw points and lines
def main():
    dialog = SettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the settings from the user
        points_count = dialog.spin_points.value()
        color_points = dialog.color_points
        color_lines = dialog.color_lines

        # Draw points and lines based on user settings
        draw_points_and_lines(points_count, color_points, color_lines)

# Run the main function
main()
