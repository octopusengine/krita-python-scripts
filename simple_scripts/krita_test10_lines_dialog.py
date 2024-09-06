import krita as k
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QDialogButtonBox, QCheckBox, QColorDialog
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PyQt5.QtCore import Qt, QByteArray


"""
This Python script for Krita allows users to draw customizable lines within their artwork. 
Through a dialog interface, users can choose the line direction (horizontal or vertical), 
select a line color, set the thickness in pixels, and define the spacing between lines. 
Additionally, there is an option to create a new layer for the lines; if this option is not selected, 
the lines will be drawn on the currently active layer. The script then processes these inputs 
and draws the lines on the canvas, updating the Krita document accordingly.
"""


# Basic class for the settings dialog
class LineSettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Line Settings')
        layout = QVBoxLayout()

        # Line direction selection
        self.label_direction = QLabel('Direction:')
        self.combo_direction = QComboBox()
        self.combo_direction.addItems(['Horizontal', 'Vertical'])

        # Line color selection
        self.label_color = QLabel('Line Color:')
        self.button_color = QPushButton('Choose Color')
        self.button_color.clicked.connect(self.choose_color)
        self.color = QColor(0, 0, 0)  # Default black color

        # Line thickness (in pixels)
        self.label_thickness = QLabel('Line Thickness (px):')
        self.spin_thickness = QSpinBox()
        self.spin_thickness.setMinimum(1)
        self.spin_thickness.setMaximum(10)
        self.spin_thickness.setValue(2)

        # Line spacing (in pixels)
        self.label_spacing = QLabel('Spacing (px):')
        self.spin_spacing = QSpinBox()
        self.spin_spacing.setMinimum(1)
        self.spin_spacing.setMaximum(500)
        self.spin_spacing.setValue(50)

        # Checkbox for creating a new layer
        self.checkbox_new_layer = QCheckBox('Create a new layer')
        self.checkbox_new_layer.setChecked(False)  # Default is unchecked

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_direction)
        layout.addWidget(self.combo_direction)
        layout.addWidget(self.label_color)
        layout.addWidget(self.button_color)
        layout.addWidget(self.label_thickness)
        layout.addWidget(self.spin_thickness)
        layout.addWidget(self.label_spacing)
        layout.addWidget(self.spin_spacing)
        layout.addWidget(self.checkbox_new_layer)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

# Function to draw lines based on user settings
def draw_lines(direction, color, thickness, spacing, create_new_layer):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer if requested
    if create_new_layer:
        new_layer = doc.createNode("Lines Layer", "paintlayer")
        doc.rootNode().addChildNode(new_layer, None)
        doc.setActiveNode(new_layer)

    # Get the active layer
    active_layer = doc.activeNode()

    # Get the width and height of the document
    width = doc.width()
    height = doc.height()

    # Get the pixel data of the current layer
    pixel_data = active_layer.pixelData(0, 0, width, height)

    # Create a QImage to draw lines on
    image = QImage(pixel_data, width, height, QImage.Format_ARGB32)

    # Create a QPainter to draw on the QImage
    painter = QPainter(image)
    painter.setPen(QPen(color, thickness))

    # Draw lines based on the selected direction
    if direction == 'Horizontal':
        for y in range(0, height, spacing):
            painter.drawLine(0, y, width, y)
    elif direction == 'Vertical':
        for x in range(0, width, spacing):
            painter.drawLine(x, 0, x, height)

    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert to QByteArray

    # Set the modified pixel data back to the layer
    active_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw lines
def main():
    # Open dialog for line settings
    dialog = LineSettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the settings from the user
        direction = dialog.combo_direction.currentText()
        color = dialog.color
        thickness = dialog.spin_thickness.value()
        spacing = dialog.spin_spacing.value()
        create_new_layer = dialog.checkbox_new_layer.isChecked()

        # Draw lines based on the user settings
        draw_lines(direction, color, thickness, spacing, create_new_layer)

# Run the main function
main()
