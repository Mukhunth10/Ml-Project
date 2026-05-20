"""
CESMM4 Standard - Civil Engineering Standard Method of Measurement, 4th Edition
Used for civil engineering projects in UK
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class CESMM4Item:
    """Represents a CESMM4 measurement item"""
    code: str
    description: str
    unit: str
    class_code: str  # Class A-Z


class CESMM4Standard:
    """
    CESMM4 (Civil Engineering Standard Method of Measurement, 4th Edition)
    For civil engineering and infrastructure projects
    """
    
    # Main work classes
    WORK_CLASSES = {
        'A': 'General items',
        'B': 'Ground investigation',
        'C': 'Geotechnical and other specialist processes',
        'D': 'Demolition and site clearance',
        'E': 'Earthworks',
        'F': 'In situ concrete',
        'G': 'Concrete ancillaries',
        'H': 'Precast concrete',
        'I': 'Pipework - pipes',
        'J': 'Pipework - fittings and valves',
        'K': 'Pipework - manholes and pipework ancillaries',
        'L': 'Pipework - supports and protection, ancillaries to laying',
        'M': 'Structural metalwork',
        'N': 'Miscellaneous metalwork',
        'O': 'Timber',
        'P': 'Piles',
        'Q': 'Piling ancillaries',
        'R': 'Roads and pavings',
        'S': 'Rail track',
        'T': 'Tunnels',
        'U': 'Brickwork, blockwork and masonry',
        'V': 'Painting',
        'W': 'Waterproofing',
        'X': 'Miscellaneous work',
        'Y': 'Sewer and water main renovation and ancillary works',
        'Z': 'Simple building works incidental to civil engineering works'
    }
    
    def __init__(self):
        self.items: Dict[str, CESMM4Item] = {}
        self._initialize_common_items()
    
    def _initialize_common_items(self):
        """Initialize commonly used CESMM4 items"""
        # Class E - Earthworks
        self._add_item("E424", "Excavation, material other than topsoil, rock or artificial hard material", "m³", "E")
        self._add_item("E522", "Filling, selected excavated material", "m³", "E")
        
        # Class F - In situ concrete
        self._add_item("F622", "Reinforced concrete, grade C30", "m³", "F")
        
        # Class I - Pipework
        self._add_item("I112", "Clay pipes, nominal bore 150mm", "m", "I")
        
        # Class R - Roads and pavings
        self._add_item("R631", "Sub-base, Type 1 granular material", "m³", "R")
        self._add_item("R716", "Binder course, 60mm thick", "m²", "R")
    
    def _add_item(self, code: str, description: str, unit: str, class_code: str):
        """Add a CESMM4 item"""
        item = CESMM4Item(
            code=code,
            description=description,
            unit=unit,
            class_code=class_code
        )
        self.items[code] = item
    
    def get_item(self, code: str) -> Optional[CESMM4Item]:
        """Get item by code"""
        return self.items.get(code)
    
    def get_class_name(self, class_code: str) -> str:
        """Get work class name"""
        return self.WORK_CLASSES.get(class_code, "Unknown")
    
    def search_by_class(self, class_code: str) -> List[CESMM4Item]:
        """Get all items in a work class"""
        return [item for item in self.items.values() if item.class_code == class_code]
