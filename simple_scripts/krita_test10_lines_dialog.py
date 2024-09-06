import krita as k
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QColorDialog, QDialogButtonBox
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PyQt5.QtCore import QByteArray, Qt

# Basic class for the settings dialog
class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Line Settings')
        layout = QVBoxLayout()

        # Direction choice (horizontal or vertical)
        self.label_direction = QLabel('Line direction:')
        self.combo_direction = QComboBox()
        self.combo_direction.addItems(['Horizontal', 'Vertical'])

        # Button for selecting line color
        self.label_color_lines = QLabel('Line color:')
        self.button_color_lines = QPushButton('Select line color')
        self.button_color_lines.clicked.connect(self.choose_color_lines)
        self.color_lines = QColor(0, 0, 0)  # Default black color

        # Line spacing (in pixels)
        self.label_spacing = QLabel('Line spacing (px):')
        self.spin_spacing = QSpinBox()
        self.spin_spacing.setMinimum(1)
        self.spin_spacing.setMaximum(1000)
        self.spin_spacing.setValue(50)

        # Line thickness (in pixels)
        self.label_thickness = QLabel('Line thickness (px):')
        self.spin_thickness = QSpinBox()
        self.spin_thickness.setMinimum(1)
        self.spin_thickness.setMaximum(100)
        self.spin_thickness.setValue(3)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_direction)
        layout.addWidget(self.combo_direction)
        layout.addWidget(self.label_color_lines)
        layout.addWidget(self.button_color_lines)
        layout.addWidget(self.label_spacing)
        layout.addWidget(self.spin_spacing)
        layout.addWidget(self.label_thickness)
        layout.addWidget(self.spin_thickness)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    # Function to select line color
    def choose_color_lines(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_lines = color

# Function to draw lines
def draw_lines(direction, color_lines, spacing, thickness):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Lines", "paintlayer")
    doc.rootNode().addChildNode(new_layer, None)

    # Set the new layer as active
    doc.setActiveNode(new_layer)

    # Access the document's width and height
    width = doc.width()
    height = doc.height()

    # Create a QImage for drawing
    image = QImage(width, height, QImage.Format_ARGB32)
    image.fill(Qt.transparent)  # Transparent background

    # Create QPainter for drawing on the QImage
    painter = QPainter(image)

    # Set line color and thickness
    pen_line = QPen(color_lines)
    pen_line.setWidth(thickness)
    painter.setPen(pen_line)

    # Draw lines based on the selected direction
    if direction == 'Horizontal':
        for y in range(0, height, spacing):
            painter.drawLine(0, y, width, y)
    elif direction == 'Vertical':
        for x in range(0, width, spacing):
            painter.drawLine(x, 0, x, height)

    # Release the painter memory
    painter.end()

    # Convert QImage to QByteArray
    image_bits = image.constBits()  # Get pointer to image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert to QByteArray

    # Set the modified pixel data back to the new layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Function to show the dialog and draw the lines
def main():
    dialog = SettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the settings from the user
        direction = dialog.combo_direction.currentText()
        color_lines = dialog.color_lines
        spacing = dialog.spin_spacing.value()
        thickness = dialog.spin_thickness.value()

        # Draw the lines based on the settings
        draw_lines(direction, color_lines, spacing, thickness)

# Run the main function
main()
