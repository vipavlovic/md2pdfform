import re
import sys
import argparse
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfform
from reportlab.lib.colors import black, blue, red
from reportlab.lib.utils import simpleSplit
import markdown
from bs4 import BeautifulSoup

class MarkdownToPDFForm:
    def __init__(self):
        self.width, self.height = letter
        self.margin = 72  # 1 inch margins
        self.line_height = 14
        self.current_y = self.height - self.margin
        self.available_width = self.width - (2 * self.margin)  # Width minus both margins
        
    def parse_markdown_forms(self, md_text):
        """Parse markdown text and identify form field patterns"""
        # Define patterns for different form field types
        patterns = {
            'text': r'\{\{text:([^}]+)\}\}',           # {{text:field_name}}
            'email': r'\{\{email:([^}]+)\}\}',         # {{email:field_name}}
            'number': r'\{\{number:([^}]+)\}\}',       # {{number:field_name}}
            'date': r'\{\{date:([^}]+)\}\}',           # {{date:field_name}}
            'textarea_with_lines': r'\{\{textarea:([^}]+):(\d+)\}\}',  # {{textarea:field_name:lines}}
            'textarea': r'\{\{textarea:([^}]+)\}\}',   # {{textarea:field_name}} - defaults to 3 lines
            'checkbox': r'\{\{checkbox:([^}]+)\}\}',   # {{checkbox:field_name}}
            'radio': r'\{\{radio:([^}]+):([^}]+)\}\}', # {{radio:field_name:option1,option2}}
            'dropdown': r'\{\{dropdown:([^}]+):([^}]+)\}\}', # {{dropdown:field_name:option1,option2}}
            'underlines': r'_{4,}',                    # Four or more underscores
        }
        
        form_fields = []
        processed_text = md_text
        
        # Collect ALL matches from ALL patterns first
        all_matches = []
        
        for field_type, pattern in patterns.items():
            print(f"Searching for pattern: {field_type} = {pattern}")
            matches = re.finditer(pattern, md_text)
            for match in matches:
                print(f"  Found match: {match.group()} at position {match.start()}-{match.end()}")
                match_info = {
                    'field_type': field_type,
                    'match': match,
                    'start': match.start(),
                    'end': match.end(),
                    'text': match.group()
                }
                
                if field_type in ['radio', 'dropdown']:
                    match_info['field_name'] = match.group(1)
                    match_info['options'] = match.group(2).split(',')
                elif field_type == 'textarea_with_lines':
                    match_info['field_name'] = match.group(1)
                    match_info['lines'] = int(match.group(2))
                elif field_type == 'textarea':
                    match_info['field_name'] = match.group(1)
                    match_info['lines'] = 3  # Default to 3 lines
                elif field_type == 'underlines':
                    match_info['field_name'] = f"field_{len(all_matches) + 1}"
                    match_info['field_type'] = 'text'  # Convert underlines to text
                else:
                    match_info['field_name'] = match.group(1)
                
                all_matches.append(match_info)
                print(f"    Added field: {match_info.get('field_name', 'unnamed')} ({match_info['field_type']})")
        
        # Sort all matches by position to avoid conflicts
        all_matches.sort(key=lambda x: x['start'])
        
        # Convert to the expected format
        for match_info in all_matches:
            field_data = {
                'type': match_info['field_type'],
                'name': match_info['field_name'],
                'match': match_info['match'],
                'start': match_info['start'],
                'end': match_info['end'],
                'placeholder': match_info['text']
            }
            
            if 'options' in match_info:
                field_data['options'] = [opt.strip() for opt in match_info['options']]
            if 'lines' in match_info:
                field_data['lines'] = match_info['lines']
            
            form_fields.append(field_data)
        
        print(f"Total fields found: {len(form_fields)}")
        return form_fields, processed_text
    
    def test_basic_pdf_creation(self, filename):
        """Test basic PDF creation to verify ReportLab works"""
        print(f"Testing basic PDF creation: {filename}")
        try:
            c = canvas.Canvas(filename, pagesize=letter)
            c.drawString(100, 750, "Hello World - Test PDF")
            c.save()
            print(f"Basic PDF test completed")
            
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"Test PDF created successfully: {size} bytes")
                return True
            else:
                print("Test PDF was not created")
                return False
        except Exception as e:
            print(f"Error in basic PDF test: {e}")
            import traceback
            traceback.print_exc()
            return False

    def create_pdf_form_from_file(self, input_file, output_file=None):
        """Convert markdown file to PDF form"""
        print(f"Starting conversion of: {input_file}")
        
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        print(f"Input file exists: {input_file}")
        
        # Generate output filename if not provided
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_form.pdf"
        
        print(f"Output file will be: {output_file}")
        
        # Read markdown file
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            print(f"Read {len(markdown_content)} characters from file")
            print(f"Content preview: {repr(markdown_content[:100])}")
        except Exception as e:
            raise Exception(f"Error reading file {input_file}: {e}")
        
        # Create PDF form
        print("Calling create_pdf_form...")
        try:
            result = self.create_pdf_form(markdown_content, output_file)
            print("create_pdf_form completed successfully")
        except Exception as e:
            print(f"Exception in create_pdf_form: {e}")
            import traceback
            traceback.print_exc()
            raise
        print("Returning from create_pdf_form_from_file")
        return output_file

    def create_pdf_form(self, md_text, output_filename):
        """Convert markdown text with form patterns to PDF form"""
        print(f"Processing markdown text ({len(md_text)} characters)")
        
        try:
            # Remove existing file if it exists
            if os.path.exists(output_filename):
                print(f"Removing existing file: {output_filename}")
                try:
                    os.remove(output_filename)
                    print(f"Successfully removed existing file")
                except OSError as e:
                    print(f"Warning: Could not remove existing file: {e}")
                    # Try to continue anyway
            
            form_fields, text = self.parse_markdown_forms(md_text)
            print(f"Found {len(form_fields)} form fields")
            
            # Create PDF canvas
            print(f"Creating canvas for: {output_filename}")
            c = canvas.Canvas(output_filename, pagesize=letter)
            print(f"Canvas created successfully")
            
            # Convert markdown to HTML first, then extract text
            html = markdown.markdown(text)
            soup = BeautifulSoup(html, 'html.parser')
            
            # Process text line by line
            lines = text.split('\n')
            print(f"Processing {len(lines)} lines")
            
            lines_processed = 0
            for i, line in enumerate(lines):
                print(f"Line {i}: '{line[:50]}{'...' if len(line) > 50 else ''}'")
                
                if not line.strip():
                    self.current_y -= self.line_height
                    # Check for page break on empty lines too
                    if self.current_y < self.margin:
                        c.showPage()
                        self.current_y = self.height - self.margin
                    continue
                    
                # Check if this line contains a form field
                field_in_line = None
                for field in form_fields:
                    if field['match'].group() in line:
                        field_in_line = field
                        print(f"Found field in line {i}: {field['type']} - {field['name']}")
                        break
                
                try:
                    if field_in_line:
                        # Process line with form field
                        print(f"Processing field line: {field_in_line['name']}")
                        self._process_line_with_field(c, line, field_in_line)
                    else:
                        # Regular text line - handle with wrapping
                        print(f"Processing text line")
                        self._draw_text_line(c, line)
                    lines_processed += 1
                except Exception as e:
                    print(f"Error processing line {i}: {e}")
                    import traceback
                    traceback.print_exc()
            
            print(f"Processed {lines_processed} lines successfully")
            
            # Ensure we have at least one page with content
            if self.current_y >= self.height - self.margin - 20:  # If we haven't drawn anything
                print("No content drawn, adding placeholder text")
                c.drawString(self.margin, self.current_y, "No content to display")
            
            print("Attempting to save PDF...")
            c.save()
            print(f"PDF save() completed")
            
            # Verify file was created and check size
            if os.path.exists(output_filename):
                file_size = os.path.getsize(output_filename)
                print(f"File verified: {file_size} bytes")
                if file_size == 0:
                    print("WARNING: PDF file is empty (0 bytes)")
            else:
                print(f"ERROR: PDF file was not created at {output_filename}")
                
        except Exception as e:
            print(f"Exception in create_pdf_form: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _wrap_text(self, canvas, text, max_width, font_name="Helvetica", font_size=10):
        """Wrap text to fit within the specified width"""
        canvas.setFont(font_name, font_size)
        return simpleSplit(text, font_name, font_size, max_width)
    
    def _check_page_break(self, canvas, lines_needed=1):
        """Check if we need a page break and create one if necessary"""
        space_needed = lines_needed * self.line_height
        if self.current_y - space_needed < self.margin:
            canvas.showPage()
            self.current_y = self.height - self.margin
            return True
        return False
    
    def _draw_wrapped_text(self, canvas, text, x, font_name="Helvetica", font_size=10, bold=False):
        """Draw text with proper wrapping and page breaks"""
        if not text.strip():
            return 0
            
        if bold:
            font_name = "Helvetica-Bold"
        
        canvas.setFont(font_name, font_size)
        
        # Calculate available width from the x position
        available_width = self.width - self.margin - x
        if available_width <= 0:
            available_width = self.available_width
        
        # Wrap the text
        wrapped_lines = self._wrap_text(canvas, text, available_width, font_name, font_size)
        
        # Check if we need page breaks
        self._check_page_break(canvas, len(wrapped_lines))
        
        # Draw each line
        for line in wrapped_lines:
            canvas.drawString(x, self.current_y, line)
            self.current_y -= self.line_height
            
            # Check for page break after each line
            if self.current_y < self.margin:
                canvas.showPage()
                self.current_y = self.height - self.margin
        
        return len(wrapped_lines)

    def _handle_line_with_fields(self, canvas, line, fields):
        """NEW METHOD: Handle a line containing one or more form fields"""
        print(f"\n--- _handle_line_with_fields called with {len(fields)} fields ---")
        for field in fields:
            print(f"    Field: {field['name']} ({field['type']}) = '{field['placeholder']}'")
        
        # Simple approach: process each field sequentially
        current_x = self.margin
        remaining_text = line
        
        # Sort fields by their original position in the document
        sorted_fields = sorted(fields, key=lambda f: f['start'])
        print(f"Fields sorted by position: {[f['name'] for f in sorted_fields]}")
        
        self._check_page_break(canvas, 1)
        
        for i, field in enumerate(sorted_fields):
            placeholder = field['placeholder']
            print(f"\nProcessing field {i+1}/{len(sorted_fields)}: {field['name']}")
            print(f"Looking for placeholder: '{placeholder}'")
            print(f"In remaining text: '{remaining_text}'")
            
            # Find the placeholder in the remaining text
            pos = remaining_text.find(placeholder)
            if pos == -1:
                print(f"WARNING: Placeholder not found in remaining text!")
                continue
            
            # Draw text before the field
            before_text = remaining_text[:pos]
            print(f"Text before field: '{before_text}'")
            
            if before_text:
                canvas.setFont("Helvetica", 10)
                text_width = canvas.stringWidth(before_text)
                remaining_width = self.width - self.margin - current_x
                
                if text_width <= remaining_width:
                    canvas.drawString(current_x, self.current_y, before_text)
                    current_x += text_width
                else:
                    # Move to new line
                    self.current_y -= self.line_height
                    self._check_page_break(canvas, 1)
                    current_x = self.margin
                    canvas.drawString(current_x, self.current_y, before_text)
                    current_x += text_width
            
            # Create the form field
            print(f"Creating form field at ({current_x}, {self.current_y})")
            field_width = self._create_form_field(canvas, field, current_x, self.current_y)
            current_x += field_width
            print(f"Field created, width: {field_width}, new x: {current_x}")
            
            # Update remaining text
            after_pos = pos + len(placeholder)
            remaining_text = remaining_text[after_pos:]
            print(f"Updated remaining text: '{remaining_text}'")
        
        # Draw any remaining text
        if remaining_text.strip():
            print(f"Drawing final remaining text: '{remaining_text}'")
            canvas.setFont("Helvetica", 10)
            text_width = canvas.stringWidth(remaining_text)
            remaining_width = self.width - self.margin - current_x
            
            if text_width <= remaining_width:
                canvas.drawString(current_x, self.current_y, remaining_text)
            else:
                # Move to new line
                self.current_y -= self.line_height
                self._check_page_break(canvas, 1)
                canvas.drawString(self.margin, self.current_y, remaining_text)
        
        # Move to next line
        self.current_y -= self.line_height
        print(f"--- _handle_line_with_fields completed ---\n")

    def _process_line_with_multiple_fields(self, canvas, line, fields):
        """Process a line containing one or more form fields"""
        print(f"Processing line with {len(fields)} fields: {[f['name'] for f in fields]}")
        
        # Special handling for textarea - it should start on a new line
        textarea_fields = [f for f in fields if f['type'] == 'textarea']
        if textarea_fields:
            # If there are textareas, process them individually using the original method
            for field in fields:
                if field['type'] == 'textarea':
                    # Extract just the part of the line for this field
                    field_placeholder = field['match'].group()
                    field_start = line.find(field_placeholder)
                    field_end = field_start + len(field_placeholder)
                    
                    # Create a line with just this textarea and its label
                    before_field = line[:field_start]
                    after_field = line[field_end:]
                    field_line = before_field + field_placeholder + after_field
                    
                    self._process_line_with_field(canvas, field_line, field)
            return
        
        # For non-textarea fields, process multiple fields on the same line
        current_x = self.margin
        work_line = line  # Working copy of the line
        
        # Sort fields by their position in the original line
        fields_sorted = sorted(fields, key=lambda f: f['start'])
        print(f"Fields sorted by position: {[(f['name'], f['start']) for f in fields_sorted]}")
        
        self._check_page_break(canvas, 1)
        
        # Process each field in order
        for i, field in enumerate(fields_sorted):
            field_placeholder = field['placeholder']
            print(f"Processing field {i+1}/{len(fields_sorted)}: {field['name']} = '{field_placeholder}'")
            
            # Find this field in the current working line
            field_pos = work_line.find(field_placeholder)
            print(f"Field position in work_line: {field_pos}")
            
            if field_pos == -1:
                print(f"Warning: Field {field['name']} not found in remaining line: '{work_line}'")
                continue
            
            # Draw text before this field
            before_field = work_line[:field_pos]
            print(f"Text before field: '{before_field}'")
            
            if before_field:
                # Check if we need to handle bold formatting
                bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
                has_bold = bool(re.search(bold_pattern, before_field))
                
                if has_bold:
                    temp_width = self._calculate_formatted_text_width(canvas, before_field)
                    remaining_width = self.width - self.margin - current_x
                    
                    if temp_width <= remaining_width:
                        current_x = self._draw_formatted_text_inline(canvas, before_field, current_x)
                    else:
                        # Text doesn't fit, move to new line
                        self.current_y -= self.line_height
                        self._check_page_break(canvas, 1)
                        current_x = self.margin
                        current_x = self._draw_formatted_text_inline(canvas, before_field, current_x)
                else:
                    # Simple text without bold
                    canvas.setFont("Helvetica", 10)
                    text_width = canvas.stringWidth(before_field)
                    remaining_width = self.width - self.margin - current_x
                    
                    if text_width <= remaining_width:
                        canvas.drawString(current_x, self.current_y, before_field)
                        current_x += text_width
                    else:
                        # Text doesn't fit, move to new line
                        self.current_y -= self.line_height
                        self._check_page_break(canvas, 1)
                        current_x = self.margin
                        canvas.drawString(current_x, self.current_y, before_field)
                        current_x += text_width
            
            # Create the form field
            print(f"Creating field at position ({current_x}, {self.current_y})")
            field_width = self._create_form_field(canvas, field, current_x, self.current_y)
            current_x += field_width
            print(f"Field width: {field_width}, new current_x: {current_x}")
            
            # Update working line to remove processed part
            field_end_pos = field_pos + len(field_placeholder)
            work_line = work_line[field_end_pos:]
            print(f"Remaining work_line: '{work_line}'")
        
        # Draw any remaining text after the last field
        if work_line.strip():
            print(f"Drawing remaining text: '{work_line}'")
            
            # Check if we need to handle bold formatting
            bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
            has_bold = bool(re.search(bold_pattern, work_line))
            
            remaining_width = self.width - self.margin - current_x
            
            if has_bold:
                temp_width = self._calculate_formatted_text_width(canvas, work_line)
                if temp_width <= remaining_width:
                    self._draw_formatted_text_inline(canvas, work_line, current_x)
                else:
                    # Text doesn't fit, move to new line
                    self.current_y -= self.line_height
                    self._check_page_break(canvas, 1)
                    line_advanced = self._draw_formatted_text(canvas, work_line.strip(), self.margin)
                    if not line_advanced:
                        self.current_y -= self.line_height
                    return
            else:
                # Simple text
                canvas.setFont("Helvetica", 10)
                text_width = canvas.stringWidth(work_line)
                
                if text_width <= remaining_width:
                    canvas.drawString(current_x, self.current_y, work_line)
                else:
                    # Text doesn't fit, move to new line
                    self.current_y -= self.line_height
                    self._check_page_break(canvas, 1)
                    canvas.drawString(self.margin, self.current_y, work_line)
        
        # Move to next line after processing all fields
        self.current_y -= self.line_height
        print(f"Finished processing multiple fields line")

    def _process_line_with_field(self, canvas, line, field):
        """Process a line containing a form field with proper text wrapping and bold formatting"""
        field_match = field['match']
        field_placeholder = field_match.group()
        
        # Special handling for textarea - it should start on a new line
        if field['type'] == 'textarea':
            # Split the line at the field position
            start_pos = line.find(field_placeholder)
            before_field = line[:start_pos]
            after_field = line[start_pos + len(field_placeholder):]
            
            # Draw text before field (usually a label)
            if before_field.strip():
                self._check_page_break(canvas, 1)
                line_advanced = self._draw_formatted_text(canvas, before_field.strip(), self.margin)
                if not line_advanced:
                    self.current_y -= self.line_height
            
            # Move to new line for textarea
            self._check_page_break(canvas, 1)
            
            # Create the textarea field
            field_height = self._create_form_field(canvas, field, self.margin, self.current_y)
            
            # Move current_y down by the height of the textarea
            lines = field.get('lines', 3)
            textarea_height = lines * self.line_height + 8  # 8 pixels padding
            self.current_y -= textarea_height
            
            # Draw text after field on new line if it exists
            if after_field.strip():
                self._check_page_break(canvas, 1)
                line_advanced = self._draw_formatted_text(canvas, after_field.strip(), self.margin)
                if not line_advanced:
                    self.current_y -= self.line_height
            
            return
        
        # For all other field types, use the existing logic
        # Split the line at the field position
        start_pos = line.find(field_placeholder)
        before_field = line[:start_pos]
        after_field = line[start_pos + len(field_placeholder):]
        
        # Start at left margin
        x_pos = self.margin
        
        # Handle text before field (with potential bold formatting)
        if before_field.strip():
            # Check if the before_field text is too long
            canvas.setFont("Helvetica", 10)
            
            # Use formatted text drawing to handle bold formatting
            # First check if it fits on one line
            temp_width = self._calculate_formatted_text_width(canvas, before_field)
            
            if temp_width > self.available_width:
                # Text is too long, need to wrap
                # For now, fall back to plain text for wrapping
                plain_before = self._strip_bold_formatting(before_field)
                wrapped_lines = self._wrap_text(canvas, plain_before, self.available_width)
                self._check_page_break(canvas, len(wrapped_lines) + 1)  # +1 for the field
                
                # Draw all wrapped lines except the last one
                for i, wrapped_line in enumerate(wrapped_lines[:-1]):
                    canvas.drawString(self.margin, self.current_y, wrapped_line)
                    self.current_y -= self.line_height
                    self._check_page_break(canvas, 1)
                
                # Draw the last line and continue with field on same line
                last_line = wrapped_lines[-1]
                canvas.drawString(self.margin, self.current_y, last_line)
                x_pos = self.margin + canvas.stringWidth(last_line)
            else:
                # Text fits on one line - draw with bold formatting
                self._check_page_break(canvas, 1)
                x_pos = self._draw_formatted_text_inline(canvas, before_field, x_pos)
        else:
            # No text before field, just check for page break
            self._check_page_break(canvas, 1)
        
        # Create the form field
        field_width = self._create_form_field(canvas, field, x_pos, self.current_y)
        x_pos += field_width
        
        # Handle text after field (with potential bold formatting)
        if after_field.strip():
            remaining_width = self.width - self.margin - x_pos
            
            # Check if it's simple text without bold formatting first
            bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
            has_bold = bool(re.search(bold_pattern, after_field))
            
            if not has_bold:
                # Simple text without bold formatting
                canvas.setFont("Helvetica", 10)
                text_width = canvas.stringWidth(after_field)
                
                if text_width <= remaining_width:
                    # Simple text fits on same line
                    canvas.drawString(x_pos, self.current_y, after_field)
                    self.current_y -= self.line_height
                else:
                    # Text doesn't fit entirely, but start on same line and wrap
                    words = after_field.split()
                    current_x = x_pos
                    current_remaining = remaining_width
                    
                    for i, word in enumerate(words):
                        word_to_draw = word if i == 0 else " " + word
                        word_width = canvas.stringWidth(word_to_draw)
                        
                        if word_width <= current_remaining:
                            # Word fits on current line
                            canvas.drawString(current_x, self.current_y, word_to_draw)
                            current_x += word_width
                            current_remaining -= word_width
                        else:
                            # Word doesn't fit, move to next line
                            self.current_y -= self.line_height
                            page_break_occurred = self._check_page_break(canvas, 1)
                            if page_break_occurred:
                                canvas.setFont("Helvetica", 10)
                            
                            # Reset position for new line
                            current_x = self.margin
                            current_remaining = self.available_width
                            
                            # Draw word on new line (without leading space)
                            word_to_draw = word
                            word_width = canvas.stringWidth(word_to_draw)
                            
                            if word_width <= current_remaining:
                                canvas.drawString(current_x, self.current_y, word_to_draw)
                                current_x += word_width
                                current_remaining -= word_width
                            else:
                                # Word is too long for any line, break it
                                self._draw_long_word_wrapped(canvas, word, "Helvetica", current_x)
                                current_x = self.margin
                                current_remaining = self.available_width
                    
                    self.current_y -= self.line_height
            else:
                # Text has bold formatting - try to start on same line
                temp_width = self._calculate_formatted_text_width(canvas, after_field)
                
                if temp_width <= remaining_width:
                    # Text fits on same line - draw with bold formatting
                    end_x = self._draw_formatted_text_inline(canvas, after_field, x_pos)
                    self.current_y -= self.line_height
                else:
                    # Text doesn't fit entirely - start on same line and wrap
                    # For now, this is complex, so move to next line
                    # TODO: Could improve this to start on same line
                    self.current_y -= self.line_height
                    self._check_page_break(canvas, 1)
                    line_advanced = self._draw_formatted_text(canvas, after_field, self.margin)
                    if not line_advanced:
                        self.current_y -= self.line_height
        else:
            # No text after field, just move to next line
            self.current_y -= self.line_height

    def _calculate_formatted_text_width(self, canvas, text):
        """Calculate the total width of text with bold formatting"""
        # Use the same robust pattern
        bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
        total_width = 0
        last_end = 0
        
        for match in re.finditer(bold_pattern, text):
            # Add width of regular text before bold
            if match.start() > last_end:
                regular_text = text[last_end:match.start()]
                canvas.setFont("Helvetica", 10)
                total_width += canvas.stringWidth(regular_text)
            
            # Add width of bold text
            bold_text = match.group(1)
            canvas.setFont("Helvetica-Bold", 10)
            total_width += canvas.stringWidth(bold_text)
            
            last_end = match.end()
        
        # Add width of remaining regular text
        if last_end < len(text):
            remaining_text = text[last_end:]
            canvas.setFont("Helvetica", 10)
            total_width += canvas.stringWidth(remaining_text)
        
        return total_width

    def _draw_formatted_text_inline(self, canvas, text, x_start):
        """Draw formatted text inline and return the ending x position"""
        # Use the same robust pattern
        bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
        current_x = x_start
        last_end = 0
        
        for match in re.finditer(bold_pattern, text):
            # Draw regular text before bold
            if match.start() > last_end:
                regular_text = text[last_end:match.start()]
                canvas.setFont("Helvetica", 10)
                canvas.drawString(current_x, self.current_y, regular_text)
                current_x += canvas.stringWidth(regular_text)
            
            # Draw bold text
            bold_text = match.group(1)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(current_x, self.current_y, bold_text)
            current_x += canvas.stringWidth(bold_text)
            
            last_end = match.end()
        
        # Draw remaining regular text
        if last_end < len(text):
            remaining_text = text[last_end:]
            canvas.setFont("Helvetica", 10)
            canvas.drawString(current_x, self.current_y, remaining_text)
            current_x += canvas.stringWidth(remaining_text)
        
        return current_x

    def _strip_bold_formatting(self, text):
        """Remove bold formatting markers from text"""
        # Use the same robust pattern
        bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
        return re.sub(bold_pattern, r'\1', text)

    def _create_form_field(self, canvas, field, x, y):
        """Create a form field at the specified position"""
        field_type = field['type']
        field_name = field['name']
        
        try:
            if field_type in ['text', 'email', 'number', 'date']:
                # Text input field
                width = 150
                height = 12
                canvas.acroForm.textfield(
                    name=field_name,
                    tooltip=f"Enter {field_type}",
                    x=x, y=y-2,
                    borderStyle='inset',
                    width=width,
                    height=height,
                    textColor=black,
                    fillColor=None,
                    borderColor=black,
                    forceBorder=True,
                    fontName="Helvetica",  # Match document font
                    fontSize=10           # Match document font size
                )
                return width
                
            elif field_type == 'textarea':
                # Multi-line text field with specified number of lines
                lines = field.get('lines', 3)  # Default to 3 lines if not specified
                width = 400  # Wider for text areas
                height = lines * self.line_height + 8  # Height based on line count + padding
                
                try:
                    canvas.acroForm.textfield(
                        name=field_name,
                        tooltip=f"Enter text ({lines} lines)",
                        x=x, y=y-height+10,
                        borderStyle='inset',
                        width=width,
                        height=height,
                        textColor=black,
                        fillColor=None,
                        borderColor=black,
                        forceBorder=True,
                        multiline=True,
                        fontName="Helvetica",  # Match document font
                        fontSize=10           # Match document font size
                    )
                except TypeError:
                    # Fallback for older ReportLab versions without multiline
                    canvas.acroForm.textfield(
                        name=field_name,
                        tooltip=f"Enter text ({lines} lines)",
                        x=x, y=y-height+10,
                        borderStyle='inset',
                        width=width,
                        height=height,
                        textColor=black,
                        fillColor=None,
                        borderColor=black,
                        forceBorder=True,
                        fontName="Helvetica",  # Match document font
                        fontSize=10           # Match document font size
                    )
                return height  # Return height so caller can adjust positioning
                
            elif field_type == 'checkbox':
                # Checkbox field
                size = 12
                canvas.acroForm.checkbox(
                    name=field_name,
                    tooltip="Check this box",
                    x=x, y=y-2,
                    size=size,
                    borderColor=black,
                    fillColor=None,
                    textColor=black,
                    forceBorder=True
                )
                return size + 5
                
            elif field_type == 'radio':
                # Radio button group - handle differently based on number of options
                num_options = len(field['options'])
                
                if num_options <= 2:
                    # Use checkboxes styled as radio buttons for 2 or fewer options
                    # This avoids ReportLab's radio button double-circle issues
                    for i, option in enumerate(field['options']):
                        if i > 0:
                            # Move to next line for second option
                            self.current_y -= self.line_height
                            self._check_page_break(canvas, 1)
                            current_line_x = self.margin
                            current_y = self.current_y
                        else:
                            current_line_x = x
                            current_y = y
                        
                        option_value = option.strip()
                        
                        # Use checkbox but with circular appearance
                        canvas.acroForm.checkbox(
                            name=f"{field_name}_{i}",
                            tooltip=f"Select {option_value} (choose only one)",
                            x=current_line_x, 
                            y=current_y - 2,
                            size=12,
                            borderColor=black,
                            fillColor=None,
                            textColor=black,
                            forceBorder=True,
                            shape='circle'  # This might make it circular
                        )
                        print(f"Created radio-style checkbox: {field_name}_{i} = {option_value}")
                        
                        # Add option label with proper spacing
                        label_x = current_line_x + 18  # Space for button + gap
                        canvas.setFont("Helvetica", 10)
                        canvas.drawString(label_x, current_y, option_value)
                    
                    # Add instruction for mutual exclusivity
                    if num_options == 2:
                        self.current_y -= self.line_height // 2
                        canvas.setFont("Helvetica", 8)
                        canvas.drawString(self.margin, self.current_y, "(Select only one option)")
                        canvas.setFont("Helvetica", 10)
                    
                    return 200
                    
                else:
                    # For more than 2 options, use a dropdown (which works reliably)
                    print(f"Using dropdown for {num_options} radio options (ReportLab limitation)")
                    
                    # Add a label indicating this is a single-choice selection
                    canvas.setFont("Helvetica", 10)
                    canvas.drawString(x, y, "Select one:")
                    
                    # Move dropdown slightly to the right and down
                    dropdown_x = x
                    dropdown_y = y - 16
                    
                    width = 300  # Wider to accommodate long option text
                    height = 14
                    options = field['options']
                    
                    try:
                        canvas.acroForm.choice(
                            name=field_name,
                            tooltip="Select one option",
                            x=dropdown_x, y=dropdown_y,
                            width=width,
                            height=height,
                            borderColor=black,
                            fillColor=None,
                            textColor=black,
                            forceBorder=True,
                            options=[(opt.strip(), opt.strip()) for opt in options],
                            value=options[0].strip() if options else "",
                            fontName="Helvetica",  # Match document font
                            fontSize=10           # Match document font size
                        )
                        print(f"Created dropdown with {len(options)} options")
                        
                        # Move current_y to account for the dropdown
                        self.current_y -= 20  # Space for the dropdown
                        
                        return width
                    except Exception as e:
                        print(f"Dropdown creation failed: {e}")
                        # Ultimate fallback: list the options as text with checkboxes
                        canvas.drawString(x, dropdown_y, "Options (select one):")
                        self.current_y -= self.line_height
                        
                        for i, option in enumerate(options):
                            self.current_y -= self.line_height
                            self._check_page_break(canvas, 1)
                            
                            # Create checkbox
                            canvas.acroForm.checkbox(
                                name=f"{field_name}_{i}",
                                tooltip=f"Select {option.strip()}",
                                x=self.margin, 
                                y=self.current_y - 2,
                                size=12,
                                borderColor=black,
                                fillColor=None,
                                textColor=black,
                                forceBorder=True
                            )
                            
                            # Add option text
                            canvas.setFont("Helvetica", 10)
                            canvas.drawString(self.margin + 18, self.current_y, option.strip())
                        
                        return 200
                
            elif field_type == 'dropdown':
                # Dropdown/select field
                width = 150
                height = 14
                options = field['options']
                
                try:
                    canvas.acroForm.choice(
                        name=field_name,
                        tooltip="Select an option",
                        x=x, y=y-2,
                        width=width,
                        height=height,
                        borderColor=black,
                        fillColor=None,
                        textColor=black,
                        forceBorder=True,
                        options=[(opt.strip(), opt.strip()) for opt in options],
                        value=options[0].strip() if options else "",
                        fontName="Helvetica",  # Match document font
                        fontSize=10           # Match document font size
                    )
                except Exception as e:
                    # Fallback: create a text field with options as tooltip
                    print(f"Warning: Dropdown not supported, using text field. Error: {e}")
                    canvas.acroForm.textfield(
                        name=field_name,
                        tooltip=f"Options: {', '.join(options)}",
                        x=x, y=y-2,
                        borderStyle='inset',
                        width=width,
                        height=height,
                        textColor=black,
                        fillColor=None,
                        borderColor=black,
                        forceBorder=True,
                        fontName="Helvetica",  # Match document font
                        fontSize=10           # Match document font size
                    )
                return width
        
        except Exception as e:
            print(f"Error creating field {field_name}: {e}")
            # Fallback: draw text indicating field position
            canvas.drawString(x, y, f"[{field_name}]")
            return 100
        
        return 0
    
    def _draw_text_line(self, canvas, line):
        """Draw a regular text line with proper formatting and wrapping"""
        if not line.strip():
            self.current_y -= self.line_height
            return
            
        # Handle basic markdown formatting and wrapping
        if line.startswith('# '):
            # Heading 1
            self._check_page_break(canvas, 2)  # Extra space for headings
            text = line[2:].strip()
            if text:
                self._draw_wrapped_text(canvas, text, self.margin, "Helvetica-Bold", 16)
                # Add extra space after heading
                self.current_y -= self.line_height // 2
            
        elif line.startswith('## '):
            # Heading 2
            self._check_page_break(canvas, 2)
            text = line[3:].strip()
            if text:
                self._draw_wrapped_text(canvas, text, self.margin, "Helvetica-Bold", 14)
                # Add extra space after heading
                self.current_y -= self.line_height // 2
            
        elif line.startswith('### '):
            # Heading 3
            self._check_page_break(canvas, 1)
            text = line[4:].strip()
            if text:
                self._draw_wrapped_text(canvas, text, self.margin, "Helvetica-Bold", 12)
            
        elif line.strip() in ['---', '***', '___'] or (len(line.strip()) >= 3 and all(c in '-*_' for c in line.strip()) and len(set(line.strip())) == 1):
            # Horizontal rule - support ---, ***, ___, or 3+ of the same character
            self._check_page_break(canvas, 2)  # Space before rule
            
            # Draw horizontal line
            line_y = self.current_y - (self.line_height // 2)
            canvas.setStrokeColor(black)
            canvas.setLineWidth(1)
            canvas.line(self.margin, line_y, self.width - self.margin, line_y)
            
            # Add space after the rule
            self.current_y -= self.line_height
            
        elif line.startswith('**') and line.endswith('**') and len(line) > 4:
            # Bold text (entire line)
            self._check_page_break(canvas, 1)
            text = line[2:-2].strip()
            if text:
                self._draw_wrapped_text(canvas, text, self.margin, "Helvetica-Bold", 10)
                
        elif line.startswith('- ') or line.startswith('* '):
            # Bullet points
            self._check_page_break(canvas, 1)
            bullet_text = line[2:].strip()
            if bullet_text:
                canvas.setFont("Helvetica", 10)
                canvas.drawString(self.margin, self.current_y, "•")
                # Indent the bullet text and handle bold formatting within it
                line_advanced = self._draw_formatted_text(canvas, bullet_text, self.margin + 20)
                # Always move to next line after bullet point
                self.current_y -= self.line_height
            
        else:
            # Regular text with potential inline bold formatting
            text = line.strip()
            if text:  # Only process non-empty lines
                self._check_page_break(canvas, 1)
                line_advanced = self._draw_formatted_text(canvas, text, self.margin)
                # Always move to next line after processing a text line
                # (line_advanced tells us if wrapping already moved lines, but we still need to advance once more)
                self.current_y -= self.line_height
            else:
                # Empty line - just add space
                self.current_y -= self.line_height

    def _draw_formatted_text(self, canvas, text, x_start):
        """Draw text with inline bold formatting support and proper wrapping"""
        if not text.strip():
            return False
        
        # More robust pattern to find **bold** text, including punctuation and special chars
        bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
        
        # Check if there's any bold formatting in the text
        has_bold = bool(re.search(bold_pattern, text))
        
        if not has_bold:
            # No bold formatting - use regular text wrapping
            canvas.setFont("Helvetica", 10)
            available_width = self.width - self.margin - x_start
            
            if canvas.stringWidth(text) <= available_width:
                # Fits on one line
                canvas.drawString(x_start, self.current_y, text)
                return False
            else:
                # Needs wrapping
                wrapped_lines = self._wrap_text(canvas, text, available_width, "Helvetica", 10)
                for i, line in enumerate(wrapped_lines):
                    canvas.setFont("Helvetica", 10)  # Set font for each line
                    canvas.drawString(x_start if i == 0 else self.margin, self.current_y, line)
                    if i < len(wrapped_lines) - 1:
                        self.current_y -= self.line_height
                        page_break_occurred = self._check_page_break(canvas, 1)
                        # Only reset font if page break actually occurred
                        if page_break_occurred:
                            canvas.setFont("Helvetica", 10)
                return len(wrapped_lines) > 1
        
        # Has bold formatting - process it with smart wrapping
        return self._draw_formatted_text_with_wrapping(canvas, text, x_start, bold_pattern)
    
    def _draw_formatted_text_with_wrapping(self, canvas, text, x_start, bold_pattern):
        """Draw formatted text with proper wrapping that preserves bold formatting"""
        available_width = self.width - self.margin - x_start
        
        # Parse the text into formatted parts
        parts = self._parse_formatted_parts(text, bold_pattern)
        
        # Debug: print what parts we found
        print(f"DEBUG: Parsing text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        for i, (part_type, part_text) in enumerate(parts):
            print(f"  Part {i}: {part_type} = '{part_text}'")
        
        # Calculate if everything fits on one line
        total_width = self._calculate_parts_width(canvas, parts)
        
        print(f"DEBUG: Total width: {total_width}, Available: {available_width}")
        
        if total_width <= available_width:
            # Everything fits on one line
            print(f"DEBUG: Drawing on one line")
            current_x = x_start
            for part_type, part_text in parts:
                font_name = "Helvetica-Bold" if part_type == 'bold' else "Helvetica"
                canvas.setFont(font_name, 10)
                canvas.drawString(current_x, self.current_y, part_text)
                current_x += canvas.stringWidth(part_text)
            return False  # Didn't wrap
        else:
            # Need to wrap - break into words while preserving formatting
            print(f"DEBUG: Need to wrap text")
            wrapped = self._wrap_formatted_text(canvas, parts, x_start)
            return True  # Always return True when wrapping occurred, regardless of internal line advances
    
    def _parse_formatted_parts(self, text, bold_pattern):
        """Parse text into regular and bold parts"""
        parts = []
        last_end = 0
        
        for match in re.finditer(bold_pattern, text):
            # Add regular text before the bold part
            if match.start() > last_end:
                regular_text = text[last_end:match.start()]
                if regular_text:
                    parts.append(('regular', regular_text))
            
            # Add the bold part
            bold_text = match.group(1)
            if bold_text:
                parts.append(('bold', bold_text))
            
            last_end = match.end()
        
        # Add any remaining regular text
        if last_end < len(text):
            remaining_text = text[last_end:]
            if remaining_text:
                parts.append(('regular', remaining_text))
        
        return parts
    
    def _calculate_parts_width(self, canvas, parts):
        """Calculate total width of formatted parts"""
        total_width = 0
        for part_type, part_text in parts:
            font_name = "Helvetica-Bold" if part_type == 'bold' else "Helvetica"
            canvas.setFont(font_name, 10)
            total_width += canvas.stringWidth(part_text)
        return total_width
    
    def _wrap_formatted_text(self, canvas, parts, x_start):
        """Wrap formatted text while preserving bold formatting"""
        lines_drawn = 0
        current_x = x_start
        available_width = self.width - self.margin - x_start
        
        for part_index, (part_type, part_text) in enumerate(parts):
            font_name = "Helvetica-Bold" if part_type == 'bold' else "Helvetica"
            canvas.setFont(font_name, 10)
            
            # Handle spacing: if this isn't the first part and doesn't start with space,
            # and the previous part didn't end with space, we need to add a space
            needs_leading_space = (part_index > 0 and 
                                 not part_text.startswith(' ') and 
                                 current_x > self.margin)
            
            if needs_leading_space:
                # Check if we have room for a space
                space_width = canvas.stringWidth(' ')
                if current_x + space_width <= self.width - self.margin:
                    canvas.drawString(current_x, self.current_y, ' ')
                    current_x += space_width
                else:
                    # No room for space, move to next line
                    self.current_y -= self.line_height
                    self._check_page_break(canvas, 1)
                    current_x = self.margin
                    lines_drawn += 1
            
            # Now handle the actual part text
            part_width = canvas.stringWidth(part_text)
            
            # Check if the entire part fits on current line
            if current_x + part_width <= self.width - self.margin:
                # Entire part fits on current line
                canvas.drawString(current_x, self.current_y, part_text)
                current_x += part_width
            else:
                # Part doesn't fit, need to wrap within this part
                words = part_text.split()
                
                for i, word in enumerate(words):
                    # Add space before word (except first word in part or if we're at start of line)
                    word_to_draw = word
                    if i > 0:  # Not the first word in this part
                        word_to_draw = " " + word
                    
                    word_width = canvas.stringWidth(word_to_draw)
                    
                    # Check if word fits on current line
                    if current_x + word_width > self.width - self.margin:
                        # Move to next line
                        self.current_y -= self.line_height
                        page_break_occurred = self._check_page_break(canvas, 1)
                        if page_break_occurred:
                            # Re-establish font after page break
                            canvas.setFont(font_name, 10)
                        current_x = self.margin
                        available_width = self.available_width
                        lines_drawn += 1
                        
                        # Draw word without leading space on new line
                        word_to_draw = word
                        word_width = canvas.stringWidth(word_to_draw)
                        
                        # Check if word is too long for any line
                        if word_width > available_width:
                            # Word is too long, need to break it
                            self._draw_long_word_wrapped(canvas, word, font_name, current_x)
                            # Estimate position after drawing broken word
                            current_x = self.margin + (word_width % available_width)
                        else:
                            # Draw word on new line
                            canvas.drawString(current_x, self.current_y, word_to_draw)
                            current_x += word_width
                    else:
                        # Word fits on current line
                        canvas.drawString(current_x, self.current_y, word_to_draw)
                        current_x += word_width
        
        return lines_drawn > 0
    
    def _draw_long_word_wrapped(self, canvas, word, font_name, start_x):
        """Draw a word that's too long for one line by breaking it"""
        canvas.setFont(font_name, 10)
        current_x = start_x
        available_width = self.width - self.margin - current_x
        
        i = 0
        while i < len(word):
            # Find how many characters fit on current line
            chars_that_fit = 0
            width_so_far = 0
            
            for j in range(i, len(word)):
                char_width = canvas.stringWidth(word[j])
                if width_so_far + char_width > available_width:
                    break
                width_so_far += char_width
                chars_that_fit += 1
            
            if chars_that_fit == 0:
                chars_that_fit = 1  # Force at least one character
            
            # Draw the characters that fit
            char_segment = word[i:i + chars_that_fit]
            canvas.drawString(current_x, self.current_y, char_segment)
            
            i += chars_that_fit
            
            if i < len(word):
                # More characters remaining, move to next line
                self.current_y -= self.line_height
                page_break_occurred = self._check_page_break(canvas, 1)
                if page_break_occurred:
                    # Re-establish font after page break
                    canvas.setFont(font_name, 10)
                current_x = self.margin
                available_width = self.available_width
            else:
                # Update current_x to position after the word
                current_x += width_so_far

def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to interactive PDF forms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.md                    # Creates input_form.pdf
  %(prog)s input.md -o output.pdf      # Creates output.pdf
  %(prog)s form.md --output myform.pdf # Creates myform.pdf

Field Syntax:
  {{text:field_name}}                  # Text input
  {{email:email_field}}                # Email input
  {{date:date_field}}                  # Date input
  {{textarea:comments}}                # Multi-line text (3 lines default)
  {{textarea:comments:4}}              # Multi-line text (4 lines)
  {{checkbox:option}}                  # Checkbox
  {{radio:group:opt1,opt2}}            # Radio buttons
  {{dropdown:field:opt1,opt2,opt3}}    # Dropdown list
  ______                               # Underscores become text fields
        """
    )
    
    parser.add_argument(
        'input',
        help='Input Markdown file (.md)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output PDF file (default: input_form.pdf)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate input file
    if not args.input.lower().endswith('.md'):
        print("Warning: Input file doesn't have .md extension")
    
    try:
        # Create converter and process file
        print("Creating MarkdownToPDFForm converter...")
        converter = MarkdownToPDFForm()
        print("Converter created successfully")
        
        # Test basic PDF creation first
        print("Testing basic PDF functionality...")
        test_result = converter.test_basic_pdf_creation("test_basic.pdf")
        if not test_result:
            print("❌ Basic PDF creation failed. Check ReportLab installation.")
            sys.exit(1)
        else:
            print("✅ Basic PDF creation works")
        
        print(f"Processing file: {args.input}")
        output_file = converter.create_pdf_form_from_file(args.input, args.output)
        
        print(f"✅ Successfully converted '{args.input}' to '{output_file}'")
        print(f"📄 PDF form created with interactive fields")
        
        # Check if file exists and show size
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"📊 File size: {file_size:,} bytes")
        else:
            print(f"❌ Warning: Output file does not exist: {output_file}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def demo():
    """Run a demonstration with sample markdown content"""
    print("Running demonstration...")
    
    # Sample markdown with form fields
    markdown_content = """
# Employee Information Form

Please fill out the following information:

**Name:** {{text:full_name}}

**Email:** {{email:email_address}}

**Phone:** {{text:phone_number}}

**Date of Birth:** {{date:birth_date}}

**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}

## Emergency Contact

**Contact Name:** {{text:emergency_name}}

**Contact Phone:** {{text:emergency_phone}}

**Relationship:** {{dropdown:relationship:Spouse,Parent,Sibling,Friend,Other}}

## Preferences

**Preferred Communication:**
{{radio:communication:Email,Phone,Text}}

**Subscribe to Newsletter:** {{checkbox:newsletter}}

## Additional Comments

{{textarea:comments}}

**Signature:** ________________________

Thank you for completing this form!
"""
    
    # Create the converter and generate PDF
    converter = MarkdownToPDFForm()
    converter.create_pdf_form(markdown_content, "demo_employee_form.pdf")
    print("✅ Demo PDF created: demo_employee_form.pdf")

if __name__ == "__main__":
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        print("Markdown to PDF Form Converter")
        print("==============================")
        print()
        print("Usage: python markdown_to_pdf_form.py <input.md> [-o output.pdf]")
        print()
        print("Run with --help for detailed usage information")
        print("Run demo by adding 'demo' as argument")
        print()
        sys.exit(0)
    
    # Handle demo mode
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'demo':
        demo()
    else:
        main()