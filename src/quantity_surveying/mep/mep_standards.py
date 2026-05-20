"""
MEP Standards for UK and Ireland
"""
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class MEPStandardItem:
    """MEP standard item"""
    code: str
    description: str
    unit: str
    discipline: str
    category: str
    notes: str = ""


class MEPStandards:
    """
    MEP measurement standards based on:
    - NRM2 Section 5: Services
    - CIBSE guides
    - BS standards
    """
    
    def __init__(self):
        self.items: Dict[str, MEPStandardItem] = {}
        self._initialize_electrical_standards()
        self._initialize_mechanical_standards()
        self._initialize_plumbing_standards()
        self._initialize_fire_protection_standards()
    
    def _initialize_electrical_standards(self):
        """Initialize electrical standards from NRM2 Section 5"""
        
        # 5.8 Electrical Installations
        electrical_items = [
            # Power Distribution
            ("5.8.1.1", "Main switchboard, incoming supply", "nr", "Electrical", "Power Distribution"),
            ("5.8.1.2", "Main distribution board, up to 400A", "nr", "Electrical", "Power Distribution"),
            ("5.8.1.3", "Sub-distribution board, up to 125A", "nr", "Electrical", "Power Distribution"),
            ("5.8.1.4", "Final distribution board, single phase", "nr", "Electrical", "Power Distribution"),
            ("5.8.1.5", "Three phase distribution board", "nr", "Electrical", "Power Distribution"),
            
            # Transformers and Generators
            ("5.8.2.1", "Transformer, oil filled, 500kVA", "nr", "Electrical", "Transformers"),
            ("5.8.2.2", "Transformer, cast resin, 250kVA", "nr", "Electrical", "Transformers"),
            ("5.8.2.3", "Diesel generator, 100kVA", "nr", "Electrical", "Generators"),
            ("5.8.2.4", "UPS system, 50kVA", "nr", "Electrical", "UPS"),
            
            # Cables - Power
            ("5.8.3.1", "Cable, PVC/SWA, 2.5mm² 3-core", "m", "Electrical", "Cables"),
            ("5.8.3.2", "Cable, PVC/SWA, 4mm² 3-core", "m", "Electrical", "Cables"),
            ("5.8.3.3", "Cable, PVC/SWA, 6mm² 3-core", "m", "Electrical", "Cables"),
            ("5.8.3.4", "Cable, PVC/SWA, 10mm² 3-core", "m", "Electrical", "Cables"),
            ("5.8.3.5", "Cable, PVC/SWA, 16mm² 3-core", "m", "Electrical", "Cables"),
            ("5.8.3.6", "Cable, PVC/SWA, 25mm² 4-core", "m", "Electrical", "Cables"),
            ("5.8.3.7", "Cable, PVC/SWA, 35mm² 4-core", "m", "Electrical", "Cables"),
            ("5.8.3.8", "Cable, PVC/SWA, 50mm² 4-core", "m", "Electrical", "Cables"),
            ("5.8.3.9", "Cable, PVC/SWA, 70mm² 4-core", "m", "Electrical", "Cables"),
            ("5.8.3.10", "Cable, PVC/SWA, 95mm² 4-core", "m", "Electrical", "Cables"),
            
            # Cables - Data
            ("5.8.3.20", "Cable, Cat 6 UTP data cable", "m", "Electrical", "Data Cables"),
            ("5.8.3.21", "Cable, Cat 6A STP data cable", "m", "Electrical", "Data Cables"),
            ("5.8.3.22", "Cable, Fibre optic, 6 core", "m", "Electrical", "Data Cables"),
            ("5.8.3.23", "Cable, Fire alarm, 2-core", "m", "Electrical", "Fire Alarm"),
            
            # Cable Management
            ("5.8.4.1", "Cable tray, ladder type, 300mm wide", "m", "Electrical", "Cable Tray"),
            ("5.8.4.2", "Cable tray, ladder type, 450mm wide", "m", "Electrical", "Cable Tray"),
            ("5.8.4.3", "Cable tray, perforated, 300mm wide", "m", "Electrical", "Cable Tray"),
            ("5.8.4.4", "Cable tray, perforated, 450mm wide", "m", "Electrical", "Cable Tray"),
            ("5.8.4.5", "Conduit, steel heavy gauge, 20mm", "m", "Electrical", "Conduit"),
            ("5.8.4.6", "Conduit, steel heavy gauge, 25mm", "m", "Electrical", "Conduit"),
            ("5.8.4.7", "Conduit, steel heavy gauge, 32mm", "m", "Electrical", "Conduit"),
            ("5.8.4.8", "Trunking, PVC, 100x50mm", "m", "Electrical", "Trunking"),
            ("5.8.4.9", "Trunking, PVC, 100x100mm", "m", "Electrical", "Trunking"),
            
            # Lighting
            ("5.8.5.1", "Luminaire, LED panel, 600x600mm, 40W", "nr", "Electrical", "Lighting"),
            ("5.8.5.2", "Luminaire, LED panel, 1200x600mm, 60W", "nr", "Electrical", "Lighting"),
            ("5.8.5.3", "Luminaire, LED downlight, 20W", "nr", "Electrical", "Lighting"),
            ("5.8.5.4", "Luminaire, LED bulkhead, 20W", "nr", "Electrical", "Lighting"),
            ("5.8.5.5", "Luminaire, LED high bay, 150W", "nr", "Electrical", "Lighting"),
            ("5.8.5.6", "Emergency lighting, LED, maintained", "nr", "Electrical", "Emergency Lighting"),
            ("5.8.5.7", "Emergency lighting, LED, non-maintained", "nr", "Electrical", "Emergency Lighting"),
            ("5.8.5.8", "Exit sign, LED, self-contained", "nr", "Electrical", "Emergency Lighting"),
            
            # Power Outlets
            ("5.8.6.1", "Socket outlet, 13A single, switched", "nr", "Electrical", "Outlets"),
            ("5.8.6.2", "Socket outlet, 13A double, switched", "nr", "Electrical", "Outlets"),
            ("5.8.6.3", "Socket outlet, 13A twin, floor box", "nr", "Electrical", "Outlets"),
            ("5.8.6.4", "Socket outlet, 16A single phase", "nr", "Electrical", "Outlets"),
            ("5.8.6.5", "Socket outlet, 32A three phase", "nr", "Electrical", "Outlets"),
            
            # Earthing and Protection
            ("5.8.7.1", "Earth rod, copper bonded, 1.2m", "nr", "Electrical", "Earthing"),
            ("5.8.7.2", "Lightning protection air terminal", "nr", "Electrical", "Lightning Protection"),
            ("5.8.7.3", "Surge protection device, Type 2", "nr", "Electrical", "Protection"),
            
            # Fire Alarm
            ("5.8.8.1", "Fire alarm panel, 8 zone", "nr", "Electrical", "Fire Alarm"),
            ("5.8.8.2", "Smoke detector, optical", "nr", "Electrical", "Fire Alarm"),
            ("5.8.8.3", "Heat detector", "nr", "Electrical", "Fire Alarm"),
            ("5.8.8.4", "Manual call point", "nr", "Electrical", "Fire Alarm"),
            ("5.8.8.5", "Sounder, visual alarm device", "nr", "Electrical", "Fire Alarm"),
        ]
        
        for code, desc, unit, discipline, category in electrical_items:
            self.items[code] = MEPStandardItem(code, desc, unit, discipline, category)
    
    def _initialize_mechanical_standards(self):
        """Initialize mechanical/HVAC standards"""
        
        mechanical_items = [
            # 5.6 Space Heating and Air Conditioning
            # Air Handling Units
            ("5.6.1.1", "Air handling unit, 5000 l/s", "nr", "Mechanical", "AHU"),
            ("5.6.1.2", "Air handling unit, 10000 l/s", "nr", "Mechanical", "AHU"),
            ("5.6.1.3", "Fan coil unit, 2-pipe, 2.5kW", "nr", "Mechanical", "FCU"),
            ("5.6.1.4", "Fan coil unit, 4-pipe, 5kW", "nr", "Mechanical", "FCU"),
            ("5.6.1.5", "VAV box, pressure independent", "nr", "Mechanical", "VAV"),
            
            # Fans
            ("5.6.2.1", "Extract fan, axial, 500 l/s", "nr", "Mechanical", "Fans"),
            ("5.6.2.2", "Extract fan, centrifugal, 1000 l/s", "nr", "Mechanical", "Fans"),
            ("5.6.2.3", "Supply fan, centrifugal, 2000 l/s", "nr", "Mechanical", "Fans"),
            
            # Ductwork - Rectangular
            ("5.6.3.1", "Ductwork, galvanized steel, 300x200mm", "m", "Mechanical", "Ductwork"),
            ("5.6.3.2", "Ductwork, galvanized steel, 400x300mm", "m", "Mechanical", "Ductwork"),
            ("5.6.3.3", "Ductwork, galvanized steel, 600x400mm", "m", "Mechanical", "Ductwork"),
            ("5.6.3.4", "Ductwork, galvanized steel, 800x600mm", "m", "Mechanical", "Ductwork"),
            
            # Ductwork - Circular
            ("5.6.3.10", "Ductwork, spiral, galv., 100mm dia", "m", "Mechanical", "Ductwork"),
            ("5.6.3.11", "Ductwork, spiral, galv., 150mm dia", "m", "Mechanical", "Ductwork"),
            ("5.6.3.12", "Ductwork, spiral, galv., 200mm dia", "m", "Mechanical", "Ductwork"),
            ("5.6.3.13", "Ductwork, spiral, galv., 250mm dia", "m", "Mechanical", "Ductwork"),
            ("5.6.3.14", "Ductwork, spiral, galv., 315mm dia", "m", "Mechanical", "Ductwork"),
            
            # Flexible Ductwork
            ("5.6.3.20", "Flexible ductwork, insulated, 150mm", "m", "Mechanical", "Flexible Duct"),
            ("5.6.3.21", "Flexible ductwork, insulated, 200mm", "m", "Mechanical", "Flexible Duct"),
            
            # Dampers
            ("5.6.4.1", "Fire damper, motorized, 300x200mm", "nr", "Mechanical", "Fire Dampers"),
            ("5.6.4.2", "Fire damper, motorized, 600x400mm", "nr", "Mechanical", "Fire Dampers"),
            ("5.6.4.3", "Volume control damper, 300x200mm", "nr", "Mechanical", "VCD"),
            
            # Diffusers and Grilles
            ("5.6.5.1", "Ceiling diffuser, 4-way, 300x300mm", "nr", "Mechanical", "Diffusers"),
            ("5.6.5.2", "Ceiling diffuser, 4-way, 600x600mm", "nr", "Mechanical", "Diffusers"),
            ("5.6.5.3", "Linear diffuser, 1200mm", "nr", "Mechanical", "Diffusers"),
            ("5.6.5.4", "Return grille, 600x600mm", "nr", "Mechanical", "Grilles"),
            ("5.6.5.5", "Extract grille, 300x300mm", "nr", "Mechanical", "Grilles"),
            
            # Chillers and Cooling
            ("5.6.6.1", "Chiller, air cooled, 100kW", "nr", "Mechanical", "Chillers"),
            ("5.6.6.2", "Chiller, water cooled, 200kW", "nr", "Mechanical", "Chillers"),
            ("5.6.6.3", "Cooling tower, 300kW", "nr", "Mechanical", "Cooling Towers"),
            ("5.6.6.4", "Split AC unit, 5kW cooling", "nr", "Mechanical", "Split AC"),
            ("5.6.6.5", "VRF outdoor unit, 30kW", "nr", "Mechanical", "VRF"),
            ("5.6.6.6", "VRF indoor unit, cassette, 5kW", "nr", "Mechanical", "VRF"),
            
            # 5.5 Heat Source
            # Boilers
            ("5.5.1.1", "Boiler, gas fired, floor standing, 100kW", "nr", "Mechanical", "Boilers"),
            ("5.5.1.2", "Boiler, gas fired, wall mounted, 30kW", "nr", "Mechanical", "Boilers"),
            ("5.5.1.3", "Boiler, condensing, 50kW", "nr", "Mechanical", "Boilers"),
            
            # Radiators
            ("5.5.2.1", "Radiator, steel panel, 1200x600mm", "nr", "Mechanical", "Radiators"),
            ("5.5.2.2", "Radiator, steel panel, 1600x600mm", "nr", "Mechanical", "Radiators"),
            ("5.5.2.3", "Radiator, LST, 1200x600mm", "nr", "Mechanical", "Radiators"),
            
            # Pipework - Heating/Cooling
            ("5.5.3.1", "Pipework, steel, welded, 50mm", "m", "Mechanical", "Pipework"),
            ("5.5.3.2", "Pipework, steel, welded, 80mm", "m", "Mechanical", "Pipework"),
            ("5.5.3.3", "Pipework, steel, welded, 100mm", "m", "Mechanical", "Pipework"),
            ("5.5.3.4", "Pipework, copper, 15mm", "m", "Mechanical", "Pipework"),
            ("5.5.3.5", "Pipework, copper, 22mm", "m", "Mechanical", "Pipework"),
            ("5.5.3.6", "Pipework, copper, 28mm", "m", "Mechanical", "Pipework"),
            
            # Insulation
            ("5.6.7.1", "Duct insulation, 25mm thick", "m²", "Mechanical", "Insulation"),
            ("5.6.7.2", "Pipe insulation, 25mm thick, 15mm bore", "m", "Mechanical", "Insulation"),
            ("5.6.7.3", "Pipe insulation, 25mm thick, 22mm bore", "m", "Mechanical", "Insulation"),
            ("5.6.7.4", "Pipe insulation, 32mm thick, 50mm bore", "m", "Mechanical", "Insulation"),
        ]
        
        for code, desc, unit, discipline, category in mechanical_items:
            self.items[code] = MEPStandardItem(code, desc, unit, discipline, category)
    
    def _initialize_plumbing_standards(self):
        """Initialize plumbing standards"""
        
        plumbing_items = [
            # 5.1 Sanitary Installations
            # WCs
            ("5.1.1.1", "WC suite, close coupled, floor mounted", "nr", "Plumbing", "WCs"),
            ("5.1.1.2", "WC suite, wall hung", "nr", "Plumbing", "WCs"),
            ("5.1.1.3", "WC suite, accessible, with grab rails", "nr", "Plumbing", "WCs"),
            ("5.1.1.4", "Urinal, wall hung, stainless steel", "nr", "Plumbing", "Urinals"),
            ("5.1.1.5", "Urinal, bowl type, vitreous china", "nr", "Plumbing", "Urinals"),
            
            # Wash Basins
            ("5.1.2.1", "Wash hand basin, wall hung, 550mm", "nr", "Plumbing", "Basins"),
            ("5.1.2.2", "Wash hand basin, pedestal, 600mm", "nr", "Plumbing", "Basins"),
            ("5.1.2.3", "Wash hand basin, countertop, 450mm", "nr", "Plumbing", "Basins"),
            
            # Showers and Baths
            ("5.1.3.1", "Shower tray, acrylic, 900x900mm", "nr", "Plumbing", "Showers"),
            ("5.1.3.2", "Shower enclosure, glass, 900x900mm", "nr", "Plumbing", "Showers"),
            ("5.1.3.3", "Shower mixer valve, thermostatic", "nr", "Plumbing", "Showers"),
            ("5.1.3.4", "Bath, acrylic, 1700x700mm", "nr", "Plumbing", "Baths"),
            
            # Sinks
            ("5.1.4.1", "Sink, stainless steel, single bowl", "nr", "Plumbing", "Sinks"),
            ("5.1.4.2", "Sink, stainless steel, double bowl", "nr", "Plumbing", "Sinks"),
            ("5.1.4.3", "Cleaners sink, Belfast, 600x450mm", "nr", "Plumbing", "Sinks"),
            
            # 5.4 Water Installations
            # Cold Water Pipework
            ("5.4.1.1", "Pipework, copper, 15mm, cold water", "m", "Plumbing", "Cold Water"),
            ("5.4.1.2", "Pipework, copper, 22mm, cold water", "m", "Plumbing", "Cold Water"),
            ("5.4.1.3", "Pipework, copper, 28mm, cold water", "m", "Plumbing", "Cold Water"),
            ("5.4.1.4", "Pipework, copper, 35mm, cold water", "m", "Plumbing", "Cold Water"),
            ("5.4.1.5", "Pipework, copper, 42mm, cold water", "m", "Plumbing", "Cold Water"),
            
            # Hot Water Pipework
            ("5.4.2.1", "Pipework, copper, 15mm, hot water", "m", "Plumbing", "Hot Water"),
            ("5.4.2.2", "Pipework, copper, 22mm, hot water", "m", "Plumbing", "Hot Water"),
            ("5.4.2.3", "Pipework, copper, 28mm, hot water", "m", "Plumbing", "Hot Water"),
            
            # Water Storage and Heating
            ("5.4.3.1", "Cold water storage tank, 500L", "nr", "Plumbing", "Water Tanks"),
            ("5.4.3.2", "Cold water storage tank, 1000L", "nr", "Plumbing", "Water Tanks"),
            ("5.4.3.3", "Hot water cylinder, indirect, 250L", "nr", "Plumbing", "Water Heaters"),
            ("5.4.3.4", "Hot water cylinder, indirect, 500L", "nr", "Plumbing", "Water Heaters"),
            ("5.4.3.5", "Water heater, instantaneous, 10L", "nr", "Plumbing", "Water Heaters"),
            
            # Pumps
            ("5.4.4.1", "Pump, booster, 0.5kW", "nr", "Plumbing", "Pumps"),
            ("5.4.4.2", "Pump, circulation, 0.3kW", "nr", "Plumbing", "Pumps"),
            ("5.4.4.3", "Pump set, pressure boosting, twin", "nr", "Plumbing", "Pumps"),
            
            # 5.3 Disposal Installations
            # Soil and Waste
            ("5.3.1.1", "Soil pipe, PVC-U, 110mm", "m", "Plumbing", "Soil & Waste"),
            ("5.3.1.2", "Waste pipe, PVC-U, 32mm", "m", "Plumbing", "Soil & Waste"),
            ("5.3.1.3", "Waste pipe, PVC-U, 40mm", "m", "Plumbing", "Soil & Waste"),
            ("5.3.1.4", "Waste pipe, PVC-U, 50mm", "m", "Plumbing", "Soil & Waste"),
            
            # Drainage
            ("5.3.2.1", "Floor drain, stainless steel, 150mm", "nr", "Plumbing", "Drainage"),
            ("5.3.2.2", "Gully, trapped, 110mm", "nr", "Plumbing", "Drainage"),
            ("5.3.2.3", "Inspection chamber, 450mm dia", "nr", "Plumbing", "Drainage"),
            ("5.3.2.4", "Manhole cover, D400, 600x450mm", "nr", "Plumbing", "Drainage"),
            
            # Underground Drainage
            ("5.3.3.1", "Drainage pipe, PVC-U, 110mm, below ground", "m", "Plumbing", "Underground"),
            ("5.3.3.2", "Drainage pipe, PVC-U, 160mm, below ground", "m", "Plumbing", "Underground"),
            ("5.3.3.3", "Manhole, brick, 1200mm deep", "nr", "Plumbing", "Underground"),
        ]
        
        for code, desc, unit, discipline, category in plumbing_items:
            self.items[code] = MEPStandardItem(code, desc, unit, discipline, category)
    
    def _initialize_fire_protection_standards(self):
        """Initialize fire protection standards"""
        
        fire_items = [
            # 5.11 Fire and Lightning Protection
            ("5.11.1.1", "Sprinkler head, pendant, 68°C", "nr", "Fire", "Sprinklers"),
            ("5.11.1.2", "Sprinkler head, recessed, 68°C", "nr", "Fire", "Sprinklers"),
            ("5.11.1.3", "Sprinkler head, sidewall, 68°C", "nr", "Fire", "Sprinklers"),
            ("5.11.1.4", "Sprinkler pipework, steel, 25mm", "m", "Fire", "Sprinklers"),
            ("5.11.1.5", "Sprinkler pipework, steel, 50mm", "m", "Fire", "Sprinklers"),
            ("5.11.1.6", "Sprinkler pipework, steel, 100mm", "m", "Fire", "Sprinklers"),
            ("5.11.1.7", "Alarm valve set, wet pipe", "nr", "Fire", "Sprinklers"),
            
            ("5.11.2.1", "Fire hose reel, 30m", "nr", "Fire", "Hose Reels"),
            ("5.11.2.2", "Fire hydrant, landing valve", "nr", "Fire", "Hydrants"),
            ("5.11.2.3", "Fire pump, diesel, 500 l/min", "nr", "Fire", "Pumps"),
            ("5.11.2.4", "Fire water tank, 50m³", "nr", "Fire", "Tanks"),
            
            ("5.11.3.1", "Wet riser, 100mm", "m", "Fire", "Risers"),
            ("5.11.3.2", "Dry riser, 100mm", "m", "Fire", "Risers"),
        ]
        
        for code, desc, unit, discipline, category in fire_items:
            self.items[code] = MEPStandardItem(code, desc, unit, discipline, category)
    
    def get_item(self, code: str) -> Optional[MEPStandardItem]:
        """Get standard item by code"""
        return self.items.get(code)
    
    def search_by_discipline(self, discipline: str) -> List[MEPStandardItem]:
        """Search items by discipline"""
        return [item for item in self.items.values() if item.discipline.lower() == discipline.lower()]
    
    def search_by_keyword(self, keyword: str) -> List[MEPStandardItem]:
        """Search items by keyword"""
        keyword_lower = keyword.lower()
        return [
            item for item in self.items.values()
            if keyword_lower in item.description.lower() or keyword_lower in item.category.lower()
        ]
    
    def get_all_by_category(self, category: str) -> List[MEPStandardItem]:
        """Get all items in a category"""
        return [item for item in self.items.values() if item.category == category]
    
    def get_electrical_items(self) -> List[MEPStandardItem]:
        """Get all electrical items"""
        return self.search_by_discipline("Electrical")
    
    def get_mechanical_items(self) -> List[MEPStandardItem]:
        """Get all mechanical items"""
        return self.search_by_discipline("Mechanical")
    
    def get_plumbing_items(self) -> List[MEPStandardItem]:
        """Get all plumbing items"""
        return self.search_by_discipline("Plumbing")
    
    def get_fire_protection_items(self) -> List[MEPStandardItem]:
        """Get all fire protection items"""
        return self.search_by_discipline("Fire")
