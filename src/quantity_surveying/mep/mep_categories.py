"""
MEP Categories and Element Definitions
"""
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional


class MEPDiscipline(Enum):
    """MEP disciplines"""
    ELECTRICAL = "electrical"
    MECHANICAL = "mechanical"
    PLUMBING = "plumbing"
    FIRE_PROTECTION = "fire_protection"
    BMS = "bms"  # Building Management System
    TELECOM = "telecom"
    SECURITY = "security"


class ElectricalCategory(Enum):
    """Electrical system categories"""
    # Power Distribution
    MAIN_SWITCHBOARD = "main_switchboard"
    SUB_DISTRIBUTION_BOARD = "sub_distribution_board"
    FINAL_DISTRIBUTION_BOARD = "final_distribution_board"
    TRANSFORMERS = "transformers"
    GENERATORS = "generators"
    UPS_SYSTEMS = "ups_systems"
    
    # Cable Management
    CABLES_POWER = "cables_power"
    CABLES_DATA = "cables_data"
    CABLE_TRAY = "cable_tray"
    CABLE_LADDER = "cable_ladder"
    CONDUIT = "conduit"
    TRUNKING = "trunking"
    
    # Lighting
    LIGHTING_FIXTURES_INTERNAL = "lighting_fixtures_internal"
    LIGHTING_FIXTURES_EXTERNAL = "lighting_fixtures_external"
    EMERGENCY_LIGHTING = "emergency_lighting"
    LED_STRIPS = "led_strips"
    
    # Power Outlets
    SOCKETS_SINGLE = "sockets_single"
    SOCKETS_DOUBLE = "sockets_double"
    DEDICATED_OUTLETS = "dedicated_outlets"
    FLOOR_BOXES = "floor_boxes"
    
    # Earthing & Protection
    EARTHING_SYSTEM = "earthing_system"
    LIGHTNING_PROTECTION = "lightning_protection"
    SURGE_PROTECTION = "surge_protection"
    
    # Special Systems
    FIRE_ALARM = "fire_alarm"
    SMOKE_DETECTORS = "smoke_detectors"
    HEAT_DETECTORS = "heat_detectors"


class MechanicalCategory(Enum):
    """Mechanical/HVAC system categories"""
    # Air Handling
    AHU = "ahu"  # Air Handling Units
    FCU = "fcu"  # Fan Coil Units
    VAV_BOXES = "vav_boxes"  # Variable Air Volume
    EXHAUST_FANS = "exhaust_fans"
    SUPPLY_FANS = "supply_fans"
    VENTILATION_UNITS = "ventilation_units"
    
    # Ductwork
    DUCTWORK_SUPPLY = "ductwork_supply"
    DUCTWORK_RETURN = "ductwork_return"
    DUCTWORK_EXTRACT = "ductwork_extract"
    DUCTWORK_FLEXIBLE = "ductwork_flexible"
    DUCT_FITTINGS = "duct_fittings"
    FIRE_DAMPERS = "fire_dampers"
    VOLUME_CONTROL_DAMPERS = "volume_control_dampers"
    
    # Diffusers & Grilles
    SUPPLY_DIFFUSERS = "supply_diffusers"
    RETURN_GRILLES = "return_grilles"
    EXTRACT_GRILLES = "extract_grilles"
    LINEAR_DIFFUSERS = "linear_diffusers"
    
    # Heating Systems
    BOILERS = "boilers"
    RADIATORS = "radiators"
    UNDERFLOOR_HEATING = "underfloor_heating"
    HEATING_MANIFOLDS = "heating_manifolds"
    
    # Cooling Systems
    CHILLERS = "chillers"
    COOLING_TOWERS = "cooling_towers"
    SPLIT_AC_UNITS = "split_ac_units"
    VRF_SYSTEMS = "vrf_systems"  # Variable Refrigerant Flow
    
    # Pipework (Heating/Cooling)
    CHILLED_WATER_PIPEWORK = "chilled_water_pipework"
    HEATING_WATER_PIPEWORK = "heating_water_pipework"
    CONDENSATE_PIPEWORK = "condensate_pipework"
    REFRIGERANT_PIPEWORK = "refrigerant_pipework"
    
    # Insulation
    DUCT_INSULATION = "duct_insulation"
    PIPE_INSULATION = "pipe_insulation"
    
    # Controls
    THERMOSTATS = "thermostats"
    SENSORS = "sensors"
    ACTUATORS = "actuators"


class PlumbingCategory(Enum):
    """Plumbing and drainage system categories"""
    # Water Supply
    COLD_WATER_PIPEWORK = "cold_water_pipework"
    HOT_WATER_PIPEWORK = "hot_water_pipework"
    WATER_STORAGE_TANKS = "water_storage_tanks"
    WATER_HEATERS = "water_heaters"
    WATER_PUMPS = "water_pumps"
    PRESSURE_BOOSTING = "pressure_boosting"
    
    # Sanitary Fixtures
    WC_TOILETS = "wc_toilets"
    URINALS = "urinals"
    WASH_HAND_BASINS = "wash_hand_basins"
    SHOWERS = "showers"
    BATHS = "baths"
    BIDETS = "bidets"
    SINKS_KITCHEN = "sinks_kitchen"
    SINKS_CLEANERS = "sinks_cleaners"
    DRINKING_FOUNTAINS = "drinking_fountains"
    
    # Drainage
    SOIL_WASTE_PIPEWORK = "soil_waste_pipework"
    WASTE_PIPEWORK = "waste_pipework"
    RAINWATER_PIPEWORK = "rainwater_pipework"
    FLOOR_DRAINS = "floor_drains"
    GULLIES = "gullies"
    INSPECTION_CHAMBERS = "inspection_chambers"
    MANHOLE_COVERS = "manhole_covers"
    
    # Drainage Above Ground
    SOIL_STACK = "soil_stack"
    WASTE_STACK = "waste_stack"
    VENT_STACK = "vent_stack"
    AAV = "aav"  # Air Admittance Valves
    
    # Drainage Below Ground
    UNDERGROUND_DRAINAGE = "underground_drainage"
    SEPTIC_TANKS = "septic_tanks"
    PUMPING_STATIONS = "pumping_stations"
    INTERCEPTORS = "interceptors"
    
    # Specialized
    MEDICAL_GAS_PIPEWORK = "medical_gas_pipework"
    LABORATORY_SERVICES = "laboratory_services"
    COMPRESSED_AIR = "compressed_air"


class FireProtectionCategory(Enum):
    """Fire protection system categories"""
    SPRINKLER_HEADS = "sprinkler_heads"
    SPRINKLER_PIPEWORK = "sprinkler_pipework"
    SPRINKLER_VALVES = "sprinkler_valves"
    FIRE_HOSE_REELS = "fire_hose_reels"
    FIRE_HYDRANTS = "fire_hydrants"
    FIRE_PUMPS = "fire_pumps"
    FIRE_WATER_TANKS = "fire_water_tanks"
    WET_RISER = "wet_riser"
    DRY_RISER = "dry_riser"
    FOAM_SYSTEMS = "foam_systems"
    GAS_SUPPRESSION = "gas_suppression"


@dataclass
class MEPElement:
    """Represents an MEP element"""
    element_id: str
    discipline: MEPDiscipline
    category: str  # One of the category enums
    name: str
    description: str
    
    # Technical specifications
    size: Optional[str] = None  # e.g., "100mm", "32A", "10kW"
    capacity: Optional[float] = None
    rating: Optional[str] = None
    
    # Installation details
    quantity: float = 0.0
    unit: str = "nr"
    length: Optional[float] = None  # For pipework, cables, ductwork
    area: Optional[float] = None  # For insulation, diffusers
    
    # Costing
    material_cost: float = 0.0
    labor_cost: float = 0.0
    total_cost: float = 0.0
    
    # Location
    floor_level: Optional[str] = None
    zone: Optional[str] = None
    room: Optional[str] = None
    
    # Standards and specs
    standard_reference: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    
    # Installation
    mounting_height: Optional[float] = None
    installation_notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'element_id': self.element_id,
            'discipline': self.discipline.value,
            'category': self.category,
            'name': self.name,
            'description': self.description,
            'size': self.size,
            'capacity': self.capacity,
            'rating': self.rating,
            'quantity': self.quantity,
            'unit': self.unit,
            'length': self.length,
            'area': self.area,
            'material_cost': self.material_cost,
            'labor_cost': self.labor_cost,
            'total_cost': self.total_cost,
            'floor_level': self.floor_level,
            'zone': self.zone,
            'room': self.room,
            'standard_reference': self.standard_reference,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'mounting_height': self.mounting_height,
            'installation_notes': self.installation_notes
        }


class MEPCategories:
    """Manage MEP categories and color schemes"""
    
    # MEP-specific color scheme
    MEP_COLORS = {
        # Electrical - Yellows and Oranges
        'Main Switchboard': '#FFD700',
        'Distribution Boards': '#FFA500',
        'Power Cables': '#FF8C00',
        'Data Cables': '#00CED1',
        'Cable Tray': '#DAA520',
        'Conduit': '#B8860B',
        'Lighting Fixtures': '#FFFF00',
        'Emergency Lighting': '#FF6347',
        'Power Outlets': '#FFD93D',
        'Fire Alarm': '#FF0000',
        'Earthing': '#8B4513',
        
        # Mechanical - Blues and Greens
        'AHU': '#4169E1',
        'FCU': '#5F9EA0',
        'Ductwork Supply': '#87CEEB',
        'Ductwork Return': '#B0C4DE',
        'Ductwork Extract': '#708090',
        'Diffusers': '#ADD8E6',
        'Grilles': '#AFEEEE',
        'Chillers': '#00BFFF',
        'Boilers': '#FF4500',
        'Radiators': '#FF6347',
        'VRF Systems': '#4682B4',
        'Fire Dampers': '#DC143C',
        
        # Plumbing - Blues and Browns
        'Cold Water': '#0000FF',
        'Hot Water': '#FF0000',
        'Heating Water': '#FF6347',
        'Chilled Water': '#00BFFF',
        'Soil & Waste': '#8B4513',
        'Rainwater': '#4682B4',
        'WC Toilets': '#D3D3D3',
        'Wash Basins': '#E0E0E0',
        'Showers': '#B0E0E6',
        'Floor Drains': '#696969',
        'Water Tanks': '#1E90FF',
        
        # Fire Protection - Reds
        'Sprinklers': '#DC143C',
        'Fire Hose Reels': '#B22222',
        'Fire Hydrants': '#8B0000',
        'Wet Riser': '#CD5C5C',
        
        # BMS & Controls
        'BMS': '#9370DB',
        'Sensors': '#BA55D3',
        'Actuators': '#8A2BE2',
        'Thermostats': '#9932CC'
    }
    
    @staticmethod
    def get_electrical_categories() -> List[str]:
        """Get all electrical categories"""
        return [cat.value for cat in ElectricalCategory]
    
    @staticmethod
    def get_mechanical_categories() -> List[str]:
        """Get all mechanical categories"""
        return [cat.value for cat in MechanicalCategory]
    
    @staticmethod
    def get_plumbing_categories() -> List[str]:
        """Get all plumbing categories"""
        return [cat.value for cat in PlumbingCategory]
    
    @staticmethod
    def get_fire_protection_categories() -> List[str]:
        """Get all fire protection categories"""
        return [cat.value for cat in FireProtectionCategory]
    
    @staticmethod
    def get_all_categories() -> Dict[str, List[str]]:
        """Get all MEP categories organized by discipline"""
        return {
            'Electrical': MEPCategories.get_electrical_categories(),
            'Mechanical': MEPCategories.get_mechanical_categories(),
            'Plumbing': MEPCategories.get_plumbing_categories(),
            'Fire Protection': MEPCategories.get_fire_protection_categories()
        }
    
    @staticmethod
    def get_color_for_category(category: str) -> str:
        """Get color for MEP category"""
        # Try direct match first
        for key, color in MEPCategories.MEP_COLORS.items():
            if key.lower() == category.lower() or category.lower() in key.lower():
                return color
        
        # Default colors by discipline keywords
        category_lower = category.lower()
        if any(word in category_lower for word in ['cable', 'electrical', 'power', 'lighting', 'socket']):
            return '#FFD700'
        elif any(word in category_lower for word in ['duct', 'hvac', 'air', 'ventilation', 'ahu', 'fcu']):
            return '#87CEEB'
        elif any(word in category_lower for word in ['water', 'plumbing', 'drainage', 'pipe']):
            return '#0000FF'
        elif any(word in category_lower for word in ['fire', 'sprinkler']):
            return '#DC143C'
        
        return '#808080'  # Default grey
    
    @staticmethod
    def get_units_for_category(category: str) -> str:
        """Get typical unit for category"""
        category_lower = category.lower()
        
        # Linear measurements
        if any(word in category_lower for word in ['cable', 'pipe', 'duct', 'conduit', 'tray', 'ladder']):
            return 'm'
        
        # Area measurements
        if any(word in category_lower for word in ['insulation', 'diffuser', 'grille']):
            return 'm²'
        
        # Count items
        if any(word in category_lower for word in ['fixture', 'outlet', 'socket', 'board', 'panel', 
                                                      'unit', 'detector', 'sensor', 'valve', 'damper',
                                                      'wc', 'basin', 'shower', 'tank']):
            return 'nr'
        
        # Default
        return 'nr'
