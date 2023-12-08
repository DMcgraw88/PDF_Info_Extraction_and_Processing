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


import os
import string
import unicodedata
from pdf2image import convert_from_path
import pytesseract
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

# Sanitize text to ensure valid characters for file naming
def sanitize_text(text):
    if text is None:
        return ''  # Return an empty string for None values
    valid_chars = f"-_.() {string.ascii_letters}{string.digits}"
    normalized_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()
    # Filter out characters not in valid_chars
    sanitized_text = ''.join(c if c in valid_chars else '' for c in normalized_text)
    return sanitized_text


# Monitor the input folder for new PDF files
class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:  # Skip directories
            return
        if event.src_path.endswith('.pdf'):  # Process only PDF files
            process_file(event.src_path)



# Extract all numbers from the defined region
def extract_numbers_from_region(region):
    extracted_text = pytesseract.image_to_string(region)
    numbers = re.findall(r'\d+', extracted_text)  # Extract all numerical values
    concatenated_numbers = ''.join(numbers)  # Concatenate all extracted numbers
    return concatenated_numbers


# Extract text after "Job Name" until two consecutive empty spaces
def extract_text_after_job_name(text):
    match = re.search(r'Job Name:(.*?)\n\n', text, re.DOTALL)
    if match:
        job_name_info = match.group(1).strip()
        return job_name_info
    else:
        return None  # Return None if "Job Name" info is not found
    
# Extract the first line as the Dealer Name from the specified region
def extract_dealer_name(text):
    lines = text.split('\n')
    if lines:
        return lines[0].strip()  # Extract the first line as the dealer name
    else:
        return None  # Return None if no lines are found


def process_file(pdf_path):
    # Convert the first page of the PDF to an image
    pages = convert_from_path(pdf_path, first_page=1, last_page=1)

    # Assuming x1, y1, x2, y2 are the coordinates of the regions you want to extract text from
    x1_1, y1_1, x2_1, y2_1 = 1300, 150, 2000, 400
    x1_2, y1_2, x2_2, y2_2 = 20, 700, 900, 900
    x1_3, y1_3, x2_3, y2_3 = 90, 480, 900, 720

    # Extract text from the specified regions
    for i, page in enumerate(pages):
        # Crop regions from the page image
        region1 = page.crop((x1_1, y1_1, x2_1, y2_1))
        region2 = page.crop((x1_2, y1_2, x2_2, y2_2))
        region3 = page.crop((x1_3, y1_3, x2_3, y2_3))

        # Perform OCR on cropped regions
        OrderNumber = extract_numbers_from_region(region1)
        extracted_text = pytesseract.image_to_string(region2)
        JobName = extract_text_after_job_name(extracted_text)
        extracted_text = pytesseract.image_to_string(region3)
        DealerName = extract_dealer_name(extracted_text)


        # Rename the file using extracted variables
        base_name, extension = os.path.splitext(pdf_path)
        new_file_name = f"{sanitize_text(OrderNumber)}_{sanitize_text(JobName)}{extension}"
        os.rename(pdf_path, new_file_name)

        # For debugging
        #print(f"Text from Region 1 on page {i + 1}:")
        #print(OrderNumber)
        #print(f"Text from Region 2 on page {i + 1}:")
        #print(JobName)
        #print(f"Text from Region 3 on page {i + 1}:")
        #print(DealerName)

        # Generate the destination folder based on DealerName
        dealer_folder = sanitize_text(DealerName)  # Sanitize the DealerName for folder naming
        destination_folder = f'/ your output folder path here /{dealer_folder}' # Replace with output folder path

        # Create the dealer-specific folder if it doesn't exist
        os.makedirs(destination_folder, exist_ok=True)

        # Move the file to the dealer-specific folder
        shutil.move(new_file_name, os.path.join(destination_folder, new_file_name))
        
 # Run the script       
if __name__ == "__main__":
    folder_to_watch = '/ your input folder path here'  # Replace with folder to monitor

    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
