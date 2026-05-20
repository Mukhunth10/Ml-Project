"""
HVAC System Calculator
"""
from typing import Dict, List
import math


class HVACCalculator:
    """Specialized calculator for HVAC systems"""
    
    def __init__(self):
        self.air_density = 1.2  # kg/m³ at 20°C
        self.specific_heat_air = 1.005  # kJ/kg·K
    
    def calculate_airflow_requirement(
        self,
        area_m2: float = None,
        volume_m3: float = None,
        occupants: int = None,
        space_type: str = "office"
    ) -> Dict:
        """
        Calculate fresh air requirements
        
        Args:
            area_m2: Floor area
            volume_m3: Room volume
            occupants: Number of occupants
            space_type: Type of space
            
        Returns:
            Airflow calculation
        """
        # Fresh air rates (L/s per person) - UK Building Regulations
        fresh_air_rates = {
            'office': 10,
            'meeting_room': 15,
            'classroom': 8,
            'restaurant': 12,
            'retail': 8,
            'warehouse': 5,
            'gym': 15
        }
        
        fresh_air_per_person = fresh_air_rates.get(space_type, 10)
        
        # If occupants not specified, estimate from area
        if occupants is None and area_m2:
            # Typical occupancy densities (m² per person)
            densities = {
                'office': 10,
                'meeting_room': 2,
                'classroom': 2,
                'restaurant': 1.5,
                'retail': 5,
                'warehouse': 20,
                'gym': 5
            }
            density = densities.get(space_type, 10)
            occupants = math.ceil(area_m2 / density)
        
        # Calculate fresh air requirement
        fresh_air_lps = occupants * fresh_air_per_person if occupants else 0
        fresh_air_m3h = fresh_air_lps * 3.6
        
        # Air changes per hour (if volume provided)
        if volume_m3:
            air_changes_hr = (fresh_air_m3h / volume_m3)
        else:
            air_changes_hr = None
        
        # Total supply air (including recirculation)
        # Typically 4-6 times fresh air for comfort
        supply_air_factor = 5
        total_supply_lps = fresh_air_lps * supply_air_factor
        total_supply_m3h = total_supply_lps * 3.6
        
        return {
            'space_type': space_type,
            'area_m2': area_m2,
            'volume_m3': volume_m3,
            'occupants': occupants,
            'fresh_air_per_person_lps': fresh_air_per_person,
            'fresh_air_lps': fresh_air_lps,
            'fresh_air_m3h': fresh_air_m3h,
            'air_changes_per_hour': air_changes_hr,
            'total_supply_air_lps': total_supply_lps,
            'total_supply_air_m3h': total_supply_m3h
        }
    
    def calculate_cooling_load_detailed(
        self,
        area_m2: float,
        occupants: int,
        lighting_w_m2: float = 12,
        equipment_w_m2: float = 15,
        solar_gain_w_m2: float = 30,
        infiltration_w_m2: float = 10
    ) -> Dict:
        """
        Detailed cooling load calculation
        
        Args:
            area_m2: Floor area
            occupants: Number of occupants
            lighting_w_m2: Lighting load per m²
            equipment_w_m2: Equipment load per m²
            solar_gain_w_m2: Solar heat gain per m²
            infiltration_w_m2: Infiltration/ventilation load per m²
            
        Returns:
            Detailed cooling load breakdown
        """
        # Heat gains
        lighting_load_w = area_m2 * lighting_w_m2
        equipment_load_w = area_m2 * equipment_w_m2
        solar_gain_w = area_m2 * solar_gain_w_m2
        infiltration_w = area_m2 * infiltration_w_m2
        
        # Occupant heat gain (sensible + latent)
        occupant_sensible_w = occupants * 75  # W per person (sensible)
        occupant_latent_w = occupants * 55  # W per person (latent)
        
        # Total sensible heat gain
        total_sensible_w = (lighting_load_w + equipment_load_w + 
                           solar_gain_w + infiltration_w + occupant_sensible_w)
        
        # Total latent heat gain
        total_latent_w = occupant_latent_w
        
        # Total cooling load
        total_cooling_w = total_sensible_w + total_latent_w
        total_cooling_kw = total_cooling_w / 1000
        
        # Add safety factor (10-15%)
        safety_factor = 1.15
        design_cooling_kw = total_cooling_kw * safety_factor
        
        # Convert to tons of refrigeration
        tons_refrigeration = design_cooling_kw / 3.517
        
        # Sensible Heat Ratio
        shr = total_sensible_w / total_cooling_w
        
        return {
            'area_m2': area_m2,
            'occupants': occupants,
            'lighting_load_w': lighting_load_w,
            'equipment_load_w': equipment_load_w,
            'solar_gain_w': solar_gain_w,
            'infiltration_w': infiltration_w,
            'occupant_sensible_w': occupant_sensible_w,
            'occupant_latent_w': occupant_latent_w,
            'total_sensible_w': total_sensible_w,
            'total_latent_w': total_latent_w,
            'total_cooling_w': total_cooling_w,
            'total_cooling_kw': total_cooling_kw,
            'safety_factor': safety_factor,
            'design_cooling_kw': design_cooling_kw,
            'tons_refrigeration': tons_refrigeration,
            'sensible_heat_ratio': shr
        }
    
    def calculate_duct_sizing(
        self,
        airflow_lps: float,
        max_velocity_ms: float = 6.0,
        duct_shape: str = "rectangular"
    ) -> Dict:
        """
        Calculate duct size
        
        Args:
            airflow_lps: Airflow in liters per second
            max_velocity_ms: Maximum air velocity
            duct_shape: rectangular or circular
            
        Returns:
            Duct sizing recommendation
        """
        # Convert to m³/s
        airflow_m3s = airflow_lps / 1000
        
        # Calculate required area
        required_area_m2 = airflow_m3s / max_velocity_ms
        
        if duct_shape == "circular":
            # Calculate diameter
            diameter_m = math.sqrt((4 * required_area_m2) / math.pi)
            diameter_mm = diameter_m * 1000
            
            # Standard circular duct sizes
            standard_sizes = [100, 125, 150, 160, 200, 250, 315, 355, 400, 450, 500, 630, 800, 1000]
            
            recommended_size = None
            for size in standard_sizes:
                if size >= diameter_mm:
                    recommended_size = size
                    break
            
            if recommended_size is None:
                recommended_size = standard_sizes[-1]
            
            # Actual velocity
            actual_area_m2 = math.pi * ((recommended_size / 1000) / 2) ** 2
            actual_velocity_ms = airflow_m3s / actual_area_m2
            
            return {
                'airflow_lps': airflow_lps,
                'max_velocity_ms': max_velocity_ms,
                'duct_shape': duct_shape,
                'required_diameter_mm': diameter_mm,
                'recommended_diameter_mm': recommended_size,
                'actual_velocity_ms': actual_velocity_ms
            }
        
        else:  # rectangular
            # Assume aspect ratio of 2:1 for rectangular ducts
            # A = w × h, and w = 2h
            # A = 2h²
            h = math.sqrt(required_area_m2 / 2)
            w = 2 * h
            
            h_mm = h * 1000
            w_mm = w * 1000
            
            # Round to standard sizes (multiples of 50mm)
            h_std = math.ceil(h_mm / 50) * 50
            w_std = math.ceil(w_mm / 50) * 50
            
            # Keep aspect ratio reasonable (between 1:1 and 4:1)
            if w_std / h_std > 4:
                w_std = h_std * 4
            
            # Actual velocity
            actual_area_m2 = (w_std * h_std) / 1_000_000
            actual_velocity_ms = airflow_m3s / actual_area_m2
            
            return {
                'airflow_lps': airflow_lps,
                'max_velocity_ms': max_velocity_ms,
                'duct_shape': duct_shape,
                'recommended_width_mm': w_std,
                'recommended_height_mm': h_std,
                'actual_velocity_ms': actual_velocity_ms,
                'aspect_ratio': w_std / h_std
            }
    
    def calculate_pressure_drop(
        self,
        airflow_lps: float,
        duct_length_m: float,
        duct_diameter_mm: float = None,
        duct_width_mm: float = None,
        duct_height_mm: float = None,
        roughness: float = 0.09  # mm for galvanized steel
    ) -> Dict:
        """
        Calculate pressure drop in ductwork
        
        Args:
            airflow_lps: Airflow
            duct_length_m: Duct length
            duct_diameter_mm: Diameter for circular duct
            duct_width_mm: Width for rectangular duct
            duct_height_mm: Height for rectangular duct
            roughness: Surface roughness
            
        Returns:
            Pressure drop calculation
        """
        # Convert to m³/s
        airflow_m3s = airflow_lps / 1000
        
        if duct_diameter_mm:
            # Circular duct
            diameter_m = duct_diameter_mm / 1000
            area_m2 = math.pi * (diameter_m / 2) ** 2
            hydraulic_diameter_m = diameter_m
        elif duct_width_mm and duct_height_mm:
            # Rectangular duct
            width_m = duct_width_mm / 1000
            height_m = duct_height_mm / 1000
            area_m2 = width_m * height_m
            # Hydraulic diameter = 4A/P
            perimeter_m = 2 * (width_m + height_m)
            hydraulic_diameter_m = (4 * area_m2) / perimeter_m
        else:
            return {'error': 'Must provide duct dimensions'}
        
        # Calculate velocity
        velocity_ms = airflow_m3s / area_m2
        
        # Simplified pressure drop calculation
        # ΔP (Pa/m) ≈ 0.02 × v² × (1 + ε/D)
        # where ε is roughness, D is hydraulic diameter
        
        roughness_m = roughness / 1000
        friction_factor = 0.02 * (1 + (roughness_m / hydraulic_diameter_m))
        
        # Pressure drop per meter
        pressure_drop_pa_m = friction_factor * velocity_ms ** 2
        
        # Total pressure drop
        total_pressure_drop_pa = pressure_drop_pa_m * duct_length_m
        
        # Add fittings (assume 30% additional)
        fittings_allowance = 0.3
        total_with_fittings_pa = total_pressure_drop_pa * (1 + fittings_allowance)
        
        return {
            'airflow_lps': airflow_lps,
            'duct_length_m': duct_length_m,
            'hydraulic_diameter_m': hydraulic_diameter_m,
            'velocity_ms': velocity_ms,
            'pressure_drop_pa_m': pressure_drop_pa_m,
            'friction_pressure_drop_pa': total_pressure_drop_pa,
            'fittings_allowance': fittings_allowance,
            'total_pressure_drop_pa': total_with_fittings_pa
        }
    
    def calculate_fan_power(
        self,
        airflow_lps: float,
        total_pressure_pa: float,
        fan_efficiency: float = 0.7
    ) -> Dict:
        """
        Calculate fan power requirement
        
        Args:
            airflow_lps: Airflow
            total_pressure_pa: Total system pressure drop
            fan_efficiency: Fan total efficiency
            
        Returns:
            Fan power calculation
        """
        # Convert to m³/s
        airflow_m3s = airflow_lps / 1000
        
        # Fan power (W) = (Q × ΔP) / η
        fan_power_w = (airflow_m3s * total_pressure_pa) / fan_efficiency
        fan_power_kw = fan_power_w / 1000
        
        # Add motor efficiency (typically 0.9)
        motor_efficiency = 0.9
        motor_power_kw = fan_power_kw / motor_efficiency
        
        # Round up to standard motor size
        standard_motors = [0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11, 15, 18.5, 22, 30]
        recommended_motor = None
        for motor in standard_motors:
            if motor >= motor_power_kw:
                recommended_motor = motor
                break
        
        if recommended_motor is None:
            recommended_motor = standard_motors[-1]
        
        return {
            'airflow_lps': airflow_lps,
            'airflow_m3s': airflow_m3s,
            'total_pressure_pa': total_pressure_pa,
            'fan_efficiency': fan_efficiency,
            'fan_power_w': fan_power_w,
            'fan_power_kw': fan_power_kw,
            'motor_efficiency': motor_efficiency,
            'motor_power_kw': motor_power_kw,
            'recommended_motor_kw': recommended_motor
        }
    
    def calculate_chiller_efficiency(
        self,
        cooling_capacity_kw: float,
        chiller_power_kw: float
    ) -> Dict:
        """
        Calculate chiller efficiency (COP and EER)
        
        Args:
            cooling_capacity_kw: Cooling capacity
            chiller_power_kw: Electrical power input
            
        Returns:
            Efficiency metrics
        """
        # Coefficient of Performance
        cop = cooling_capacity_kw / chiller_power_kw
        
        # Energy Efficiency Ratio (BTU/Wh)
        # 1 kW = 3412 BTU/h
        cooling_capacity_btu_hr = cooling_capacity_kw * 3412
        chiller_power_w = chiller_power_kw * 1000
        eer = cooling_capacity_btu_hr / chiller_power_w
        
        # kW per ton (1 ton = 3.517 kW cooling)
        tons = cooling_capacity_kw / 3.517
        kw_per_ton = chiller_power_kw / tons
        
        return {
            'cooling_capacity_kw': cooling_capacity_kw,
            'chiller_power_kw': chiller_power_kw,
            'cop': cop,
            'eer': eer,
            'cooling_capacity_tons': tons,
            'kw_per_ton': kw_per_ton
        }
    
    def calculate_heating_load_detailed(
        self,
        volume_m3: float,
        outside_temp_c: float = -5,
        inside_temp_c: float = 21,
        u_value_walls: float = 0.25,
        u_value_windows: float = 1.8,
        u_value_roof: float = 0.15,
        u_value_floor: float = 0.20,
        wall_area_m2: float = None,
        window_area_m2: float = None,
        roof_area_m2: float = None,
        floor_area_m2: float = None
    ) -> Dict:
        """
        Detailed heating load calculation
        
        Args:
            volume_m3: Room volume
            outside_temp_c: Design outside temperature
            inside_temp_c: Design inside temperature
            u_value_walls: U-value for walls
            u_value_windows: U-value for windows
            u_value_roof: U-value for roof
            u_value_floor: U-value for floor
            wall_area_m2: Wall area (will estimate if not provided)
            window_area_m2: Window area
            roof_area_m2: Roof area
            floor_area_m2: Floor area
            
        Returns:
            Detailed heating load breakdown
        """
        temp_difference = inside_temp_c - outside_temp_c
        
        # Estimate areas if not provided (rough approximation)
        if floor_area_m2 is None:
            floor_area_m2 = volume_m3 / 3  # Assume 3m ceiling height
        
        if wall_area_m2 is None:
            perimeter = 4 * math.sqrt(floor_area_m2)  # Assume square
            wall_area_m2 = perimeter * 3  # 3m height
        
        if window_area_m2 is None:
            window_area_m2 = wall_area_m2 * 0.2  # 20% glazing
        
        if roof_area_m2 is None:
            roof_area_m2 = floor_area_m2
        
        # Calculate fabric heat losses
        wall_loss_w = (wall_area_m2 - window_area_m2) * u_value_walls * temp_difference
        window_loss_w = window_area_m2 * u_value_windows * temp_difference
        roof_loss_w = roof_area_m2 * u_value_roof * temp_difference
        floor_loss_w = floor_area_m2 * u_value_floor * temp_difference
        
        total_fabric_loss_w = wall_loss_w + window_loss_w + roof_loss_w + floor_loss_w
        
        # Ventilation heat loss (1 ACH minimum)
        air_changes_hr = 1.0
        ventilation_loss_w = 0.33 * volume_m3 * air_changes_hr * temp_difference
        
        # Total heat loss
        total_heat_loss_w = total_fabric_loss_w + ventilation_loss_w
        total_heat_loss_kw = total_heat_loss_w / 1000
        
        # Add safety margin (20%)
        safety_factor = 1.2
        design_heat_loss_kw = total_heat_loss_kw * safety_factor
        
        return {
            'volume_m3': volume_m3,
            'temp_difference_c': temp_difference,
            'wall_area_m2': wall_area_m2 - window_area_m2,
            'window_area_m2': window_area_m2,
            'roof_area_m2': roof_area_m2,
            'floor_area_m2': floor_area_m2,
            'wall_loss_w': wall_loss_w,
            'window_loss_w': window_loss_w,
            'roof_loss_w': roof_loss_w,
            'floor_loss_w': floor_loss_w,
            'total_fabric_loss_w': total_fabric_loss_w,
            'ventilation_loss_w': ventilation_loss_w,
            'total_heat_loss_w': total_heat_loss_w,
            'total_heat_loss_kw': total_heat_loss_kw,
            'safety_factor': safety_factor,
            'design_heat_loss_kw': design_heat_loss_kw
        }
