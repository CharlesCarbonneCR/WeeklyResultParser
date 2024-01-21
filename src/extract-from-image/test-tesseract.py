import pytesseract
from PIL import Image

# Open the image file
image = Image.open('./test.jpeg')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Perform OCR using PyTesseract
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)


#C:\Program Files\Tesseract-OCR
