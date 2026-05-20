"""
IFC Handler - Process IFC (Industry Foundation Classes) files
"""
from typing import Dict, List, Optional, Tuple
import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.shape
from dataclasses import dataclass


@dataclass
class IFCElement:
    """Represents an IFC element with quantities"""
    global_id: str
    ifc_type: str
    name: str
    description: str
    properties: Dict
    quantities: Dict
    material: Optional[str] = None
    location: Optional[Tuple[float, float, float]] = None


class IFCHandler:
    """Handle IFC file processing and quantity extraction"""
    
    def __init__(self, ifc_file_path: str = None):
        """
        Initialize IFC handler
        
        Args:
            ifc_file_path: Path to IFC file
        """
        self.ifc_file_path = ifc_file_path
        self.ifc_file = None
        self.elements: Dict[str, IFCElement] = {}
        
        if ifc_file_path:
            self.load_file(ifc_file_path)
    
    def load_file(self, ifc_file_path: str):
        """
        Load an IFC file
        
        Args:
            ifc_file_path: Path to IFC file
        """
        try:
            self.ifc_file = ifcopenshell.open(ifc_file_path)
            self.ifc_file_path = ifc_file_path
            print(f"IFC file loaded: {ifc_file_path}")
            print(f"Schema: {self.ifc_file.schema}")
        except Exception as e:
            raise Exception(f"Error loading IFC file: {str(e)}")
    
    def get_project_info(self) -> Dict:
        """Get project information from IFC file"""
        if not self.ifc_file:
            return {}
        
        project = self.ifc_file.by_type('IfcProject')[0]
        
        info = {
            'name': project.Name if hasattr(project, 'Name') else 'Unknown',
            'description': project.Description if hasattr(project, 'Description') else '',
            'schema': self.ifc_file.schema,
            'file_path': self.ifc_file_path
        }
        
        return info
    
    def extract_elements_by_type(self, ifc_type: str) -> List[IFCElement]:
        """
        Extract elements of a specific IFC type
        
        Args:
            ifc_type: IFC type (e.g., 'IfcWall', 'IfcSlab', 'IfcColumn')
            
        Returns:
            List of IFC elements
        """
        if not self.ifc_file:
            return []
        
        elements = []
        ifc_elements = self.ifc_file.by_type(ifc_type)
        
        for element in ifc_elements:
            ifc_element = self._extract_element_data(element)
            elements.append(ifc_element)
            self.elements[ifc_element.global_id] = ifc_element
        
        return elements
    
    def _extract_element_data(self, element) -> IFCElement:
        """Extract data from an IFC element"""
        # Basic properties
        global_id = element.GlobalId
        ifc_type = element.is_a()
        name = element.Name if hasattr(element, 'Name') else ''
        description = element.Description if hasattr(element, 'Description') else ''
        
        # Properties
        properties = {}
        if hasattr(element, 'IsDefinedBy'):
            for definition in element.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a('IfcPropertySet'):
                        for prop in property_set.HasProperties:
                            if prop.is_a('IfcPropertySingleValue'):
                                properties[prop.Name] = prop.NominalValue.wrappedValue if prop.NominalValue else None
        
        # Quantities
        quantities = self._extract_quantities(element)
        
        # Material
        material = self._extract_material(element)
        
        # Location (simplified)
        location = self._extract_location(element)
        
        return IFCElement(
            global_id=global_id,
            ifc_type=ifc_type,
            name=name,
            description=description,
            properties=properties,
            quantities=quantities,
            material=material,
            location=location
        )
    
    def _extract_quantities(self, element) -> Dict:
        """Extract quantities from element"""
        quantities = {}
        
        if hasattr(element, 'IsDefinedBy'):
            for definition in element.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    property_set = definition.RelatingPropertyDefinition
                    if property_set.is_a('IfcElementQuantity'):
                        for quantity in property_set.Quantities:
                            if quantity.is_a('IfcQuantityLength'):
                                quantities[quantity.Name] = {
                                    'value': quantity.LengthValue,
                                    'unit': 'm'
                                }
                            elif quantity.is_a('IfcQuantityArea'):
                                quantities[quantity.Name] = {
                                    'value': quantity.AreaValue,
                                    'unit': 'm²'
                                }
                            elif quantity.is_a('IfcQuantityVolume'):
                                quantities[quantity.Name] = {
                                    'value': quantity.VolumeValue,
                                    'unit': 'm³'
                                }
                            elif quantity.is_a('IfcQuantityCount'):
                                quantities[quantity.Name] = {
                                    'value': quantity.CountValue,
                                    'unit': 'nr'
                                }
                            elif quantity.is_a('IfcQuantityWeight'):
                                quantities[quantity.Name] = {
                                    'value': quantity.WeightValue,
                                    'unit': 'kg'
                                }
        
        return quantities
    
    def _extract_material(self, element) -> Optional[str]:
        """Extract material information"""
        material = None
        
        if hasattr(element, 'HasAssociations'):
            for association in element.HasAssociations:
                if association.is_a('IfcRelAssociatesMaterial'):
                    material_select = association.RelatingMaterial
                    if material_select.is_a('IfcMaterial'):
                        material = material_select.Name
                    elif material_select.is_a('IfcMaterialLayerSetUsage'):
                        material = material_select.ForLayerSet.LayerSetName
        
        return material
    
    def _extract_location(self, element) -> Optional[Tuple[float, float, float]]:
        """Extract element location (simplified)"""
        try:
            if hasattr(element, 'ObjectPlacement'):
                # This is a simplified extraction
                # Full 3D location extraction would require more complex logic
                return (0.0, 0.0, 0.0)  # Placeholder
        except:
            pass
        
        return None
    
    def get_elements_by_type_summary(self) -> Dict[str, int]:
        """Get count of elements by type"""
        if not self.ifc_file:
            return {}
        
        summary = {}
        
        # Common building element types
        element_types = [
            'IfcWall', 'IfcSlab', 'IfcColumn', 'IfcBeam', 'IfcDoor', 'IfcWindow',
            'IfcStair', 'IfcRoof', 'IfcRailing', 'IfcCovering', 'IfcFooting'
        ]
        
        for element_type in element_types:
            elements = self.ifc_file.by_type(element_type)
            if elements:
                summary[element_type] = len(elements)
        
        return summary
    
    def extract_all_quantities(self) -> Dict[str, List[Dict]]:
        """Extract quantities from all building elements"""
        if not self.ifc_file:
            return {}
        
        all_quantities = {}
        
        element_types = [
            'IfcWall', 'IfcSlab', 'IfcColumn', 'IfcBeam', 'IfcDoor', 'IfcWindow',
            'IfcStair', 'IfcRoof', 'IfcRailing', 'IfcCovering', 'IfcFooting'
        ]
        
        for element_type in element_types:
            elements = self.extract_elements_by_type(element_type)
            if elements:
                all_quantities[element_type] = [
                    {
                        'name': elem.name,
                        'material': elem.material,
                        'quantities': elem.quantities
                    }
                    for elem in elements
                ]
        
        return all_quantities
    
    def get_element_by_guid(self, global_id: str) -> Optional[IFCElement]:
        """Get element by GlobalId"""
        return self.elements.get(global_id)
    
    def search_elements(self, keyword: str) -> List[IFCElement]:
        """Search elements by keyword in name or description"""
        keyword_lower = keyword.lower()
        return [
            elem for elem in self.elements.values()
            if keyword_lower in elem.name.lower() or keyword_lower in elem.description.lower()
        ]
    
    def export_to_boq_format(self) -> List[Dict]:
        """Export IFC quantities in BOQ format"""
        boq_items = []
        
        for element in self.elements.values():
            for qty_name, qty_data in element.quantities.items():
                boq_items.append({
                    'description': f"{element.ifc_type} - {element.name} - {qty_name}",
                    'unit': qty_data.get('unit', 'nr'),
                    'quantity': qty_data.get('value', 0),
                    'category': element.ifc_type,
                    'material': element.material,
                    'notes': f"IFC GUID: {element.global_id}"
                })
        
        return boq_items
