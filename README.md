# Typeset to Normal PDF Converter

A Python script to convert a typeset PDF into a readable, normal book format. It splits pages into left and right halves, reorders them, and removes empty halves while preserving specified initial pages.

## How to Use
1. Place the input typeset PDF in a directory of your choice.
2. Update the following variables in the script:
   - `input_pdf_path`: Set this to the full path of the input file (e.g., `"/path/to/your/Typeset.pdf"`).
   - `output_pdf_name`: Set this to the desired name of the output file (e.g., `"Converted_Book.pdf"`).
3. Run the script:
```bash
python script.py
```
4. The output PDF will be saved with the name you specified in `output_pdf_name` in the same directory as the script.

## Configuration
- **Signature Size**: Adjust `signature_size` in the script to control the number of pages processed per forward/backward loop.
- **Initial Pages**: Modify `first_pages_keep_empty` to preserve blank halves in the first few pages.

## Requirements
- Python 3.8+

### Install dependencies:
```bash
pip install pymupdf pypdf
```


