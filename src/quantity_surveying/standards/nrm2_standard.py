"""
NRM2 Standard - New Rules of Measurement 2: Detailed measurement for building works
Used in UK for building projects
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class NRM2Item:
    """Represents an NRM2 measurement item"""
    code: str
    description: str
    unit: str
    measurement_rules: str
    level: int  # 1, 2, or 3 for hierarchy
    parent_code: Optional[str] = None


class NRM2Standard:
    """
    NRM2 (New Rules of Measurement 2) Standard Implementation
    RICS standard for detailed measurement for building works
    """
    
    def __init__(self):
        self.items: Dict[str, NRM2Item] = {}
        self._initialize_nrm2_structure()
    
    def _initialize_nrm2_structure(self):
        """Initialize NRM2 work sections"""
        
        # Group 1: Facilitating Works
        self._add_section("1", "FACILITATING WORKS", 1)
        self._add_item("1.1", "Toxic/hazardous/contaminated material treatment", "Item", 1, "1")
        self._add_item("1.2", "Major demolition works", "m²", 1, "1")
        self._add_item("1.3", "Temporary support to adjacent structures", "Item", 1, "1")
        self._add_item("1.4", "Specialist groundworks", "m³", 1, "1")
        self._add_item("1.5", "Temporary diversion works", "Item", 1, "1")
        
        # Group 2: Substructure
        self._add_section("2", "SUBSTRUCTURE", 1)
        self._add_item("2.1", "Excavation", "m³", 1, "2")
        self._add_item("2.2", "Underpinning", "m", 1, "2")
        self._add_item("2.3", "Piling", "m", 1, "2")
        self._add_item("2.4", "Substructure concrete works", "m³", 1, "2")
        self._add_item("2.5", "Basement excavation", "m³", 1, "2")
        self._add_item("2.6", "Basement waterproofing", "m²", 1, "2")
        
        # Group 3: Superstructure
        self._add_section("3", "SUPERSTRUCTURE", 1)
        
        # 3.1 Frame
        self._add_item("3.1", "Frame", "", 1, "3")
        self._add_item("3.1.1", "Steel frames", "tonne", 2, "3.1")
        self._add_item("3.1.2", "Space frames/decks", "m²", 2, "3.1")
        self._add_item("3.1.3", "Concrete frames", "m³", 2, "3.1")
        self._add_item("3.1.4", "Timber frames", "m²", 2, "3.1")
        
        # 3.2 Upper Floors
        self._add_item("3.2", "Upper floors", "", 1, "3")
        self._add_item("3.2.1", "Floor structure", "m²", 2, "3.2")
        self._add_item("3.2.2", "Balconies", "m²", 2, "3.2")
        
        # 3.3 Roof
        self._add_item("3.3", "Roof", "", 1, "3")
        self._add_item("3.3.1", "Roof structure", "m²", 2, "3.3")
        self._add_item("3.3.2", "Roof coverings", "m²", 2, "3.3")
        self._add_item("3.3.3", "Roof drainage", "m", 2, "3.3")
        self._add_item("3.3.4", "Roof lights/lanterns", "nr", 2, "3.3")
        
        # 3.4 Stairs and Ramps
        self._add_item("3.4", "Stairs and ramps", "", 1, "3")
        self._add_item("3.4.1", "Stair structures", "nr", 2, "3.4")
        self._add_item("3.4.2", "Stair balustrades/handrails", "m", 2, "3.4")
        self._add_item("3.4.3", "Ramps", "m²", 2, "3.4")
        
        # 3.5 External Walls
        self._add_item("3.5", "External walls", "", 1, "3")
        self._add_item("3.5.1", "External walls", "m²", 2, "3.5")
        self._add_item("3.5.2", "External windows", "m²", 2, "3.5")
        self._add_item("3.5.3", "External doors", "nr", 2, "3.5")
        
        # 3.6 Internal Walls and Partitions
        self._add_item("3.6", "Internal walls and partitions", "", 1, "3")
        self._add_item("3.6.1", "Walls and partitions", "m²", 2, "3.6")
        self._add_item("3.6.2", "Balustrades and handrails", "m", 2, "3.6")
        self._add_item("3.6.3", "Movable room dividers", "m²", 2, "3.6")
        self._add_item("3.6.4", "Internal doors", "nr", 2, "3.6")
        
        # Group 4: Internal Finishes
        self._add_section("4", "INTERNAL FINISHES", 1)
        self._add_item("4.1", "Wall finishes", "m²", 1, "4")
        self._add_item("4.2", "Floor finishes", "m²", 1, "4")
        self._add_item("4.3", "Ceiling finishes", "m²", 1, "4")
        
        # Group 5: Services
        self._add_section("5", "SERVICES", 1)
        
        # 5.1 Sanitary Installations
        self._add_item("5.1", "Sanitary installations", "nr", 1, "5")
        
        # 5.2 Services Equipment
        self._add_item("5.2", "Services equipment", "Item", 1, "5")
        
        # 5.3 Disposal Installations
        self._add_item("5.3", "Disposal installations", "m", 1, "5")
        
        # 5.4 Water Installations
        self._add_item("5.4", "Water installations", "m", 1, "5")
        
        # 5.5 Heat Source
        self._add_item("5.5", "Heat source", "nr", 1, "5")
        
        # 5.6 Space Heating and Air Conditioning
        self._add_item("5.6", "Space heating and air conditioning", "m²", 1, "5")
        
        # 5.7 Ventilation
        self._add_item("5.7", "Ventilation", "m²", 1, "5")
        
        # 5.8 Electrical Installations
        self._add_item("5.8", "Electrical installations", "nr", 1, "5")
        
        # 5.9 Fuel Installations
        self._add_item("5.9", "Fuel installations", "m", 1, "5")
        
        # 5.10 Lift and Conveyor Installations
        self._add_item("5.10", "Lift and conveyor installations", "nr", 1, "5")
        
        # 5.11 Fire and Lightning Protection
        self._add_item("5.11", "Fire and lightning protection", "nr", 1, "5")
        
        # 5.12 Communication, Security and Control Systems
        self._add_item("5.12", "Communication, security and control systems", "nr", 1, "5")
        
        # 5.13 Specialist Installations
        self._add_item("5.13", "Specialist installations", "Item", 1, "5")
        
        # 5.14 Builder's Work in Connection with Services
        self._add_item("5.14", "Builder's work in connection with services", "Item", 1, "5")
        
        # Group 6: External Works
        self._add_section("6", "EXTERNAL WORKS", 1)
        self._add_item("6.1", "Site preparation works", "m²", 1, "6")
        self._add_item("6.2", "Roads, paths, pavings and surfacing", "m²", 1, "6")
        self._add_item("6.3", "Soft landscaping", "m²", 1, "6")
        self._add_item("6.4", "Fencing, railings and walls", "m", 1, "6")
        self._add_item("6.5", "External fixtures", "nr", 1, "6")
        self._add_item("6.6", "External drainage", "m", 1, "6")
        self._add_item("6.7", "External services", "m", 1, "6")
        self._add_item("6.8", "Minor building works and ancillary buildings", "nr", 1, "6")
    
    def _add_section(self, code: str, description: str, level: int):
        """Add a section header"""
        item = NRM2Item(
            code=code,
            description=description,
            unit="",
            measurement_rules="Section header",
            level=level
        )
        self.items[code] = item
    
    def _add_item(self, code: str, description: str, unit: str, level: int, parent_code: str):
        """Add a measurement item"""
        item = NRM2Item(
            code=code,
            description=description,
            unit=unit,
            measurement_rules=f"Measured in {unit}",
            level=level,
            parent_code=parent_code
        )
        self.items[code] = item
    
    def get_item(self, code: str) -> Optional[NRM2Item]:
        """Get item by code"""
        return self.items.get(code)
    
    def search_items(self, keyword: str) -> List[NRM2Item]:
        """Search items by keyword in description"""
        keyword_lower = keyword.lower()
        return [
            item for item in self.items.values()
            if keyword_lower in item.description.lower()
        ]
    
    def get_hierarchy(self, code: str) -> List[NRM2Item]:
        """Get full hierarchy path for an item"""
        item = self.get_item(code)
        if not item:
            return []
        
        hierarchy = [item]
        while item.parent_code:
            item = self.get_item(item.parent_code)
            if item:
                hierarchy.insert(0, item)
            else:
                break
        
        return hierarchy
    
    def get_children(self, code: str) -> List[NRM2Item]:
        """Get all child items of a parent"""
        return [
            item for item in self.items.values()
            if item.parent_code == code
        ]
    
    def get_all_groups(self) -> List[NRM2Item]:
        """Get all top-level groups"""
        return [item for item in self.items.values() if item.level == 1]
    
    def format_item_description(self, item: NRM2Item) -> str:
        """Format item description with code"""
        return f"{item.code} - {item.description} ({item.unit})"
