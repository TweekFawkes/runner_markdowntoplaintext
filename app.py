import sys
import os
import re
import unicodedata
from markdown import Markdown
from io import StringIO


def unmark_element(element, stream=None):
    """
    Recursively extract text from HTML elements.
    """
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()


# Configure Markdown converter
Markdown.output_formats["plain"] = unmark_element
__md = Markdown(output_format="plain")
__md.stripTopLevelTags = False


def unmark(text):
    """
    Convert markdown to plain text using markdown library.
    """
    return __md.convert(text)


def normalize_text(text):
    """
    Normalize special characters for better TTS reading.
    """
    # Normalize the text to handle various quotation marks and apostrophes
    text = unicodedata.normalize('NFKD', text)
    
    # Replace common problematic unicode characters
    replacements = {
        'â€™': "'",
        'â€œ': '"',
        'â€': '"',
        'â€"': '-',
        'â€"': '-',
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201c': '"',  # Left double quotation mark
        '\u201d': '"',  # Right double quotation mark
        '\u2013': '-',  # En dash
        '\u2014': '-',  # Em dash
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def optimize_for_tts(text):
    """
    Apply TTS-specific optimizations to the plain text.
    """
    # Remove standalone URLs that might have survived
    text = re.sub(r'https?://\S+', '', text)
    
    # Remove citation references in parentheses - made more general
    text = re.sub(r'\s*\([^()]{0,50}(References?|Source|SaaS|Marketing|Strategy|Solutions|Results|Statistics|Guide|ROI|Timeline|Campaign)[^()]{0,50}\)', '', text)
    
    # Expand abbreviations for better readability
    text = re.sub(r'\(e\.g\.\s*([^)]+)\)', r'for example, \1', text)
    text = re.sub(r'\(i\.e\.\s*([^)]+)\)', r'that is, \1', text)
    text = re.sub(r'\be\.g\.\s*', 'for example, ', text)
    text = re.sub(r'\bi\.e\.\s*', 'that is, ', text)
    
    # Clean up code blocks markdown artifacts
    text = re.sub(r'```[a-zA-Z0-9_\-]*\n', '', text)  # Remove code block language identifiers (allowing more characters)
    text = re.sub(r'```', '', text)  # Remove remaining code block markers
    
    # Add periods after section titles to improve TTS pausing
    text = re.sub(r'(^[A-Z][A-Za-z0-9\s():,\-\']+:?)\n', r'\1.\n', text, flags=re.MULTILINE)
    
    # Clean up excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)  # Replace multiple newlines with two
    text = re.sub(r'\s+$', '', text, flags=re.MULTILINE)  # Remove trailing whitespace
    
    # Add spacing after periods that are followed by letters (missed sentence breaks)
    text = re.sub(r'\.([A-Za-z])', r'. \1', text)
    
    return text


def convert_markdown_to_plaintext(markdown_text):
    """
    Convert markdown to TTS-friendly plain text.
    """
    # First normalize any special characters
    normalized_text = normalize_text(markdown_text)
    
    # Use the markdown library to convert to plain text
    plain_text = unmark(normalized_text)
    
    # Apply TTS-specific optimizations
    optimized_text = optimize_for_tts(plain_text)
    
    return optimized_text


def main():
    # Check if command line argument is provided
    if len(sys.argv) < 2:
        print("Error: Please provide a file name as an argument")
        print("Usage: python app.py <filename>")
        sys.exit(1)
    
    file_name = sys.argv[1]
    input_dir = os.path.join(os.getcwd(), "inputs")
    
    # Ensure inputs directory exists
    if not os.path.exists(input_dir):
        print(f"Creating 'inputs' directory at {input_dir}")
        try:
            os.makedirs(input_dir, exist_ok=True)
            print(f"Please place your Markdown files in the 'inputs' directory and try again.")
            sys.exit(0)
        except PermissionError:
            print(f"Error: Cannot create 'inputs' directory due to permission issues.")
            sys.exit(1)
    
    input_path = os.path.join(input_dir, file_name)
    
    # Verify if the file exists
    if not os.path.exists(input_path):
        print(f"Error: File not found at {input_path}")
        print(f"Make sure the file exists in the 'inputs' directory.")
        sys.exit(1)
    
    # Create output filename (same name but in outputs directory)
    base_name, _ = os.path.splitext(file_name)
    output_dir = os.path.join(os.getcwd(), "outputs")
    output_file = os.path.join(output_dir, f"{base_name}.txt")
    
    # Ensure outputs directory exists
    try:
        os.makedirs(output_dir, exist_ok=True)
    except PermissionError:
        print(f"Error: Cannot create 'outputs' directory due to permission issues.")
        sys.exit(1)
    
    print(f"Converting: {input_path}")
    print(f"Output will be saved to: {output_file}")
    
    try:
        # Read the entire file
        try:
            with open(input_path, 'r', encoding='utf-8') as file:
                markdown_content = file.read()
        except UnicodeDecodeError:
            # Fallback to another encoding if UTF-8 fails
            try:
                with open(input_path, 'r', encoding='latin-1') as file:
                    markdown_content = file.read()
                print("Note: The file was not in UTF-8 format. Used latin-1 encoding instead.")
            except Exception as e:
                print(f"Error: Unable to read the file. Reason: {e}")
                sys.exit(1)
        
        # Convert markdown to plain text
        plain_text = convert_markdown_to_plaintext(markdown_content)
        
        # Write the plain text to output file
        try:
            with open(output_file, 'w', encoding='utf-8') as out_file:
                out_file.write(plain_text)
        except Exception as e:
            print(f"Error: Failed to write output file. Reason: {e}")
            sys.exit(1)
        
        print(f"Conversion completed successfully.")
        print(f"The plain text version is ready for text-to-speech applications.")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
