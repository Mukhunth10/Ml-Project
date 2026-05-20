"""
Shape Tools - Define and manage measurement shapes
"""
from enum import Enum
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field
import uuid
import json


class ShapeType(Enum):
    """Types of measurement shapes"""
    LINE = "line"
    POLYLINE = "polyline"
    RECTANGLE = "rectangle"
    POLYGON = "polygon"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"
    COUNT_MARKER = "count_marker"
    AREA = "area"
    VOLUME = "volume"


@dataclass
class MeasurementShape:
    """Represents a measurement shape on a drawing"""
    
    shape_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    shape_type: ShapeType = ShapeType.LINE
    points: List[Tuple[float, float]] = field(default_factory=list)
    color: str = "#FF0000"  # Red by default
    label: str = ""
    description: str = ""
    category: str = "General"  # e.g., "Walls", "Doors", "Windows"
    
    # Measurement results
    length: Optional[float] = None  # For linear measurements
    area: Optional[float] = None  # For area measurements
    count: Optional[int] = None  # For count measurements
    
    # Additional properties
    thickness: float = 2.0  # Line thickness for display
    layer: str = "default"
    locked: bool = False
    visible: bool = True
    
    # Units
    units: str = "mm"
    
    # Metadata
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    notes: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'shape_id': self.shape_id,
            'shape_type': self.shape_type.value,
            'points': self.points,
            'color': self.color,
            'label': self.label,
            'description': self.description,
            'category': self.category,
            'length': self.length,
            'area': self.area,
            'count': self.count,
            'thickness': self.thickness,
            'layer': self.layer,
            'locked': self.locked,
            'visible': self.visible,
            'units': self.units,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MeasurementShape':
        """Create from dictionary"""
        data = data.copy()
        if 'shape_type' in data:
            data['shape_type'] = ShapeType(data['shape_type'])
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'MeasurementShape':
        """Create from JSON string"""
        return cls.from_dict(json.loads(json_str))


class ShapeTools:
    """Tools for creating and managing measurement shapes"""
    
    def __init__(self):
        self.shapes: Dict[str, MeasurementShape] = {}
        self.active_layer = "default"
        self.layers: Dict[str, Dict] = {
            "default": {"name": "Default", "visible": True, "locked": False}
        }
    
    def create_line(
        self, 
        start: Tuple[float, float], 
        end: Tuple[float, float],
        **kwargs
    ) -> MeasurementShape:
        """Create a line measurement"""
        shape = MeasurementShape(
            shape_type=ShapeType.LINE,
            points=[start, end],
            layer=self.active_layer,
            **kwargs
        )
        self.shapes[shape.shape_id] = shape
        return shape
    
    def create_polyline(
        self, 
        points: List[Tuple[float, float]],
        **kwargs
    ) -> MeasurementShape:
        """Create a polyline measurement"""
        shape = MeasurementShape(
            shape_type=ShapeType.POLYLINE,
            points=points,
            layer=self.active_layer,
            **kwargs
        )
        self.shapes[shape.shape_id] = shape
        return shape
    
    def create_rectangle(
        self, 
        corner1: Tuple[float, float], 
        corner2: Tuple[float, float],
        **kwargs
    ) -> MeasurementShape:
        """Create a rectangle measurement"""
        # Create 4 corners
        x1, y1 = corner1
        x2, y2 = corner2
        points = [
            (x1, y1),
            (x2, y1),
            (x2, y2),
            (x1, y2),
            (x1, y1)  # Close the shape
        ]
        
        shape = MeasurementShape(
            shape_type=ShapeType.RECTANGLE,
            points=points,
            layer=self.active_layer,
            **kwargs
        )
        self.shapes[shape.shape_id] = shape
        return shape
    
    def create_polygon(
        self, 
        points: List[Tuple[float, float]],
        **kwargs
    ) -> MeasurementShape:
        """Create a polygon measurement"""
        # Ensure polygon is closed
        if points[0] != points[-1]:
            points = points + [points[0]]
        
        shape = MeasurementShape(
            shape_type=ShapeType.POLYGON,
            points=points,
            layer=self.active_layer,
            **kwargs
        )
        self.shapes[shape.shape_id] = shape
        return shape
    
    def create_circle(
        self, 
        center: Tuple[float, float], 
        radius_point: Tuple[float, float],
        **kwargs
    ) -> MeasurementShape:
        """Create a circle measurement"""
        shape = MeasurementShape(
            shape_type=ShapeType.CIRCLE,
            points=[center, radius_point],
            layer=self.active_layer,
            **kwargs
        )
        self.shapes[shape.shape_id] = shape
        return shape
    
    def create_count_marker(
        self, 
        position: Tuple[float, float],
        **kwargs
    ) -> MeasurementShape:
        """Create a count marker"""
        shape = MeasurementShape(
            shape_type=ShapeType.COUNT_MARKER,
            points=[position],
            count=1,
            layer=self.active_layer,
            **kwargs
        )
        self.shapes[shape.shape_id] = shape
        return shape
    
    def add_shape(self, shape: MeasurementShape):
        """Add an existing shape"""
        self.shapes[shape.shape_id] = shape
    
    def get_shape(self, shape_id: str) -> Optional[MeasurementShape]:
        """Get shape by ID"""
        return self.shapes.get(shape_id)
    
    def delete_shape(self, shape_id: str) -> bool:
        """Delete a shape"""
        if shape_id in self.shapes:
            del self.shapes[shape_id]
            return True
        return False
    
    def update_shape(self, shape_id: str, **updates) -> bool:
        """Update shape properties"""
        if shape_id in self.shapes:
            shape = self.shapes[shape_id]
            for key, value in updates.items():
                if hasattr(shape, key):
                    setattr(shape, key, value)
            return True
        return False
    
    def get_shapes_by_layer(self, layer: str) -> List[MeasurementShape]:
        """Get all shapes on a specific layer"""
        return [s for s in self.shapes.values() if s.layer == layer]
    
    def get_shapes_by_category(self, category: str) -> List[MeasurementShape]:
        """Get all shapes in a specific category"""
        return [s for s in self.shapes.values() if s.category == category]
    
    def get_all_shapes(self) -> List[MeasurementShape]:
        """Get all shapes"""
        return list(self.shapes.values())
    
    def create_layer(self, name: str, visible: bool = True, locked: bool = False):
        """Create a new layer"""
        self.layers[name] = {
            "name": name,
            "visible": visible,
            "locked": locked
        }
    
    def set_active_layer(self, layer: str):
        """Set the active layer for new shapes"""
        if layer in self.layers:
            self.active_layer = layer
        else:
            raise ValueError(f"Layer '{layer}' does not exist")
    
    def toggle_layer_visibility(self, layer: str):
        """Toggle layer visibility"""
        if layer in self.layers:
            self.layers[layer]["visible"] = not self.layers[layer]["visible"]
    
    def lock_layer(self, layer: str):
        """Lock a layer"""
        if layer in self.layers:
            self.layers[layer]["locked"] = True
    
    def unlock_layer(self, layer: str):
        """Unlock a layer"""
        if layer in self.layers:
            self.layers[layer]["locked"] = False
    
    def export_shapes(self) -> List[Dict]:
        """Export all shapes as list of dictionaries"""
        return [shape.to_dict() for shape in self.shapes.values()]
    
    def import_shapes(self, shapes_data: List[Dict]):
        """Import shapes from list of dictionaries"""
        for shape_data in shapes_data:
            shape = MeasurementShape.from_dict(shape_data)
            self.shapes[shape.shape_id] = shape
    
    def clear_all(self):
        """Clear all shapes"""
        self.shapes.clear()
    
    def get_summary(self) -> Dict:
        """Get summary of all measurements"""
        summary = {
            'total_shapes': len(self.shapes),
            'by_type': {},
            'by_category': {},
            'by_layer': {}
        }
        
        for shape in self.shapes.values():
            # Count by type
            shape_type = shape.shape_type.value
            summary['by_type'][shape_type] = summary['by_type'].get(shape_type, 0) + 1
            
            # Count by category
            category = shape.category
            summary['by_category'][category] = summary['by_category'].get(category, 0) + 1
            
            # Count by layer
            layer = shape.layer
            summary['by_layer'][layer] = summary['by_layer'].get(layer, 0) + 1
        
        return summary
