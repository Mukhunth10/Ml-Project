# MEP Systems Module - Complete Guide

## Overview

Comprehensive MEP (Mechanical, Electrical, Plumbing) calculation and estimation system for construction projects. Designed specifically for MEP contractors, consultants, and quantity surveyors.

## Features

### 🔌 Electrical Systems
- **Cable Sizing**: Voltage drop calculations, current carrying capacity
- **Circuit Protection**: Breaker and fuse sizing
- **Lighting Design**: Lux level calculations, fixture counts
- **Power Distribution**: Transformer and generator sizing
- **Earthing & Lightning Protection**: Earth conductor sizing
- **UPS Systems**: Backup time calculations
- **Load Analysis**: Diversity factors, power demand

### 🌡️ Mechanical/HVAC Systems
- **Cooling Load Calculations**: Sensible & latent heat gains
- **Heating Load Calculations**: Fabric and ventilation losses
- **Airflow Requirements**: Fresh air, ventilation rates
- **Duct Sizing**: Rectangular and circular ducts
- **Pressure Drop**: Friction losses, system resistance
- **Fan Selection**: Power requirements, motor sizing
- **Chiller/Boiler Sizing**: Capacity calculations
- **Equipment Selection**: AHU, FCU, VRF systems

### 💧 Plumbing Systems
- **Fixture Units**: Load calculations (Hunter's method)
- **Pipe Sizing**: Water supply, drainage
- **Pump Selection**: Head calculations, power requirements
- **Hot Water Systems**: Storage sizing, recovery time
- **Drainage Design**: Slope, capacity calculations
- **Rainwater Systems**: Gutter and downpipe sizing
- **Pressure Calculations**: Static and dynamic pressures

### 🔥 Fire Protection
- **Sprinkler Systems**: Head spacing, pipe sizing
- **Fire Hydrants**: Coverage calculations
- **Fire Pumps**: Duty requirements
- **Detection Systems**: Coverage areas

### 📋 Standards Compliance
- **NRM2 Section 5 Services**: Complete implementation
- **200+ Standard Items**: Electrical, Mechanical, Plumbing
- **UK Building Regulations**: Ventilation, drainage standards
- **BS Standards**: Referenced throughout
- **CIBSE Guidelines**: Design calculations

### 📊 BOQ Generation
- **Automated Takeoff**: From calculations to BOQ
- **Standard Item Linking**: NRM2 codes
- **Cost Estimation**: Material + labor
- **Excel Export**: Professional formatting
- **Discipline Segregation**: Separate electrical, mechanical, plumbing

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Example 1: Electrical Cable Sizing

```python
from src.quantity_surveying.mep import ElectricalCalculator

elec = ElectricalCalculator()

# Size a cable for a 50kW load, 75m run
result = elec.calculate_cable_size(
    load_kw=50,
    length_m=75,
    voltage_drop_percent=3.0,
    phases=3,
    installation_method='tray'
)

print(f"Recommended Cable: {result['recommended_cable_size_mm2']} mm²")
print(f"Current: {result['current_a']:.2f} A")
print(f"Voltage Drop: {result['max_voltage_drop_v']:.2f} V")
```

### Example 2: HVAC Cooling Load

```python
from src.quantity_surveying.mep import HVACCalculator

hvac = HVACCalculator()

# Calculate cooling load for an office
cooling = hvac.calculate_cooling_load_detailed(
    area_m2=200,
    occupants=20,
    lighting_w_m2=12,
    equipment_w_m2=15,
    solar_gain_w_m2=30
)

print(f"Design Cooling Load: {cooling['design_cooling_kw']:.2f} kW")
print(f"Tons of Refrigeration: {cooling['tons_refrigeration']:.2f} TR")
print(f"Sensible Heat Ratio: {cooling['sensible_heat_ratio']:.2f}")
```

### Example 3: Plumbing Pipe Sizing

```python
from src.quantity_surveying.mep import PlumbingCalculator

plumb = PlumbingCalculator()

# Calculate fixture units
fixtures = [
    {'type': 'wc', 'quantity': 10},
    {'type': 'wash_basin', 'quantity': 8},
    {'type': 'urinal', 'quantity': 4}
]

fixture_units = plumb.calculate_fixture_units(fixtures)
water_demand = plumb.calculate_water_demand(
    fixture_units=fixture_units['total_fixture_units']
)

pipe_sizing = plumb.calculate_pipe_sizing(
    flow_rate_lps=water_demand['flow_rate_lps'],
    max_velocity_ms=2.0,
    pipe_material='copper'
)

print(f"Total Fixture Units: {fixture_units['total_fixture_units']}")
print(f"Water Demand: {water_demand['flow_rate_lps']:.2f} L/s")
print(f"Recommended Pipe: {pipe_sizing['recommended_size_mm']}mm")
```

### Example 4: Complete MEP BOQ

```python
from src.quantity_surveying.mep import MEPStandards
from src.quantity_surveying.boq import BOQGenerator, BOQExporter

boq = BOQGenerator("Office Building MEP Works")
mep_std = MEPStandards()

# Electrical items
boq.create_section_header("ELECTRICAL INSTALLATION", level=1)
boq.create_item(
    description="Main distribution board, 400A",
    unit="nr",
    quantity=1,
    rate=4500.00,
    category="Electrical",
    standard_code="5.8.1.2"
)

boq.create_item(
    description="Cable, PVC/SWA, 10mm² 3-core",
    unit="m",
    quantity=450,
    rate=8.50,
    category="Electrical",
    standard_code="5.8.3.4"
)

# Mechanical items
boq.create_section_header("MECHANICAL INSTALLATION", level=1)
boq.create_item(
    description="Air handling unit, 5000 L/s",
    unit="nr",
    quantity=2,
    rate=18500.00,
    category="Mechanical",
    standard_code="5.6.1.1"
)

# Export to Excel
exporter = BOQExporter(boq.to_dict())
exporter.to_excel('mep_boq.xlsx')
```

## MEP Categories

### Electrical Categories (40+)
- Power Distribution (switchboards, panels, transformers)
- Cables (power, data, fire alarm)
- Cable Management (trays, conduits, trunking)
- Lighting (internal, external, emergency)
- Power Outlets (sockets, dedicated supplies)
- Earthing & Protection
- Fire Alarm Systems
- Generators & UPS

### Mechanical Categories (50+)
- Air Handling (AHU, FCU, VAV)
- Ductwork (supply, return, extract)
- Diffusers & Grilles
- Heating Systems (boilers, radiators)
- Cooling Systems (chillers, split AC, VRF)
- Pipework (LTHW, CHW, condensate)
- Insulation
- Controls (thermostats, sensors, actuators)

### Plumbing Categories (40+)
- Water Supply (cold, hot, storage)
- Sanitary Fixtures (WCs, basins, showers)
- Drainage (above ground, below ground)
- Pumps & Boosters
- Water Treatment
- Medical/Laboratory Services

### Fire Protection Categories
- Sprinkler Systems
- Fire Hose Reels
- Fire Hydrants
- Risers (wet, dry)
- Pumps & Tanks

## Calculation Methods

### Electrical
- **Cable Sizing**: BS 7671 (IET Wiring Regulations)
- **Voltage Drop**: As per cable length and load
- **Circuit Protection**: MCB/MCCB selection
- **Transformer**: kVA calculation with diversity
- **Lighting**: Lux level method, LLF, UF
- **Earthing**: Adiabatic equation

### Mechanical
- **Cooling Load**: CIBSE Guide A
- **Heating Load**: Heat loss calculations
- **Airflow**: CIBSE Guide B, Building Regs Part F
- **Duct Sizing**: Equal friction method
- **Pressure Drop**: Darcy-Weisbach equation
- **Fan Power**: Based on airflow and pressure

### Plumbing
- **Fixture Units**: Hunter's curve
- **Pipe Sizing**: Velocity method (max 2 m/s)
- **Pump Head**: Static + friction + minor losses
- **Drainage**: Manning's equation
- **Hot Water**: Storage based on occupancy
- **Rainwater**: BS EN 12056

## MEP Standards Reference

### NRM2 Section 5 Implementation

**5.1 Sanitary Installations**
- WCs, urinals, basins, showers, baths, sinks

**5.2 Services Equipment**
- Water heaters, treatment systems, specialised equipment

**5.3 Disposal Installations**
- Soil, waste, drainage pipework and fittings

**5.4 Water Installations**
- Cold and hot water systems, storage, pumps

**5.5 Heat Source**
- Boilers, calorifiers, heat pumps

**5.6 Space Heating and Air Conditioning**
- AHU, FCU, ductwork, diffusers, chillers, pipework

**5.7 Ventilation**
- Extract fans, natural ventilation systems

**5.8 Electrical Installations**
- Distribution boards, cables, lighting, outlets, earthing

**5.9 Fuel Installations**
- Gas, oil supply systems

**5.10 Lift and Conveyor Installations**
- Lifts, escalators, conveyors

**5.11 Fire and Lightning Protection**
- Sprinklers, hose reels, detection systems

**5.12 Communication, Security and Control Systems**
- Fire alarm, CCTV, access control, BMS

**5.13 Specialist Installations**
- Medical gases, laboratory services

**5.14 Builder's Work**
- Holes, chases, supports for services

## Color Coding

MEP elements are automatically color-coded for easy identification:

**Electrical** (Yellow/Orange tones)
- Main equipment: #FFD700 (Gold)
- Power cables: #FF8C00 (Dark Orange)
- Data cables: #00CED1 (Cyan)
- Lighting: #FFFF00 (Yellow)

**Mechanical** (Blue/Green tones)
- Ductwork supply: #87CEEB (Sky Blue)
- Ductwork return: #B0C4DE (Light Steel Blue)
- Chilled water: #00BFFF (Deep Sky Blue)
- Heating water: #FF6347 (Tomato)

**Plumbing** (Blue/Brown tones)
- Cold water: #0000FF (Blue)
- Hot water: #FF0000 (Red)
- Drainage: #8B4513 (Saddle Brown)
- Rainwater: #4682B4 (Steel Blue)

**Fire Protection** (Red tones)
- Sprinklers: #DC143C (Crimson)
- Fire systems: #B22222 (Fire Brick)

## Running Demos

### Complete MEP Demo
```bash
python examples/mep_demo.py
```

This demonstrates:
- All electrical calculations
- All plumbing calculations
- All HVAC calculations
- MEP standards library
- MEP BOQ generation

### Output includes:
- Cable sizing for 50kW load
- Lighting design for 200m² space
- Transformer sizing (500 kVA load)
- Plumbing pipe sizing for 24 fixtures
- Hot water storage for 50 people
- Cooling load for office (20 occupants)
- Duct sizing and fan selection
- Complete MEP BOQ with costs

## API Integration

All MEP calculations are available via the REST API:

```bash
# Start API server
python src/quantity_surveying/api/app.py
```

### API Endpoints

```
POST /api/mep/electrical/cable-sizing
POST /api/mep/electrical/breaker-sizing
POST /api/mep/electrical/lighting
POST /api/mep/plumbing/pipe-sizing
POST /api/mep/plumbing/pump-head
POST /api/mep/hvac/cooling-load
POST /api/mep/hvac/duct-sizing
POST /api/mep/standards/search
```

## Best Practices

### For Electrical Estimating
1. Always include 5-10% cable waste
2. Consider derating factors for installation method
3. Check voltage drop is < 3% for power, < 5% for lighting
4. Include diversity factors for large installations
5. Size breakers 125% of continuous load

### For Mechanical Estimating
1. Add 15-20% for duct fittings
2. Keep duct velocity < 6 m/s for low noise
3. Use appropriate safety factors (10-20%)
4. Consider part load performance
5. Include for insulation and supports

### For Plumbing Estimating
1. Use fixture units method for sizing
2. Keep water velocity < 2 m/s to avoid noise
3. Add 10% for pipe fittings
4. Size hot water storage for peak demand
5. Check drainage gradients (minimum 1:80)

## Integration with IFC/BIM

Extract MEP quantities directly from BIM models:

```python
from src.quantity_surveying.revit_integration import IFCHandler

ifc = IFCHandler('building_model.ifc')

# Extract electrical elements
cables = ifc.extract_elements_by_type('IfcCableSegment')
lights = ifc.extract_elements_by_type('IfcLightFixture')

# Extract mechanical elements
ducts = ifc.extract_elements_by_type('IfcDuctSegment')
air_terminals = ifc.extract_elements_by_type('IfcAirTerminal')

# Extract plumbing elements
pipes = ifc.extract_elements_by_type('IfcPipeSegment')
sanitary_fixtures = ifc.extract_elements_by_type('IfcSanitaryTerminal')

# Generate BOQ from model
boq_items = ifc.export_to_boq_format()
```

## Troubleshooting

**Issue**: Calculations seem incorrect
- Check units are consistent (mm, m, kW, etc.)
- Verify input values are reasonable
- Review diversity and safety factors

**Issue**: BOQ export fails
- Ensure all quantities are positive numbers
- Check standard codes are valid
- Verify file path has write permissions

**Issue**: IFC import errors
- Ensure IFC file is valid (IFC2x3 or IFC4)
- Check ifcopenshell is installed correctly
- Try opening IFC in another viewer first

## Support & Resources

- **Documentation**: README_QUANTITY_SURVEYING.md
- **Examples**: examples/mep_demo.py
- **Standards**: MEP standards library (200+ items)
- **API Docs**: See API section above

## Contributing

To extend MEP functionality:
1. Add new calculation methods to respective calculators
2. Add standard items to MEPStandards
3. Update category enums in mep_categories.py
4. Add tests and examples

## License

Part of the Quantity Surveying Application suite.

---

**Built for MEP professionals by understanding real-world estimation needs.**
