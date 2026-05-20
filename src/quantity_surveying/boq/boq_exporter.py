"""
BOQ Exporter - Export BOQ to various formats (Excel, PDF, CSV)
"""
from typing import Dict, List
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
import csv
from io import BytesIO


class BOQExporter:
    """Export BOQ to different formats"""
    
    def __init__(self, boq_data: Dict):
        """
        Initialize exporter
        
        Args:
            boq_data: BOQ data dictionary from BOQGenerator.to_dict()
        """
        self.boq_data = boq_data
        self.metadata = boq_data.get('metadata', {})
        self.items = boq_data.get('items', [])
        self.totals = boq_data.get('totals', {})
    
    def to_excel(self, filename: str = None) -> BytesIO:
        """
        Export to Excel format
        
        Args:
            filename: Optional filename to save to disk
            
        Returns:
            BytesIO buffer with Excel data
        """
        wb = Workbook()
        ws = wb.active
        ws.title = "Bill of Quantities"
        
        # Styles
        header_font = Font(bold=True, size=14)
        section_font = Font(bold=True, size=12)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        section_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Title
        ws.merge_cells('A1:G1')
        title_cell = ws['A1']
        title_cell.value = self.metadata.get('project_name', 'Bill of Quantities')
        title_cell.font = Font(bold=True, size=16)
        title_cell.alignment = Alignment(horizontal='center')
        
        # Metadata
        row = 3
        ws[f'A{row}'] = 'Date:'
        ws[f'B{row}'] = self.metadata.get('created_date', '')
        ws[f'E{row}'] = 'Currency:'
        ws[f'F{row}'] = self.metadata.get('currency', 'GBP')
        
        # Column headers
        row = 5
        headers = ['Item No.', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount', 'Notes']
        for col, header in enumerate(headers, start=1):
            cell = ws.cell(row=row, column=col)
            cell.value = header
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
            cell.border = border
        
        # Data rows
        row = 6
        for item in self.items:
            if item.get('level', 1) == 1 and item.get('quantity', 0) == 0:
                # Section header
                ws.merge_cells(f'A{row}:G{row}')
                cell = ws[f'A{row}']
                cell.value = item['description']
                cell.font = section_font
                cell.fill = section_fill
                cell.border = border
            else:
                # Regular item
                ws[f'A{row}'] = item.get('item_number', '')
                ws[f'B{row}'] = item.get('description', '')
                ws[f'C{row}'] = item.get('unit', '')
                ws[f'D{row}'] = item.get('quantity', 0)
                ws[f'E{row}'] = item.get('rate', 0)
                ws[f'F{row}'] = item.get('amount', 0)
                ws[f'G{row}'] = item.get('notes', '')
                
                # Format numbers
                ws[f'D{row}'].number_format = '#,##0.00'
                ws[f'E{row}'].number_format = '#,##0.00'
                ws[f'F{row}'].number_format = '#,##0.00'
                
                # Apply borders
                for col in range(1, 8):
                    ws.cell(row=row, column=col).border = border
            
            row += 1
        
        # Totals
        row += 1
        ws[f'E{row}'] = 'Subtotal:'
        ws[f'E{row}'].font = Font(bold=True)
        ws[f'F{row}'] = self.totals.get('subtotal', 0)
        ws[f'F{row}'].number_format = '#,##0.00'
        ws[f'F{row}'].font = Font(bold=True)
        
        row += 1
        ws[f'E{row}'] = f"VAT ({self.totals.get('vat_rate', 0) * 100}%):"
        ws[f'F{row}'] = self.totals.get('vat', 0)
        ws[f'F{row}'].number_format = '#,##0.00'
        
        row += 1
        ws[f'E{row}'] = 'Total:'
        ws[f'E{row}'].font = Font(bold=True, size=12)
        ws[f'F{row}'] = self.totals.get('total', 0)
        ws[f'F{row}'].number_format = '#,##0.00'
        ws[f'F{row}'].font = Font(bold=True, size=12)
        
        # Column widths
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 50
        ws.column_dimensions['C'].width = 10
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 12
        ws.column_dimensions['F'].width = 15
        ws.column_dimensions['G'].width = 30
        
        # Save to buffer or file
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        if filename:
            wb.save(filename)
        
        return buffer
    
    def to_csv(self, filename: str = None) -> str:
        """
        Export to CSV format
        
        Args:
            filename: Optional filename to save to disk
            
        Returns:
            CSV string
        """
        output = []
        
        # Headers
        output.append(['Item No.', 'Description', 'Unit', 'Quantity', 'Rate', 'Amount', 'Notes'])
        
        # Items
        for item in self.items:
            output.append([
                item.get('item_number', ''),
                item.get('description', ''),
                item.get('unit', ''),
                item.get('quantity', 0),
                item.get('rate', 0),
                item.get('amount', 0),
                item.get('notes', '')
            ])
        
        # Totals
        output.append([])
        output.append(['', '', '', '', 'Subtotal:', self.totals.get('subtotal', 0), ''])
        output.append(['', '', '', '', f"VAT ({self.totals.get('vat_rate', 0) * 100}%):", self.totals.get('vat', 0), ''])
        output.append(['', '', '', '', 'Total:', self.totals.get('total', 0), ''])
        
        # Write to file or string
        if filename:
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(output)
        
        # Return as string
        from io import StringIO
        string_buffer = StringIO()
        writer = csv.writer(string_buffer)
        writer.writerows(output)
        return string_buffer.getvalue()
    
    def to_dataframe(self) -> pd.DataFrame:
        """Export to pandas DataFrame"""
        return pd.DataFrame(self.items)
    
    def to_json(self) -> Dict:
        """Export to JSON-serializable dictionary"""
        return self.boq_data
    
    def get_summary_report(self) -> str:
        """Generate a text summary report"""
        report = []
        report.append("=" * 60)
        report.append(f"BILL OF QUANTITIES - {self.metadata.get('project_name', 'Untitled')}")
        report.append("=" * 60)
        report.append(f"Date: {self.metadata.get('created_date', '')}")
        report.append(f"Currency: {self.metadata.get('currency', 'GBP')}")
        report.append("")
        
        # Summary by category
        report.append("SUMMARY BY CATEGORY:")
        report.append("-" * 60)
        
        categories = {}
        for item in self.items:
            category = item.get('category', 'General')
            if category not in categories:
                categories[category] = 0.0
            categories[category] += item.get('amount', 0)
        
        for category, amount in sorted(categories.items()):
            report.append(f"{category:40s} {amount:15,.2f}")
        
        report.append("")
        report.append("TOTALS:")
        report.append("-" * 60)
        report.append(f"Subtotal:                                {self.totals.get('subtotal', 0):15,.2f}")
        report.append(f"VAT ({self.totals.get('vat_rate', 0) * 100}%):                                   {self.totals.get('vat', 0):15,.2f}")
        report.append(f"Total:                                   {self.totals.get('total', 0):15,.2f}")
        report.append("=" * 60)
        
        return "\n".join(report)
