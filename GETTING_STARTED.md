# Getting Started with Quantity Surveying Application

## Quick Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Mukhunth10/Ml-Project.git
cd Ml-Project
```

### 2. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils python3-pip
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
- Download and install Poppler from https://github.com/oschwartz10612/poppler-windows/releases/
- Add to PATH

### 3. Install Python Dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Run the Demo

```bash
python examples/demo_usage.py
```

This will demonstrate:
- Creating measurements with scale calibration
- Working with UK/Ireland standards (NRM2, CESMM4, ARM)
- Generating Bills of Quantities
- Managing colors and layers
- IFC/BIM integration capabilities

## Start the API Server

```bash
python src/quantity_surveying/api/app.py
```

The API will be available at http://localhost:5000

Test it:
```bash
curl http://localhost:5000/health
```

## Basic Usage Examples

### Example 1: Process a PDF Drawing

```python
from src.quantity_surveying.pdf_processing import PDFHandler, ScaleDetector
from src.quantity_surveying.pdf_processing import CoordinateSystem

# Load your PDF
pdf = PDFHandler('/path/to/your/drawing.pdf')

# Get drawing information
info = pdf.extract_drawing_info(page_num=0)
print(f"Drawing scale: {info['scale']}")

# Convert to image for markup
images = pdf.convert_to_images(dpi=300)

# Set up scale
scale = ScaleDetector()
# For a 1:100 scale drawing at 300 DPI
scale.set_scale_from_ratio(scale_denominator=100, units='mm', dpi=300)

print(f"Scale configured: {scale.scale_text}")
```

### Example 2: Create Measurements

```python
from src.quantity_surveying.measurement_tools import ShapeTools, MeasurementCalculator

# Initialize
shapes = ShapeTools()
coord_sys = CoordinateSystem(image_width=2480, image_height=3508)
calculator = MeasurementCalculator(scale, coord_sys)

# Measure a wall
wall = shapes.create_polyline(
    points=[(100, 100), (800, 100), (800, 200), (100, 200)],
    category='Walls',
    color='#FF6B6B',
    label='North External Wall',
    description='Brick wall, 215mm thick'
)

# Calculate real measurements
wall = calculator.calculate_shape_measurements(wall)
print(f"Wall length: {wall.length:.2f} mm = {wall.length/1000:.2f} m")

# Measure floor area
floor = shapes.create_rectangle(
    corner1=(100, 100),
    corner2=(800, 600),
    category='Floors',
    label='Ground Floor Slab'
)

floor = calculator.calculate_shape_measurements(floor)
print(f"Floor area: {floor.area/1000000:.2f} m²")
```

### Example 3: Generate a BOQ

```python
from src.quantity_surveying.boq import BOQGenerator, BOQExporter

# Create BOQ
boq = BOQGenerator(project_name="Commercial Office Fit-out")

# Add sections and items
boq.create_section_header("2. SUBSTRUCTURE", level=1)

boq.create_item(
    description="Excavation for foundations, max depth 1.5m",
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

boq.create_section_header("3. SUPERSTRUCTURE", level=1)

boq.create_item(
    description="Brick external wall, 215mm thick",
    unit="m²",
    quantity=145.50,
    rate=85.00,
    category="Walls",
    standard_code="3.5.1"
)

# Calculate totals
totals = boq.calculate_totals()
print(f"Total cost: £{totals['total']:,.2f}")

# Export to Excel
exporter = BOQExporter(boq.to_dict())
exporter.to_excel('my_boq.xlsx')
print("BOQ exported to my_boq.xlsx")
```

### Example 4: Work with Standards

```python
from src.quantity_surveying.standards import StandardsManager, StandardType

# Initialize
standards = StandardsManager(default_standard=StandardType.NRM2)

# Search for items
results = standards.search_all_standards('wall')
for standard, items in results.items():
    print(f"\n{standard}:")
    for item in items[:3]:
        print(f"  {item.code}: {item.description} ({item.unit})")

# Get NRM2 superstructure items
nrm2 = standards.nrm2
superstructure = nrm2.get_children('3')
for item in superstructure:
    print(f"{item.code}: {item.description}")
```

### Example 5: Process IFC Files

```python
from src.quantity_surveying.revit_integration import IFCHandler, ModelQuantityExtractor

# Load IFC file (exported from Revit, ArchiCAD, etc.)
ifc = IFCHandler('/path/to/your/model.ifc')

# Get project info
project_info = ifc.get_project_info()
print(f"Project: {project_info['name']}")

# Extract all walls
walls = ifc.extract_elements_by_type('IfcWall')
print(f"Found {len(walls)} walls")

for wall in walls[:5]:  # Show first 5
    print(f"\n{wall.name}:")
    print(f"  Material: {wall.material}")
    for qty_name, qty_data in wall.quantities.items():
        print(f"  {qty_name}: {qty_data['value']} {qty_data['unit']}")

# Generate BOQ from model
extractor = ModelQuantityExtractor()
extractor.load_from_ifc('/path/to/your/model.ifc')

boq_items = extractor.generate_boq_from_model()
print(f"\nGenerated {len(boq_items)} BOQ items from model")

# Export report
report = extractor.export_quantities_report()
print(report)
```

## API Usage Examples

### Upload PDF
```bash
curl -X POST http://localhost:5000/api/pdf/upload \
  -F "file=@/path/to/drawing.pdf"
```

### Create Measurement
```bash
curl -X POST http://localhost:5000/api/measurements/create \
  -H "Content-Type: application/json" \
  -d '{
    "shape_type": "rectangle",
    "points": [[100, 100], [500, 300]],
    "properties": {
      "category": "Walls",
      "label": "Wall A",
      "color": "#FF6B6B"
    }
  }'
```

### Generate BOQ
```bash
curl -X POST http://localhost:5000/api/boq/create \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "My Project",
    "measurements": []
  }'
```

### Search Standards
```bash
curl http://localhost:5000/api/standards/search?keyword=concrete
```

### Upload IFC File
```bash
curl -X POST http://localhost:5000/api/ifc/upload \
  -F "file=@/path/to/model.ifc"
```

## Database Setup

```python
from src.quantity_surveying.database import Database, Project

# Initialize database
db = Database('sqlite:///my_projects.db')
db.create_tables()

# Create a project
with db.get_session() as session:
    project = Project(
        name='Shopping Centre Renovation',
        location='London, UK',
        client='ABC Developments Ltd',
        standard_type='NRM2',
        currency='GBP'
    )
    session.add(project)
    session.commit()
    
    print(f"Project created with ID: {project.id}")
```

## Next Steps

1. **Read the full documentation**: See [README_QUANTITY_SURVEYING.md](README_QUANTITY_SURVEYING.md)

2. **Explore the API**: Start the server and explore all endpoints

3. **Try with your own drawings**: Process your PDF drawings and IFC models

4. **Customize**: Extend the code with your specific requirements

5. **Build a frontend**: Use the REST API to build a web or mobile interface

## Common Use Cases

### Use Case 1: Takeoff from PDF Drawings
1. Upload PDF drawing
2. Calibrate scale
3. Create measurements using shape tools
4. Generate BOQ
5. Export to Excel

### Use Case 2: Quantity Extraction from BIM
1. Export IFC from Revit/ArchiCAD
2. Upload IFC file
3. Extract quantities automatically
4. Review and adjust
5. Generate BOQ

### Use Case 3: Cost Estimation
1. Import measurements or IFC quantities
2. Link to standard work items
3. Add rates
4. Generate cost estimate
5. Export professional BOQ

## Troubleshooting

### PDF Processing Issues
- Ensure poppler-utils is installed
- Check PDF file is not password protected
- Try converting to images first

### IFC Processing Issues
- Ensure ifcopenshell is installed correctly
- Check IFC file is valid (IFC2x3 or IFC4)
- Try opening in another IFC viewer first

### API Issues
- Check port 5000 is not in use
- Enable CORS if accessing from web frontend
- Check file upload size limits

## Support

- Documentation: [README_QUANTITY_SURVEYING.md](README_QUANTITY_SURVEYING.md)
- Issues: https://github.com/Mukhunth10/Ml-Project/issues
- Email: mukhunth1@gmail.com

## License

This is a demonstration project for educational purposes.
