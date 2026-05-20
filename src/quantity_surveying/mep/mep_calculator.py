"""
MEP Calculator - Calculate quantities for MEP systems
"""
from typing import Dict, List
from .mep_categories import MEPElement, MEPDiscipline


class MEPCalculator:
    """Calculate quantities and costs for MEP elements"""
    
    def __init__(self):
        self.elements: Dict[str, MEPElement] = {}
        self.waste_factors = {
            'cables': 1.05,  # 5% waste
            'pipework': 1.10,  # 10% waste
            'ductwork': 1.15,  # 15% waste
            'fittings': 1.02,  # 2% waste
        }
    
    def add_element(self, element: MEPElement):
        """Add MEP element"""
        self.elements[element.element_id] = element
    
    def calculate_cable_quantities(
        self, 
        cable_size: str,
        route_length: float,
        circuits: int = 1,
        include_waste: bool = True
    ) -> Dict:
        """
        Calculate cable quantities
        
        Args:
            cable_size: Cable size (e.g., "2.5mm²", "4mm²")
            route_length: Length of cable route in meters
            circuits: Number of circuits
            include_waste: Include waste factor
            
        Returns:
            Calculation dictionary
        """
        base_length = route_length * circuits
        
        if include_waste:
            total_length = base_length * self.waste_factors['cables']
        else:
            total_length = base_length
        
        return {
            'cable_size': cable_size,
            'route_length': route_length,
            'circuits': circuits,
            'base_length': base_length,
            'waste_factor': self.waste_factors['cables'] if include_waste else 1.0,
            'total_length': total_length,
            'unit': 'm'
        }
    
    def calculate_pipework_quantities(
        self,
        pipe_size: str,
        route_length: float,
        fittings_allowance: float = 0.1,
        include_waste: bool = True
    ) -> Dict:
        """
        Calculate pipework quantities
        
        Args:
            pipe_size: Pipe size (e.g., "15mm", "22mm", "50mm")
            route_length: Length of pipe route
            fittings_allowance: Additional length for fittings (10% default)
            include_waste: Include waste factor
            
        Returns:
            Calculation dictionary
        """
        base_length = route_length * (1 + fittings_allowance)
        
        if include_waste:
            total_length = base_length * self.waste_factors['pipework']
        else:
            total_length = base_length
        
        return {
            'pipe_size': pipe_size,
            'route_length': route_length,
            'fittings_allowance': fittings_allowance,
            'base_length': base_length,
            'waste_factor': self.waste_factors['pipework'] if include_waste else 1.0,
            'total_length': total_length,
            'unit': 'm'
        }
    
    def calculate_ductwork_quantities(
        self,
        duct_size: str,
        route_length: float,
        fittings_factor: float = 0.15,
        include_waste: bool = True
    ) -> Dict:
        """
        Calculate ductwork quantities
        
        Args:
            duct_size: Duct size (e.g., "300x200mm", "200mm dia")
            route_length: Length of duct route
            fittings_factor: Additional for fittings (15% default)
            include_waste: Include waste factor
            
        Returns:
            Calculation dictionary
        """
        base_length = route_length * (1 + fittings_factor)
        
        if include_waste:
            total_length = base_length * self.waste_factors['ductwork']
        else:
            total_length = base_length
        
        return {
            'duct_size': duct_size,
            'route_length': route_length,
            'fittings_factor': fittings_factor,
            'base_length': base_length,
            'waste_factor': self.waste_factors['ductwork'] if include_waste else 1.0,
            'total_length': total_length,
            'unit': 'm'
        }
    
    def calculate_insulation_area(
        self,
        pipe_diameter: float,  # in mm
        pipe_length: float,  # in m
        insulation_thickness: float = 25  # in mm
    ) -> Dict:
        """
        Calculate insulation surface area
        
        Args:
            pipe_diameter: Pipe outer diameter in mm
            pipe_length: Pipe length in meters
            insulation_thickness: Insulation thickness in mm
            
        Returns:
            Calculation dictionary
        """
        import math
        
        # Calculate outer diameter after insulation
        insulated_diameter = pipe_diameter + (2 * insulation_thickness)
        
        # Calculate surface area (πDL)
        area = (math.pi * insulated_diameter / 1000) * pipe_length
        
        return {
            'pipe_diameter': pipe_diameter,
            'pipe_length': pipe_length,
            'insulation_thickness': insulation_thickness,
            'insulated_diameter': insulated_diameter,
            'insulation_area': area,
            'unit': 'm²'
        }
    
    def calculate_power_load(
        self,
        equipment_list: List[Dict]
    ) -> Dict:
        """
        Calculate total power load
        
        Args:
            equipment_list: List of equipment with power ratings
            Format: [{'name': 'AHU-01', 'power_kw': 15.0, 'quantity': 2}]
            
        Returns:
            Power load summary
        """
        total_connected_load = 0.0
        diversity_factor = 0.7  # Typical diversity factor
        
        equipment_details = []
        
        for equipment in equipment_list:
            name = equipment.get('name', 'Unknown')
            power = equipment.get('power_kw', 0.0)
            qty = equipment.get('quantity', 1)
            
            connected_load = power * qty
            total_connected_load += connected_load
            
            equipment_details.append({
                'name': name,
                'power_kw': power,
                'quantity': qty,
                'connected_load_kw': connected_load
            })
        
        design_load = total_connected_load * diversity_factor
        
        # Recommend cable/breaker sizing (simplified)
        voltage = 400  # 3-phase
        design_current = (design_load * 1000) / (voltage * 1.732 * 0.9)  # √3 * pf
        
        return {
            'equipment_details': equipment_details,
            'total_connected_load_kw': total_connected_load,
            'diversity_factor': diversity_factor,
            'design_load_kw': design_load,
            'estimated_current_a': design_current,
            'voltage': voltage
        }
    
    def calculate_cooling_load(
        self,
        area: float,  # m²
        cooling_load_per_m2: float = 100,  # W/m²
        safety_factor: float = 1.15
    ) -> Dict:
        """
        Calculate cooling load (simplified)
        
        Args:
            area: Floor area in m²
            cooling_load_per_m2: Cooling load per m² (W/m²)
            safety_factor: Safety factor
            
        Returns:
            Cooling load calculation
        """
        base_load_w = area * cooling_load_per_m2
        design_load_w = base_load_w * safety_factor
        design_load_kw = design_load_w / 1000
        
        # Convert to tons of refrigeration (1 ton = 3.517 kW)
        tons_refrigeration = design_load_kw / 3.517
        
        return {
            'area_m2': area,
            'cooling_load_per_m2': cooling_load_per_m2,
            'base_load_w': base_load_w,
            'safety_factor': safety_factor,
            'design_load_w': design_load_w,
            'design_load_kw': design_load_kw,
            'tons_refrigeration': tons_refrigeration
        }
    
    def calculate_heating_load(
        self,
        volume: float,  # m³
        temp_difference: float = 21,  # °C (outside to inside)
        u_value: float = 0.25,  # W/m²K
        surface_area: float = None  # m²
    ) -> Dict:
        """
        Calculate heating load (simplified)
        
        Args:
            volume: Room volume in m³
            temp_difference: Temperature difference
            u_value: Overall U-value of building fabric
            surface_area: Surface area exposed to outside
            
        Returns:
            Heating load calculation
        """
        if surface_area is None:
            # Estimate surface area from volume (rough approximation)
            surface_area = volume ** (2/3) * 6
        
        # Heat loss = U × A × ΔT
        heat_loss_w = u_value * surface_area * temp_difference
        
        # Add ventilation heat loss (simplified - 0.33 W/m³K)
        ventilation_loss_w = 0.33 * volume * temp_difference
        
        total_heat_loss_w = heat_loss_w + ventilation_loss_w
        total_heat_loss_kw = total_heat_loss_w / 1000
        
        return {
            'volume_m3': volume,
            'surface_area_m2': surface_area,
            'temp_difference_c': temp_difference,
            'u_value': u_value,
            'fabric_heat_loss_w': heat_loss_w,
            'ventilation_heat_loss_w': ventilation_loss_w,
            'total_heat_loss_w': total_heat_loss_w,
            'total_heat_loss_kw': total_heat_loss_kw
        }
    
    def calculate_water_supply_sizing(
        self,
        fixture_units: float,
        system_type: str = "flush_valve"  # or "flush_tank"
    ) -> Dict:
        """
        Calculate water supply pipe sizing based on fixture units
        
        Args:
            fixture_units: Total fixture units
            system_type: "flush_valve" or "flush_tank"
            
        Returns:
            Recommended pipe sizing
        """
        # Hunter's curve (simplified)
        if system_type == "flush_valve":
            flow_rate_lps = 0.3 * (fixture_units ** 0.5)
        else:
            flow_rate_lps = 0.2 * (fixture_units ** 0.5)
        
        # Recommend pipe size based on flow rate
        # Velocity should be < 2 m/s for noise control
        if flow_rate_lps <= 0.5:
            pipe_size = "15mm"
        elif flow_rate_lps <= 1.0:
            pipe_size = "22mm"
        elif flow_rate_lps <= 2.0:
            pipe_size = "28mm"
        elif flow_rate_lps <= 3.5:
            pipe_size = "35mm"
        elif flow_rate_lps <= 5.0:
            pipe_size = "42mm"
        else:
            pipe_size = "50mm+"
        
        return {
            'fixture_units': fixture_units,
            'system_type': system_type,
            'flow_rate_lps': flow_rate_lps,
            'flow_rate_lpm': flow_rate_lps * 60,
            'recommended_pipe_size': pipe_size
        }
    
    def aggregate_by_discipline(self) -> Dict:
        """Aggregate all elements by discipline"""
        aggregated = {}
        
        for discipline in MEPDiscipline:
            discipline_elements = [
                e for e in self.elements.values() 
                if e.discipline == discipline
            ]
            
            if discipline_elements:
                aggregated[discipline.value] = {
                    'count': len(discipline_elements),
                    'total_cost': sum(e.total_cost for e in discipline_elements),
                    'elements': discipline_elements
                }
        
        return aggregated
    
    def generate_mep_summary(self) -> Dict:
        """Generate comprehensive MEP summary"""
        summary = {
            'total_elements': len(self.elements),
            'by_discipline': {},
            'total_cost': 0.0
        }
        
        aggregated = self.aggregate_by_discipline()
        
        for discipline, data in aggregated.items():
            summary['by_discipline'][discipline] = {
                'count': data['count'],
                'total_cost': data['total_cost']
            }
            summary['total_cost'] += data['total_cost']
        
        return summary
