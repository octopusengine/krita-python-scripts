import krita as k
import math
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QSpinBox, QComboBox, QPushButton, QColorDialog, QDialogButtonBox
from PyQt5.QtGui import QPainter, QColor, QPen, QImage
from PyQt5.QtCore import Qt, QPointF, QByteArray

# Basic class for the settings dialog
class Function3DDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('3D Function Plot Settings')
        layout = QVBoxLayout()

        # Function selection
        self.label_function = QLabel('Select Function:')
        self.combo_function = QComboBox()
        self.combo_function.addItems([
            'sin(A*(x^2 + y^2))/A',
            'sin(A*x) * cos(A*y)/A',
            'sin(A*sqrt(x^2 + y^2))'
        ])

        # A parameter input
        self.label_A = QLabel('A (parameter):')
        self.spin_A = QSpinBox()
        self.spin_A.setMinimum(-20)
        self.spin_A.setMaximum(20)
        self.spin_A.setValue(5)

        # K parameter input
        self.label_K = QLabel('K (coefficient):')
        self.spin_K = QSpinBox()
        self.spin_K.setMinimum(-10)
        self.spin_K.setMaximum(10)
        self.spin_K.setValue(2)

        # Density input
        self.label_density = QLabel('Density:')
        self.spin_density = QSpinBox()
        self.spin_density.setMinimum(10)
        self.spin_density.setMaximum(300)
        self.spin_density.setValue(150)

        # Scale factor input
        self.label_scale = QLabel('Scale Factor:')
        self.spin_scale = QSpinBox()
        self.spin_scale.setMinimum(1)
        self.spin_scale.setMaximum(50)
        self.spin_scale.setValue(20)

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
        layout.addWidget(self.label_function)
        layout.addWidget(self.combo_function)
        layout.addWidget(self.label_A)
        layout.addWidget(self.spin_A)
        layout.addWidget(self.label_K)
        layout.addWidget(self.spin_K)
        layout.addWidget(self.label_density)
        layout.addWidget(self.spin_density)
        layout.addWidget(self.label_scale)
        layout.addWidget(self.spin_scale)
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

# Function to calculate z-value for the selected 3D function
def calculate_z_value(func_index, A, K, x, y):
    A = A/10
    if func_index == 0:
        return math.sin(A /2 *  (x ** 2 + y ** 2))* K
    elif func_index == 1:
        return math.sin(A *  x) * math.cos(A * K * y)* K
    elif func_index == 2:
        return math.sin(A * math.sqrt(x ** 2 + y ** 2))* K

# Function to project 3D points into 2D space (isometric projection)
def project_3d_to_2d(x, y, z, scale):
    # Isometric projection formulas (scaled and rotated)
    iso_x = (x - y) * math.sqrt(2) / 2
    iso_y = (x + y) * math.sqrt(2) / 4 - z
    return iso_x * scale, iso_y * scale

# Function to draw 3D function plot
def draw_3d_function_plot(func_index, A, K, density, scale, line_thickness, color):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("3D Function Plot", "paintlayer")
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

    # Define the grid size based on density
    step_size = 50 / density

    # Draw the 3D function as a wireframe
    for x in range(-density, density):
        for y in range(-density, density):
            # Calculate z value based on the selected function
            z = calculate_z_value(func_index, A, K, x * step_size, y * step_size)

            # Project the 3D point to 2D
            proj_x, proj_y = project_3d_to_2d(x, y, z, scale)

            # Offset the projection to center it on the canvas
            proj_x += center_x
            proj_y += center_y

            # Draw a point or short line (simulating a grid)
            if x < density - 1 and y < density - 1:
                z_next_x = calculate_z_value(func_index, A, K, (x + 1) * step_size, y * step_size)
                z_next_y = calculate_z_value(func_index, A, K, x * step_size, (y + 1) * step_size)

                # Project the next points
                proj_x_next, proj_y_next = project_3d_to_2d(x + 1, y, z_next_x, scale)
                proj_x_next += center_x
                proj_y_next += center_y

                proj_x_next_y, proj_y_next_y = project_3d_to_2d(x, y + 1, z_next_y, scale)
                proj_x_next_y += center_x
                proj_y_next_y += center_y

                # Draw lines connecting points (forming a grid)
                painter.drawLine(QPointF(proj_x, proj_y), QPointF(proj_x_next, proj_y_next))
                painter.drawLine(QPointF(proj_x, proj_y), QPointF(proj_x_next_y, proj_y_next_y))

    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert to QByteArray

    # Set the modified pixel data back to the layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw 3D function plot
def main():
    # Open the settings dialog
    dialog = Function3DDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the user-selected settings
        func_index = dialog.combo_function.currentIndex()
        A = dialog.spin_A.value()
        K = dialog.spin_K.value()
        density = dialog.spin_density.value()
        scale = dialog.spin_scale.value()
        line_thickness = dialog.spin_thickness.value()
        color = dialog.color

        # Draw the 3D function plot based on the settings
        draw_3d_function_plot(func_index, A, K, density, scale, line_thickness, color)

# Run the main function
main()
