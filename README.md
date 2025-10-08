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
**Name with default:** {{text:full_name::John Doe}}
**Email with width and default:** {{text:email:200:user@example.com}}
```

You can optionally specify the field width in pixels and a default value. Syntax: `{{text:field_name:width:default_value}}`

### Number Fields
```markdown
**Age:** {{number:age}}
**Age (narrow):** {{number:age:60}}
**Population:** {{number:population:200}}
**Age with default:** {{number:age::25}}
**Score with width and default:** {{number:score:80:100}}
```

### Email Fields
```markdown
**Email:** {{email:email_address}}
**Email (wide):** {{email:email_address:250}}
**Email with default:** {{email:contact::user@example.com}}
```

### Date Fields
```markdown
**Date of Birth:** {{date:birth_date}}
**Event Date:** {{date:event_date:180}}
**Date with default:** {{date:start_date::2024-01-01}}
```

### Text Area Fields
```markdown
**Comments:** {{textarea:comments}} # Default 3 lines, 400px width
**Detailed Feedback:** {{textarea:feedback:5}} # Custom 5 lines, default width
**Notes:** {{textarea:notes:10:500}} # Custom 10 lines, 500px width
**Bio with default:** {{textarea:bio:5::Enter your biography here}}
**Description:** {{textarea:desc:3:400:Sample description}}
```

Text areas support optional parameters: line count, width, and default value. Syntax: `{{textarea:name:lines:width:default}}`

### Checkbox Fields
```markdown
**Subscribe to newsletter:** {{checkbox:newsletter}}
**I agree to terms:** {{checkbox:terms_agreement}}
**Checked by default:** {{checkbox:consent:true}}
**Unchecked by default:** {{checkbox:optional:false}}
```

Checkboxes can have default checked state. Use `true`, `yes`, `1`, or `checked` to check by default.

### Radio Button Groups
```markdown
**Gender:** {{radio:gender:Male,Female}}
**Size:** {{radio:size:Small,Medium,Large}}
**Gender with default:** {{radio:gender:Male,Female:Male}}
**Status with default:** {{radio:status:Active,Inactive:Active}}
```

Radio buttons can have a default selected option. Syntax: `{{radio:name:option1,option2:default_option}}`

**Note:** Radio groups with 2 or fewer options show as circular radio buttons on the same line. Groups with 3+ options automatically convert to dropdown menus.

### Dropdown Menus
```markdown
**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}
**Country:** {{dropdown:country:USA,Canada,UK,Australia,Other}}
```

### Multiple Fields Per Line
```markdown
Total time: {{number:hours:60}} hours {{number:minutes:60}} minutes
Name: {{text:first:120:John}} {{text:last:120:Smith}}
Date: {{date:day:100:2024-01-01}} Time: {{text:time:80:14:00}}
```

### Underscore Text Fields
```markdown
Name: ________________________
```
(Four or more underscores automatically convert to text fields with default width)

### Code Blocks
```markdown
Use triple backticks or triple quotes to create code blocks:

\```
def example_function():
    return "Code is rendered in monospace"
\```
```

Code blocks are rendered with monospace font (Courier) and a light gray background.

## Comprehensive Demo File

A complete demonstration file (`demo.md`) is available that showcases all features of md2pdfform. This demo includes:

### All Field Types:
- **Text fields** for various inputs with customizable widths and default values
- **Number fields** for numeric values with optional width and defaults
- **Email fields** with validation, custom widths, and default values
- **Date fields** for standardized date input with width control and defaults
- **Checkbox fields** for yes/no selections with default checked states
- **Radio button groups** (2 options displayed inline) with pre-selected defaults
- **Dropdown menus** (3+ options)
- **Text areas** with custom line counts, optional widths, and default text
- **Underscore-to-field** auto-conversion
- **Code blocks** with syntax preservation

### Advanced Features:
- **Default values** - Pre-filled form fields with example data
- **Multiple fields per line** - Demonstrates compact form layouts
- **Bold text formatting** - Both inline and full-line bold text
- **Headers** - All heading levels (H1-H4)
- **Bullet lists** - Including lists with bold text
- **Horizontal rules** - Using `---`, `***`, or `___`
- **Text wrapping** - Long paragraphs with automatic wrapping
- **Mixed content** - Complex forms combining multiple element types
- **Code blocks** - Monospace code with syntax preservation

### Demo Structure:
The demo is organized into 21 sections covering:
1. Text Input Fields (including custom widths and defaults)
2. Number and Email Fields (with width and default examples)
3. Date Fields (with width customization and defaults)
4. Checkbox Fields (with default checked states)
5. Radio Button Groups (inline display with pre-selected options)
6. Dropdown Menus
7. Text Area Fields (with custom lines, widths, and default text)
8. Multiple Fields Per Line (with custom widths and defaults)
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
20. Code Block Demonstration
21. Final Notes

### Running the Demo:
```bash
python md2pdfform.py demo.md -o demo_form.pdf
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

## Exporting Filled Forms to Excel

After users fill out your PDF forms, you can extract the data and export it to Excel using the included `pdfform2excel.py` script.

### Installation

```bash
# Install required packages for Excel export
pip install PyPDF2 openpyxl
```

### Usage

**Export a single filled PDF:**
```bash
python pdfform2excel.py demo_form.pdf -o demo_data.xlsx
```

**Export multiple filled PDFs (combines into one Excel file):**
```bash
python pdfform2excel.py form1.pdf form2.pdf form3.pdf -o combined_data.xlsx
```

**Export all PDFs in a directory:**
```bash
python pdfform2excel.py *.pdf -o all_forms.xlsx
```

### Export Modes

- **Single PDF Mode**: Creates a two-column spreadsheet (Field Name | Value)
- **Multiple PDF Mode**: Each PDF becomes a row, with all unique fields as columns - perfect for analyzing survey results or comparing multiple submissions

### Example Workflow

```bash
# 1. Create a PDF form from markdown
python md2pdfform.py demo.md -o demo_form.pdf

# 2. Distribute demo_form.pdf to users for completion

# 3. After receiving filled forms, export to Excel
python pdfform2excel.py filled_form1.pdf filled_form2.pdf filled_form3.pdf -o results.xlsx
```

The Excel export includes:
- Formatted headers with blue background
- Auto-adjusted column widths
- All field types (text, numbers, dates, checkboxes, radio buttons, dropdowns)
- Checkbox values shown as "Yes"/"No"
- Empty fields preserved for data consistency

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
- **Unicode Characters**: Superscripts and subscripts are converted to caret/underscore notation (e.g., x² becomes x^2)

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

### Version 1.3.0
- ✨ **Default field values** - Pre-fill forms with example data or placeholders
- ✨ **Code block support** - Render code with monospace font and gray background
- ✨ **Unicode normalization** - Convert superscripts/subscripts to readable notation
- 🐛 **Fixed dropdown field names** - Proper field naming without options included
- 🐛 **Fixed text wrapping after fields** - Correct spacing for wrapped text
- 🐛 **Fixed empty default values** - Support for fields with `::` syntax
- 📊 **PDF to Excel export** - New `pdfform2excel.py` script for data extraction

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