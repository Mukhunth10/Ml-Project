"""
Report Generator - Generate various reports
"""
from typing import Dict, List
from datetime import datetime
from ..boq import BOQGenerator


class ReportGenerator:
    """Generate reports from project data"""
    
    def __init__(self, project_data: Dict):
        """
        Initialize report generator
        
        Args:
            project_data: Project data dictionary
        """
        self.project_data = project_data
        self.project_name = project_data.get('name', 'Untitled Project')
    
    def generate_project_summary(self) -> str:
        """Generate project summary report"""
        report = []
        report.append("="*80)
        report.append(f"PROJECT SUMMARY REPORT")
        report.append("="*80)
        report.append(f"Project: {self.project_name}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Project details
        if 'location' in self.project_data:
            report.append(f"Location: {self.project_data['location']}")
        if 'client' in self.project_data:
            report.append(f"Client: {self.project_data['client']}")
        if 'standard' in self.project_data:
            report.append(f"Measurement Standard: {self.project_data['standard']}")
        
        report.append("")
        report.append("-"*80)
        
        # Statistics
        stats = self.project_data.get('statistics', {})
        if stats:
            report.append("PROJECT STATISTICS:")
            report.append(f"  Total Drawings: {stats.get('drawings', 0)}")
            report.append(f"  Total Measurements: {stats.get('measurements', 0)}")
            report.append(f"  BOQ Items: {stats.get('boq_items', 0)}")
        
        report.append("")
        report.append("="*80)
        
        return "\n".join(report)
    
    def generate_measurement_summary(self, measurements: List[Dict]) -> str:
        """Generate measurement summary report"""
        report = []
        report.append("="*80)
        report.append(f"MEASUREMENT SUMMARY")
        report.append("="*80)
        
        # Group by category
        by_category = {}
        for measurement in measurements:
            category = measurement.get('category', 'General')
            if category not in by_category:
                by_category[category] = {
                    'count': 0,
                    'total_length': 0.0,
                    'total_area': 0.0
                }
            
            by_category[category]['count'] += 1
            if measurement.get('length'):
                by_category[category]['total_length'] += measurement['length']
            if measurement.get('area'):
                by_category[category]['total_area'] += measurement['area']
        
        report.append(f"\nTotal Measurements: {len(measurements)}")
        report.append(f"\nBy Category:")
        report.append("-"*80)
        
        for category, data in sorted(by_category.items()):
            report.append(f"\n{category}:")
            report.append(f"  Count: {data['count']}")
            if data['total_length'] > 0:
                report.append(f"  Total Length: {data['total_length']:,.2f} m")
            if data['total_area'] > 0:
                report.append(f"  Total Area: {data['total_area']:,.2f} m²")
        
        report.append("\n" + "="*80)
        
        return "\n".join(report)
    
    def generate_cost_comparison(self, boq1: Dict, boq2: Dict, labels: tuple = ('Original', 'Revised')) -> str:
        """Generate cost comparison report between two BOQs"""
        report = []
        report.append("="*80)
        report.append(f"COST COMPARISON REPORT")
        report.append("="*80)
        report.append(f"Comparing: {labels[0]} vs {labels[1]}")
        report.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        report.append("")
        
        totals1 = boq1.get('totals', {})
        totals2 = boq2.get('totals', {})
        
        subtotal1 = totals1.get('subtotal', 0)
        subtotal2 = totals2.get('subtotal', 0)
        total1 = totals1.get('total', 0)
        total2 = totals2.get('total', 0)
        
        diff_subtotal = subtotal2 - subtotal1
        diff_total = total2 - total1
        pct_change = ((total2 - total1) / total1 * 100) if total1 > 0 else 0
        
        report.append(f"{labels[0]:20s} {labels[1]:20s} Difference          % Change")
        report.append("-"*80)
        report.append(f"Subtotal:")
        report.append(f"£{subtotal1:>15,.2f} £{subtotal2:>15,.2f} £{diff_subtotal:>15,.2f} {pct_change:>8.2f}%")
        report.append("")
        report.append(f"Total (inc. VAT):")
        report.append(f"£{total1:>15,.2f} £{total2:>15,.2f} £{diff_total:>15,.2f} {pct_change:>8.2f}%")
        
        if diff_total > 0:
            report.append(f"\n⚠️  Cost INCREASE of £{abs(diff_total):,.2f} ({abs(pct_change):.2f}%)")
        elif diff_total < 0:
            report.append(f"\n✓ Cost DECREASE of £{abs(diff_total):,.2f} ({abs(pct_change):.2f}%)")
        else:
            report.append(f"\n= No change in cost")
        
        report.append("\n" + "="*80)
        
        return "\n".join(report)
    
    def generate_progress_report(self, progress_data: Dict) -> str:
        """Generate project progress report"""
        report = []
        report.append("="*80)
        report.append(f"PROJECT PROGRESS REPORT")
        report.append("="*80)
        report.append(f"Project: {self.project_name}")
        report.append(f"Report Date: {datetime.now().strftime('%Y-%m-%d')}")
        report.append("")
        
        # Overall progress
        overall = progress_data.get('overall_completion', 0)
        report.append(f"Overall Completion: {overall:.1f}%")
        report.append(f"[{'#' * int(overall/2)}{'-' * (50-int(overall/2))}]")
        report.append("")
        
        # By work package
        packages = progress_data.get('work_packages', {})
        if packages:
            report.append("Work Package Completion:")
            report.append("-"*80)
            for package, completion in packages.items():
                bar = '#' * int(completion/5)
                report.append(f"{package:30s} {completion:>6.1f}% [{bar:20s}]")
        
        report.append("")
        report.append("="*80)
        
        return "\n".join(report)
