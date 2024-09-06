import krita as k
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QImage
from PyQt5.QtCore import QByteArray, Qt

# Get Krita instance
krita_instance = k.Krita.instance()

# Get the active document
doc = krita_instance.activeDocument()

# Check if there is an active document
if not doc:
    raise Exception("No active document found.")

# Create a new layer
new_layer = doc.createNode("Lines and Text", "paintlayer")
doc.rootNode().addChildNode(new_layer, None)  # Add the new layer to the root node

# Set the new layer as active
doc.setActiveNode(new_layer)

# Get the document's width and height
width = doc.width()
height = doc.height()

# Define the area to draw on (x, y, width, height)
x = 0
y = 0

# Create a QImage for drawing
image = QImage(width, height, QImage.Format_ARGB32)
image.fill(Qt.transparent)  # Set the background to transparent

# Create a QPainter to draw on the QImage
painter = QPainter(image)

# Set the black color for the lines
pen = QPen(QColor(0, 0, 0))  # Black color
pen.setWidth(2)  # Set line width to 2px
painter.setPen(pen)

# Starting position for the lines
start_y = 80  # Start drawing lines 80px from the top to leave space for the text
spacing = 50  # Spacing between the lines

# Draw horizontal lines every 50px
for y_position in range(start_y, height, spacing):
    painter.drawLine(0, y_position, width, y_position)

# Set the black color for the text
painter.setPen(QColor(0, 0, 0))

# Set the font for the text
font = QFont("Verdana", 50)  # Use Verdana font, size 50
painter.setFont(font)

# Calculate the position to center the text
text = "test"
text_width = painter.fontMetrics().width(text)
text_x = (width - text_width) // 2  # Center the text horizontally
text_y = 70  # Position the text 40px from the top

# Draw the text
painter.drawText(text_x, text_y, text)

# Release the painter to free memory
painter.end()

# Convert the QImage to QByteArray
image_bits = image.constBits()  # Get a pointer to the image data
image_bytes = QByteArray(image_bits.asstring(image.byteCount()))  # Convert the data to QByteArray

# Set the modified pixel data back to the new layer
new_layer.setPixelData(image_bytes, x, y, width, height)

# Refresh the document to apply changes
doc.refreshProjection()  # Refresh the document projection
