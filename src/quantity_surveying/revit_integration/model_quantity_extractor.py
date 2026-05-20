"""
Model Quantity Extractor - Extract and process quantities from BIM models
"""
from typing import Dict, List, Optional
from .ifc_handler import IFCHandler
from .revit_connector import RevitConnector


class ModelQuantityExtractor:
    """Extract quantities from BIM models (IFC or Revit)"""
    
    def __init__(self):
        self.ifc_handler: Optional[IFCHandler] = None
        self.revit_connector: Optional[RevitConnector] = None
        self.source_type = None
    
    def load_from_ifc(self, ifc_file_path: str):
        """
        Load model from IFC file
        
        Args:
            ifc_file_path: Path to IFC file
        """
        self.ifc_handler = IFCHandler(ifc_file_path)
        self.source_type = 'IFC'
        print(f"Loaded IFC model from: {ifc_file_path}")
    
    def connect_to_revit(self, revit_version: str = "2024"):
        """
        Connect to Revit application
        
        Args:
            revit_version: Revit version
        """
        self.revit_connector = RevitConnector()
        self.revit_connector.connect(revit_version)
        self.source_type = 'Revit'
    
    def get_project_info(self) -> Dict:
        """Get project information"""
        if self.source_type == 'IFC' and self.ifc_handler:
            return self.ifc_handler.get_project_info()
        elif self.source_type == 'Revit' and self.revit_connector:
            return self.revit_connector.get_active_document_info()
        else:
            return {}
    
    def get_element_types_summary(self) -> Dict[str, int]:
        """Get summary of element types in model"""
        if self.source_type == 'IFC' and self.ifc_handler:
            return self.ifc_handler.get_elements_by_type_summary()
        else:
            return {}
    
    def extract_quantities_by_category(self, category: str) -> List[Dict]:
        """
        Extract quantities for a specific category
        
        Args:
            category: Category name (e.g., 'Walls', 'Slabs', 'Columns')
            
        Returns:
            List of quantity dictionaries
        """
        if self.source_type == 'IFC' and self.ifc_handler:
            # Map common names to IFC types
            ifc_type_mapping = {
                'Walls': 'IfcWall',
                'Slabs': 'IfcSlab',
                'Floors': 'IfcSlab',
                'Columns': 'IfcColumn',
                'Beams': 'IfcBeam',
                'Doors': 'IfcDoor',
                'Windows': 'IfcWindow',
                'Stairs': 'IfcStair',
                'Roofs': 'IfcRoof',
                'Railings': 'IfcRailing'
            }
            
            ifc_type = ifc_type_mapping.get(category, category)
            elements = self.ifc_handler.extract_elements_by_type(ifc_type)
            
            return [
                {
                    'name': elem.name,
                    'type': elem.ifc_type,
                    'material': elem.material,
                    'quantities': elem.quantities,
                    'properties': elem.properties
                }
                for elem in elements
            ]
        
        return []
    
    def extract_all_quantities(self) -> Dict[str, List[Dict]]:
        """Extract all quantities from model"""
        if self.source_type == 'IFC' and self.ifc_handler:
            return self.ifc_handler.extract_all_quantities()
        return {}
    
    def generate_boq_from_model(self) -> List[Dict]:
        """
        Generate BOQ items from model quantities
        
        Returns:
            List of BOQ item dictionaries
        """
        if self.source_type == 'IFC' and self.ifc_handler:
            return self.ifc_handler.export_to_boq_format()
        return []
    
    def aggregate_quantities(self, group_by: str = 'type') -> Dict:
        """
        Aggregate quantities by type or material
        
        Args:
            group_by: 'type' or 'material'
            
        Returns:
            Aggregated quantities dictionary
        """
        all_quantities = self.extract_all_quantities()
        aggregated = {}
        
        for element_type, elements in all_quantities.items():
            for element in elements:
                if group_by == 'type':
                    key = element_type
                elif group_by == 'material':
                    key = element.get('material', 'Unknown')
                else:
                    key = 'All'
                
                if key not in aggregated:
                    aggregated[key] = {
                        'total_area': 0.0,
                        'total_volume': 0.0,
                        'total_length': 0.0,
                        'count': 0
                    }
                
                quantities = element.get('quantities', {})
                for qty_name, qty_data in quantities.items():
                    value = qty_data.get('value', 0)
                    unit = qty_data.get('unit', '')
                    
                    if unit == 'm²':
                        aggregated[key]['total_area'] += value
                    elif unit == 'm³':
                        aggregated[key]['total_volume'] += value
                    elif unit == 'm':
                        aggregated[key]['total_length'] += value
                    elif unit == 'nr':
                        aggregated[key]['count'] += int(value)
        
        return aggregated
    
    def export_quantities_report(self) -> str:
        """Generate a text report of quantities"""
        report = []
        report.append("=" * 60)
        report.append("MODEL QUANTITIES REPORT")
        report.append("=" * 60)
        
        # Project info
        project_info = self.get_project_info()
        report.append(f"Project: {project_info.get('name', 'Unknown')}")
        report.append(f"Source: {self.source_type}")
        report.append("")
        
        # Element types summary
        summary = self.get_element_types_summary()
        report.append("ELEMENT TYPES:")
        report.append("-" * 60)
        for element_type, count in summary.items():
            report.append(f"{element_type:30s} {count:>10} elements")
        
        report.append("")
        
        # Aggregated quantities
        aggregated = self.aggregate_quantities('type')
        report.append("AGGREGATED QUANTITIES BY TYPE:")
        report.append("-" * 60)
        for element_type, quantities in aggregated.items():
            report.append(f"\n{element_type}:")
            if quantities['total_length'] > 0:
                report.append(f"  Length: {quantities['total_length']:.2f} m")
            if quantities['total_area'] > 0:
                report.append(f"  Area: {quantities['total_area']:.2f} m²")
            if quantities['total_volume'] > 0:
                report.append(f"  Volume: {quantities['total_volume']:.2f} m³")
            if quantities['count'] > 0:
                report.append(f"  Count: {quantities['count']}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
