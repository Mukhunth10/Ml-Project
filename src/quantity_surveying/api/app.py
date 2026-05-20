"""
Flask API Application
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from typing import Dict
import os
from io import BytesIO

# Import our modules
from ..pdf_processing import PDFHandler, ScaleDetector
from ..measurement_tools import ShapeTools, MeasurementCalculator
from ..markup import ColorManager, LayerManager, Annotation
from ..standards import StandardsManager, StandardType
from ..boq import BOQGenerator, BOQExporter
from ..revit_integration import IFCHandler, ModelQuantityExtractor


def create_app(config: Dict = None) -> Flask:
    """
    Create and configure Flask application
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Configured Flask app
    """
    app = Flask(__name__)
    CORS(app)  # Enable CORS for web frontend
    
    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    
    if config:
        app.config.update(config)
    
    # Create upload folder
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize managers (in production, use proper state management)
    shape_tools = ShapeTools()
    color_manager = ColorManager()
    layer_manager = LayerManager()
    standards_manager = StandardsManager()
    
    # Routes
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'version': '0.1.0'})
    
    # PDF Processing Routes
    
    @app.route('/api/pdf/upload', methods=['POST'])
    def upload_pdf():
        """Upload and process PDF"""
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        try:
            pdf_bytes = file.read()
            pdf_handler = PDFHandler(pdf_bytes=pdf_bytes)
            
            # Extract basic info
            pages_info = pdf_handler.get_page_info()
            
            return jsonify({
                'success': True,
                'pages_count': pdf_handler.pages_count,
                'metadata': pdf_handler.metadata,
                'pages_info': pages_info
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/pdf/extract-text/<int:page_num>', methods=['GET'])
    def extract_text(page_num):
        """Extract text from PDF page"""
        # In production, retrieve stored PDF handler
        return jsonify({'text': 'Text extraction not implemented in this demo'})
    
    # Measurement Routes
    
    @app.route('/api/measurements/create', methods=['POST'])
    def create_measurement():
        """Create a new measurement shape"""
        data = request.json
        
        try:
            shape_type = data.get('shape_type')
            points = data.get('points', [])
            
            if shape_type == 'line' and len(points) >= 2:
                shape = shape_tools.create_line(
                    tuple(points[0]),
                    tuple(points[1]),
                    **data.get('properties', {})
                )
            elif shape_type == 'polyline':
                shape = shape_tools.create_polyline(
                    [tuple(p) for p in points],
                    **data.get('properties', {})
                )
            elif shape_type == 'rectangle' and len(points) >= 2:
                shape = shape_tools.create_rectangle(
                    tuple(points[0]),
                    tuple(points[1]),
                    **data.get('properties', {})
                )
            elif shape_type == 'polygon':
                shape = shape_tools.create_polygon(
                    [tuple(p) for p in points],
                    **data.get('properties', {})
                )
            else:
                return jsonify({'error': 'Invalid shape type or points'}), 400
            
            return jsonify({
                'success': True,
                'shape': shape.to_dict()
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/measurements/list', methods=['GET'])
    def list_measurements():
        """List all measurements"""
        shapes = shape_tools.get_all_shapes()
        return jsonify({
            'shapes': [shape.to_dict() for shape in shapes],
            'summary': shape_tools.get_summary()
        })
    
    @app.route('/api/measurements/<shape_id>', methods=['DELETE'])
    def delete_measurement(shape_id):
        """Delete a measurement"""
        success = shape_tools.delete_shape(shape_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Shape not found'}), 404
    
    # BOQ Routes
    
    @app.route('/api/boq/create', methods=['POST'])
    def create_boq():
        """Create a new BOQ"""
        data = request.json
        project_name = data.get('project_name', 'Untitled Project')
        
        boq = BOQGenerator(project_name)
        
        # Import measurements if provided
        measurements = data.get('measurements', [])
        if measurements:
            boq.import_from_measurements(measurements)
        
        return jsonify({
            'success': True,
            'boq': boq.to_dict()
        })
    
    @app.route('/api/boq/export/excel', methods=['POST'])
    def export_boq_excel():
        """Export BOQ to Excel"""
        data = request.json
        
        try:
            exporter = BOQExporter(data)
            excel_buffer = exporter.to_excel()
            
            return send_file(
                excel_buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='boq.xlsx'
            )
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/boq/export/csv', methods=['POST'])
    def export_boq_csv():
        """Export BOQ to CSV"""
        data = request.json
        
        try:
            exporter = BOQExporter(data)
            csv_data = exporter.to_csv()
            
            return send_file(
                BytesIO(csv_data.encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name='boq.csv'
            )
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Standards Routes
    
    @app.route('/api/standards/list', methods=['GET'])
    def list_standards():
        """List available standards"""
        return jsonify({
            'standards': [
                {
                    'type': 'NRM2',
                    'info': standards_manager.get_standard_info(StandardType.NRM2)
                },
                {
                    'type': 'CESMM4',
                    'info': standards_manager.get_standard_info(StandardType.CESMM4)
                },
                {
                    'type': 'ARM',
                    'info': standards_manager.get_standard_info(StandardType.ARM)
                }
            ]
        })
    
    @app.route('/api/standards/search', methods=['GET'])
    def search_standards():
        """Search standards"""
        keyword = request.args.get('keyword', '')
        results = standards_manager.search_all_standards(keyword)
        
        # Convert to JSON-serializable format
        json_results = {}
        for standard, items in results.items():
            json_results[standard] = [
                {
                    'code': item.code,
                    'description': item.description,
                    'unit': item.unit
                }
                for item in items
            ]
        
        return jsonify({'results': json_results})
    
    # IFC/Revit Routes
    
    @app.route('/api/ifc/upload', methods=['POST'])
    def upload_ifc():
        """Upload and process IFC file"""
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        try:
            # Save file temporarily
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            # Process IFC
            ifc_handler = IFCHandler(file_path)
            project_info = ifc_handler.get_project_info()
            summary = ifc_handler.get_elements_by_type_summary()
            
            return jsonify({
                'success': True,
                'project_info': project_info,
                'summary': summary
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/ifc/extract-quantities', methods=['POST'])
    def extract_ifc_quantities():
        """Extract quantities from IFC file"""
        data = request.json
        file_path = data.get('file_path')
        
        if not file_path or not os.path.exists(file_path):
            return jsonify({'error': 'Invalid file path'}), 400
        
        try:
            extractor = ModelQuantityExtractor()
            extractor.load_from_ifc(file_path)
            
            boq_items = extractor.generate_boq_from_model()
            
            return jsonify({
                'success': True,
                'boq_items': boq_items,
                'summary': extractor.get_element_types_summary()
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Color and Layer Routes
    
    @app.route('/api/colors/list', methods=['GET'])
    def list_colors():
        """List available colors"""
        return jsonify({'colors': color_manager.get_all_colors()})
    
    @app.route('/api/layers/list', methods=['GET'])
    def list_layers():
        """List layers"""
        return jsonify({
            'layers': layer_manager.export_layers(),
            'active_layer': layer_manager.active_layer
        })
    
    @app.route('/api/layers/create', methods=['POST'])
    def create_layer():
        """Create a new layer"""
        data = request.json
        layer = layer_manager.create_layer(**data)
        return jsonify({'success': True, 'layer': layer.to_dict()})
    
    return app


# Run the application
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
