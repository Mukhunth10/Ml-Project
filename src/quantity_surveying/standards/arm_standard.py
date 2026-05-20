"""
ARM Standard - Agreed Rules of Measurement (Ireland)
Used in Ireland for building measurement
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ARMItem:
    """Represents an ARM measurement item"""
    code: str
    description: str
    unit: str
    section: str


class ARMStandard:
    """
    ARM (Agreed Rules of Measurement)
    Standard for building measurement in Ireland
    """
    
    SECTIONS = {
        'A': 'Preliminaries',
        'B': 'Demolitions and alterations',
        'C': 'Excavation and earthwork',
        'D': 'Concrete work',
        'E': 'Brickwork and blockwork',
        'F': 'Masonry',
        'G': 'Structural steelwork',
        'H': 'Metalwork',
        'I': 'Timber work',
        'J': 'Waterproofing',
        'K': 'Linings and partitions',
        'L': 'Windows, doors and glazing',
        'M': 'Surface finishes',
        'N': 'Furniture and equipment',
        'P': 'Plumbing and mechanical services',
        'Q': 'Electrical services',
        'R': 'External works'
    }
    
    def __init__(self):
        self.items: Dict[str, ARMItem] = {}
        self._initialize_common_items()
    
    def _initialize_common_items(self):
        """Initialize commonly used ARM items"""
        # Section C - Excavation
        self._add_item("C10", "Excavating", "m³", "C")
        self._add_item("C20", "Filling", "m³", "C")
        
        # Section D - Concrete work
        self._add_item("D10", "In situ concrete", "m³", "D")
        self._add_item("D20", "Formwork", "m²", "D")
        self._add_item("D30", "Reinforcement", "tonne", "D")
        
        # Section E - Brickwork
        self._add_item("E10", "Brick walling", "m²", "E")
        self._add_item("E20", "Block walling", "m²", "E")
        
        # Section M - Finishes
        self._add_item("M10", "Plaster and render", "m²", "M")
        self._add_item("M20", "Tiling", "m²", "M")
        self._add_item("M40", "Painting", "m²", "M")
        self._add_item("M50", "Floor finishes", "m²", "M")
    
    def _add_item(self, code: str, description: str, unit: str, section: str):
        """Add an ARM item"""
        item = ARMItem(
            code=code,
            description=description,
            unit=unit,
            section=section
        )
        self.items[code] = item
    
    def get_item(self, code: str) -> Optional[ARMItem]:
        """Get item by code"""
        return self.items.get(code)
    
    def get_section_name(self, section_code: str) -> str:
        """Get section name"""
        return self.SECTIONS.get(section_code, "Unknown")
    
    def search_by_section(self, section_code: str) -> List[ARMItem]:
        """Get all items in a section"""
        return [item for item in self.items.values() if item.section == section_code]
