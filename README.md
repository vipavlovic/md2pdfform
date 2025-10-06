# md2pdfform

A Python script that converts Markdown documents into interactive PDF forms using ReportLab. Transform your Markdown text with special field syntax into fillable PDF forms that users can complete and save.

## Features

- 🔄 **Convert Markdown to Interactive PDFs** - Transform text documents into fillable forms
- 📝 **Multiple Field Types** - Support for text, email, number, date, textarea, checkbox, radio buttons, and dropdowns
- 🔢 **Multiple Fields Per Line** - Place multiple form fields on the same line
- 📄 **Multi-Line Text Areas** - Configurable line count for textarea fields
- 🎨 **Markdown Formatting** - Bold text, headers, bullet points, and horizontal rules
- 📏 **Smart Text Handling** - Automatic text wrapping and page breaks
- 🎯 **Professional Output** - Clean, properly formatted PDF forms with consistent fonts
- 🛡️ **Error Handling** - Graceful fallbacks for different ReportLab versions

## Installation

### Prerequisites
- Python 3.6+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/vipavlovic/md2pdfform.git
cd md2pdfform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install reportlab markdown beautifulsoup4
```

## Usage

### Command Line

```bash
# Basic usage - creates input_form.pdf
python md2pdfform.py input.md

# Specify output file
python md2pdfform.py input.md -o output.pdf

# Show help
python md2pdfform.py --help

# Run demo
python md2pdfform.py demo
```

### Python API

```python
from md2pdfform import MarkdownToPDFForm

# Create converter instance
converter = MarkdownToPDFForm()

# Convert markdown file to PDF form
converter.create_pdf_form_from_file("input.md", "output.pdf")

# Or convert markdown text directly
markdown_text = """
# Contact Form
**Name:** {{text:full_name}}
**Email:** {{email:email_address}}
"""
converter.create_pdf_form(markdown_text, "output_form.pdf")
```

## Field Syntax

Use these patterns in your Markdown to create form fields:

### Text Fields
```markdown
**Name:** {{text:full_name}}
**Phone:** {{text:phone_number}}
**Short Code:** {{text:code:80}}
**Long Address:** {{text:address:250}}
```

You can optionally specify the field width in pixels as the last parameter. Default width is 150px.

### Number Fields
```markdown
**Age:** {{number:age}}
**Age (narrow):** {{number:age:60}}
**Population:** {{number:population:200}}
```

### Email Fields
```markdown
**Email:** {{email:email_address}}
**Email (wide):** {{email:email_address:250}}
```

### Date Fields
```markdown
**Date of Birth:** {{date:birth_date}}
**Event Date:** {{date:event_date:180}}
```

### Text Area Fields
```markdown
**Comments:** {{textarea:comments}} # Default 3 lines, 400px width
**Detailed Feedback:** {{textarea:feedback:5}} # Custom 5 lines, default width
**Notes:** {{textarea:notes:10:500}} # Custom 10 lines, 500px width
```

Text areas support two optional parameters: line count and width. The line count comes first, then the width.

### Checkbox Fields
```markdown
**Subscribe to newsletter:** {{checkbox:newsletter}}
**I agree to terms:** {{checkbox:terms_agreement}}
```

### Radio Button Groups
```markdown
**Gender:** {{radio:gender:Male,Female}}
**Size:** {{radio:size:Small,Medium,Large}}
```

**Note:** Radio groups with 2 or fewer options show as circular radio buttons on the same line. Groups with 3+ options automatically convert to dropdown menus.

### Dropdown Menus
```markdown
**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}
**Country:** {{dropdown:country:USA,Canada,UK,Australia,Other}}
```

### Multiple Fields Per Line
```markdown
Total time: {{number:hours:60}} hours {{number:minutes:60}} minutes
Name: {{text:first:120}} {{text:last:120}}
Date: {{date:day:100}} Time: {{text:time:80}}
```

### Underscore Text Fields
```markdown
Name: ________________________
```
(Four or more underscores automatically convert to text fields with default width)

## Comprehensive Demo File

A complete demonstration file (`comprehensive-demo.md`) is available that showcases all features of md2pdfform. This demo includes:

### All Field Types:
- **Text fields** for various inputs (names, addresses, etc.) with customizable widths
- **Number fields** for numeric values with optional width specification
- **Email fields** with validation and custom widths
- **Date fields** for standardized date input with width control
- **Checkbox fields** for yes/no selections
- **Radio button groups** (2 options displayed inline)
- **Dropdown menus** (3+ options)
- **Text areas** with custom line counts (3, 5, 7, 10 lines) and optional widths
- **Underscore-to-field** auto-conversion

### Advanced Features:
- **Multiple fields per line** - Demonstrates compact form layouts
- **Bold text formatting** - Both inline and full-line bold text
- **Headers** - All heading levels (H1-H4)
- **Bullet lists** - Including lists with bold text
- **Horizontal rules** - Using `---`, `***`, or `___`
- **Text wrapping** - Long paragraphs with automatic wrapping
- **Mixed content** - Complex forms combining multiple element types

### Demo Structure:
The demo is organized into 20 sections covering:
1. Text Input Fields (including custom widths)
2. Number and Email Fields (with width examples)
3. Date Fields (with width customization)
4. Checkbox Fields
5. Radio Button Groups (inline display for 2 options)
6. Dropdown Menus
7. Text Area Fields (with custom lines and widths)
8. Multiple Fields Per Line (with custom widths)
9. Underscore Text Fields
10. Markdown Formatting Features
11. Bullet Lists with Formatting
12. Horizontal Rules
13. Mixed Content Example
14. Long Text Wrapping Test
15. Complex Form Section
16. Survey Questions
17. Date and Time Information
18. Terms and Certification
19. Signature Block
20. Final Notes

### Running the Demo:
```bash
python md2pdfform.py comprehensive-demo.md -o demo_output.pdf
```

This generates a complete PDF form demonstrating all capabilities of the tool, making it perfect for testing, learning the syntax, and as a reference for creating your own forms.

## Example Document

```markdown
# Employee Information Form

Please fill out the following information:

---

## Personal Details

**Full Name:** {{text:full_name}}
**Email Address:** {{email:email_address}}
**Phone Number:** {{text:phone_number}}
**Date of Birth:** {{date:birth_date}}

## Work Information

**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}
**Start Date:** {{date:start_date}}
**Employment Type:** {{radio:employment_type:Full-time,Part-time}}

---

## Emergency Contact

**Contact Name:** {{text:emergency_name}}
**Contact Phone:** {{text:emergency_phone}}
**Relationship:** {{dropdown:relationship:Spouse,Parent,Sibling,Friend,Other}}

## Preferences

**Preferred Communication:** {{radio:communication:Email,Phone}}
**Subscribe to company newsletter:** {{checkbox:newsletter}}
**Receive SMS notifications:** {{checkbox:sms_notifications}}

---

## Additional Information

**Please provide any comments or special requirements:**

{{textarea:comments:5}}

**I certify that the information provided is accurate:**
{{checkbox:certification}}

**Signature:** ________________________ **Date:** {{date:signature_date}}

---

Thank you for completing this form!
```

## Supported Markdown Features

The converter supports standard Markdown formatting:

### Headers
```markdown
# Heading 1
## Heading 2
### Heading 3
```

### Bold Text
```markdown
This is **bold text** in a paragraph.
**Entire line is bold**
```

### Bullet Lists
```markdown
- First item
- Second item with **bold text**
- Third item
```

### Horizontal Rules
```markdown
---
***
___
```

## Text Handling Features

### Bold Text Wrapping
- Inline bold: `This is **bold** text` - preserves bold formatting even when text wraps
- Entire line bold: `**This entire line is bold**`
- Bold in lists: `- Item with **bold** text`

### Automatic Text Wrapping
- Long paragraphs automatically wrap to fit page width
- Bold formatting is preserved across line breaks
- Text before and after form fields wraps intelligently

### Page Breaks
- Automatic page breaks when content exceeds page height
- Prevents form fields from being split across pages
- Maintains consistent font sizes across pages

### Textarea Behavior
- Textareas always start on a new line for clarity
- Label text appears above the textarea
- Content after textarea continues on a new line

## Customization

### Field Appearance

Edit the `_create_form_field` method to customize field appearance:

```python
# In _create_form_field method:
width = 200  # Increase text field width
height = 16  # Increase text field height

# Change colors
borderColor = blue
textColor = red
fillColor = lightgrey
```

### Default Textarea Lines

Modify the default in `parse_markdown_forms`:

```python
if field_info['type'] == 'textarea' and 'lines' not in field_info:
    field_info['lines'] = 5  # Change from 3 to 5
```

### Page Margins

Modify in `__init__` method:

```python
self.margin = 50  # Decrease margins (was 72 = 1 inch)
```

### Font Settings

Modify font settings in text drawing methods:

```python
canvas.setFont("Times-Roman", 12)  # Change from Helvetica 10
```

## Troubleshooting

### 1. Radio buttons showing as squares
- Radio groups with 2 options show as radio buttons
- Groups with 3+ options use dropdowns (ReportLab limitation)

### 2. TypeError with 'multiline' parameter
- The script includes automatic fallbacks for older ReportLab versions
- Try upgrading:
```bash
pip install --upgrade reportlab
```

### 3. Dropdown/choice fields not supported
- Fallback to text fields with options in tooltips
- Consider upgrading ReportLab to version 3.6.0 or higher

## Requirements

- Python: 3.6+
- ReportLab: 3.0+ (3.6+ recommended for full feature support)
- Markdown: 3.3+
- BeautifulSoup4: 4.9+
- Tested on: Windows, macOS, Linux

## Batch Processing

```python
import os
from md2pdfform import MarkdownToPDFForm

converter = MarkdownToPDFForm()

# Process all .md files in a directory
input_dir = 'markdown_files/'
output_dir = 'output_pdfs/'

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith('.md'):
        input_path = os.path.join(input_dir, filename)
        output_name = filename.replace('.md', '_form.pdf')
        output_path = os.path.join(output_dir, output_name)
        
        converter.create_pdf_form_from_file(input_path, output_path)
        print(f"Converted: {filename} -> {output_name}")
```

## Known Limitations

- **Radio Buttons**: Due to ReportLab limitations, radio groups with more than 2 options are converted to dropdown menus
- **Images**: Markdown images are not currently supported
- **Tables**: Markdown tables are not currently supported
- **Links**: Hyperlinks are not preserved in the PDF
- **Code Blocks**: Code blocks are rendered as plain text

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Support

For issues and questions:
- Check the troubleshooting section above
- Ensure you have the latest version of dependencies
- Review the example markdown document
- Open an issue on GitHub with:
  - Your Python version
  - Your ReportLab version
  - Sample markdown that causes the issue
  - Error message or unexpected behavior description

## Changelog

### Version 1.2.0
- ✨ **Field width customization** - Specify custom widths for text, email, number, and date fields
- ✨ **Textarea width control** - Set custom widths for text area fields
- 🐛 **Fixed radio button layout** - 2-option radio groups now display inline on the same line
- 🐛 **Fixed checkbox text wrapping** - Checkbox labels now stay on the same line as the checkbox
- 🐛 **Improved heading spacing** - Proper blank lines before headings following form fields
- 📏 **Better field spacing** - Automatic space insertion between fields and following text

### Version 1.1.0
- ✨ Multiple fields per line - Support for multiple form fields on the same line
- 📏 Smart text wrapping - Long text wraps intelligently, preserving formatting
- **Bold text support** - Full inline `**bold**` text with wrapping preservation
- 📐 Page width checking - Prevents content from exceeding page boundaries
- 🎯 Textarea line count - Configurable textarea height with `{{textarea:name:lines}}`
- 📄 Horizontal rules - Support for `---`, `***`, `___`
- 🔤 Font consistency - All form fields use consistent Helvetica 10pt font
- 🛠️ Improved error handling - Better fallbacks for ReportLab version differences
- 🐛 Bug fixes - Fixed duplicate textareas, checkbox wrapping, and radio button rendering

### Version 1.0.0
- Initial release
- Basic field types support
- Markdown formatting preservation
- Error handling and fallbacks