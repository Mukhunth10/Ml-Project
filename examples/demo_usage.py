"""
Demonstration of Quantity Surveying Application Usage
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.quantity_surveying.measurement_tools import ShapeTools, MeasurementCalculator
from src.quantity_surveying.pdf_processing import ScaleDetector, CoordinateSystem
from src.quantity_surveying.markup import ColorManager, LayerManager
from src.quantity_surveying.standards import StandardsManager, StandardType
from src.quantity_surveying.boq import BOQGenerator, BOQExporter


def demo_measurements():
    """Demonstrate measurement creation and calculation"""
    print("\n" + "="*60)
    print("DEMO 1: Creating Measurements")
    print("="*60)
    
    # Initialize tools
    shape_tools = ShapeTools()
    scale_detector = ScaleDetector()
    coord_system = CoordinateSystem(image_width=2480, image_height=3508)
    
    # Set scale (1:100 at 300 DPI)
    scale_detector.set_scale_from_ratio(scale_denominator=100, units='mm', dpi=300)
    print(f"Scale set to: {scale_detector.scale_text}")
    
    # Create calculator
    calculator = MeasurementCalculator(scale_detector, coord_system)
    
    # Create some measurements
    print("\nCreating measurements...")
    
    # Wall measurement
    wall = shape_tools.create_polyline(
        points=[(100, 100), (500, 100), (500, 200), (100, 200)],
        category='Walls',
        color='#FF6B6B',
        label='External Wall - North',
        description='Brick wall, 215mm thick'
    )
    wall = calculator.calculate_shape_measurements(wall)
    print(f"✓ Wall: {wall.label}")
    print(f"  Length: {wall.length:.2f} mm ({wall.length/1000:.2f} m)")
    
    # Floor area
    floor = shape_tools.create_rectangle(
        corner1=(100, 100),
        corner2=(800, 600),
        category='Floors',
        color='#96CEB4',
        label='Ground Floor Slab'
    )
    floor = calculator.calculate_shape_measurements(floor)
    print(f"✓ Floor: {floor.label}")
    print(f"  Area: {floor.area:.2f} mm² ({floor.area/1000000:.2f} m²)")
    
    # Count doors
    for i in range(3):
        door = shape_tools.create_count_marker(
            position=(200 + i*100, 150),
            category='Doors',
            color='#FFD93D',
            label=f'Door D{i+1:02d}'
        )
        print(f"✓ {door.label}")
    
    # Summary
    summary = shape_tools.get_summary()
    print(f"\nSummary:")
    print(f"  Total shapes: {summary['total_shapes']}")
    print(f"  By category: {summary['by_category']}")


def demo_standards():
    """Demonstrate standards usage"""
    print("\n" + "="*60)
    print("DEMO 2: Working with Standards")
    print("="*60)
    
    standards = StandardsManager()
    
    # List all standards
    print("\nAvailable Standards:")
    for std_type in [StandardType.NRM2, StandardType.CESMM4, StandardType.ARM]:
        info = standards.get_standard_info(std_type)
        print(f"  • {info['name']}")
        print(f"    Region: {info['region']}, Application: {info['application']}")
    
    # Search across standards
    print("\nSearching for 'concrete'...")
    results = standards.search_all_standards('concrete')
    for standard, items in results.items():
        print(f"\n  {standard}:")
        for item in items[:3]:  # Show first 3
            print(f"    {item.code}: {item.description} ({item.unit})")
    
    # Get specific NRM2 items
    print("\nNRM2 Superstructure Items:")
    nrm2 = standards.nrm2
    superstructure = nrm2.get_item('3')
    children = nrm2.get_children('3')
    print(f"  {superstructure.code}: {superstructure.description}")
    for child in children[:5]:
        print(f"    {child.code}: {child.description}")
    
    # Recommend standard
    recommendation = standards.recommend_standard('building', 'uk')
    print(f"\nRecommended standard for UK building project: {recommendation.value}")


def demo_boq_generation():
    """Demonstrate BOQ generation"""
    print("\n" + "="*60)
    print("DEMO 3: Generating Bill of Quantities")
    print("="*60)
    
    # Create BOQ
    boq = BOQGenerator(project_name="Office Refurbishment - London")
    
    # Add metadata
    boq.metadata['client'] = 'ABC Corporation'
    boq.metadata['location'] = 'London, UK'
    
    # Add items by section
    print("\nBuilding BOQ...")
    
    # Substructure
    boq.create_section_header("2. SUBSTRUCTURE", level=1)
    boq.create_item(
        description="Excavation for foundations, maximum depth 1.5m",
        unit="m³",
        quantity=45.50,
        rate=25.00,
        category="Excavation",
        standard_code="2.1"
    )
    boq.create_item(
        description="Mass concrete foundation, grade C20",
        unit="m³",
        quantity=32.00,
        rate=95.00,
        category="Concrete",
        standard_code="2.4"
    )
    
    # Superstructure
    boq.create_section_header("3. SUPERSTRUCTURE", level=1)
    
    boq.create_section_header("3.5 External Walls", level=2)
    boq.create_item(
        description="Brick external wall, 215mm thick, facing bricks",
        unit="m²",
        quantity=145.50,
        rate=85.00,
        category="Walls",
        standard_code="3.5.1"
    )
    
    boq.create_section_header("3.5.3 External Doors", level=2)
    boq.create_item(
        description="External door, hardwood, 900x2100mm, including frame",
        unit="nr",
        quantity=3,
        rate=650.00,
        category="Doors",
        standard_code="3.5.3"
    )
    boq.create_item(
        description="External door, aluminium & glass, 1800x2100mm",
        unit="nr",
        quantity=1,
        rate=1250.00,
        category="Doors",
        standard_code="3.5.3"
    )
    
    # Internal Finishes
    boq.create_section_header("4. INTERNAL FINISHES", level=1)
    boq.create_item(
        description="Wall plaster, two coat work, 13mm thick",
        unit="m²",
        quantity=280.00,
        rate=18.50,
        category="Finishes",
        standard_code="4.1"
    )
    boq.create_item(
        description="Carpet tiles, 500x500mm, including adhesive",
        unit="m²",
        quantity=125.00,
        rate=35.00,
        category="Flooring",
        standard_code="4.2"
    )
    
    print(f"✓ Added {len(boq.items)} BOQ items")
    
    # Calculate totals
    totals = boq.calculate_totals()
    print(f"\nBOQ Totals:")
    print(f"  Subtotal: £{totals['subtotal']:,.2f}")
    print(f"  VAT (20%): £{totals['vat']:,.2f}")
    print(f"  Total: £{totals['total']:,.2f}")
    
    # Summary by category
    print(f"\nCost Breakdown by Category:")
    category_summary = boq.get_summary_by_category()
    for category, amount in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:20s} £{amount:>12,.2f}")
    
    # Export
    print(f"\nExporting BOQ...")
    exporter = BOQExporter(boq.to_dict())
    
    # Export to CSV
    csv_data = exporter.to_csv()
    print(f"✓ CSV export ready ({len(csv_data)} bytes)")
    
    # Print summary report
    print(f"\n{exporter.get_summary_report()}")
    
    return boq


def demo_color_and_layers():
    """Demonstrate color and layer management"""
    print("\n" + "="*60)
    print("DEMO 4: Colors and Layers")
    print("="*60)
    
    color_manager = ColorManager()
    layer_manager = LayerManager()
    
    # Show standard colors
    print("\nStandard Color Scheme:")
    colors = color_manager.STANDARD_COLORS
    for category, color in list(colors.items())[:10]:
        print(f"  {category:20s} {color}")
    
    # Custom color
    color_manager.set_custom_color('Temporary Works', '#FFA500')
    print(f"\n✓ Added custom color for Temporary Works")
    
    # Layers
    print(f"\nDefault Layers:")
    for layer in layer_manager.get_all_layers():
        status = "✓" if layer.visible else "✗"
        lock = "🔒" if layer.locked else "🔓"
        print(f"  {status} {lock} {layer.name}")
    
    # Create custom layer
    layer_manager.create_layer(
        'MEP Systems',
        visible=True,
        locked=False,
        color='#00CED1',
        description='Mechanical, Electrical, Plumbing'
    )
    print(f"\n✓ Created custom layer: MEP Systems")
    
    # Layer operations
    layer_manager.set_active_layer('MEP Systems')
    print(f"✓ Active layer: {layer_manager.active_layer}")


def demo_ifc_integration():
    """Demonstrate IFC file processing"""
    print("\n" + "="*60)
    print("DEMO 5: IFC/BIM Integration")
    print("="*60)
    
    print("\nIFC File Processing:")
    print("  To process an IFC file:")
    print("  1. Export your Revit/ArchiCAD model to IFC")
    print("  2. Use IFCHandler to load the file")
    print("  3. Extract quantities automatically")
    
    print("\n  Example code:")
    print("  ```python")
    print("  from src.quantity_surveying.revit_integration import IFCHandler")
    print("  ")
    print("  ifc = IFCHandler('/path/to/model.ifc')")
    print("  project_info = ifc.get_project_info()")
    print("  ")
    print("  # Extract all walls")
    print("  walls = ifc.extract_elements_by_type('IfcWall')")
    print("  for wall in walls:")
    print("      print(f'{wall.name}: {wall.quantities}')")
    print("  ")
    print("  # Generate BOQ")
    print("  boq_items = ifc.export_to_boq_format()")
    print("  ```")
    
    print("\n  Supported IFC Elements:")
    elements = [
        'IfcWall', 'IfcSlab', 'IfcColumn', 'IfcBeam', 
        'IfcDoor', 'IfcWindow', 'IfcStair', 'IfcRoof'
    ]
    for elem in elements:
        print(f"    ✓ {elem}")


def main():
    """Run all demonstrations"""
    print("\n" + "="*60)
    print("QUANTITY SURVEYING APPLICATION - DEMONSTRATION")
    print("="*60)
    print("\nThis demo shows the key features of the application:")
    print("1. Creating and calculating measurements")
    print("2. Working with UK/Ireland standards (NRM2, CESMM4, ARM)")
    print("3. Generating Bills of Quantities")
    print("4. Managing colors and layers")
    print("5. IFC/BIM integration")
    
    try:
        demo_measurements()
        demo_standards()
        demo_boq_generation()
        demo_color_and_layers()
        demo_ifc_integration()
        
        print("\n" + "="*60)
        print("DEMONSTRATION COMPLETE")
        print("="*60)
        print("\nNext steps:")
        print("  1. See README_QUANTITY_SURVEYING.md for full documentation")
        print("  2. Run API: python src/quantity_surveying/api/app.py")
        print("  3. Try processing your own PDF drawings")
        print("  4. Export IFC from Revit and process quantities")
        
    except Exception as e:
        print(f"\nError during demonstration: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
