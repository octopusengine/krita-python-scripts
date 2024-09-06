import krita as k
import os
import sys
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QDialogButtonBox
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QByteArray, Qt

# Basic class for the settings dialog
class ImageSelectionDialog(QDialog):
    def __init__(self, image_files):
        super().__init__()

        self.setWindowTitle('Select an Image, Position and Zoom')
        layout = QVBoxLayout()

        # Dropdown for image file selection
        self.label_image = QLabel('Select Image:')
        self.combo_image = QComboBox()
        self.combo_image.addItems(image_files)

        # X Position for the image
        self.label_x = QLabel('X Position (px):')
        self.spin_x = QSpinBox()
        self.spin_x.setMinimum(0)
        self.spin_x.setMaximum(10000)
        self.spin_x.setValue(0)

        # Y Position for the image
        self.label_y = QLabel('Y Position (px):')
        self.spin_y = QSpinBox()
        self.spin_y.setMinimum(0)
        self.spin_y.setMaximum(10000)
        self.spin_y.setValue(0)

        # Zoom for the image
        self.label_zoom = QLabel('Zoom Factor (1-20):')
        self.spin_zoom = QSpinBox()
        self.spin_zoom.setMinimum(1)
        self.spin_zoom.setMaximum(100)
        self.spin_zoom.setValue(1)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_image)
        layout.addWidget(self.combo_image)
        layout.addWidget(self.label_x)
        layout.addWidget(self.spin_x)
        layout.addWidget(self.label_y)
        layout.addWidget(self.spin_y)
        layout.addWidget(self.label_zoom)
        layout.addWidget(self.spin_zoom)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

# Function to get all image files (PNG, JPG, JPEG) from the directory
def get_image_files(directory):
    return [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Function to load and draw the selected image at the specified position with zoom
def draw_image(selected_image, x, y, zoom_factor):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Imported Image", "paintlayer")
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

    # Load the selected image using its full path
    img_path = selected_image
    imported_image = QImage(img_path)

    # Calculate the new size based on the zoom factor (no filtering, sharp pixels)
    new_width = imported_image.width() * zoom_factor
    new_height = imported_image.height() * zoom_factor
    zoomed_image = imported_image.scaled(new_width, new_height, Qt.IgnoreAspectRatio, Qt.FastTransformation)

    # Draw the image at the specified position (x, y)
    painter.drawImage(x, y, zoomed_image)

    # Release the painter to free memory
    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert the image data to QByteArray

    # Set the modified pixel data back to the new layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and load an image
def main():
    # Use __file__ if possible to get the directory where the script is located
    try:
        script_directory = os.path.dirname(os.path.realpath(__file__))
    except NameError:
        # Fallback for environments where __file__ is not available (like some Krita environments)
        script_directory = os.path.dirname(os.path.realpath(sys.argv[0]))

    print(f"Looking for image files in: {script_directory}")  # Print the script directory
    image_files = get_image_files(script_directory)

    if not image_files:
        raise Exception(f"No image files found in the script's directory: {script_directory}")

    # Add full paths to the image files for easier loading
    image_files_with_paths = [os.path.join(script_directory, f) for f in image_files]

    # Open dialog for image selection and position input
    dialog = ImageSelectionDialog(image_files_with_paths)
    if dialog.exec_() == QDialog.Accepted:
        # Get the selected image, position and zoom from the user
        selected_image = dialog.combo_image.currentText()
        x = dialog.spin_x.value()
        y = dialog.spin_y.value()
        zoom_factor = dialog.spin_zoom.value()

        # Draw the selected image at the specified position with zoom
        draw_image(selected_image, x, y, zoom_factor)

# Run the main function
main()
