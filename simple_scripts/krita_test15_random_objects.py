import krita as k
import random
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QCheckBox, QPushButton, QColorDialog, QDialogButtonBox, QComboBox
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QImage
from PyQt5.QtCore import Qt, QRectF, QPointF, QByteArray

# Basic class for the settings dialog
class RandomShapesDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Random Shapes Settings')
        layout = QVBoxLayout()

        # Shape selection (Circle or Square)
        self.label_shape = QLabel('Shape:')
        self.combo_shape = QComboBox()
        self.combo_shape.addItems(['Circle', 'Square'])

        # Size input (from and to)
        self.label_size_from = QLabel('Size from:')
        self.spin_size_from = QSpinBox()
        self.spin_size_from.setMinimum(2)
        self.spin_size_from.setMaximum(300)
        self.spin_size_from.setValue(10)

        self.label_size_to = QLabel('Size to:')
        self.spin_size_to = QSpinBox()
        self.spin_size_to.setMinimum(2)
        self.spin_size_to.setMaximum(300)
        self.spin_size_to.setValue(10)

        # Distance input (X and Y)
        self.label_distance = QLabel('Distance (X and Y):')
        self.spin_distance = QSpinBox()
        self.spin_distance.setMinimum(10)
        self.spin_distance.setMaximum(300)
        self.spin_distance.setValue(20)

        # Random color checkbox
        self.checkbox_random_color = QCheckBox('Random Color')
        self.checkbox_random_color.setChecked(False)

        # Fill checkbox
        self.checkbox_fill = QCheckBox('Fill Shapes')
        self.checkbox_fill.setChecked(False)

        # Line thickness input
        self.label_line_thickness = QLabel('Line Thickness:')
        self.spin_line_thickness = QSpinBox()
        self.spin_line_thickness.setMinimum(1)
        self.spin_line_thickness.setMaximum(20)
        self.spin_line_thickness.setValue(2)

        # Color selection
        self.label_color = QLabel('Line/Fill Color:')
        self.button_color = QPushButton('Choose Color')
        self.button_color.clicked.connect(self.choose_color)
        self.color = QColor(0, 0, 0)  # Default black color

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_shape)
        layout.addWidget(self.combo_shape)
        layout.addWidget(self.label_size_from)
        layout.addWidget(self.spin_size_from)
        layout.addWidget(self.label_size_to)
        layout.addWidget(self.spin_size_to)
        layout.addWidget(self.label_distance)
        layout.addWidget(self.spin_distance)
        layout.addWidget(self.checkbox_random_color)
        layout.addWidget(self.checkbox_fill)
        layout.addWidget(self.label_line_thickness)
        layout.addWidget(self.spin_line_thickness)
        layout.addWidget(self.label_color)
        layout.addWidget(self.button_color)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

# Function to draw random shapes
def draw_random_shapes(shape, size_from, size_to, distance, random_color, fill, line_thickness, color):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Random Shapes", "paintlayer")
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

    if fill:
        painter.setPen(Qt.NoPen)
    else:
        pen = QPen(color)
        pen.setWidth(line_thickness)
        painter.setPen(pen)

    for x in range(0, width, distance):
        for y in range(0, height, distance):
            # Determine size of the shape
            size = random.randint(size_from, size_to)

            # Randomize color if needed
            if random_color:
                shape_color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            else:
                shape_color = color

            if fill:
                brush = QBrush(shape_color)
                painter.setBrush(brush)
            else:
                painter.setBrush(Qt.NoBrush)

            # Draw the shape
            if shape == 'Circle':
                painter.drawEllipse(QPointF(x, y), size / 2, size / 2)
            elif shape == 'Square':
                painter.drawRect(QRectF(x - size / 2, y - size / 2, size, size))

    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert to QByteArray

    # Set the modified pixel data back to the layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw random shapes
def main():
    # Open the settings dialog
    dialog = RandomShapesDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the user-selected settings
        shape = dialog.combo_shape.currentText()
        size_from = dialog.spin_size_from.value()
        size_to = dialog.spin_size_to.value()
        distance = dialog.spin_distance.value()
        random_color = dialog.checkbox_random_color.isChecked()
        fill = dialog.checkbox_fill.isChecked()
        line_thickness = dialog.spin_line_thickness.value()
        color = dialog.color

        # Draw the random shapes based on the settings
        draw_random_shapes(shape, size_from, size_to, distance, random_color, fill, line_thickness, color)

# Run the main function
main()
