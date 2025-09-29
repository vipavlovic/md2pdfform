# Markdown to PDF Form Converter

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

### 1. Create a Virtual Environment

```bash
# Create project directory
mkdir md2pdfform
cd md2pdfform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install reportlab markdown beautifulsoup4
```

### 3. Download the Script

Save the script as `md2pdfform.py` in your project directory.

## Usage

### Command Line Usage

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

### Programmatic Usage

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

### Text Input Fields
```markdown
**Name:** {{text:full_name}}
**Phone:** {{text:phone_number}}
**Age:** {{number:age}}
**Email:** {{email:email_address}}
**Date of Birth:** {{date:birth_date}}
```

### Multi-line Text Areas
```markdown
**Comments:** {{textarea:comments}}              # Default 3 lines
**Detailed Feedback:** {{textarea:feedback:5}}   # Custom 5 lines
**Notes:** {{textarea:notes:10}}                 # Custom 10 lines
```

### Checkboxes
```markdown
**Subscribe to newsletter:** {{checkbox:newsletter}}
**I agree to terms:** {{checkbox:terms_agreement}}
```

### Radio Buttons
```markdown
**Gender:** {{radio:gender:Male,Female}}

**Size:** {{radio:size:Small,Medium,Large}}

**Note:** Radio groups with 2 or fewer options show as circular radio buttons.
Groups with 3+ options automatically convert to dropdown menus.
```

### Dropdown Lists
```markdown
**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}
**Country:** {{dropdown:country:USA,Canada,UK,Australia,Other}}
```

### Multiple Fields Per Line
```markdown
Total time: {{number:hours}} hours {{number:minutes}} minutes

Name: {{text:first}} {{text:last}}

Date: {{date:day}} Time: {{text:time}}
```

### Legacy Underlines
```markdown
Name: ________________________
```
(Four or more underscores automatically convert to text fields)

## Example Markdown Document

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

## Customization

### Modify Field Appearance

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

### Change Textarea Default Lines

Modify the default in `parse_markdown_forms`:

```python
if field_info['type'] == 'textarea' and 'lines' not in field_info:
    field_info['lines'] = 5  # Change from 3 to 5
```

### Adjust Page Margins

Modify in `__init__` method:

```python
self.margin = 50  # Decrease margins (was 72 = 1 inch)
```

### Custom Fonts

Modify font settings in text drawing methods:

```python
canvas.setFont("Times-Roman", 12)  # Change from Helvetica 10
```

## Troubleshooting

### Common Issues

**1. Radio buttons showing as squares**
- Radio groups with 2 options show as radio buttons
- Groups with 3+ options use dropdowns (ReportLab limitation)

**2. TypeError with 'multiline' parameter**
- The script includes automatic fallbacks for older ReportLab versions
- Try upgrading: `pip install --upgrade reportlab`

**3. Dropdown/choice fields not supported**
- Fallback to text fields with options in tooltips
- Consider upgrading ReportLab to version 3.6.0 or higher

### Version Compatibility

- **Python:** 3.6+
- **ReportLab:** 3.0+ (3.6+ recommended for full feature support)
- **Markdown:** 3.3+
- **BeautifulSoup4:** 4.9+
- **Tested on:** Windows, macOS, Linux

## Processing Multiple Files

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

1. **Radio Buttons:** Due to ReportLab limitations, radio groups with more than 2 options are converted to dropdown menus
2. **Images:** Markdown images are not currently supported
3. **Tables:** Markdown tables are not currently supported
4. **Links:** Hyperlinks are not preserved in the PDF
5. **Code Blocks:** Code blocks are rendered as plain text

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

1. Check the troubleshooting section above
2. Ensure you have the latest version of dependencies
3. Review the example markdown document
4. Open an issue on GitHub with:
   - Your Python version
   - Your ReportLab version
   - Sample markdown that causes the issue
   - Error message or unexpected behavior description

## Changelog

### v2.0 (Current)
- ✨ Multiple fields per line support
- 📄 Configurable textarea line count
- 🎨 Enhanced markdown formatting support
- 🔤 Consistent font rendering across all form fields
- 🐛 Bug fixes and improved error handling

### v1.0
- Initial release
- Basic field types support
- Markdown formatting preservation
- Error handling and fallbacks

## Field Syntax

Use these patterns in your Markdown to create form fields:

### Text Input Fields
```markdown
**Name:** {{text:full_name}}
**Phone:** {{text:phone_number}}
**Age:** {{number:age}}
**Email:** {{email:email_address}}
**Date of Birth:** {{date:birth_date}}
```

### Multi-line Text Areas
```markdown
**Comments:** {{textarea:comments}}              # Default 3 lines
**Detailed Feedback:** {{textarea:feedback:5}}   # Custom 5 lines
**Notes:** {{textarea:notes:10}}                 # Custom 10 lines
```

### Checkboxes
```markdown
**Subscribe to newsletter:** {{checkbox:newsletter}}
**I agree to terms:** {{checkbox:terms_agreement}}
```

### Radio Buttons
```markdown
**Gender:** {{radio:gender:Male,Female}}

**Size:** {{radio:size:Small,Medium,Large}}

**Note:** Radio groups with 2 or fewer options show as circular radio buttons.
Groups with 3+ options automatically convert to dropdown menus.
```

### Dropdown Lists
```markdown
**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}
**Country:** {{dropdown:country:USA,Canada,UK,Australia,Other}}
```

### Multiple Fields Per Line
```markdown
Total time: {{number:hours}} hours {{number:minutes}} minutes

Name: {{text:first}} {{text:last}}

Date: {{date:day}} Time: {{text:time}}
```

### Legacy Underlines
```markdown
Name: ________________________
```
(Four or more underscores automatically convert to text fields)

## Example Markdown Document

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

## Customization

### Modify Field Appearance

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

### Change Textarea Default Lines

Modify the default in `parse_markdown_forms`:

```python
if field_info['type'] == 'textarea' and 'lines' not in field_info:
    field_info['lines'] = 5  # Change from 3 to 5
```

### Adjust Page Margins

Modify in `__init__` method:

```python
self.margin = 50  # Decrease margins (was 72 = 1 inch)
```

### Custom Fonts

Modify font settings in text drawing methods:

```python
canvas.setFont("Times-Roman", 12)  # Change from Helvetica 10
```

## Troubleshooting

### Common Issues

**1. Radio buttons showing as squares**
- Radio groups with 2 options show as radio buttons
- Groups with 3+ options use dropdowns (ReportLab limitation)

**2. TypeError with 'multiline' parameter**
- The script includes automatic fallbacks for older ReportLab versions
- Try upgrading: `pip install --upgrade reportlab`

**3. Dropdown/choice fields not supported**
- Fallback to text fields with options in tooltips
- Consider upgrading ReportLab to version 3.6.0 or higher

### Version Compatibility

- **Python:** 3.6+
- **ReportLab:** 3.0+ (3.6+ recommended for full feature support)
- **Markdown:** 3.3+
- **BeautifulSoup4:** 4.9+
- **Tested on:** Windows, macOS, Linux

## Processing Multiple Files

```python
import os
from mk2pdfform import MarkdownToPDFForm

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

1. **Radio Buttons:** Due to ReportLab limitations, radio groups with more than 2 options are converted to dropdown menus
2. **Images:** Markdown images are not currently supported
3. **Tables:** Markdown tables are not currently supported
4. **Links:** Hyperlinks are not preserved in the PDF
5. **Code Blocks:** Code blocks are rendered as plain text

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

1. Check the troubleshooting section above
2. Ensure you have the latest version of dependencies
3. Review the example markdown document
4. Open an issue on GitHub with:
   - Your Python version
   - Your ReportLab version
   - Sample markdown that causes the issue
   - Error message or unexpected behavior description

## Changelog

### v2.0 (Current)
- ✨ Multiple fields per line support
- 📄 Configurable textarea line count
- 🎨 Enhanced markdown formatting support
- 🔤 Consistent font rendering across all form fields
- 🐛 Bug fixes and improved error handling

### v1.0
- Initial release
- Basic field types support
- Markdown formatting preservation
- Error handling and fallbacks

## Installation

### 1. Create a Virtual Environment

```bash
# Create project directory
mkdir mk2pdfform
cd mk2pdfform

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install reportlab markdown beautifulsoup4
```

### 3. Download the Script

Save the script as `mk2pdfform.py` in your project directory.

## Usage

### Command Line Usage

```bash
# Basic usage - creates input_form.pdf
python mk2pdfform.py input.md

# Specify output file
python mk2pdfform.py input.md -o output.pdf

# Show help
python mk2pdfform.py --help

# Run demo
python mk2pdfform.py demo
```

### Programmatic Usage

```python
from mk2pdfform import MarkdownToPDFForm

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

### Text Input Fields
```markdown
**Name:** {{text:full_name}}
**Phone:** {{text:phone_number}}
**Age:** {{number:age}}
**Email:** {{email:email_address}}
**Date of Birth:** {{date:birth_date}}
```

### Multi-line Text Areas
```markdown
**Comments:** {{textarea:comments}}              # Default 3 lines
**Detailed Feedback:** {{textarea:feedback:5}}   # Custom 5 lines
**Notes:** {{textarea:notes:10}}                 # Custom 10 lines
```

### Checkboxes
```markdown
**Subscribe to newsletter:** {{checkbox:newsletter}}
**I agree to terms:** {{checkbox:terms_agreement}}
```

### Radio Buttons
```markdown
**Gender:** {{radio:gender:Male,Female}}

**Size:** {{radio:size:Small,Medium,Large}}

**Note:** Radio groups with 2 or fewer options show as circular radio buttons.
Groups with 3+ options automatically convert to dropdown menus for better UX.
```

### Dropdown Lists
```markdown
**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}
**Country:** {{dropdown:country:USA,Canada,UK,Australia,Other}}
```

### Multiple Fields Per Line
```markdown
Total time: {{number:hours}} hours {{number:minutes}} minutes

Name: {{text:first}} {{text:last}}
```

### Legacy Underlines
```markdown
Name: ________________________
```
(Four or more underscores automatically convert to text fields)

## Markdown Formatting Support

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

### Bullet Points
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

## Example Markdown Document

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

## Advanced Features

### Bold Text Formatting
- **Inline bold:** `This is **bold** text` - preserves bold formatting even when text wraps
- **Entire line bold:** `**This entire line is bold**`
- **Bold in lists:** `- Item with **bold** text`

### Smart Text Wrapping
- Long paragraphs automatically wrap to fit page width
- Bold formatting is preserved across line breaks
- Text before and after form fields wraps intelligently

### Page Break Management
- Automatic page breaks when content exceeds page height
- Prevents form fields from being split across pages
- Maintains consistent font sizes across pages

### Textarea Positioning
- Textareas always start on a new line for clarity
- Label text appears above the textarea
- Content after textarea continues on a new line

## Customization

### Modify Field Appearance

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

### Change Textarea Default Lines

Modify the default in `parse_markdown_forms`:

```python
if field_info['type'] == 'textarea' and 'lines' not in field_info:
    field_info['lines'] = 5  # Change from 3 to 5
```

### Adjust Page Margins

Modify in `__init__` method:

```python
self.margin = 50  # Decrease margins (was 72 = 1 inch)
```

### Custom Fonts

Modify font settings in text drawing methods:

```python
canvas.setFont("Times-Roman", 12)  # Change from Helvetica 10
```

## Troubleshooting

### Common Issues

**1. Multiple fields on same line not rendering**
- ✅ **Fixed in current version** - Multiple fields per line now fully supported

**2. Text exceeding page width**
- ✅ **Fixed in current version** - Automatic text wrapping prevents overflow

**3. Bold text not rendering**
- ✅ **Fixed in current version** - Full bold text support with wrapping

**4. Font size inconsistent across pages**
- ✅ **Fixed in current version** - Font consistency maintained across page breaks

**5. Dropdown text doesn't match document font**
- ✅ **Fixed in current version** - All form fields use Helvetica 10pt

**6. Radio buttons showing as squares**
- Note: Radio groups with 2 options show as radio buttons
- Groups with 3+ options use dropdowns (ReportLab limitation)

**7. TypeError with 'multiline' parameter**
- The script includes automatic fallbacks for older ReportLab versions
- Try upgrading: `pip install --upgrade reportlab`

### Version Compatibility

- **Python:** 3.6+
- **ReportLab:** 3.0+ (3.6+ recommended for full feature support)
- **Markdown:** 3.3+
- **BeautifulSoup4:** 4.9+
- **Tested on:** Windows, macOS, Linux

## Processing Multiple Files

```python
import os
from mk2pdfform import MarkdownToPDFForm

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

1. **Radio Buttons:** Due to ReportLab limitations, radio groups with more than 2 options are converted to dropdown menus for reliability
2. **Images:** Markdown images are not currently supported
3. **Tables:** Markdown tables are not currently supported
4. **Links:** Hyperlinks are not preserved in the PDF
5. **Code Blocks:** Code blocks are rendered as plain text

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

1. Check the troubleshooting section above
2. Ensure you have the latest version of dependencies
3. Review the example markdown document
4. Open an issue on GitHub with:
   - Your Python version
   - Your ReportLab version
   - Sample markdown that causes the issue
   - Error message or unexpected behavior description

## Changelog

### v2.0 (Current)
- ✨ **Multiple fields per line** - Support for multiple form fields on the same line
- 📏 **Smart text wrapping** - Long text wraps intelligently, preserving formatting
- **Bold text support** - Full inline `**bold**` text with wrapping preservation
- 📐 **Page width checking** - Prevents content from exceeding page boundaries
- 🎯 **Textarea line count** - Configurable textarea height with `{{textarea:name:lines}}`
- 📄 **Horizontal rules** - Support for `---`, `***`, `___`
- 🔤 **Font consistency** - All form fields use consistent Helvetica 10pt font
- 🛠️ **Improved error handling** - Better fallbacks for ReportLab version differences
- 🐛 **Bug fixes** - Fixed duplicate textareas, checkbox wrapping, and radio button rendering

### v1.0
- Initial release
- Basic field types support
- Markdown formatting preservation
- Error handling and fallbacks
