"""
MEP Systems Demonstration
Comprehensive examples for MEP (Mechanical, Electrical, Plumbing) calculations
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.quantity_surveying.mep import (
    MEPCategories,
    MEPElement,
    MEPDiscipline,
    MEPCalculator,
    MEPStandards,
    ElectricalCalculator,
    PlumbingCalculator,
    HVACCalculator
)
from src.quantity_surveying.boq import BOQGenerator, BOQExporter


def demo_electrical_calculations():
    """Demonstrate electrical system calculations"""
    print("\n" + "=" * 70)
    print("ELECTRICAL SYSTEMS DEMO")
    print("=" * 70)
    
    elec_calc = ElectricalCalculator()
    
    # Cable sizing
    print("\n1. Cable Sizing Calculation:")
    cable_sizing = elec_calc.calculate_cable_size(
        load_kw=50,
        length_m=75,
        voltage_drop_percent=3.0,
        phases=3,
        installation_method='tray'
    )
    print(f"   Load: {cable_sizing['load_kw']} kW")
    print(f"   Current: {cable_sizing['current_a']:.2f} A")
    print(f"   Cable Length: {cable_sizing['cable_length_m']} m")
    print(f"   Recommended Cable: {cable_sizing['recommended_cable_size_mm2']} mm²")
    print(f"   Voltage Drop: {cable_sizing['max_voltage_drop_v']:.2f} V")
    
    # Circuit breaker sizing
    print("\n2. Circuit Breaker Sizing:")
    breaker = elec_calc.calculate_circuit_breaker_rating(
        load_kw=25,
        phases=3
    )
    print(f"   Load: {breaker['load_kw']} kW")
    print(f"   Calculated Current: {breaker['calculated_current_a']:.2f} A")
    print(f"   Recommended Breaker: {breaker['recommended_breaker_rating_a']} A")
    
    # Lighting calculation
    print("\n3. Lighting Load Calculation:")
    lighting = elec_calc.calculate_lighting_load(
        area_m2=200,
        lux_level=300,
        luminaire_efficacy=100
    )
    print(f"   Area: {lighting['area_m2']} m²")
    print(f"   Illuminance Level: {lighting['lux_level']} lux")
    print(f"   Total Power: {lighting['total_power_kw']:.2f} kW")
    print(f"   Estimated Fixtures: {lighting['estimated_fixtures']}")
    
    # Transformer sizing
    print("\n4. Transformer Sizing:")
    transformer = elec_calc.calculate_transformer_sizing(
        connected_load_kva=500,
        diversity_factor=0.7,
        future_growth=0.2
    )
    print(f"   Connected Load: {transformer['connected_load_kva']} kVA")
    print(f"   Design Load: {transformer['design_load_kva']:.2f} kVA")
    print(f"   Recommended Transformer: {transformer['recommended_transformer_kva']} kVA")
    print(f"   Loading: {transformer['loading_percent']:.1f}%")
    
    # Generator sizing
    print("\n5. Generator Sizing:")
    generator = elec_calc.calculate_generator_sizing(
        essential_load_kw=150,
        starting_load_kw=50,
        power_factor=0.8
    )
    print(f"   Essential Load: {generator['essential_load_kw']} kW")
    print(f"   Design Load: {generator['design_load_kva']:.2f} kVA")
    print(f"   Recommended Generator: {generator['recommended_generator_kva']} kVA")


def demo_plumbing_calculations():
    """Demonstrate plumbing system calculations"""
    print("\n" + "=" * 70)
    print("PLUMBING SYSTEMS DEMO")
    print("=" * 70)
    
    plumb_calc = PlumbingCalculator()
    
    # Fixture units calculation
    print("\n1. Fixture Units & Water Demand:")
    fixtures = [
        {'type': 'wc', 'quantity': 10},
        {'type': 'wash_basin', 'quantity': 8},
        {'type': 'urinal', 'quantity': 4},
        {'type': 'shower', 'quantity': 2}
    ]
    
    fixture_units = plumb_calc.calculate_fixture_units(fixtures)
    print(f"   Fixture Breakdown:")
    for fixture in fixture_units['fixture_breakdown']:
        print(f"     - {fixture['type'].title()}: {fixture['quantity']} units "
              f"= {fixture['total_fu']:.1f} FU")
    print(f"   Total Fixture Units: {fixture_units['total_fixture_units']:.1f} FU")
    
    # Water demand
    water_demand = plumb_calc.calculate_water_demand(
        fixture_units=fixture_units['total_fixture_units']
    )
    print(f"\n   Water Demand:")
    print(f"     Flow Rate: {water_demand['flow_rate_lps']:.2f} L/s "
          f"({water_demand['flow_rate_lpm']:.1f} L/min)")
    
    # Pipe sizing
    pipe_sizing = plumb_calc.calculate_pipe_sizing(
        flow_rate_lps=water_demand['flow_rate_lps'],
        max_velocity_ms=2.0,
        pipe_material='copper'
    )
    print(f"     Recommended Pipe Size: {pipe_sizing['recommended_size_mm']}mm copper")
    print(f"     Actual Velocity: {pipe_sizing['actual_velocity_ms']:.2f} m/s")
    
    # Hot water storage
    print("\n2. Hot Water Storage:")
    hw_storage = plumb_calc.calculate_hot_water_storage(
        occupants=50,
        dwelling_type='commercial'
    )
    print(f"   Occupants: {hw_storage['occupants']}")
    print(f"   Daily Usage: {hw_storage['daily_usage_l']:.0f} liters")
    print(f"   Recommended Cylinder: {hw_storage['recommended_cylinder_l']} liters")
    print(f"   Recovery Time: {hw_storage['recovery_time_hours']:.1f} hours")
    
    # Drainage sizing
    print("\n3. Drainage Sizing:")
    drainage = plumb_calc.calculate_drainage_sizing(
        fixture_units=fixture_units['total_fixture_units'],
        slope_percent=1.0
    )
    print(f"   Fixture Units: {drainage['fixture_units']:.1f}")
    print(f"   Recommended Pipe Size: {drainage['recommended_pipe_size_mm']}mm")
    print(f"   Flow Capacity: {drainage['flow_capacity_lps']:.2f} L/s")
    
    # Pump sizing
    print("\n4. Pump Head Calculation:")
    pump = plumb_calc.calculate_pump_head(
        vertical_lift_m=15,
        pipe_length_m=50,
        pipe_size_mm=50,
        flow_rate_lps=5
    )
    print(f"   Static Head: {pump['static_head_m']:.1f} m")
    print(f"   Friction Losses: {pump['friction_head_m']:.2f} m")
    print(f"   Design Head: {pump['design_head_m']:.1f} m")
    print(f"   Required Power: {pump['required_power_kw']:.2f} kW")
    
    # Rainwater drainage
    print("\n5. Rainwater Drainage:")
    rainwater = plumb_calc.calculate_rainwater_drainage(
        roof_area_m2=500,
        rainfall_intensity_mm_hr=75
    )
    print(f"   Roof Area: {rainwater['roof_area_m2']} m²")
    print(f"   Flow Rate: {rainwater['flow_rate_lps']:.2f} L/s")
    print(f"   Gutter Size: {rainwater['recommended_gutter_size_mm']}mm")
    print(f"   Downpipe Size: {rainwater['recommended_downpipe_size_mm']}mm")
    print(f"   Number of Downpipes: {rainwater['number_of_downpipes']}")


def demo_hvac_calculations():
    """Demonstrate HVAC system calculations"""
    print("\n" + "=" * 70)
    print("HVAC SYSTEMS DEMO")
    print("=" * 70)
    
    hvac_calc = HVACCalculator()
    
    # Airflow requirements
    print("\n1. Fresh Air Requirements:")
    airflow = hvac_calc.calculate_airflow_requirement(
        area_m2=200,
        occupants=20,
        space_type='office'
    )
    print(f"   Space: {airflow['space_type'].title()}, {airflow['area_m2']} m²")
    print(f"   Occupants: {airflow['occupants']}")
    print(f"   Fresh Air: {airflow['fresh_air_lps']:.1f} L/s ({airflow['fresh_air_m3h']:.0f} m³/h)")
    print(f"   Total Supply Air: {airflow['total_supply_air_lps']:.1f} L/s")
    
    # Cooling load
    print("\n2. Cooling Load Calculation:")
    cooling = hvac_calc.calculate_cooling_load_detailed(
        area_m2=200,
        occupants=20,
        lighting_w_m2=12,
        equipment_w_m2=15
    )
    print(f"   Lighting Load: {cooling['lighting_load_w']/1000:.2f} kW")
    print(f"   Equipment Load: {cooling['equipment_load_w']/1000:.2f} kW")
    print(f"   Occupant Load: {(cooling['occupant_sensible_w'] + cooling['occupant_latent_w'])/1000:.2f} kW")
    print(f"   Design Cooling Load: {cooling['design_cooling_kw']:.2f} kW")
    print(f"   Tons of Refrigeration: {cooling['tons_refrigeration']:.2f} TR")
    print(f"   Sensible Heat Ratio: {cooling['sensible_heat_ratio']:.2f}")
    
    # Duct sizing
    print("\n3. Duct Sizing:")
    duct_rect = hvac_calc.calculate_duct_sizing(
        airflow_lps=airflow['total_supply_air_lps'],
        max_velocity_ms=6.0,
        duct_shape='rectangular'
    )
    print(f"   Rectangular Duct:")
    print(f"     Size: {duct_rect['recommended_width_mm']}mm x {duct_rect['recommended_height_mm']}mm")
    print(f"     Velocity: {duct_rect['actual_velocity_ms']:.2f} m/s")
    
    duct_circ = hvac_calc.calculate_duct_sizing(
        airflow_lps=airflow['total_supply_air_lps'],
        max_velocity_ms=6.0,
        duct_shape='circular'
    )
    print(f"   Circular Duct:")
    print(f"     Diameter: {duct_circ['recommended_diameter_mm']}mm")
    print(f"     Velocity: {duct_circ['actual_velocity_ms']:.2f} m/s")
    
    # Pressure drop
    print("\n4. Pressure Drop Calculation:")
    pressure = hvac_calc.calculate_pressure_drop(
        airflow_lps=airflow['total_supply_air_lps'],
        duct_length_m=30,
        duct_diameter_mm=duct_circ['recommended_diameter_mm']
    )
    print(f"   Duct Length: {pressure['duct_length_m']} m")
    print(f"   Velocity: {pressure['velocity_ms']:.2f} m/s")
    print(f"   Pressure Drop: {pressure['total_pressure_drop_pa']:.1f} Pa")
    
    # Fan power
    print("\n5. Fan Power Calculation:")
    fan = hvac_calc.calculate_fan_power(
        airflow_lps=airflow['total_supply_air_lps'],
        total_pressure_pa=pressure['total_pressure_drop_pa']
    )
    print(f"   Airflow: {fan['airflow_lps']:.1f} L/s")
    print(f"   Total Pressure: {fan['total_pressure_pa']:.1f} Pa")
    print(f"   Fan Power: {fan['fan_power_kw']:.2f} kW")
    print(f"   Recommended Motor: {fan['recommended_motor_kw']} kW")
    
    # Heating load
    print("\n6. Heating Load Calculation:")
    heating = hvac_calc.calculate_heating_load_detailed(
        volume_m3=600,  # 200m² × 3m height
        outside_temp_c=-5,
        inside_temp_c=21,
        floor_area_m2=200
    )
    print(f"   Fabric Heat Loss: {heating['total_fabric_loss_w']/1000:.2f} kW")
    print(f"   Ventilation Loss: {heating['ventilation_loss_w']/1000:.2f} kW")
    print(f"   Design Heat Loss: {heating['design_heat_loss_kw']:.2f} kW")


def demo_mep_standards():
    """Demonstrate MEP standards"""
    print("\n" + "=" * 70)
    print("MEP STANDARDS DEMO")
    print("=" * 70)
    
    mep_std = MEPStandards()
    
    # Electrical standards
    print("\n1. Electrical Standards (Sample):")
    elec_items = mep_std.get_electrical_items()[:5]
    for item in elec_items:
        print(f"   {item.code}: {item.description} ({item.unit})")
    
    # Mechanical standards
    print("\n2. Mechanical Standards (Sample):")
    mech_items = mep_std.get_mechanical_items()[:5]
    for item in mech_items:
        print(f"   {item.code}: {item.description} ({item.unit})")
    
    # Plumbing standards
    print("\n3. Plumbing Standards (Sample):")
    plumb_items = mep_std.get_plumbing_items()[:5]
    for item in plumb_items:
        print(f"   {item.code}: {item.description} ({item.unit})")
    
    # Search standards
    print("\n4. Search for 'Cable':")
    search_results = mep_std.search_by_keyword('cable')
    for item in search_results[:5]:
        print(f"   {item.code}: {item.description} ({item.unit})")


def demo_mep_boq_generation():
    """Generate MEP BOQ"""
    print("\n" + "=" * 70)
    print("MEP BOQ GENERATION DEMO")
    print("=" * 70)
    
    boq = BOQGenerator(project_name="Commercial Office Building - MEP Works")
    boq.metadata['client'] = 'Tech Corp Ltd'
    boq.metadata['location'] = 'Dublin, Ireland'
    
    mep_std = MEPStandards()
    
    # Electrical Section
    boq.create_section_header("ELECTRICAL INSTALLATION", level=1)
    
    boq.create_section_header("5.8.1 Power Distribution", level=2)
    boq.create_item(
        description="Main distribution board, 400A, TP&N",
        unit="nr",
        quantity=1,
        rate=4500.00,
        category="Electrical",
        standard_code="5.8.1.2"
    )
    boq.create_item(
        description="Sub-distribution board, 125A, TP&N",
        unit="nr",
        quantity=3,
        rate=1200.00,
        category="Electrical",
        standard_code="5.8.1.3"
    )
    
    boq.create_section_header("5.8.3 Cables", level=2)
    boq.create_item(
        description="Cable, PVC/SWA, 10mm² 3-core",
        unit="m",
        quantity=450,
        rate=8.50,
        category="Electrical",
        standard_code="5.8.3.4"
    )
    boq.create_item(
        description="Cable, PVC/SWA, 2.5mm² 3-core",
        unit="m",
        quantity=1200,
        rate=3.20,
        category="Electrical",
        standard_code="5.8.3.1"
    )
    
    boq.create_section_header("5.8.4 Cable Management", level=2)
    boq.create_item(
        description="Cable tray, ladder type, 300mm wide",
        unit="m",
        quantity=85,
        rate=35.00,
        category="Electrical",
        standard_code="5.8.4.1"
    )
    
    boq.create_section_header("5.8.5 Lighting", level=2)
    boq.create_item(
        description="LED panel luminaire, 600x600mm, 40W",
        unit="nr",
        quantity=120,
        rate=75.00,
        category="Electrical",
        standard_code="5.8.5.1"
    )
    boq.create_item(
        description="Emergency lighting, LED, non-maintained",
        unit="nr",
        quantity=25,
        rate=95.00,
        category="Electrical",
        standard_code="5.8.5.7"
    )
    
    # Mechanical Section
    boq.create_section_header("MECHANICAL INSTALLATION", level=1)
    
    boq.create_section_header("5.6.1 Air Handling Equipment", level=2)
    boq.create_item(
        description="Air handling unit, 5000 L/s, with controls",
        unit="nr",
        quantity=2,
        rate=18500.00,
        category="Mechanical",
        standard_code="5.6.1.1"
    )
    boq.create_item(
        description="Fan coil unit, 4-pipe, 5kW",
        unit="nr",
        quantity=15,
        rate=850.00,
        category="Mechanical",
        standard_code="5.6.1.4"
    )
    
    boq.create_section_header("5.6.3 Ductwork", level=2)
    boq.create_item(
        description="Ductwork, galvanized steel, 400x300mm",
        unit="m",
        quantity=180,
        rate=45.00,
        category="Mechanical",
        standard_code="5.6.3.2"
    )
    boq.create_item(
        description="Ductwork, spiral, galv., 200mm dia",
        unit="m",
        quantity=240,
        rate=28.00,
        category="Mechanical",
        standard_code="5.6.3.12"
    )
    
    boq.create_section_header("5.6.5 Diffusers and Grilles", level=2)
    boq.create_item(
        description="Ceiling diffuser, 4-way, 600x600mm",
        unit="nr",
        quantity=85,
        rate=65.00,
        category="Mechanical",
        standard_code="5.6.5.2"
    )
    
    # Plumbing Section
    boq.create_section_header("PLUMBING INSTALLATION", level=1)
    
    boq.create_section_header("5.1.1 Sanitary Fixtures", level=2)
    boq.create_item(
        description="WC suite, wall hung, complete",
        unit="nr",
        quantity=12,
        rate=450.00,
        category="Plumbing",
        standard_code="5.1.1.2"
    )
    boq.create_item(
        description="Wash hand basin, wall hung, 550mm",
        unit="nr",
        quantity=10,
        rate=280.00,
        category="Plumbing",
        standard_code="5.1.2.1"
    )
    
    boq.create_section_header("5.4.1 Water Services", level=2)
    boq.create_item(
        description="Pipework, copper, 22mm, cold water",
        unit="m",
        quantity=150,
        rate=12.50,
        category="Plumbing",
        standard_code="5.4.1.2"
    )
    boq.create_item(
        description="Pipework, copper, 15mm, hot water",
        unit="m",
        quantity=120,
        rate=9.80,
        category="Plumbing",
        standard_code="5.4.2.1"
    )
    
    boq.create_section_header("5.3.1 Drainage", level=2)
    boq.create_item(
        description="Soil pipe, PVC-U, 110mm",
        unit="m",
        quantity=65,
        rate=18.50,
        category="Plumbing",
        standard_code="5.3.1.1"
    )
    
    # Calculate totals
    totals = boq.calculate_totals()
    
    print(f"\nBOQ Generated:")
    print(f"  Total Items: {totals['item_count']}")
    print(f"  Subtotal: €{totals['subtotal']:,.2f}")
    print(f"  VAT (20%): €{totals['vat']:,.2f}")
    print(f"  Total: €{totals['total']:,.2f}")
    
    # Cost breakdown
    print(f"\nCost Breakdown by Discipline:")
    category_summary = boq.get_summary_by_category()
    for category, amount in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
        if amount > 0:
            percentage = (amount / totals['subtotal']) * 100
            print(f"  {category:20s} €{amount:>12,.2f} ({percentage:>5.1f}%)")
    
    return boq


def main():
    """Run all MEP demonstrations"""
    print("\n" + "=" * 70)
    print("MEP SYSTEMS - COMPREHENSIVE DEMONSTRATION")
    print("=" * 70)
    print("\nThis demo covers:")
    print("1. Electrical calculations (cables, breakers, lighting, etc.)")
    print("2. Plumbing calculations (pipe sizing, pumps, drainage, etc.)")
    print("3. HVAC calculations (cooling loads, duct sizing, fan power, etc.)")
    print("4. MEP standards (NRM2 Section 5)")
    print("5. MEP BOQ generation")
    
    try:
        demo_electrical_calculations()
        demo_plumbing_calculations()
        demo_hvac_calculations()
        demo_mep_standards()
        boq = demo_mep_boq_generation()
        
        print("\n" + "=" * 70)
        print("MEP DEMONSTRATION COMPLETE")
        print("=" * 70)
        print("\nYour MEP estimation toolkit includes:")
        print("  ✓ Electrical design calculations")
        print("  ✓ Plumbing and drainage sizing")
        print("  ✓ HVAC load calculations and duct sizing")
        print("  ✓ 200+ MEP standard items (NRM2)")
        print("  ✓ Automated BOQ generation")
        print("  ✓ Excel/CSV export capabilities")
        
    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
