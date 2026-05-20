"""
Measurement Calculator - Calculate quantities from shapes
"""
from typing import List, Dict, Tuple
import numpy as np
from ..pdf_processing.scale_detector import ScaleDetector
from ..pdf_processing.coordinate_system import CoordinateSystem
from .shape_tools import MeasurementShape, ShapeType


class MeasurementCalculator:
    """Calculate measurements from shapes with scale calibration"""
    
    def __init__(self, scale_detector: ScaleDetector, coordinate_system: CoordinateSystem):
        """
        Initialize measurement calculator
        
        Args:
            scale_detector: Scale detector for unit conversions
            coordinate_system: Coordinate system for calculations
        """
        self.scale_detector = scale_detector
        self.coordinate_system = coordinate_system
    
    def calculate_shape_measurements(self, shape: MeasurementShape) -> MeasurementShape:
        """
        Calculate measurements for a shape
        
        Args:
            shape: Measurement shape
            
        Returns:
            Updated shape with calculated measurements
        """
        if shape.shape_type == ShapeType.LINE:
            shape.length = self._calculate_line_length(shape.points)
        
        elif shape.shape_type == ShapeType.POLYLINE:
            shape.length = self._calculate_polyline_length(shape.points)
        
        elif shape.shape_type == ShapeType.RECTANGLE:
            shape.area = self._calculate_polygon_area(shape.points)
            shape.length = self._calculate_polyline_length(shape.points)
        
        elif shape.shape_type == ShapeType.POLYGON:
            shape.area = self._calculate_polygon_area(shape.points)
            shape.length = self._calculate_polyline_length(shape.points)
        
        elif shape.shape_type == ShapeType.CIRCLE:
            if len(shape.points) >= 2:
                radius = self.coordinate_system.calculate_distance(
                    shape.points[0], shape.points[1]
                )
                shape.area = self._calculate_circle_area(radius)
                shape.length = 2 * np.pi * radius
        
        elif shape.shape_type == ShapeType.COUNT_MARKER:
            if shape.count is None:
                shape.count = 1
        
        return shape
    
    def _calculate_line_length(self, points: List[Tuple[float, float]]) -> float:
        """Calculate length of a line in real-world units"""
        if len(points) < 2:
            return 0.0
        
        pixel_length = self.coordinate_system.calculate_distance(points[0], points[1])
        return self.scale_detector.pixels_to_real_distance(pixel_length)
    
    def _calculate_polyline_length(self, points: List[Tuple[float, float]]) -> float:
        """Calculate total length of a polyline in real-world units"""
        if len(points) < 2:
            return 0.0
        
        pixel_length = self.coordinate_system.calculate_polyline_length(points)
        return self.scale_detector.pixels_to_real_distance(pixel_length)
    
    def _calculate_polygon_area(self, points: List[Tuple[float, float]]) -> float:
        """Calculate area of a polygon in real-world units"""
        if len(points) < 3:
            return 0.0
        
        pixel_area = self.coordinate_system.calculate_polygon_area(points)
        return self.scale_detector.calculate_area(pixel_area)
    
    def _calculate_circle_area(self, radius_pixels: float) -> float:
        """Calculate area of a circle in real-world units"""
        pixel_area = np.pi * radius_pixels ** 2
        return self.scale_detector.calculate_area(pixel_area)
    
    def calculate_volume(
        self, 
        area: float, 
        depth: float, 
        units: str = "m3"
    ) -> float:
        """
        Calculate volume from area and depth
        
        Args:
            area: Area in square units
            depth: Depth/height in linear units
            units: Target volume units
            
        Returns:
            Volume
        """
        # Convert to consistent units if needed
        volume = area * depth
        return volume
    
    def aggregate_measurements(
        self, 
        shapes: List[MeasurementShape], 
        group_by: str = "category"
    ) -> Dict:
        """
        Aggregate measurements by category or type
        
        Args:
            shapes: List of measurement shapes
            group_by: 'category', 'layer', or 'shape_type'
            
        Returns:
            Dictionary with aggregated measurements
        """
        aggregated = {}
        
        for shape in shapes:
            if group_by == "category":
                key = shape.category
            elif group_by == "layer":
                key = shape.layer
            elif group_by == "shape_type":
                key = shape.shape_type.value
            else:
                key = "All"
            
            if key not in aggregated:
                aggregated[key] = {
                    'total_length': 0.0,
                    'total_area': 0.0,
                    'total_count': 0,
                    'shapes': []
                }
            
            if shape.length:
                aggregated[key]['total_length'] += shape.length
            if shape.area:
                aggregated[key]['total_area'] += shape.area
            if shape.count:
                aggregated[key]['total_count'] += shape.count
            
            aggregated[key]['shapes'].append(shape)
        
        return aggregated
    
    def convert_units(
        self, 
        value: float, 
        from_units: str, 
        to_units: str
    ) -> float:
        """
        Convert between different measurement units
        
        Args:
            value: Value to convert
            from_units: Source units
            to_units: Target units
            
        Returns:
            Converted value
        """
        return self.scale_detector._convert_units(value, from_units, to_units)
