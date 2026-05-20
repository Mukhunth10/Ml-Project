"""
Coordinate System - Manage coordinate transformations for drawings
"""
from typing import Tuple, List, Dict
import numpy as np


class CoordinateSystem:
    """Manage coordinate transformations between screen and drawing coordinates"""
    
    def __init__(self, image_width: int, image_height: int):
        """
        Initialize coordinate system
        
        Args:
            image_width: Width of image/drawing in pixels
            image_height: Height of image/drawing in pixels
        """
        self.image_width = image_width
        self.image_height = image_height
        self.origin = (0, 0)  # Top-left by default
        self.rotation = 0  # Rotation angle in degrees
        self.zoom = 1.0
        self.pan_offset = (0, 0)
    
    def screen_to_image(self, screen_point: Tuple[float, float]) -> Tuple[float, float]:
        """
        Convert screen coordinates to image coordinates
        
        Args:
            screen_point: (x, y) in screen coordinates
            
        Returns:
            (x, y) in image coordinates
        """
        x, y = screen_point
        
        # Apply pan offset
        x = (x - self.pan_offset[0]) / self.zoom
        y = (y - self.pan_offset[1]) / self.zoom
        
        # Apply rotation if needed
        if self.rotation != 0:
            x, y = self._rotate_point((x, y), -self.rotation)
        
        return (x, y)
    
    def image_to_screen(self, image_point: Tuple[float, float]) -> Tuple[float, float]:
        """
        Convert image coordinates to screen coordinates
        
        Args:
            image_point: (x, y) in image coordinates
            
        Returns:
            (x, y) in screen coordinates
        """
        x, y = image_point
        
        # Apply rotation if needed
        if self.rotation != 0:
            x, y = self._rotate_point((x, y), self.rotation)
        
        # Apply zoom and pan
        x = x * self.zoom + self.pan_offset[0]
        y = y * self.zoom + self.pan_offset[1]
        
        return (x, y)
    
    def _rotate_point(
        self, 
        point: Tuple[float, float], 
        angle: float
    ) -> Tuple[float, float]:
        """
        Rotate a point around origin
        
        Args:
            point: (x, y) coordinates
            angle: Rotation angle in degrees
            
        Returns:
            Rotated (x, y) coordinates
        """
        angle_rad = np.radians(angle)
        x, y = point
        
        # Rotate around center of image
        cx, cy = self.image_width / 2, self.image_height / 2
        
        # Translate to origin
        x -= cx
        y -= cy
        
        # Rotate
        x_new = x * np.cos(angle_rad) - y * np.sin(angle_rad)
        y_new = x * np.sin(angle_rad) + y * np.cos(angle_rad)
        
        # Translate back
        x_new += cx
        y_new += cy
        
        return (x_new, y_new)
    
    def set_zoom(self, zoom: float):
        """Set zoom level"""
        self.zoom = max(0.1, min(10.0, zoom))  # Clamp between 0.1x and 10x
    
    def set_pan(self, offset: Tuple[float, float]):
        """Set pan offset"""
        self.pan_offset = offset
    
    def set_rotation(self, angle: float):
        """Set rotation angle in degrees"""
        self.rotation = angle % 360
    
    def calculate_distance(
        self, 
        point1: Tuple[float, float], 
        point2: Tuple[float, float]
    ) -> float:
        """
        Calculate distance between two points
        
        Args:
            point1: First point (x, y)
            point2: Second point (x, y)
            
        Returns:
            Distance in pixels
        """
        return np.sqrt(
            (point2[0] - point1[0])**2 + 
            (point2[1] - point1[1])**2
        )
    
    def calculate_polygon_area(self, points: List[Tuple[float, float]]) -> float:
        """
        Calculate area of a polygon using shoelace formula
        
        Args:
            points: List of (x, y) coordinates defining polygon
            
        Returns:
            Area in square pixels
        """
        if len(points) < 3:
            return 0.0
        
        # Shoelace formula
        area = 0.0
        n = len(points)
        
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        
        return abs(area) / 2.0
    
    def calculate_rectangle_area(
        self, 
        point1: Tuple[float, float], 
        point2: Tuple[float, float]
    ) -> float:
        """
        Calculate area of rectangle
        
        Args:
            point1: First corner (x, y)
            point2: Opposite corner (x, y)
            
        Returns:
            Area in square pixels
        """
        width = abs(point2[0] - point1[0])
        height = abs(point2[1] - point1[1])
        return width * height
    
    def calculate_circle_area(
        self, 
        center: Tuple[float, float], 
        radius: float
    ) -> float:
        """
        Calculate area of circle
        
        Args:
            center: Center point (x, y)
            radius: Radius in pixels
            
        Returns:
            Area in square pixels
        """
        return np.pi * radius ** 2
    
    def calculate_polyline_length(self, points: List[Tuple[float, float]]) -> float:
        """
        Calculate total length of a polyline
        
        Args:
            points: List of (x, y) coordinates
            
        Returns:
            Total length in pixels
        """
        if len(points) < 2:
            return 0.0
        
        total_length = 0.0
        for i in range(len(points) - 1):
            total_length += self.calculate_distance(points[i], points[i + 1])
        
        return total_length
    
    def is_point_in_bounds(self, point: Tuple[float, float]) -> bool:
        """Check if point is within image bounds"""
        x, y = point
        return 0 <= x <= self.image_width and 0 <= y <= self.image_height
    
    def get_bounds(self) -> Dict:
        """Get current bounds information"""
        return {
            'width': self.image_width,
            'height': self.image_height,
            'zoom': self.zoom,
            'rotation': self.rotation,
            'pan_offset': self.pan_offset
        }
