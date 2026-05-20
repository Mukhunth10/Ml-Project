## End to End Machine Learning Project

This repository contains multiple projects:

1. **Machine Learning Pipeline** - End-to-end ML project with data ingestion, transformation, and model training
2. **Quantity Surveying Application** - Comprehensive construction estimation and BOQ extraction tool

---

## Quantity Surveying Application

A professional quantity surveying and Bill of Quantities (BOQ) extraction application similar to Bluebeam, designed specifically for UK and Ireland construction markets.

### Key Features
- 📐 PDF drawing processing with scale detection
- 📏 Measurement tools (lines, areas, volumes, counts)
- 🎨 Markup and annotation system
- 📋 UK & Ireland standards (NRM2, CESMM4, ARM)
- 📊 Automated BOQ generation with Excel export
- 🏗️ BIM integration (IFC file support)
- 🌐 REST API for integration
- 💾 Database for project management

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run demonstration
python examples/demo_usage.py

# Start API server
python src/quantity_surveying/api/app.py
```

### Documentation
See [README_QUANTITY_SURVEYING.md](README_QUANTITY_SURVEYING.md) for complete documentation, API reference, and usage examples.

---

## Machine Learning Project

Original end-to-end machine learning project with data pipeline components. 