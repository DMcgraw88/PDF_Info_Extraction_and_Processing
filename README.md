# PDF_Info_Extraction_and_Processing
# Description:
# This script monitors an input folder for newly added PDF files. Upon detecting a new PDF, it extracts information from
# predefined regions using OCR. It extracts the order number, job name, and dealer name from respective regions in the PDF.
# The extracted text is sanitized for valid characters for file naming. The script renames the file using extracted variables
# and moves it to a specific folder based on the dealer name.

# Dependencies:
# - Python 3.x
# - pdf2image (pip install pdf2image)
# - pytesseract (pip install pytesseract)
# - watchdog (pip install watchdog)
# - PyPDF2 (for some PDF processing methods)

# Setup:
# 1. Install Python 3.x
# 2. Install the required libraries using `pip`:
#    - `pdf2image`: For converting PDF files to images.
#    - `pytesseract`: For performing OCR (Optical Character Recognition).
#    - `watchdog`: For monitoring file system events.
#    - `PyPDF2`: For some PDF processing methods.
# 3. Install Tesseract OCR and set the path (if not done already):
#    - Download and install Tesseract OCR from

# how to use this script:
# 1. Define the path to the folder where incoming PDFs will be dropped.
# 2. Define the path to the folder where renamed and categorized PDFs will be moved.
# 3. Define the coordinates (`x1, y1, x2, y2`) for the regions to extract text from within the PDFs.
# 4. Ensure the input folder follows the desired structure and only contains PDF files
#    with the expected content layout for successful OCR.
