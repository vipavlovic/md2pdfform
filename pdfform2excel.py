#!/usr/bin/env python3
"""
PDF Form to Excel Exporter
Extracts filled form data from PDF files created by md2pdfform and exports to Excel
"""

import sys
import argparse
import os
from pathlib import Path

try:
    from PyPDF2 import PdfReader
except ImportError:
    print("Error: PyPDF2 is required. Install with: pip install PyPDF2")
    sys.exit(1)

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
except ImportError:
    print("Error: openpyxl is required. Install with: pip install openpyxl")
    sys.exit(1)


def extract_form_data(pdf_path):
    """Extract form field data from a PDF file"""
    try:
        reader = PdfReader(pdf_path)
        
        if reader.is_encrypted:
            print(f"Warning: {pdf_path} is encrypted. Attempting to decrypt...")
            reader.decrypt('')
        
        # Get form fields
        if '/AcroForm' not in reader.trailer['/Root']:
            print(f"Warning: {pdf_path} does not contain form fields")
            return {}
        
        fields = reader.get_fields()
        
        if not fields:
            print(f"Warning: No form fields found in {pdf_path}")
            return {}
        
        # Extract field names and values
        form_data = {}
        for field_name, field_info in fields.items():
            value = field_info.get('/V', '')
            
            # Handle different value types
            if hasattr(value, 'get_object'):
                value = value.get_object()
            
            # Convert bytes to string
            if isinstance(value, bytes):
                value = value.decode('utf-8', errors='ignore')
            
            # Handle checkbox/radio button values
            if value == '/Yes':
                value = 'Yes'
            elif value == '/Off':
                value = 'No'
            elif value == '':
                value = ''
            
            form_data[field_name] = str(value) if value else ''
        
        return form_data
    
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return {}


def export_single_pdf_to_excel(pdf_path, output_path):
    """Export a single PDF form to Excel"""
    print(f"Processing: {pdf_path}")
    
    form_data = extract_form_data(pdf_path)
    
    if not form_data:
        print("No form data found to export")
        return False
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Form Data"
    
    # Add headers
    ws['A1'] = 'Field Name'
    ws['B1'] = 'Value'
    
    # Style headers
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    ws['A1'].fill = header_fill
    ws['A1'].font = header_font
    ws['B1'].fill = header_fill
    ws['B1'].font = header_font
    
    # Add data
    row = 2
    for field_name, value in sorted(form_data.items()):
        ws[f'A{row}'] = field_name
        ws[f'B{row}'] = value
        row += 1
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 40
    ws.column_dimensions['B'].width = 60
    
    # Save workbook
    wb.save(output_path)
    print(f"✅ Excel file created: {output_path}")
    print(f"📊 Exported {len(form_data)} fields")
    
    return True


def export_multiple_pdfs_to_excel(pdf_paths, output_path):
    """Export multiple PDF forms to a single Excel file with each PDF as a row"""
    print(f"Processing {len(pdf_paths)} PDF files...")
    
    all_field_names = set()
    all_data = []
    
    # First pass: collect all unique field names
    for pdf_path in pdf_paths:
        print(f"Reading: {pdf_path}")
        form_data = extract_form_data(pdf_path)
        
        if form_data:
            all_field_names.update(form_data.keys())
            all_data.append({
                'filename': os.path.basename(pdf_path),
                'data': form_data
            })
    
    if not all_data:
        print("No form data found in any PDF")
        return False
    
    # Sort field names for consistent column order
    sorted_fields = sorted(all_field_names)
    
    # Create workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Form Data"
    
    # Add headers
    ws['A1'] = 'PDF Filename'
    for col_idx, field_name in enumerate(sorted_fields, start=2):
        ws.cell(row=1, column=col_idx, value=field_name)
    
    # Style headers
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")
    for col_idx in range(1, len(sorted_fields) + 2):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
    
    # Add data rows
    for row_idx, entry in enumerate(all_data, start=2):
        ws.cell(row=row_idx, column=1, value=entry['filename'])
        
        for col_idx, field_name in enumerate(sorted_fields, start=2):
            value = entry['data'].get(field_name, '')
            ws.cell(row=row_idx, column=col_idx, value=value)
    
    # Adjust column widths
    ws.column_dimensions['A'].width = 30
    for col_idx in range(2, len(sorted_fields) + 2):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col_idx)].width = 25
    
    # Save workbook
    wb.save(output_path)
    print(f"✅ Excel file created: {output_path}")
    print(f"📊 Exported {len(all_data)} PDFs with {len(sorted_fields)} unique fields")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Extract filled PDF form data and export to Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export single PDF
  %(prog)s filled_form.pdf -o output.xlsx
  
  # Export multiple PDFs to one Excel file (each PDF is a row)
  %(prog)s form1.pdf form2.pdf form3.pdf -o combined.xlsx
  
  # Export all PDFs in a directory
  %(prog)s *.pdf -o all_forms.xlsx
        """
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='Input PDF file(s) with filled forms'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output Excel file (.xlsx)'
    )
    
    parser.add_argument(
        '--mode',
        choices=['single', 'combined'],
        default='auto',
        help='Export mode: single (one sheet per PDF) or combined (all PDFs in one sheet). Default: auto-detect'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    pdf_paths = []
    for path in args.input:
        if os.path.exists(path) and path.lower().endswith('.pdf'):
            pdf_paths.append(path)
        else:
            print(f"Warning: Skipping {path} (not found or not a PDF)")
    
    if not pdf_paths:
        print("Error: No valid PDF files provided")
        sys.exit(1)
    
    # Ensure output has .xlsx extension
    output_path = args.output
    if not output_path.lower().endswith('.xlsx'):
        output_path += '.xlsx'
    
    # Determine mode
    mode = args.mode
    if mode == 'auto':
        mode = 'single' if len(pdf_paths) == 1 else 'combined'
    
    # Export
    try:
        if mode == 'single' and len(pdf_paths) == 1:
            success = export_single_pdf_to_excel(pdf_paths[0], output_path)
        else:
            success = export_multiple_pdfs_to_excel(pdf_paths, output_path)
        
        if success:
            print(f"\n✅ Export completed successfully!")
        else:
            print(f"\n❌ Export failed")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error during export: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
