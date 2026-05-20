"""
Plumbing System Calculator
"""
from typing import Dict, List
import math


class PlumbingCalculator:
    """Specialized calculator for plumbing systems"""
    
    def __init__(self):
        # Fixture units (UK standard)
        self.fixture_units = {
            'wc': 2.0,
            'urinal': 0.5,
            'wash_basin': 1.0,
            'shower': 3.0,
            'bath': 3.0,
            'kitchen_sink': 3.0,
            'washing_machine': 3.0,
            'dishwasher': 2.0
        }
    
    def calculate_fixture_units(self, fixtures: List[Dict]) -> Dict:
        """
        Calculate total fixture units
        
        Args:
            fixtures: List of fixtures with types and quantities
            Format: [{'type': 'wc', 'quantity': 10}, ...]
            
        Returns:
            Fixture units calculation
        """
        total_fu = 0.0
        fixture_breakdown = []
        
        for fixture in fixtures:
            fixture_type = fixture.get('type', '').lower()
            quantity = fixture.get('quantity', 0)
            
            fu_per_fixture = self.fixture_units.get(fixture_type, 1.0)
            fu_total = fu_per_fixture * quantity
            total_fu += fu_total
            
            fixture_breakdown.append({
                'type': fixture_type,
                'quantity': quantity,
                'fu_per_fixture': fu_per_fixture,
                'total_fu': fu_total
            })
        
        return {
            'fixture_breakdown': fixture_breakdown,
            'total_fixture_units': total_fu
        }
    
    def calculate_water_demand(
        self,
        fixture_units: float,
        system_type: str = "flush_tank"  # or "flush_valve"
    ) -> Dict:
        """
        Calculate water demand using Hunter's curve
        
        Args:
            fixture_units: Total fixture units
            system_type: flush_tank or flush_valve
            
        Returns:
            Water demand calculation
        """
        # Hunter's curve (simplified)
        if system_type == "flush_valve":
            flow_rate_lps = 0.3 * math.sqrt(fixture_units)
        else:
            flow_rate_lps = 0.2 * math.sqrt(fixture_units)
        
        flow_rate_lpm = flow_rate_lps * 60
        flow_rate_m3h = flow_rate_lps * 3.6
        
        return {
            'fixture_units': fixture_units,
            'system_type': system_type,
            'flow_rate_lps': flow_rate_lps,
            'flow_rate_lpm': flow_rate_lpm,
            'flow_rate_m3h': flow_rate_m3h
        }
    
    def calculate_pipe_sizing(
        self,
        flow_rate_lps: float,
        max_velocity_ms: float = 2.0,
        pipe_material: str = "copper"
    ) -> Dict:
        """
        Calculate required pipe size
        
        Args:
            flow_rate_lps: Flow rate in liters per second
            max_velocity_ms: Maximum velocity
            pipe_material: Pipe material
            
        Returns:
            Pipe sizing recommendation
        """
        # Convert flow rate to m³/s
        flow_rate_m3s = flow_rate_lps / 1000
        
        # Calculate required area: A = Q / v
        required_area_m2 = flow_rate_m3s / max_velocity_ms
        
        # Calculate diameter: d = √(4A/π)
        required_diameter_m = math.sqrt((4 * required_area_m2) / math.pi)
        required_diameter_mm = required_diameter_m * 1000
        
        # Standard pipe sizes for copper (mm) - nominal bore
        standard_sizes = {
            'copper': [15, 22, 28, 35, 42, 54, 67, 76, 108],
            'steel': [15, 20, 25, 32, 40, 50, 65, 80, 100, 125, 150],
            'pvc': [32, 40, 50, 63, 75, 90, 110, 125, 160, 200]
        }
        
        sizes = standard_sizes.get(pipe_material, standard_sizes['copper'])
        
        # Select next standard size
        recommended_size = None
        for size in sizes:
            if size >= required_diameter_mm:
                recommended_size = size
                break
        
        if recommended_size is None:
            recommended_size = sizes[-1]
        
        # Calculate actual velocity with recommended size
        actual_diameter_m = recommended_size / 1000
        actual_area_m2 = math.pi * (actual_diameter_m / 2) ** 2
        actual_velocity_ms = flow_rate_m3s / actual_area_m2
        
        return {
            'flow_rate_lps': flow_rate_lps,
            'max_velocity_ms': max_velocity_ms,
            'required_diameter_mm': required_diameter_mm,
            'pipe_material': pipe_material,
            'recommended_size_mm': recommended_size,
            'actual_velocity_ms': actual_velocity_ms
        }
    
    def calculate_hot_water_storage(
        self,
        occupants: int = None,
        dwelling_type: str = "residential",  # or "commercial"
        usage_liters_per_person: float = 45
    ) -> Dict:
        """
        Calculate hot water storage capacity
        
        Args:
            occupants: Number of occupants
            dwelling_type: Type of building
            usage_liters_per_person: Daily usage per person
            
        Returns:
            Storage capacity recommendation
        """
        if occupants:
            daily_usage = occupants * usage_liters_per_person
        else:
            # Default values
            if dwelling_type == "residential":
                daily_usage = 200  # liters
            else:
                daily_usage = 500  # liters
        
        # Storage capacity (typically 1.5-2.0 times peak hourly demand)
        # Peak hour = 25% of daily usage
        peak_hour_usage = daily_usage * 0.25
        storage_capacity = peak_hour_usage * 1.75
        
        # Standard cylinder sizes (liters)
        standard_sizes = [50, 100, 120, 150, 200, 250, 300, 400, 500]
        
        recommended_size = None
        for size in standard_sizes:
            if size >= storage_capacity:
                recommended_size = size
                break
        
        if recommended_size is None:
            recommended_size = standard_sizes[-1]
        
        # Calculate recovery time (assuming 3kW immersion heater)
        heater_power_kw = 3
        temp_rise = 50  # °C (from cold to hot)
        specific_heat = 4.18  # kJ/kg°C
        
        energy_required_kj = recommended_size * specific_heat * temp_rise
        recovery_time_hours = energy_required_kj / (heater_power_kw * 3600)
        
        return {
            'occupants': occupants,
            'dwelling_type': dwelling_type,
            'usage_per_person_l': usage_liters_per_person,
            'daily_usage_l': daily_usage,
            'peak_hour_usage_l': peak_hour_usage,
            'storage_capacity_l': storage_capacity,
            'recommended_cylinder_l': recommended_size,
            'heater_power_kw': heater_power_kw,
            'recovery_time_hours': recovery_time_hours
        }
    
    def calculate_drainage_sizing(
        self,
        fixture_units: float,
        slope_percent: float = 1.0
    ) -> Dict:
        """
        Calculate drainage pipe sizing
        
        Args:
            fixture_units: Total fixture units
            slope_percent: Pipe slope
            
        Returns:
            Drainage pipe sizing
        """
        # Drainage capacity (simplified)
        # Based on fixture units and minimum flow velocity
        
        if fixture_units <= 3:
            pipe_size = 50
        elif fixture_units <= 6:
            pipe_size = 65
        elif fixture_units <= 12:
            pipe_size = 80
        elif fixture_units <= 20:
            pipe_size = 100
        elif fixture_units <= 160:
            pipe_size = 150
        else:
            pipe_size = 200
        
        # Calculate flow capacity
        # Using Manning's equation (simplified)
        n = 0.009  # Manning's coefficient for PVC
        slope = slope_percent / 100
        diameter_m = pipe_size / 1000
        area = math.pi * (diameter_m / 2) ** 2
        hydraulic_radius = diameter_m / 4  # For circular pipe running half full
        
        # v = (1/n) × R^(2/3) × S^(1/2)
        velocity = (1 / n) * (hydraulic_radius ** (2/3)) * (slope ** 0.5)
        flow_capacity_m3s = velocity * area * 0.5  # Half full
        flow_capacity_lps = flow_capacity_m3s * 1000
        
        return {
            'fixture_units': fixture_units,
            'slope_percent': slope_percent,
            'recommended_pipe_size_mm': pipe_size,
            'flow_capacity_lps': flow_capacity_lps,
            'flow_velocity_ms': velocity
        }
    
    def calculate_pump_head(
        self,
        vertical_lift_m: float,
        pipe_length_m: float,
        pipe_size_mm: float,
        flow_rate_lps: float
    ) -> Dict:
        """
        Calculate required pump head
        
        Args:
            vertical_lift_m: Static head
            pipe_length_m: Total pipe length
            pipe_size_mm: Pipe diameter
            flow_rate_lps: Flow rate
            
        Returns:
            Pump head calculation
        """
        # Static head
        static_head_m = vertical_lift_m
        
        # Friction losses (simplified - Hazen-Williams)
        # h = 10.67 × Q^1.852 × L / (C^1.852 × D^4.87)
        # C = 130 for copper, Q in m³/s, D in m
        
        C = 130  # Hazen-Williams coefficient
        Q = flow_rate_lps / 1000  # m³/s
        D = pipe_size_mm / 1000  # m
        L = pipe_length_m
        
        friction_head_m = 10.67 * (Q ** 1.852) * L / ((C ** 1.852) * (D ** 4.87))
        
        # Minor losses (fittings, valves - assume 20% of friction)
        minor_losses_m = friction_head_m * 0.2
        
        # Pressure at outlet (assume 1 bar = 10m head)
        outlet_pressure_m = 10
        
        # Total head
        total_head_m = static_head_m + friction_head_m + minor_losses_m + outlet_pressure_m
        
        # Add safety margin (10%)
        design_head_m = total_head_m * 1.1
        
        # Calculate power required
        # P (kW) = ρ × g × Q × H / (η × 1000)
        density = 1000  # kg/m³
        gravity = 9.81  # m/s²
        efficiency = 0.7  # typical pump efficiency
        
        power_kw = (density * gravity * Q * design_head_m) / (efficiency * 1000)
        
        return {
            'static_head_m': static_head_m,
            'friction_head_m': friction_head_m,
            'minor_losses_m': minor_losses_m,
            'outlet_pressure_m': outlet_pressure_m,
            'total_head_m': total_head_m,
            'design_head_m': design_head_m,
            'required_power_kw': power_kw,
            'flow_rate_lps': flow_rate_lps,
            'pipe_size_mm': pipe_size_mm
        }
    
    def calculate_rainwater_drainage(
        self,
        roof_area_m2: float,
        rainfall_intensity_mm_hr: float = 75,  # UK typical
        gutter_type: str = "half_round"
    ) -> Dict:
        """
        Calculate rainwater drainage requirements
        
        Args:
            roof_area_m2: Roof area
            rainfall_intensity_mm_hr: Rainfall intensity
            gutter_type: Type of gutter
            
        Returns:
            Rainwater drainage sizing
        """
        # Calculate flow rate
        # Q (L/s) = (A × I) / 3600
        flow_rate_lps = (roof_area_m2 * (rainfall_intensity_mm_hr / 1000)) / 3600
        
        # Gutter capacity (simplified)
        # Based on BS EN 12056
        gutter_capacities = {
            'half_round': {100: 0.78, 115: 1.11, 125: 1.37, 150: 2.16},
            'square': {100: 1.11, 115: 1.52, 125: 1.89}
        }
        
        capacities = gutter_capacities.get(gutter_type, gutter_capacities['half_round'])
        
        # Find suitable gutter size
        recommended_gutter_size = None
        for size, capacity in sorted(capacities.items()):
            if capacity >= flow_rate_lps:
                recommended_gutter_size = size
                break
        
        if recommended_gutter_size is None:
            recommended_gutter_size = max(capacities.keys())
        
        # Downpipe sizing
        # Typical: 1 downpipe per 50m² of roof
        num_downpipes = math.ceil(roof_area_m2 / 50)
        
        # Standard downpipe sizes
        if flow_rate_lps <= 1.0:
            downpipe_size = 50
        elif flow_rate_lps <= 2.3:
            downpipe_size = 68
        else:
            downpipe_size = 100
        
        return {
            'roof_area_m2': roof_area_m2,
            'rainfall_intensity_mm_hr': rainfall_intensity_mm_hr,
            'flow_rate_lps': flow_rate_lps,
            'gutter_type': gutter_type,
            'recommended_gutter_size_mm': recommended_gutter_size,
            'recommended_downpipe_size_mm': downpipe_size,
            'number_of_downpipes': num_downpipes
        }
