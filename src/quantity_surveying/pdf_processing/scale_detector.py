"""
Scale Detector - Detect and manage drawing scales
"""
from typing import Tuple, Optional, Dict
import re
import cv2
import numpy as np
from PIL import Image


class ScaleDetector:
    """Detect and manage drawing scales for accurate measurements"""
    
    def __init__(self):
        self.scale_ratio = None  # Pixels per unit (e.g., pixels per meter)
        self.scale_text = None  # e.g., "1:100"
        self.units = "mm"  # Default units
        self.calibration_points = []
    
    def parse_scale_text(self, text: str) -> Optional[float]:
        """
        Parse scale from text (e.g., "1:100" -> 100)
        
        Args:
            text: Scale text
            
        Returns:
            Scale denominator or None
        """
        patterns = [
            r'1:(\d+)',
            r'1/(\d+)',
            r'SCALE[:\s]+1:(\d+)',
            r'Scale[:\s]+1:(\d+)',
            r'@\s*1:(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                self.scale_text = f"1:{match.group(1)}"
                return float(match.group(1))
        
        return None
    
    def calibrate_from_known_distance(
        self, 
        point1: Tuple[float, float], 
        point2: Tuple[float, float], 
        known_distance: float, 
        units: str = "mm"
    ) -> float:
        """
        Calibrate scale using two points with known distance
        
        Args:
            point1: First point (x, y) in pixels
            point2: Second point (x, y) in pixels
            known_distance: Known distance between points
            units: Units of known_distance
            
        Returns:
            Scale ratio (pixels per unit)
        """
        pixel_distance = np.sqrt(
            (point2[0] - point1[0])**2 + 
            (point2[1] - point1[1])**2
        )
        
        self.scale_ratio = pixel_distance / known_distance
        self.units = units
        self.calibration_points = [point1, point2]
        
        return self.scale_ratio
    
    def calibrate_from_scale_bar(self, image: np.ndarray) -> Optional[float]:
        """
        Attempt to automatically detect and calibrate from scale bar
        
        Args:
            image: Image as numpy array
            
        Returns:
            Scale ratio or None
        """
        # This is a simplified implementation
        # In production, you'd use more sophisticated image processing
        
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        else:
            gray = image
        
        # Look for scale bar patterns (horizontal lines with text)
        # This is a placeholder for more sophisticated detection
        
        return None
    
    def pixels_to_real_distance(
        self, 
        pixel_distance: float, 
        target_units: str = None
    ) -> float:
        """
        Convert pixel distance to real-world distance
        
        Args:
            pixel_distance: Distance in pixels
            target_units: Target units (if different from calibrated units)
            
        Returns:
            Real-world distance
        """
        if self.scale_ratio is None:
            raise ValueError("Scale not calibrated. Call calibrate methods first.")
        
        real_distance = pixel_distance / self.scale_ratio
        
        if target_units and target_units != self.units:
            real_distance = self._convert_units(real_distance, self.units, target_units)
        
        return real_distance
    
    def real_to_pixel_distance(self, real_distance: float, units: str = None) -> float:
        """
        Convert real-world distance to pixels
        
        Args:
            real_distance: Distance in real-world units
            units: Units of real_distance (if different from calibrated units)
            
        Returns:
            Distance in pixels
        """
        if self.scale_ratio is None:
            raise ValueError("Scale not calibrated. Call calibrate methods first.")
        
        if units and units != self.units:
            real_distance = self._convert_units(real_distance, units, self.units)
        
        return real_distance * self.scale_ratio
    
    def _convert_units(self, value: float, from_units: str, to_units: str) -> float:
        """
        Convert between different units
        
        Args:
            value: Value to convert
            from_units: Source units
            to_units: Target units
            
        Returns:
            Converted value
        """
        # Conversion factors to meters
        to_meters = {
            'mm': 0.001,
            'cm': 0.01,
            'm': 1.0,
            'km': 1000.0,
            'in': 0.0254,
            'ft': 0.3048,
            'yd': 0.9144,
            'mi': 1609.34
        }
        
        if from_units not in to_meters or to_units not in to_meters:
            raise ValueError(f"Unsupported units: {from_units} or {to_units}")
        
        # Convert to meters, then to target units
        in_meters = value * to_meters[from_units]
        return in_meters / to_meters[to_units]
    
    def calculate_area(
        self, 
        pixel_area: float, 
        target_units: str = None
    ) -> float:
        """
        Convert pixel area to real-world area
        
        Args:
            pixel_area: Area in square pixels
            target_units: Target area units
            
        Returns:
            Real-world area
        """
        if self.scale_ratio is None:
            raise ValueError("Scale not calibrated.")
        
        real_area = pixel_area / (self.scale_ratio ** 2)
        
        if target_units and target_units != self.units:
            # For area, we need to convert squared units
            conversion = self._convert_units(1, self.units, target_units)
            real_area = real_area * (conversion ** 2)
        
        return real_area
    
    def get_scale_info(self) -> Dict:
        """Get current scale information"""
        return {
            'scale_text': self.scale_text,
            'scale_ratio': self.scale_ratio,
            'units': self.units,
            'calibrated': self.scale_ratio is not None,
            'calibration_points': self.calibration_points
        }
    
    def set_scale_from_ratio(self, scale_denominator: float, units: str = "mm", dpi: int = 300):
        """
        Set scale from scale ratio (e.g., 1:100)
        
        Args:
            scale_denominator: Scale denominator (e.g., 100 for 1:100)
            units: Drawing units
            dpi: Image DPI
        """
        # Convert based on DPI
        # At 300 DPI, 1 inch = 300 pixels = 25.4 mm
        pixels_per_mm = dpi / 25.4
        
        # For scale 1:100, 1mm on drawing = 100mm in reality
        # So pixels_per_mm represents pixels per drawing mm
        self.scale_ratio = pixels_per_mm / scale_denominator
        self.scale_text = f"1:{int(scale_denominator)}"
        self.units = units
