# Markdown to PDF Form Converter

A Python script that converts Markdown documents into interactive PDF forms using ReportLab. Transform your Markdown text with special field syntax into fillable PDF forms that users can complete and save.

## Features

- 🔄 **Convert Markdown to Interactive PDFs** - Transform text documents into fillable forms
- 📝 **Multiple Field Types** - Support for text, email, date, textarea, checkbox, radio buttons, and dropdowns
- 🎨 **Markdown Formatting** - Preserves headers, bold text, and basic formatting
- 🔧 **Flexible Syntax** - Simple field syntax that's easy to remember and use
- 🛡️ **Error Handling** - Graceful fallbacks for different ReportLab versions
- 📄 **Professional Output** - Clean, properly formatted PDF forms

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

### Basic Usage

```python
from mk2pdfform import MarkdownToPDFForm

# Create converter instance
converter = MarkdownToPDFForm()

# Convert markdown text to PDF form
markdown_text = """
# Contact Form
**Name:** {{text:full_name}}
**Email:** {{email:email_address}}
"""

converter.create_pdf_form(markdown_text, "output_form.pdf")
```

### Command Line Usage

Run the included example:

```bash
python mk2pdfform.py
```

This generates `employee_form.pdf` with a sample form.

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

### Multi-line Text
```markdown
**Comments:** {{textarea:comments}}
**Description:** {{textarea:description}}
```

### Checkboxes
```markdown
**Subscribe to newsletter:** {{checkbox:newsletter}}
**I agree to terms:** {{checkbox:terms_agreement}}
```

### Radio Buttons
```markdown
**Preferred Contact Method:**
{{radio:contact_method:Email,Phone,Text}}

**Size:**
{{radio:size:Small,Medium,Large,Extra Large}}
```

### Dropdown Lists
```markdown
**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}
**Country:** {{dropdown:country:USA,Canada,UK,Australia,Other}}
```

### Legacy Underlines
```markdown
Name: ________________________
```
(Converts underscores to text fields automatically)

## Example Markdown Document

```markdown
# Employee Information Form

Please fill out the following information:

## Personal Details

**Full Name:** {{text:full_name}}
**Email Address:** {{email:email_address}}
**Phone Number:** {{text:phone_number}}
**Date of Birth:** {{date:birth_date}}

## Work Information

**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}
**Start Date:** {{date:start_date}}
**Employment Type:** {{radio:employment_type:Full-time,Part-time,Contract}}

## Emergency Contact

**Contact Name:** {{text:emergency_name}}
**Contact Phone:** {{text:emergency_phone}}
**Relationship:** {{dropdown:relationship:Spouse,Parent,Sibling,Friend,Other}}

## Preferences

**Preferred Communication:**
{{radio:communication:Email,Phone,Text,Slack}}

**Subscribe to company newsletter:** {{checkbox:newsletter}}
**Receive SMS notifications:** {{checkbox:sms_notifications}}

## Additional Information

**Comments or Special Requirements:**
{{textarea:comments}}

**Signature:** ________________________

Thank you for completing this form!
```

## Customization

### Modify Field Appearance

You can customize the appearance by modifying the `_create_form_field` method:

```python
# Change field dimensions
width = 200  # Increase width
height = 16  # Increase height

# Change colors
borderColor = blue
textColor = red
```

### Add New Field Types

Extend the `patterns` dictionary in `parse_markdown_forms`:

```python
patterns = {
    # Existing patterns...
    'signature': r'\{\{signature:([^}]+)\}\}',  # New signature field
}
```

### Styling Options

Modify the `_draw_text_line` method to add more Markdown formatting support:

- Custom fonts
- Text colors
- Additional heading levels
- Lists and tables

## Troubleshooting

### Common Issues

**1. TypeError with 'multiline' parameter**
- Solution: The script includes fallbacks for older ReportLab versions
- Try upgrading: `pip install --upgrade reportlab`

**2. Choice fields not supported**
- Dropdowns will fallback to text fields with options in tooltips
- Consider upgrading ReportLab to version 3.6.0 or higher

**3. Font issues**
- The script uses standard fonts (Helvetica)
- For custom fonts, modify the font settings in `_draw_text_line`

### Version Compatibility

- **Python:** 3.6+
- **ReportLab:** 3.0+ (3.6+ recommended for full feature support)
- **Tested on:** Windows, macOS, Linux

## Advanced Usage

### Processing Multiple Files

```python
import os

converter = MarkdownToPDFForm()

# Process all .md files in a directory
for filename in os.listdir('markdown_files/'):
    if filename.endswith('.md'):
        with open(f'markdown_files/{filename}', 'r') as f:
            content = f.read()
        
        output_name = filename.replace('.md', '_form.pdf')
        converter.create_pdf_form(content, f'output/{output_name}')
```

### Custom Field Validation

Extend the script to add field validation:

```python
# Add validation patterns
validation_patterns = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^\+?1?-?\.?\s?\(?([0-9]{3})\)?[-\.\s]?([0-9]{3})[-\.\s]?([0-9]{4})$'
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Feel free to use, modify, and distribute as needed.

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Ensure you have the latest version of dependencies
3. Create an issue with your error message and environment details

## Changelog

### v1.0
- Initial release
- Basic field types support
- Markdown formatting preservation
- Error handling and fallbacks