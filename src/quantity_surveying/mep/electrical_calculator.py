"""
Electrical System Calculator
"""
from typing import Dict, List
import math


class ElectricalCalculator:
    """Specialized calculator for electrical systems"""
    
    def __init__(self):
        self.voltage_3ph = 400  # 3-phase voltage
        self.voltage_1ph = 230  # single phase voltage
        self.power_factor = 0.9  # typical power factor
    
    def calculate_cable_size(
        self,
        load_kw: float,
        length_m: float,
        voltage_drop_percent: float = 3.0,
        phases: int = 3,
        installation_method: str = "tray"
    ) -> Dict:
        """
        Calculate required cable size
        
        Args:
            load_kw: Load in kW
            length_m: Cable length in meters
            voltage_drop_percent: Max voltage drop %
            phases: 1 or 3 phase
            installation_method: Installation method
            
        Returns:
            Cable sizing recommendation
        """
        # Calculate current
        if phases == 3:
            current = (load_kw * 1000) / (self.voltage_3ph * math.sqrt(3) * self.power_factor)
            voltage = self.voltage_3ph
        else:
            current = (load_kw * 1000) / (self.voltage_1ph * self.power_factor)
            voltage = self.voltage_1ph
        
        # Calculate max voltage drop
        max_voltage_drop = voltage * (voltage_drop_percent / 100)
        
        # Calculate minimum cable size based on voltage drop
        # Simplified calculation
        if phases == 3:
            min_csa = (2 * 0.018 * load_kw * 1000 * length_m) / max_voltage_drop
        else:
            min_csa = (2 * 0.018 * load_kw * 1000 * length_m) / max_voltage_drop
        
        # Standard cable sizes (mm²)
        standard_sizes = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
        
        # Select next standard size
        recommended_size = None
        for size in standard_sizes:
            if size >= min_csa:
                recommended_size = size
                break
        
        if recommended_size is None:
            recommended_size = standard_sizes[-1]
        
        # Derating factors (simplified)
        derating_factors = {
            'tray': 1.0,
            'conduit': 0.8,
            'buried': 0.9,
            'clipped': 0.95
        }
        
        derating = derating_factors.get(installation_method, 1.0)
        derated_current = current / derating
        
        return {
            'load_kw': load_kw,
            'current_a': current,
            'derated_current_a': derated_current,
            'cable_length_m': length_m,
            'voltage': voltage,
            'phases': phases,
            'power_factor': self.power_factor,
            'voltage_drop_percent': voltage_drop_percent,
            'max_voltage_drop_v': max_voltage_drop,
            'min_csa_mm2': min_csa,
            'recommended_cable_size_mm2': recommended_size,
            'installation_method': installation_method,
            'derating_factor': derating
        }
    
    def calculate_circuit_breaker_rating(
        self,
        load_kw: float,
        phases: int = 3,
        safety_factor: float = 1.25
    ) -> Dict:
        """
        Calculate circuit breaker rating
        
        Args:
            load_kw: Connected load
            phases: 1 or 3
            safety_factor: Safety margin
            
        Returns:
            Breaker rating recommendation
        """
        # Calculate current
        if phases == 3:
            current = (load_kw * 1000) / (self.voltage_3ph * math.sqrt(3) * self.power_factor)
        else:
            current = (load_kw * 1000) / (self.voltage_1ph * self.power_factor)
        
        # Apply safety factor
        design_current = current * safety_factor
        
        # Standard breaker ratings (A)
        standard_ratings = [6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000]
        
        # Select next standard rating
        recommended_rating = None
        for rating in standard_ratings:
            if rating >= design_current:
                recommended_rating = rating
                break
        
        if recommended_rating is None:
            recommended_rating = standard_ratings[-1]
        
        return {
            'load_kw': load_kw,
            'calculated_current_a': current,
            'safety_factor': safety_factor,
            'design_current_a': design_current,
            'recommended_breaker_rating_a': recommended_rating,
            'phases': phases,
            'voltage': self.voltage_3ph if phases == 3 else self.voltage_1ph
        }
    
    def calculate_lighting_load(
        self,
        area_m2: float,
        lux_level: float = 300,
        luminaire_efficacy: float = 100  # lm/W
    ) -> Dict:
        """
        Calculate lighting load
        
        Args:
            area_m2: Floor area
            lux_level: Required illuminance level
            luminaire_efficacy: Luminaire efficacy (lumens per watt)
            
        Returns:
            Lighting calculation
        """
        # Utilization factor (typical for offices)
        utilization_factor = 0.6
        maintenance_factor = 0.8
        
        # Calculate required lumens
        required_lumens = (area_m2 * lux_level) / (utilization_factor * maintenance_factor)
        
        # Calculate power
        power_w = required_lumens / luminaire_efficacy
        power_kw = power_w / 1000
        
        # Calculate number of fixtures (assuming 40W LED panels)
        fixture_power = 40  # W
        num_fixtures = math.ceil(power_w / fixture_power)
        
        return {
            'area_m2': area_m2,
            'lux_level': lux_level,
            'utilization_factor': utilization_factor,
            'maintenance_factor': maintenance_factor,
            'required_lumens': required_lumens,
            'luminaire_efficacy_lm_w': luminaire_efficacy,
            'total_power_w': power_w,
            'total_power_kw': power_kw,
            'estimated_fixtures': num_fixtures,
            'fixture_power_w': fixture_power
        }
    
    def calculate_earthing_requirements(
        self,
        fault_current_ka: float,
        fault_duration_s: float = 0.5
    ) -> Dict:
        """
        Calculate earthing conductor size
        
        Args:
            fault_current_ka: Fault current in kA
            fault_duration_s: Fault clearance time
            
        Returns:
            Earthing requirements
        """
        # Using adiabatic equation: A = (I × √t) / k
        # k = 143 for copper (typical)
        k = 143
        
        fault_current_a = fault_current_ka * 1000
        
        min_csa = (fault_current_a * math.sqrt(fault_duration_s)) / k
        
        # Standard earth conductor sizes
        standard_sizes = [16, 25, 35, 50, 70, 95, 120, 150, 185, 240]
        
        recommended_size = None
        for size in standard_sizes:
            if size >= min_csa:
                recommended_size = size
                break
        
        if recommended_size is None:
            recommended_size = standard_sizes[-1]
        
        return {
            'fault_current_ka': fault_current_ka,
            'fault_duration_s': fault_duration_s,
            'k_factor': k,
            'min_csa_mm2': min_csa,
            'recommended_earth_conductor_mm2': recommended_size
        }
    
    def calculate_transformer_sizing(
        self,
        connected_load_kva: float,
        diversity_factor: float = 0.7,
        future_growth: float = 0.2,
        spare_capacity: float = 0.1
    ) -> Dict:
        """
        Calculate transformer sizing
        
        Args:
            connected_load_kva: Total connected load
            diversity_factor: Load diversity factor
            future_growth: Future growth allowance
            spare_capacity: Spare capacity margin
            
        Returns:
            Transformer sizing
        """
        # Calculate design load
        simultaneous_load = connected_load_kva * diversity_factor
        future_load = simultaneous_load * (1 + future_growth)
        design_load = future_load * (1 + spare_capacity)
        
        # Standard transformer sizes (kVA)
        standard_sizes = [100, 200, 315, 500, 630, 800, 1000, 1250, 1600, 2000, 2500]
        
        recommended_size = None
        for size in standard_sizes:
            if size >= design_load:
                recommended_size = size
                break
        
        if recommended_size is None:
            recommended_size = standard_sizes[-1]
        
        return {
            'connected_load_kva': connected_load_kva,
            'diversity_factor': diversity_factor,
            'simultaneous_load_kva': simultaneous_load,
            'future_growth': future_growth,
            'future_load_kva': future_load,
            'spare_capacity': spare_capacity,
            'design_load_kva': design_load,
            'recommended_transformer_kva': recommended_size,
            'loading_percent': (design_load / recommended_size) * 100 if recommended_size else 0
        }
    
    def calculate_generator_sizing(
        self,
        essential_load_kw: float,
        starting_load_kw: float = 0,
        power_factor: float = 0.8
    ) -> Dict:
        """
        Calculate standby generator sizing
        
        Args:
            essential_load_kw: Essential running load
            starting_load_kw: Additional starting load (motors, etc.)
            power_factor: Power factor
            
        Returns:
            Generator sizing
        """
        # Convert to kVA
        running_kva = essential_load_kw / power_factor
        
        # Peak load during starting
        peak_kva = (essential_load_kw + starting_load_kw) / power_factor
        
        # Add safety margin (20%)
        design_kva = peak_kva * 1.2
        
        # Standard generator sizes (kVA)
        standard_sizes = [20, 30, 45, 60, 80, 100, 125, 150, 200, 250, 300, 400, 500, 625, 750, 1000]
        
        recommended_size = None
        for size in standard_sizes:
            if size >= design_kva:
                recommended_size = size
                break
        
        if recommended_size is None:
            recommended_size = standard_sizes[-1]
        
        return {
            'essential_load_kw': essential_load_kw,
            'starting_load_kw': starting_load_kw,
            'power_factor': power_factor,
            'running_load_kva': running_kva,
            'peak_load_kva': peak_kva,
            'design_load_kva': design_kva,
            'recommended_generator_kva': recommended_size,
            'loading_percent': (design_kva / recommended_size) * 100 if recommended_size else 0
        }
    
    def calculate_ups_backup_time(
        self,
        ups_rating_kva: float,
        load_kw: float,
        battery_capacity_ah: float,
        battery_voltage: float = 48
    ) -> Dict:
        """
        Calculate UPS backup time
        
        Args:
            ups_rating_kva: UPS rating
            load_kw: Connected load
            battery_capacity_ah: Battery capacity
            battery_voltage: Battery voltage
            
        Returns:
            Backup time calculation
        """
        # Battery energy (Wh)
        battery_energy_wh = battery_capacity_ah * battery_voltage
        
        # Usable energy (80% depth of discharge)
        usable_energy_wh = battery_energy_wh * 0.8
        
        # UPS efficiency (typical 90%)
        efficiency = 0.9
        
        # Available energy
        available_energy_wh = usable_energy_wh * efficiency
        
        # Backup time
        load_w = load_kw * 1000
        backup_time_hours = available_energy_wh / load_w
        backup_time_minutes = backup_time_hours * 60
        
        return {
            'ups_rating_kva': ups_rating_kva,
            'load_kw': load_kw,
            'load_percent': (load_kw / ups_rating_kva) * 100,
            'battery_capacity_ah': battery_capacity_ah,
            'battery_voltage_v': battery_voltage,
            'battery_energy_wh': battery_energy_wh,
            'usable_energy_wh': usable_energy_wh,
            'efficiency': efficiency,
            'available_energy_wh': available_energy_wh,
            'backup_time_hours': backup_time_hours,
            'backup_time_minutes': backup_time_minutes
        }
