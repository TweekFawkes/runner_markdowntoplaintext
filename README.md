# Markdown to Plaintext Converter for Text-to-Speech

A Python tool that converts Markdown files to plain text optimized for text-to-speech applications like Speechify. It removes formatting, URLs, and other elements that aren't suitable for audio reading, making the content clean and easy to listen to.

## Features

- Removes Markdown formatting (**, *, #, etc.)
- Removes URLs and link references
- Normalizes special characters for better text-to-speech pronunciation
- Expands abbreviations (e.g., "e.g." becomes "for example")
- Improves structure for better text-to-speech pausing and flow
- Handles various character encodings

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/markdown-to-plaintext.git
   cd markdown-to-plaintext
   ```

2. Install the required dependency:
   ```
   pip install markdown
   ```

## Usage

1. Place your Markdown files in the `inputs` directory
2. Run the converter with:
   ```
   python app.py filename.md
   ```
3. Find the converted text file in the `outputs` directory with the same base name
4. The plaintext output is ready to be used with Speechify or other text-to-speech applications

## Examples

Input markdown:
```markdown
# Digital Marketing Strategy

This strategy outlines a **cost-effective** digital marketing plan for a cybersecurity SaaS product. 

* Focus on SEO for organic growth
* Create **high-quality** content  
* Use targeted [paid advertising](https://example.com)
```

Output plaintext:
```
Digital Marketing Strategy.

This strategy outlines a cost-effective digital marketing plan for a cybersecurity SaaS product.

Focus on SEO for organic growth
Create high-quality content
Use targeted paid advertising
```

## How It Works

The converter uses the Python `markdown` library to parse Markdown syntax and extract the plain text content. It then applies several text-to-speech optimizations:

1. Character normalization (smart quotes → standard quotes)
2. Converting Markdown to HTML and then extracting only the text content
3. Removing URLs and citations that survived the markdown parsing
4. Expanding abbreviations for better speech
5. Adding sentence structure for better TTS pausing
6. Cleaning up redundant whitespace

This approach is more robust than using regular expressions alone, as it properly handles nested Markdown structures and various syntax elements.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.