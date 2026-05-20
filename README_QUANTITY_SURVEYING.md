# Quantity Surveying Application

A comprehensive quantity surveying and Bill of Quantities (BOQ) extraction application similar to Bluebeam, designed for UK and Ireland construction markets.

## Features

### 📐 PDF and Drawing Processing
- **PDF Upload & Processing**: Upload construction drawings in PDF format
- **Scale Detection**: Automatic and manual scale calibration (1:50, 1:100, etc.)
- **Text Extraction**: Extract drawing information, scales, and specifications
- **Multi-page Support**: Handle multi-page drawing sets

### 📏 Measurement Tools
- **Shape Tools**:
  - Lines and polylines for linear measurements
  - Rectangles and polygons for area measurements
  - Circles for circular features
  - Count markers for discrete items
- **Layer Management**: Organize measurements in layers
- **Color Coding**: Assign colors by category (Walls, Doors, Windows, etc.)
- **Real-time Calculations**: Automatic length, area, and volume calculations

### 🎨 Markup and Annotation
- **Text Annotations**: Add notes and callouts
- **Visual Markup**: Clouds, arrows, stamps
- **Layer System**: Multiple layers with visibility controls
- **Color Manager**: Predefined color schemes for construction elements

### 📋 UK & Ireland Standards Support
- **NRM2** (New Rules of Measurement 2): RICS standard for building works
- **CESMM4**: Civil Engineering Standard Method of Measurement, 4th Edition
- **ARM** (Agreed Rules of Measurement): Ireland building measurement standard
- **Standard Codes**: Link measurements to standard work sections

### 📊 BOQ Generation
- **Automatic BOQ Creation**: Generate BOQ from measurements
- **Excel Export**: Professional formatted Excel exports
- **CSV Export**: Data export for further processing
- **Cost Estimation**: Add rates and calculate totals
- **VAT Calculation**: Automatic VAT calculations
- **Summary Reports**: Aggregate by category, work section, or material

### 🏗️ BIM Integration
- **IFC Support**: Import and process IFC files from Revit, ArchiCAD, etc.
- **Quantity Extraction**: Automatic quantity takeoff from BIM models
- **Model-to-BOQ**: Direct BOQ generation from BIM quantities
- **Revit Connector**: (Windows only) Direct Revit API integration

### 🌐 Web API
- **REST API**: Full REST API for integration
- **File Upload**: Upload PDFs and IFC files
- **Measurement CRUD**: Create, read, update, delete measurements
- **Export Endpoints**: Generate and download BOQ exports

### 💾 Data Management
- **SQLite Database**: Local project storage
- **PostgreSQL Support**: For multi-user deployments
- **Project Management**: Organize by projects
- **Version History**: Track changes over time

## Installation

### Prerequisites
```bash
# Python 3.8 or higher
python --version

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y poppler-utils
```

### Install Application
```bash
# Clone repository
cd /projects/sandbox/Ml-Project

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

## Quick Start

### 1. Process a PDF Drawing

```python
from src.quantity_surveying.pdf_processing import PDFHandler, ScaleDetector

# Load PDF
pdf_handler = PDFHandler('/path/to/drawing.pdf')

# Get drawing info
drawing_info = pdf_handler.extract_drawing_info(page_num=0)
print(f"Scale: {drawing_info['scale']}")

# Convert to image for markup
images = pdf_handler.convert_to_images(dpi=300)

# Set up scale
scale_detector = ScaleDetector()
scale_detector.set_scale_from_ratio(scale_denominator=100, units='mm', dpi=300)
```

### 2. Create Measurements

```python
from src.quantity_surveying.measurement_tools import ShapeTools
from src.quantity_surveying.pdf_processing import CoordinateSystem

# Initialize tools
shape_tools = ShapeTools()
coord_system = CoordinateSystem(image_width=2480, image_height=3508)

# Create measurements
wall = shape_tools.create_polyline(
    points=[(100, 100), (500, 100), (500, 200)],
    category='Walls',
    color='#FF6B6B',
    label='External Wall - North'
)

door = shape_tools.create_rectangle(
    corner1=(200, 100),
    corner2=(300, 150),
    category='Doors',
    color='#FFD93D',
    label='Door D01'
)

# Calculate measurements
from src.quantity_surveying.measurement_tools import MeasurementCalculator

calculator = MeasurementCalculator(scale_detector, coord_system)
wall = calculator.calculate_shape_measurements(wall)
print(f"Wall length: {wall.length:.2f} mm")
```

### 3. Generate BOQ

```python
from src.quantity_surveying.boq import BOQGenerator, BOQExporter

# Create BOQ
boq = BOQGenerator(project_name="Office Building Refurbishment")

# Add items
boq.create_section_header("3.5 External Walls", level=1)

boq.create_item(
    description="Brick external wall, 215mm thick",
    unit="m²",
    quantity=145.50,
    rate=85.00,
    category="Walls",
    standard_code="3.5.1"
)

boq.create_item(
    description="External door, hardwood, 900x2100mm",
    unit="nr",
    quantity=3,
    rate=650.00,
    category="Doors",
    standard_code="3.5.3"
)

# Export to Excel
exporter = BOQExporter(boq.to_dict())
exporter.to_excel('boq_export.xlsx')

# Print summary
totals = boq.calculate_totals()
print(f"Subtotal: £{totals['subtotal']:,.2f}")
print(f"VAT: £{totals['vat']:,.2f}")
print(f"Total: £{totals['total']:,.2f}")
```

### 4. Work with Standards

```python
from src.quantity_surveying.standards import StandardsManager, StandardType

# Initialize standards
standards = StandardsManager(default_standard=StandardType.NRM2)

# Search for items
results = standards.search_all_standards('concrete')
for standard, items in results.items():
    print(f"\n{standard}:")
    for item in items[:3]:  # Show first 3
        print(f"  {item.code}: {item.description} ({item.unit})")

# Get specific item
nrm2 = standards.nrm2
item = nrm2.get_item('3.1')
print(f"\n{nrm2.format_item_description(item)}")
```

### 5. Process IFC Files

```python
from src.quantity_surveying.revit_integration import IFCHandler, ModelQuantityExtractor

# Load IFC file
ifc_handler = IFCHandler('/path/to/model.ifc')

# Get project info
project_info = ifc_handler.get_project_info()
print(f"Project: {project_info['name']}")

# Extract quantities
extractor = ModelQuantityExtractor()
extractor.load_from_ifc('/path/to/model.ifc')

# Generate BOQ from model
boq_items = extractor.generate_boq_from_model()
print(f"Extracted {len(boq_items)} items from model")

# Export report
report = extractor.export_quantities_report()
print(report)
```

### 6. Run Web API

```python
from src.quantity_surveying.api import create_app

# Create and run app
app = create_app()
app.run(debug=True, host='0.0.0.0', port=5000)
```

Then access:
- Health check: `http://localhost:5000/health`
- API docs: See API section below

## API Endpoints

### PDF Processing
- `POST /api/pdf/upload` - Upload PDF drawing
- `GET /api/pdf/extract-text/<page_num>` - Extract text from page

### Measurements
- `POST /api/measurements/create` - Create measurement
- `GET /api/measurements/list` - List all measurements
- `DELETE /api/measurements/<shape_id>` - Delete measurement

### BOQ
- `POST /api/boq/create` - Create BOQ
- `POST /api/boq/export/excel` - Export to Excel
- `POST /api/boq/export/csv` - Export to CSV

### Standards
- `GET /api/standards/list` - List standards
- `GET /api/standards/search?keyword=wall` - Search standards

### IFC/BIM
- `POST /api/ifc/upload` - Upload IFC file
- `POST /api/ifc/extract-quantities` - Extract quantities

### Colors & Layers
- `GET /api/colors/list` - List colors
- `GET /api/layers/list` - List layers
- `POST /api/layers/create` - Create layer

## Database Setup

```python
from src.quantity_surveying.database import Database, Project, Measurement, BOQItem

# Initialize database
db = Database('sqlite:///projects.db')
db.create_tables()

# Create project
with db.get_session() as session:
    project = Project(
        name='Shopping Centre Renovation',
        location='Manchester, UK',
        client='ABC Developments',
        standard_type='NRM2'
    )
    session.add(project)
    session.commit()
    
    print(f"Created project: {project.name} (ID: {project.id})")
```

## Architecture

```
quantity_surveying/
├── pdf_processing/         # PDF handling and scale detection
│   ├── pdf_handler.py
│   ├── scale_detector.py
│   └── coordinate_system.py
├── measurement_tools/      # Measurement shapes and calculations
│   ├── shape_tools.py
│   └── measurement_calculator.py
├── markup/                 # Annotations and visual markup
│   ├── annotation.py
│   ├── color_manager.py
│   └── layer_manager.py
├── standards/              # UK & Ireland standards
│   ├── nrm2_standard.py
│   ├── cesmm4_standard.py
│   ├── arm_standard.py
│   └── standards_manager.py
├── boq/                    # BOQ generation and export
│   ├── boq_generator.py
│   └── boq_exporter.py
├── revit_integration/      # BIM and IFC support
│   ├── ifc_handler.py
│   ├── revit_connector.py
│   └── model_quantity_extractor.py
├── api/                    # REST API
│   └── app.py
└── database/               # Data persistence
    ├── models.py
    └── database.py
```

## Standards Coverage

### NRM2 (UK Building Works)
- Facilitating Works
- Substructure
- Superstructure (Frame, Floors, Roof, Walls)
- Internal Finishes
- Services (MEP)
- External Works

### CESMM4 (UK Civil Engineering)
- Earthworks
- In-situ Concrete
- Pipework
- Roads and Pavings
- Structural Metalwork

### ARM (Ireland Building Works)
- Excavation and Earthwork
- Concrete Work
- Brickwork and Blockwork
- Surface Finishes
- Plumbing and Services

## Roadmap

### Phase 1 (Current)
- [x] Core PDF processing
- [x] Measurement tools
- [x] BOQ generation
- [x] Standards library
- [x] IFC support
- [x] REST API

### Phase 2 (Planned)
- [ ] Web frontend with canvas drawing
- [ ] Real-time collaboration
- [ ] Advanced BIM integration
- [ ] AI-assisted quantity extraction
- [ ] Mobile app
- [ ] Cloud deployment

### Phase 3 (Future)
- [ ] Machine learning for automatic measurement
- [ ] Integration with accounting systems
- [ ] Tender management
- [ ] Progress tracking
- [ ] Cost analysis and forecasting

## Contributing

This is a demonstration project showing how to build a quantity surveying application. To extend it:

1. Add more measurement tools (angles, complex shapes)
2. Implement advanced scale detection using computer vision
3. Build interactive web UI with canvas drawing
4. Add more standards and regional variations
5. Implement real-time collaboration features
6. Add automated testing

## License

This project is for demonstration purposes.

## Support

For questions or support:
- Email: mukhunth1@gmail.com
- GitHub: Mukhunth10/Ml-Project

---

**Built with:** Python, Flask, SQLAlchemy, IfcOpenShell, OpenCV, Pandas, Openpyxl
