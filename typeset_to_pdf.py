from pypdf import PdfReader, PdfWriter
import fitz  # PyMuPDF

input_pdf_path="path to your typeset.pdf" # Path to the input typeset PDF file
output_pdf_name = "Converted_Book.pdf"  # Name of the output PDF file

# Load the PDF using PdfReader and PyMuPDF (fitz) for processing
reader = PdfReader(input_pdf_path)  # Used for manipulating PDF pages
doc = fitz.open(input_pdf_path)     # Used for text and graphical analysis
writer = PdfWriter()                # Used for writing the output PDF
number_of_pages = len(reader.pages) # total number of pages in the PDF

signature_size = 20                 # The number of pages to process in each forward/backward loop
first_pages_keep_empty = 5          # Number of initial pages where blank halves should not be skipped

current_page = 0                    # Tracks the current page being processed
is_right_side = True                # Boolean to determine whether to process the right or left half
return_point = 0                    # Temporary variable to store the page index during backward processing


def is_half_page_empty(page_number, check_right_side=True):
    """
    Check if the left or right half of the page is empty by examining its content.
    :param page_number: Index of the current page (zero-based).
    :param check_right_side: If True, check the right half; otherwise, check the left half.
    :return: True if the specified half is empty, False otherwise.
    """
    page = doc.load_page(page_number)
    rect = page.rect  # Get the page's rectangle size

    if check_right_side:
        # Define crop region for the right half
        crop_rect = fitz.Rect(rect.width / 2, 0, rect.width, rect.height)
    else:
        # Define crop region for the left half
        crop_rect = fitz.Rect(0, 0, rect.width / 2, rect.height)

    # Extract text from the cropped region
    text = page.get_text("text", clip=crop_rect)
    if not text.strip():  # If no text, check for graphical content
        pix = page.get_pixmap(clip=crop_rect)
        if pix.samples.count(255) == len(pix.samples):  # Check if all pixels are white
            return True  # Half-page is empty

    return False  # Half-page is not empty


def extract_and_add_page(current_page, is_right_side):
    """
    Extract the specified half of a page and add it to the output PDF.
    If the page is empty, it will not be added.
    :param current_page: Index of the current page (zero-based).
    :param is_right_side: If True, extract the right half; otherwise, extract the left half.
    """
    if ((not is_half_page_empty(current_page, is_right_side) and current_page > first_pages_keep_empty) or current_page < first_pages_keep_empty):
        page = reader.pages[current_page]

        # Save original MediaBox values
        original_upper_left = page.mediabox.upper_left
        original_upper_right = page.mediabox.upper_right

        # Modify the MediaBox to crop the desired half
        if is_right_side:
            page.mediabox.upper_left = (page.mediabox.right / 2, page.mediabox.top)
        else:
            page.mediabox.upper_right = (page.mediabox.right / 2, page.mediabox.top)

        writer.add_page(page)

        # Restore original MediaBox values
        page.mediabox.upper_right = original_upper_right
        page.mediabox.upper_left = original_upper_left


# Process the PDF to extract and reorder pages
while current_page < number_of_pages:
    # Forward pass: Process the next 20 pages in order
    for i in range(signature_size):
        extract_and_add_page(current_page, is_right_side)
        current_page += 1
        is_right_side = not is_right_side

    # Save the current page index and step back one page
    return_point = current_page
    current_page -= 1

    # Backward pass: Process the previous 20 pages in reverse order
    for j in range(signature_size):
        extract_and_add_page(current_page, is_right_side)
        current_page -= 1
        is_right_side = not is_right_side

    # Restore the original page index after the backward pass
    current_page = return_point

# Write the output PDF to disk
with open(output_pdf_name, "wb") as fp:
    writer.write(fp)

print("PDF processing complete. Output saved as ",output_pdf_name,".")
