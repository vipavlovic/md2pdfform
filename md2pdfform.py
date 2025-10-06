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
        self.available_width = self.width - (2 * self.margin)
        self.default_field_width = 150
        
    def parse_markdown_forms(self, md_text):
        """Parse markdown text and identify form field patterns"""
        patterns = [
            (r'\{\{text:([^}:]+)(?::(\d+))?\}\}', 'text'),
            (r'\{\{email:([^}:]+)(?::(\d+))?\}\}', 'email'),
            (r'\{\{number:([^}:]+)(?::(\d+))?\}\}', 'number'),
            (r'\{\{date:([^}:]+)(?::(\d+))?\}\}', 'date'),
            (r'\{\{textarea:([^}:]+):(\d+)(?::(\d+))?\}\}', 'textarea_lines_width'),
            (r'\{\{textarea:([^}:]+)(?::(\d+))?\}\}', 'textarea'),
            (r'\{\{checkbox:([^}]+)\}\}', 'checkbox'),
            (r'\{\{radio:([^}]+):([^}]+)\}\}', 'radio'),
            (r'\{\{dropdown:([^}]+):([^}]+)\}\}', 'dropdown'),
            (r'_{4,}', 'underlines'),
        ]
        
        all_fields = []
        
        for pattern, field_type in patterns:
            matches = list(re.finditer(pattern, md_text))
            
            for match in matches:
                field_info = {
                    'type': field_type,
                    'placeholder': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                }
                
                if field_type in ['text', 'email', 'number', 'date']:
                    field_info['name'] = match.group(1)
                    # Check if width is specified (group 2)
                    if match.group(2):
                        field_info['width'] = int(match.group(2))
                    else:
                        field_info['width'] = self.default_field_width
                        
                elif field_type == 'textarea_lines_width':
                    field_info['name'] = match.group(1)
                    field_info['lines'] = int(match.group(2))
                    field_info['type'] = 'textarea'
                    # Check if width is specified (group 3)
                    if match.group(3):
                        field_info['width'] = int(match.group(3))
                        
                elif field_type == 'textarea':
                    field_info['name'] = match.group(1)
                    # Check if the second group is lines or width
                    if match.group(2):
                        # Could be either lines or width - need to determine
                        # For backward compatibility, treat single number as lines
                        field_info['lines'] = int(match.group(2))
                    
                elif field_type == 'checkbox':
                    field_info['name'] = match.group(1)
                    
                elif field_type in ['radio', 'dropdown']:
                    field_info['name'] = match.group(1)
                    field_info['options'] = [opt.strip() for opt in match.group(2).split(',')]
                    
                elif field_type == 'underlines':
                    field_info['name'] = f"field_{len(all_fields) + 1}"
                    field_info['type'] = 'text'
                    field_info['width'] = self.default_field_width
                
                if field_info['type'] == 'textarea' and 'lines' not in field_info:
                    field_info['lines'] = 3
                
                all_fields.append(field_info)
        
        all_fields.sort(key=lambda x: x['start'])
        return all_fields, md_text

    def create_pdf_form_from_file(self, input_file, output_file=None):
        """Convert markdown file to PDF form"""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}_form.pdf"
        
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        self.create_pdf_form(markdown_content, output_file)
        return output_file

    def create_pdf_form(self, md_text, output_filename):
        """Convert markdown text with form patterns to PDF form"""
        if os.path.exists(output_filename):
            os.remove(output_filename)
        
        form_fields, text = self.parse_markdown_forms(md_text)
        c = canvas.Canvas(output_filename, pagesize=letter)
        
        lines = text.split('\n')
        
        for line_num, line in enumerate(lines):
            if not line.strip():
                self.current_y -= self.line_height
                if self.current_y < self.margin:
                    c.showPage()
                    self.current_y = self.height - self.margin
                continue
            
            # Find all fields in this line
            fields_in_line = [f for f in form_fields if f['placeholder'] in line]
            
            # Check if there's a blank line followed by a heading
            has_blank_line_before_heading = False
            if line_num + 1 < len(lines):
                # Check if next line is blank
                if not lines[line_num + 1].strip():
                    # Look for a heading after the blank line
                    for i in range(line_num + 2, len(lines)):
                        next_line = lines[i].strip()
                        if next_line:
                            if next_line.startswith('#') or (next_line.startswith('**') and next_line.endswith('**') and len(next_line) > 4):
                                has_blank_line_before_heading = True
                            break
            
            if len(fields_in_line) > 0:
                self._process_line_with_fields(c, line, fields_in_line, has_blank_line_before_heading)
            else:
                self._draw_text_line(c, line)
        
        if self.current_y >= self.height - self.margin - 20:
            c.drawString(self.margin, self.current_y, "")
        
        c.save()
        
        if os.path.exists(output_filename):
            file_size = os.path.getsize(output_filename)
            print(f"PDF created: {output_filename} ({file_size} bytes)")

    def _process_line_with_fields(self, canvas, line, fields, next_line_is_heading=False):
        """Process line with one or more form fields"""
        # Special handling for textarea - process individually and return
        textarea_fields = [f for f in fields if f['type'] == 'textarea']
        if textarea_fields:
            # Process each textarea field separately
            for field in textarea_fields:
                # For textareas, we process the entire line for this field only
                # This prevents double processing
                placeholder = field['placeholder']
                
                # Only process if this placeholder is in the line
                if placeholder in line:
                    self._process_textarea_field(canvas, line, field)
                    
                    # Remove this textarea's placeholder from the line for next iteration
                    # This prevents other textareas from being processed multiple times
                    line = line.replace(placeholder, '', 1)
            
            # Add extra space before heading
            if next_line_is_heading:
                self.current_y -= self.line_height
            return  # Important: return here to prevent further processing
        
        # Special handling for lines with only a checkbox and text
        checkbox_fields = [f for f in fields if f['type'] == 'checkbox']
        if len(fields) == 1 and len(checkbox_fields) == 1:
            # Single checkbox on this line - process specially to keep text with checkbox
            self._process_checkbox_line(canvas, line, checkbox_fields[0])
            # Add extra space before heading
            if next_line_is_heading:
                self.current_y -= self.line_height
            return
        
        # For non-textarea fields, continue with normal processing
        # Sort fields by position
        fields.sort(key=lambda f: f['start'])
        
        current_x = self.margin
        work_line = line
        
        self._check_page_break(canvas, 1)
        
        for field in fields:
            placeholder = field['placeholder']
            pos = work_line.find(placeholder)
            
            if pos == -1:
                continue
            
            # Draw text before field (with bold support)
            before_text = work_line[:pos]
            if before_text:
                # Check if text before field will fit
                text_width = self._calculate_formatted_text_width(canvas, before_text)
                remaining_width = self.width - self.margin - current_x
                
                if text_width <= remaining_width:
                    # Text fits on current line
                    current_x = self._draw_formatted_text_inline(canvas, before_text, current_x)
                else:
                    # Text doesn't fit, need to wrap to next line
                    self.current_y -= self.line_height
                    self._check_page_break(canvas, 1)
                    current_x = self.margin
                    # Draw the text on new line
                    current_x = self._draw_formatted_text_inline(canvas, before_text, current_x)
            
            # Check if field will fit on current line
            field_width = self._estimate_field_width(field)
            remaining_width = self.width - self.margin - current_x
            
            if field_width > remaining_width:
                # Field doesn't fit, move to next line
                self.current_y -= self.line_height
                self._check_page_break(canvas, 1)
                current_x = self.margin
            
            # Create field
            actual_field_width = self._create_form_field(canvas, field, current_x, self.current_y)
            current_x += actual_field_width
            
            # Update working line
            work_line = work_line[pos + len(placeholder):]
        
        # Draw remaining text
        if work_line.strip():
            # Add space before remaining text if it doesn't start with punctuation or space
            remaining_text = work_line
            if remaining_text and not remaining_text[0] in ' .,;:!?)':
                remaining_text = ' ' + remaining_text
            
            remaining_width = self.width - self.margin - current_x
            text_width = self._calculate_formatted_text_width(canvas, remaining_text)
            
            if text_width <= remaining_width:
                # Fits on same line
                self._draw_formatted_text_inline(canvas, remaining_text, current_x)
            else:
                # Doesn't fit, move to next line
                self.current_y -= self.line_height
                self._check_page_break(canvas, 1)
                self._draw_formatted_text(canvas, remaining_text.strip(), self.margin)
                # Add extra space before heading
                if next_line_is_heading:
                    self.current_y -= self.line_height
                return
        
        self.current_y -= self.line_height
        
        # Add extra space before heading
        if next_line_is_heading:
            self.current_y -= self.line_height

    def _process_checkbox_line(self, canvas, line, field):
        """Process a line with a checkbox field, keeping text with checkbox"""
        placeholder = field['placeholder']
        pos = line.find(placeholder)
        
        before_text = line[:pos]
        after_text = line[pos + len(placeholder):]
        
        self._check_page_break(canvas, 1)
        
        current_x = self.margin
        
        # Draw text before checkbox
        if before_text.strip():
            current_x = self._draw_formatted_text_inline(canvas, before_text, current_x)
        
        # Create checkbox
        checkbox_width = self._create_form_field(canvas, field, current_x, self.current_y)
        current_x += checkbox_width
        
        # Draw text after checkbox on same line with wrapping support
        if after_text.strip():
            self._draw_formatted_text_with_checkbox(canvas, after_text.strip(), current_x)
        else:
            self.current_y -= self.line_height
    
    def _draw_formatted_text_with_checkbox(self, canvas, text, x_start):
        """Draw text after checkbox with proper wrapping"""
        bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
        has_bold = bool(re.search(bold_pattern, text))
        
        if not has_bold:
            # Simple text without bold
            canvas.setFont("Helvetica", 10)
            available_width = self.width - self.margin - x_start
            
            if canvas.stringWidth(text) <= available_width:
                # Fits on same line as checkbox
                canvas.drawString(x_start, self.current_y, text)
                self.current_y -= self.line_height
            else:
                # Need to wrap - use word wrapping
                words = text.split()
                current_x = x_start
                current_line_words = []
                
                for word in words:
                    test_text = ' '.join(current_line_words + [word])
                    test_width = canvas.stringWidth(test_text)
                    
                    if current_x + test_width <= self.width - self.margin:
                        current_line_words.append(word)
                    else:
                        # Draw current line
                        if current_line_words:
                            line_text = ' '.join(current_line_words)
                            canvas.drawString(current_x, self.current_y, line_text)
                            self.current_y -= self.line_height
                            self._check_page_break(canvas, 1)
                            canvas.setFont("Helvetica", 10)
                        
                        # Start new line from margin
                        current_x = self.margin
                        current_line_words = [word]
                
                # Draw remaining words
                if current_line_words:
                    line_text = ' '.join(current_line_words)
                    canvas.drawString(current_x, self.current_y, line_text)
                    self.current_y -= self.line_height
        else:
            # Text has bold formatting
            parts = self._parse_formatted_parts(text, bold_pattern)
            current_x = x_start
            available_width = self.width - self.margin - x_start
            
            for part_type, part_text in parts:
                font_name = "Helvetica-Bold" if part_type == 'bold' else "Helvetica"
                canvas.setFont(font_name, 10)
                
                words = part_text.split()
                
                for word in words:
                    word_with_space = word if current_x == x_start or current_x == self.margin else " " + word
                    word_width = canvas.stringWidth(word_with_space)
                    
                    if current_x + word_width > self.width - self.margin:
                        # Move to next line
                        self.current_y -= self.line_height
                        self._check_page_break(canvas, 1)
                        canvas.setFont(font_name, 10)
                        current_x = self.margin
                        word_with_space = word
                        word_width = canvas.stringWidth(word_with_space)
                    
                    canvas.drawString(current_x, self.current_y, word_with_space)
                    current_x += word_width
            
            self.current_y -= self.line_height

    def _estimate_field_width(self, field):
        """Estimate the width a form field will take"""
        field_type = field['type']
        
        if field_type in ['text', 'email', 'number', 'date']:
            return field.get('width', self.default_field_width)
        elif field_type == 'checkbox':
            return 17
        elif field_type == 'dropdown':
            return 150
        elif field_type == 'radio':
            # Estimate based on number of options
            num_options = len(field.get('options', []))
            if num_options <= 2:
                return 200  # Radio buttons take more space
            else:
                return 300  # Dropdown for many options
        else:
            return 100  # Default estimate

    def _process_textarea_field(self, canvas, line, field):
        """Process textarea field with proper layout"""
        placeholder = field['placeholder']
        pos = line.find(placeholder)
        
        before_field = line[:pos]
        after_field = line[pos + len(placeholder):]
        
        # Draw label
        if before_field.strip():
            self._check_page_break(canvas, 1)
            self._draw_formatted_text(canvas, before_field.strip(), self.margin)
            self.current_y -= self.line_height
        
        # Create textarea
        self._check_page_break(canvas, 1)
        self._create_form_field(canvas, field, self.margin, self.current_y)
        
        lines = field.get('lines', 3)
        textarea_height = lines * self.line_height + 8
        self.current_y -= textarea_height
        
        # Draw text after field
        if after_field.strip():
            self._check_page_break(canvas, 1)
            self._draw_formatted_text(canvas, after_field.strip(), self.margin)
            self.current_y -= self.line_height

    def _draw_text_line(self, canvas, line):
        """Draw a regular text line with formatting"""
        if not line.strip():
            self.current_y -= self.line_height
            return
        
        # Horizontal rule
        if line.strip() in ['---', '***', '___'] or (len(line.strip()) >= 3 and all(c in '-*_' for c in line.strip()) and len(set(line.strip())) == 1):
            self._check_page_break(canvas, 2)
            line_y = self.current_y - (self.line_height // 2)
            canvas.setStrokeColor(black)
            canvas.setLineWidth(1)
            canvas.line(self.margin, line_y, self.width - self.margin, line_y)
            self.current_y -= self.line_height
            return
        
        # Headings
        if line.startswith('# '):
            self._check_page_break(canvas, 2)
            text = line[2:].strip()
            if text:
                self._draw_wrapped_text(canvas, text, self.margin, "Helvetica-Bold", 16)
                self.current_y -= self.line_height // 2
        elif line.startswith('## '):
            self._check_page_break(canvas, 2)
            text = line[3:].strip()
            if text:
                self._draw_wrapped_text(canvas, text, self.margin, "Helvetica-Bold", 14)
                self.current_y -= self.line_height // 2
        elif line.startswith('### '):
            self._check_page_break(canvas, 1)
            text = line[4:].strip()
            if text:
                self._draw_wrapped_text(canvas, text, self.margin, "Helvetica-Bold", 12)
        elif line.startswith('**') and line.endswith('**') and len(line) > 4:
            self._check_page_break(canvas, 1)
            text = line[2:-2].strip()
            if text:
                self._draw_wrapped_text(canvas, text, self.margin, "Helvetica-Bold", 10)
        elif line.startswith('- ') or line.startswith('* '):
            self._check_page_break(canvas, 1)
            bullet_text = line[2:].strip()
            if bullet_text:
                canvas.setFont("Helvetica", 10)
                canvas.drawString(self.margin, self.current_y, "•")
                self._draw_formatted_text(canvas, bullet_text, self.margin + 20)
                self.current_y -= self.line_height
        else:
            text = line.strip()
            if text:
                self._check_page_break(canvas, 1)
                self._draw_formatted_text(canvas, text, self.margin)
                self.current_y -= self.line_height
            else:
                self.current_y -= self.line_height

    def _draw_formatted_text(self, canvas, text, x_start):
        """Draw text with inline bold formatting and wrapping"""
        if not text.strip():
            return False
        
        bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
        has_bold = bool(re.search(bold_pattern, text))
        
        if not has_bold:
            canvas.setFont("Helvetica", 10)
            available_width = self.width - self.margin - x_start
            
            if canvas.stringWidth(text) <= available_width:
                canvas.drawString(x_start, self.current_y, text)
                return False
            else:
                wrapped_lines = self._wrap_text(canvas, text, available_width, "Helvetica", 10)
                for i, line in enumerate(wrapped_lines):
                    canvas.setFont("Helvetica", 10)
                    canvas.drawString(x_start if i == 0 else self.margin, self.current_y, line)
                    if i < len(wrapped_lines) - 1:
                        self.current_y -= self.line_height
                        page_break_occurred = self._check_page_break(canvas, 1)
                        if page_break_occurred:
                            canvas.setFont("Helvetica", 10)
                return len(wrapped_lines) > 1
        
        return self._draw_formatted_text_with_wrapping(canvas, text, x_start, bold_pattern)

    def _draw_formatted_text_with_wrapping(self, canvas, text, x_start, bold_pattern):
        """Draw formatted text with proper wrapping"""
        available_width = self.width - self.margin - x_start
        parts = self._parse_formatted_parts(text, bold_pattern)
        total_width = self._calculate_parts_width(canvas, parts)
        
        if total_width <= available_width:
            current_x = x_start
            for part_type, part_text in parts:
                font_name = "Helvetica-Bold" if part_type == 'bold' else "Helvetica"
                canvas.setFont(font_name, 10)
                canvas.drawString(current_x, self.current_y, part_text)
                current_x += canvas.stringWidth(part_text)
            return False
        else:
            return self._wrap_formatted_text(canvas, parts, x_start)

    def _parse_formatted_parts(self, text, bold_pattern):
        """Parse text into regular and bold parts"""
        parts = []
        last_end = 0
        
        for match in re.finditer(bold_pattern, text):
            if match.start() > last_end:
                regular_text = text[last_end:match.start()]
                if regular_text:
                    parts.append(('regular', regular_text))
            
            bold_text = match.group(1)
            if bold_text:
                parts.append(('bold', bold_text))
            
            last_end = match.end()
        
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
        """Wrap formatted text while preserving bold"""
        lines_drawn = 0
        current_x = x_start
        available_width = self.width - self.margin - x_start
        
        for part_index, (part_type, part_text) in enumerate(parts):
            font_name = "Helvetica-Bold" if part_type == 'bold' else "Helvetica"
            canvas.setFont(font_name, 10)
            
            needs_leading_space = (part_index > 0 and 
                                 not part_text.startswith(' ') and 
                                 current_x > self.margin)
            
            if needs_leading_space:
                space_width = canvas.stringWidth(' ')
                if current_x + space_width <= self.width - self.margin:
                    canvas.drawString(current_x, self.current_y, ' ')
                    current_x += space_width
                else:
                    self.current_y -= self.line_height
                    page_break_occurred = self._check_page_break(canvas, 1)
                    if page_break_occurred:
                        canvas.setFont(font_name, 10)
                    current_x = self.margin
                    lines_drawn += 1
            
            part_width = canvas.stringWidth(part_text)
            
            if current_x + part_width <= self.width - self.margin:
                canvas.drawString(current_x, self.current_y, part_text)
                current_x += part_width
            else:
                words = part_text.split()
                
                for i, word in enumerate(words):
                    word_to_draw = word if i == 0 else " " + word
                    word_width = canvas.stringWidth(word_to_draw)
                    
                    if current_x + word_width > self.width - self.margin:
                        self.current_y -= self.line_height
                        page_break_occurred = self._check_page_break(canvas, 1)
                        if page_break_occurred:
                            canvas.setFont(font_name, 10)
                        current_x = self.margin
                        available_width = self.available_width
                        lines_drawn += 1
                        
                        word_to_draw = word
                        word_width = canvas.stringWidth(word_to_draw)
                        
                        if word_width > available_width:
                            self._draw_long_word_wrapped(canvas, word, font_name, current_x)
                            current_x = self.margin
                            available_width = self.available_width
                        else:
                            canvas.drawString(current_x, self.current_y, word_to_draw)
                            current_x += word_width
                    else:
                        canvas.drawString(current_x, self.current_y, word_to_draw)
                        current_x += word_width
        
        return lines_drawn > 0

    def _draw_long_word_wrapped(self, canvas, word, font_name, start_x):
        """Draw a word that's too long for one line"""
        canvas.setFont(font_name, 10)
        current_x = start_x
        available_width = self.width - self.margin - current_x
        
        i = 0
        while i < len(word):
            chars_that_fit = 0
            width_so_far = 0
            
            for j in range(i, len(word)):
                char_width = canvas.stringWidth(word[j])
                if width_so_far + char_width > available_width:
                    break
                width_so_far += char_width
                chars_that_fit += 1
            
            if chars_that_fit == 0:
                chars_that_fit = 1
            
            char_segment = word[i:i + chars_that_fit]
            canvas.drawString(current_x, self.current_y, char_segment)
            
            i += chars_that_fit
            
            if i < len(word):
                self.current_y -= self.line_height
                page_break_occurred = self._check_page_break(canvas, 1)
                if page_break_occurred:
                    canvas.setFont(font_name, 10)
                current_x = self.margin
                available_width = self.available_width
            else:
                current_x += width_so_far

    def _draw_wrapped_text(self, canvas, text, x, font_name="Helvetica", font_size=10):
        """Draw text with wrapping"""
        if not text.strip():
            return 0
        
        canvas.setFont(font_name, font_size)
        available_width = self.width - self.margin - x
        
        if canvas.stringWidth(text) <= available_width:
            canvas.drawString(x, self.current_y, text)
            self.current_y -= self.line_height
            return 1
        else:
            wrapped_lines = simpleSplit(text, font_name, font_size, available_width)
            for i, line in enumerate(wrapped_lines):
                canvas.setFont(font_name, font_size)
                canvas.drawString(x if i == 0 else self.margin, self.current_y, line)
                if i < len(wrapped_lines) - 1:
                    self.current_y -= self.line_height
                    page_break_occurred = self._check_page_break(canvas, 1)
                    if page_break_occurred:
                        canvas.setFont(font_name, font_size)
            self.current_y -= self.line_height
            return len(wrapped_lines)

    def _draw_formatted_text_inline(self, canvas, text, x_start):
        """Draw formatted text inline and return ending x position"""
        bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
        current_x = x_start
        last_end = 0
        
        for match in re.finditer(bold_pattern, text):
            if match.start() > last_end:
                regular_text = text[last_end:match.start()]
                canvas.setFont("Helvetica", 10)
                canvas.drawString(current_x, self.current_y, regular_text)
                current_x += canvas.stringWidth(regular_text)
            
            bold_text = match.group(1)
            canvas.setFont("Helvetica-Bold", 10)
            canvas.drawString(current_x, self.current_y, bold_text)
            current_x += canvas.stringWidth(bold_text)
            
            last_end = match.end()
        
        if last_end < len(text):
            remaining_text = text[last_end:]
            canvas.setFont("Helvetica", 10)
            canvas.drawString(current_x, self.current_y, remaining_text)
            current_x += canvas.stringWidth(remaining_text)
        
        return current_x

    def _calculate_formatted_text_width(self, canvas, text):
        """Calculate the total width of text with bold formatting"""
        bold_pattern = r'\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*'
        total_width = 0
        last_end = 0
        
        for match in re.finditer(bold_pattern, text):
            if match.start() > last_end:
                regular_text = text[last_end:match.start()]
                canvas.setFont("Helvetica", 10)
                total_width += canvas.stringWidth(regular_text)
            
            bold_text = match.group(1)
            canvas.setFont("Helvetica-Bold", 10)
            total_width += canvas.stringWidth(bold_text)
            
            last_end = match.end()
        
        if last_end < len(text):
            remaining_text = text[last_end:]
            canvas.setFont("Helvetica", 10)
            total_width += canvas.stringWidth(remaining_text)
        
        return total_width

    def _wrap_text(self, canvas, text, max_width, font_name="Helvetica", font_size=10):
        """Wrap text to fit within width"""
        canvas.setFont(font_name, font_size)
        return simpleSplit(text, font_name, font_size, max_width)

    def _create_form_field(self, canvas, field, x, y):
        """Create a form field"""
        field_type = field['type']
        field_name = field['name']
        
        try:
            if field_type in ['text', 'email', 'number', 'date']:
                width = field.get('width', self.default_field_width)
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
                    fontName="Helvetica",
                    fontSize=10
                )
                return width
                
            elif field_type == 'textarea':
                lines = field.get('lines', 3)
                width = field.get('width', 400)
                height = lines * self.line_height + 8
                
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
                        fontName="Helvetica",
                        fontSize=10
                    )
                except TypeError:
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
                        fontName="Helvetica",
                        fontSize=10
                    )
                return height
                
            elif field_type == 'checkbox':
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
                num_options = len(field['options'])
                
                if num_options <= 2:
                    current_line_x = x
                    current_y = y
                    max_option_width = 0
                    
                    for i, option in enumerate(field['options']):
                        option_value = option.strip()
                        
                        try:
                            canvas.acroForm.radio(
                                name=field_name,
                                tooltip=f"Select {option_value}",
                                x=current_line_x, 
                                y=current_y - 2,
                                size=12,
                                value=option_value,
                                borderColor=black,
                                fillColor=None,
                                textColor=black,
                                forceBorder=True
                            )
                        except Exception:
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
                                shape='circle'
                            )
                        
                        label_x = current_line_x + 18
                        canvas.setFont("Helvetica", 10)
                        canvas.drawString(label_x, current_y, option_value)
                        
                        # Calculate width for this option
                        option_width = 18 + canvas.stringWidth(option_value) + 20
                        max_option_width = max(max_option_width, option_width)
                        
                        # Move to next position for second option
                        if i == 0 and num_options > 1:
                            current_line_x += option_width
                    
                    return max_option_width * num_options
                    
                else:
                    # Use dropdown for more than 2 options
                    canvas.setFont("Helvetica", 10)
                    canvas.drawString(x, y, "Select one:")
                    
                    dropdown_x = x
                    dropdown_y = y - 16
                    
                    width = 300
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
                            fontName="Helvetica",
                            fontSize=10
                        )
                        
                        self.current_y -= 20
                        return width
                    except Exception as e:
                        canvas.drawString(x, dropdown_y, "Options (select one):")
                        self.current_y -= self.line_height
                        
                        for i, option in enumerate(options):
                            self.current_y -= self.line_height
                            self._check_page_break(canvas, 1)
                            
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
                            
                            canvas.setFont("Helvetica", 10)
                            canvas.drawString(self.margin + 18, self.current_y, option.strip())
                        
                        return 200
                
            elif field_type == 'dropdown':
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
                        fontName="Helvetica",
                        fontSize=10
                    )
                except Exception as e:
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
                        fontName="Helvetica",
                        fontSize=10
                    )
                return width
        
        except Exception as e:
            print(f"Error creating field {field_name}: {e}")
            canvas.drawString(x, y, f"[{field_name}]")
            return 100
        
        return 0

    def _check_page_break(self, canvas, lines_needed=1):
        """Check if we need a page break"""
        space_needed = lines_needed * self.line_height
        if self.current_y - space_needed < self.margin:
            canvas.showPage()
            self.current_y = self.height - self.margin
            return True
        return False

    def test_basic_pdf_creation(self, filename):
        """Test basic PDF creation"""
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
  {{text:field_name}}                  # Text input (default 150px width)
  {{text:field_name:200}}              # Text input (200px width)
  {{email:email_field}}                # Email input (default width)
  {{email:email_field:250}}            # Email input (250px width)
  {{number:number_field:100}}          # Number input (100px width)
  {{date:date_field:180}}              # Date input (180px width)
  {{textarea:comments}}                # Multi-line text (3 lines, default width)
  {{textarea:comments:5}}              # Multi-line text (5 lines, default width)
  {{textarea:comments:5:500}}          # Multi-line text (5 lines, 500px width)
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
        version='%(prog)s 1.1'
    )
    
    args = parser.parse_args()
    
    if not args.input.lower().endswith('.md'):
        print("Warning: Input file doesn't have .md extension")
    
    try:
        converter = MarkdownToPDFForm()
        
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
    """Run a demonstration"""
    print("Running demonstration...")
    
    markdown_content = """
# Employee Information Form

Please fill out the following information:

**Name:** {{text:full_name}}

**Email:** {{email:email_address:250}}

**Phone:** {{text:phone_number:120}}

**Date of Birth:** {{date:birth_date:180}}

**Department:** {{dropdown:department:Engineering,Marketing,Sales,HR,Finance}}

## Emergency Contact

**Contact Name:** {{text:emergency_name}}

**Contact Phone:** {{text:emergency_phone:120}}

**Relationship:** {{dropdown:relationship:Spouse,Parent,Sibling,Friend,Other}}

## Preferences

**Preferred Communication:**
{{radio:communication:Email,Phone}}

**Subscribe to Newsletter:** {{checkbox:newsletter}}

## Additional Comments

{{textarea:comments:4}}

**Long Comments Section:**

{{textarea:long_comments:6:500}}

**Signature:** ________________________

Thank you for completing this form!
"""
    
    converter = MarkdownToPDFForm()
    converter.create_pdf_form(markdown_content, "demo_employee_form.pdf")
    print("✅ Demo PDF created: demo_employee_form.pdf")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Markdown to PDF Form Converter")
        print("==============================")
        print()
        print("Usage: python md2pdfform.py <input.md> [-o output.pdf]")
        print()
        print("Run with --help for detailed usage information")
        print("Run demo by adding 'demo' as argument")
        print()
        sys.exit(0)
    
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'demo':
        demo()
    else:
        main()