import os
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_folder = "images_current"
languages = ["eng", "bul"]
languages = "+".join(languages)

output = ""

# Iterate over the images in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".JPG") or filename.endswith(
            ".jpeg"):
        # Build the full file path
        image_path = os.path.join(image_folder, filename)

        # Open the image file
        image = Image.open(image_path)

        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(image, lang=languages)

        # Print the extracted text
        print(f"Extracting text from {filename}...")
        print(text)
#         output += text
#
# text_file = open("output.txt", "w")
# n = text_file.write(output)
# text_file.close()

# Adding new language packs
# The Tesseract installer provided by Chocolatey currently includes only English language.
# To install other languages, download the respective language pack (.traineddata file) from
# https://github.com/tesseract-ocr/tessdata/ and place it in C:\\Program Files\\Tesseract-OCR\\tessdata (or wherever
# Tesseract OCR is installed).

# First version - with one file, works perfectly
# def extract_text_from_image(path):
#     image = Image.open(path)
#     text = pytesseract.image_to_string(image)
#     return text
#
#
# image_path = "C:/Users/BorisKondev/Code/python/brain-teasers/extract-image-text/tasks.jpg"
# extracted_text = extract_text_from_image(image_path)
# print(extracted_text)
