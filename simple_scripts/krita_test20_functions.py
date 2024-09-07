import krita as k
import math
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QDoubleSpinBox, QComboBox, QPushButton, QDialogButtonBox, QColorDialog, QFrame
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PyQt5.QtCore import Qt, QPointF, QByteArray

# Basic class for the settings dialog
class FunctionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Parametric Function Settings')
        layout = QVBoxLayout()

        # Function selection
        self.label_function = QLabel('Select Function:')
        self.combo_function = QComboBox()
        self.combo_function.addItems([
            'y = A*sin((x+x0)/B) + C*cos((x+x0)*A)', 
            'y = B*sin((x+x0)/A) + C*cos((x+x0)/A)', 
            'y = A*sin((x+x0)*B) + A*C'
        ])

        # A0 input (start of A range)
        self.label_A0 = QLabel('A0 (start of A range):')
        self.spin_A0 = QDoubleSpinBox()
        self.spin_A0.setMinimum(-1000)
        self.spin_A0.setMaximum(1000)
        self.spin_A0.setValue(-5)  # Set default value to -5

        # A1 input (end of A range)
        self.label_A1 = QLabel('A1 (end of A range):')
        self.spin_A1 = QDoubleSpinBox()
        self.spin_A1.setMinimum(-1000)
        self.spin_A1.setMaximum(1000)
        self.spin_A1.setValue(5)  # Set default value to 5

        # B input
        self.label_B = QLabel('B (parameter B):')
        self.spin_B = QDoubleSpinBox()
        self.spin_B.setMinimum(-1000)
        self.spin_B.setMaximum(1000)
        self.spin_B.setValue(1)

        # C input
        self.label_C = QLabel('C (parameter C):')
        self.spin_C = QDoubleSpinBox()
        self.spin_C.setMinimum(-1000)
        self.spin_C.setMaximum(1000)
        self.spin_C.setValue(1)

        # Add a horizontal line
        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)

        # x0 input (x-axis shift)
        self.label_x0 = QLabel('x0 (x-axis shift):')
        self.spin_x0 = QDoubleSpinBox()
        self.spin_x0.setMinimum(-1000)
        self.spin_x0.setMaximum(1000)
        self.spin_x0.setValue(0)

        # y0 input (y-axis shift)
        self.label_y0 = QLabel('y0 (y-axis shift):')
        self.spin_y0 = QDoubleSpinBox()
        self.spin_y0.setMinimum(-1000)
        self.spin_y0.setMaximum(1000)
        self.spin_y0.setValue(0)

        # Add a second horizontal line
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)

        # N input (number of graphs)
        self.label_N = QLabel('N (number of graphs):')
        self.spin_N = QSpinBox()
        self.spin_N.setMinimum(1)
        self.spin_N.setMaximum(100)
        self.spin_N.setValue(21)

        # Spacing input
        self.label_spacing = QLabel('Spacing between graphs (px):')
        self.spin_spacing = QSpinBox()
        self.spin_spacing.setMinimum(1)
        self.spin_spacing.setMaximum(1000)
        self.spin_spacing.setValue(50)

        # Line thickness input
        self.label_thickness = QLabel('Line Thickness (px):')
        self.spin_thickness = QSpinBox()
        self.spin_thickness.setMinimum(1)
        self.spin_thickness.setMaximum(10)
        self.spin_thickness.setValue(2)

        # Color input
        self.label_color = QLabel('Line Color:')
        self.button_color = QPushButton('Choose Color')
        self.button_color.clicked.connect(self.choose_color)
        self.color = QColor(0, 0, 0)  # Default black color

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_function)
        layout.addWidget(self.combo_function)
        layout.addWidget(self.label_A0)
        layout.addWidget(self.spin_A0)
        layout.addWidget(self.label_A1)
        layout.addWidget(self.spin_A1)
        layout.addWidget(self.label_B)
        layout.addWidget(self.spin_B)
        layout.addWidget(self.label_C)
        layout.addWidget(self.spin_C)
        
        # Add the first horizontal line and x0/y0 inputs
        layout.addWidget(self.line1)
        layout.addWidget(self.label_x0)
        layout.addWidget(self.spin_x0)
        layout.addWidget(self.label_y0)
        layout.addWidget(self.spin_y0)
        
        # Add the second horizontal line
        layout.addWidget(self.line2)
        
        layout.addWidget(self.label_N)
        layout.addWidget(self.spin_N)
        layout.addWidget(self.label_spacing)
        layout.addWidget(self.spin_spacing)
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

# Function to draw parametric functions
def draw_functions(selected_function, A0, A1, B, C, x0, y0, N, spacing, line_thickness, line_color):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Parametric Functions", "paintlayer")
    doc.rootNode().addChildNode(new_layer, None)
    doc.setActiveNode(new_layer)

    # Get the width and height of the document
    width = doc.width()
    height = doc.height()

    # Get the pixel data of the current layer
    pixel_data = new_layer.pixelData(0, 0, width, height)

    # Create a QImage to draw functions on
    image = QImage(pixel_data, width, height, QImage.Format_ARGB32)
    image.fill(Qt.transparent)  # Set the background to transparent

    # Create a QPainter to draw on the QImage
    painter = QPainter(image)
    pen = QPen(line_color)
    pen.setWidth(line_thickness)
    painter.setPen(pen)

    # Calculate the step size for A
    step_A = (A1 - A0) / (N - 1)

    # Draw N graphs with different values of A
    for i in range(N):
        A = A0 + i * step_A
        y_offset = i * spacing

        # Loop through x values and calculate y based on the selected function
        points = []
        for x in range(width):
            x_value = x / width * 20 - 10  # Map x to range [-10, 10]

            try:
                # Evaluate the selected function, incorporating x0 and y0
                if selected_function == 'y = A*sin((x+x0)/B) + C*cos((x+x0)*A)':
                    y_value = A * math.sin((x_value + x0) / B) + C * math.cos((x_value + x0) * A)
                elif selected_function == 'y = B*sin((x+x0)/A) + C*cos((x+x0)/A)':
                    y_value = B * math.sin((x_value + x0) / A) + C * math.cos((x_value + x0) / A)
                elif selected_function == 'y = A*sin((x+x0)*B) + A*C':
                    y_value = A * math.sin((x_value + x0) * B) + A * C
            except ZeroDivisionError:
                y_value = 0  # Handle division by zero

            # Scale and offset y value to fit on canvas
            y_scaled = -y_value * 50 + height / 2 + y_offset + y0  # Apply y0 for vertical shift
            points.append(QPointF(x, y_scaled))

        # Draw the line using the points
        painter.drawPolyline(*points)

    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert to QByteArray

    # Set the modified pixel data back to the layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw functions
def main():
    # Open the settings dialog
    dialog = FunctionDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the user-selected settings
        selected_function = dialog.combo_function.currentText()
        A0 = dialog.spin_A0.value()
        A1 = dialog.spin_A1.value()
        B = dialog.spin_B.value()
        C = dialog.spin_C.value()
        x0 = dialog.spin_x0.value()
        y0 = dialog.spin_y0.value()
        N = dialog.spin_N.value()
        spacing = dialog.spin_spacing.value()
        line_thickness = dialog.spin_thickness.value()
        line_color = dialog.color

        # Draw the functions based on the settings
        draw_functions(selected_function, A0, A1, B, C, x0, y0, N, spacing, line_thickness, line_color)

# Run the main function
main()
