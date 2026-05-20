"""
Color Manager - Manage colors for measurements and markups
"""
from typing import Dict, List, Tuple
import colorsys


class ColorManager:
    """Manage color coding for measurements and categories"""
    
    # Predefined color schemes for quantity surveying
    STANDARD_COLORS = {
        # Structural
        'Walls': '#FF6B6B',
        'Columns': '#4ECDC4',
        'Beams': '#45B7D1',
        'Slabs': '#96CEB4',
        'Foundations': '#8B4513',
        
        # Architectural
        'Doors': '#FFD93D',
        'Windows': '#6BCB77',
        'Partitions': '#FFA07A',
        
        # MEP
        'Electrical': '#FFFF00',
        'Plumbing': '#0000FF',
        'HVAC': '#00CED1',
        'Fire Protection': '#FF0000',
        
        # Finishes
        'Flooring': '#DEB887',
        'Ceiling': '#F5F5DC',
        'Paint': '#FFB6C1',
        'Tiling': '#D3D3D3',
        
        # External
        'Roofing': '#8B0000',
        'Cladding': '#708090',
        'Landscaping': '#228B22',
        
        # General
        'General': '#808080',
        'Demolition': '#FF4500',
        'Temporary': '#FFA500'
    }
    
    def __init__(self):
        self.custom_colors: Dict[str, str] = {}
        self.color_to_category: Dict[str, List[str]] = {}
        self._build_reverse_mapping()
    
    def _build_reverse_mapping(self):
        """Build reverse mapping from colors to categories"""
        for category, color in self.STANDARD_COLORS.items():
            if color not in self.color_to_category:
                self.color_to_category[color] = []
            self.color_to_category[color].append(category)
    
    def get_color_for_category(self, category: str) -> str:
        """
        Get color for a category
        
        Args:
            category: Category name
            
        Returns:
            Hex color code
        """
        # Check custom colors first
        if category in self.custom_colors:
            return self.custom_colors[category]
        
        # Check standard colors
        if category in self.STANDARD_COLORS:
            return self.STANDARD_COLORS[category]
        
        # Generate a color based on hash if not found
        return self._generate_color_from_string(category)
    
    def set_custom_color(self, category: str, color: str):
        """
        Set custom color for a category
        
        Args:
            category: Category name
            color: Hex color code
        """
        if not color.startswith('#'):
            color = f'#{color}'
        
        self.custom_colors[category] = color
        
        # Update reverse mapping
        if color not in self.color_to_category:
            self.color_to_category[color] = []
        if category not in self.color_to_category[color]:
            self.color_to_category[color].append(category)
    
    def get_categories_for_color(self, color: str) -> List[str]:
        """Get all categories using a specific color"""
        return self.color_to_category.get(color, [])
    
    def _generate_color_from_string(self, text: str) -> str:
        """
        Generate a consistent color from a string
        
        Args:
            text: Input string
            
        Returns:
            Hex color code
        """
        # Use hash to generate consistent color
        hash_value = hash(text)
        hue = (hash_value % 360) / 360.0
        saturation = 0.7
        lightness = 0.6
        
        rgb = colorsys.hls_to_rgb(hue, lightness, saturation)
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        
        return hex_color
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def adjust_brightness(self, hex_color: str, factor: float) -> str:
        """
        Adjust brightness of a color
        
        Args:
            hex_color: Hex color code
            factor: Brightness factor (0.0 to 2.0, 1.0 = no change)
            
        Returns:
            Adjusted hex color
        """
        rgb = self.hex_to_rgb(hex_color)
        adjusted = tuple(int(min(255, max(0, c * factor))) for c in rgb)
        return self.rgb_to_hex(adjusted)
    
    def get_contrast_color(self, hex_color: str) -> str:
        """
        Get contrasting color (black or white) for text on colored background
        
        Args:
            hex_color: Background hex color
            
        Returns:
            Contrasting hex color
        """
        rgb = self.hex_to_rgb(hex_color)
        # Calculate luminance
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        
        return '#FFFFFF' if luminance < 0.5 else '#000000'
    
    def get_all_colors(self) -> Dict[str, str]:
        """Get all colors (standard + custom)"""
        all_colors = self.STANDARD_COLORS.copy()
        all_colors.update(self.custom_colors)
        return all_colors
    
    def export_color_scheme(self) -> Dict:
        """Export color scheme"""
        return {
            'standard_colors': self.STANDARD_COLORS,
            'custom_colors': self.custom_colors
        }
    
    def import_color_scheme(self, scheme: Dict):
        """Import color scheme"""
        if 'custom_colors' in scheme:
            self.custom_colors = scheme['custom_colors']
            self._build_reverse_mapping()
