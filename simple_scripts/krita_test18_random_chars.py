import krita as k
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QSpinBox, QPushButton, QColorDialog, QFontDialog, QDialogButtonBox
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QImage
from PyQt5.QtCore import QByteArray, Qt
import random
import string

print("random chars - 2409")

# Basic class for the settings dialog
class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Random Characters Settings')
        layout = QVBoxLayout()

        # Character type selection
        self.label_char_type = QLabel('Character Type:')
        self.combo_char_type = QComboBox()
        self.combo_char_type.addItems(['Binary (0, 1)', 'Hexadecimal (0-F)', 'Alphanumeric (A-z, 0-9)'])

        # Button to select font
        self.label_font = QLabel('Font:')
        self.button_font = QPushButton('Choose Font')
        self.button_font.clicked.connect(self.choose_font)
        self.font = QFont("Arial", 12)  # Default font

        # Button to select color
        self.label_color = QLabel('Character Color:')
        self.button_color = QPushButton('Choose Color')
        self.button_color.clicked.connect(self.choose_color)
        self.color = QColor(0, 0, 0)  # Default black color

        # Character size (height)
        self.label_size = QLabel('Character Size (px):')
        self.spin_size = QSpinBox()
        self.spin_size.setMinimum(5)
        self.spin_size.setMaximum(100)
        self.spin_size.setValue(20)

        # Spacing between characters
        self.label_spacing = QLabel('Character Spacing (px):')
        self.spin_spacing = QSpinBox()
        self.spin_spacing.setMinimum(0)
        self.spin_spacing.setMaximum(100)
        self.spin_spacing.setValue(10)

        # Line spacing
        self.label_line_spacing = QLabel('Line Spacing (px):')
        self.spin_line_spacing = QSpinBox()
        self.spin_line_spacing.setMinimum(0)
        self.spin_line_spacing.setMaximum(100)
        self.spin_line_spacing.setValue(10)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # Add widgets to the layout
        layout.addWidget(self.label_char_type)
        layout.addWidget(self.combo_char_type)
        layout.addWidget(self.label_font)
        layout.addWidget(self.button_font)
        layout.addWidget(self.label_color)
        layout.addWidget(self.button_color)
        ##layout.addWidget(self.label_size)
        ##layout.addWidget(self.spin_size)
        layout.addWidget(self.label_spacing)
        layout.addWidget(self.spin_spacing)
        layout.addWidget(self.label_line_spacing)
        layout.addWidget(self.spin_line_spacing)
        layout.addWidget(self.buttons)

        self.setLayout(layout)

    # Function to choose the font
    def choose_font(self):
        font, ok = QFontDialog.getFont(self.font)
        if ok:
            self.font = font

    # Function to choose the color for characters
    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

# Function to generate random characters based on the selected type
def generate_random_character(char_type):
    if char_type == 'Binary (0, 1)':
        return random.choice(['0', '1'])
    elif char_type == 'Hexadecimal (0-F)':
        return random.choice('0123456789ABCDEF')
    elif char_type == 'Alphanumeric (A-z, 0-9)':
        return random.choice(string.ascii_letters + string.digits)

# Function to draw random characters on the canvas
def draw_random_characters(char_type, font, color, char_size, char_spacing, line_spacing):
    krita_instance = k.Krita.instance()
    doc = krita_instance.activeDocument()

    if not doc:
        raise Exception("No active document found.")

    # Create a new layer
    new_layer = doc.createNode("Random Characters", "paintlayer")
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
    painter.setFont(font)  # Set the chosen font

    # Set the pen for drawing characters
    pen = QPen(color)
    painter.setPen(pen)

    # Start drawing characters row by row
    y_position = 0
    while y_position < height:
        x_position = 0
        while x_position < width:
            random_char = generate_random_character(char_type)  # Generate a random character
            painter.drawText(x_position, y_position, random_char)  # Draw the character
            x_position += char_size + char_spacing  # Move to the next position horizontally
        y_position += char_size + line_spacing  # Move to the next line

    # Release the painter to free memory
    painter.end()

    # Convert the QImage to QByteArray
    image_bits = image.constBits()  # Get a pointer to the image data
    image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert the image data to QByteArray

    # Set the modified pixel data back to the new layer
    new_layer.setPixelData(image_bytes, 0, 0, width, height)

    # Refresh the document to apply the changes
    doc.refreshProjection()

# Main function to run the dialog and draw random characters
def main():
    dialog = SettingsDialog()
    if dialog.exec_() == QDialog.Accepted:
        # Get the settings from the user
        char_type = dialog.combo_char_type.currentText()
        font = dialog.font
        color = dialog.color
        char_size = dialog.spin_size.value()
        char_spacing = dialog.spin_spacing.value()
        line_spacing = dialog.spin_line_spacing.value()

        # Draw random characters based on user settings
        draw_random_characters(char_type, font, color, char_size, char_spacing, line_spacing)

# Run the main function
main()
