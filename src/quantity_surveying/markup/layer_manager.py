"""
Layer Manager - Manage drawing layers
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class Layer:
    """Represents a drawing layer"""
    name: str
    visible: bool = True
    locked: bool = False
    color: str = "#000000"
    opacity: float = 1.0
    description: str = ""
    order: int = 0  # Display order (higher = on top)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'visible': self.visible,
            'locked': self.locked,
            'color': self.color,
            'opacity': self.opacity,
            'description': self.description,
            'order': self.order
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Layer':
        """Create from dictionary"""
        return cls(**data)


class LayerManager:
    """Manage drawing layers for organization and visibility control"""
    
    DEFAULT_LAYERS = [
        'Background',
        'Measurements',
        'Annotations',
        'Dimensions',
        'Markup',
        'Notes'
    ]
    
    def __init__(self):
        self.layers: Dict[str, Layer] = {}
        self.active_layer: str = 'Measurements'
        self._initialize_default_layers()
    
    def _initialize_default_layers(self):
        """Initialize default layers"""
        for i, layer_name in enumerate(self.DEFAULT_LAYERS):
            self.layers[layer_name] = Layer(
                name=layer_name,
                order=i,
                description=f"Default {layer_name} layer"
            )
    
    def create_layer(
        self, 
        name: str, 
        visible: bool = True, 
        locked: bool = False,
        color: str = "#000000",
        opacity: float = 1.0,
        description: str = ""
    ) -> Layer:
        """
        Create a new layer
        
        Args:
            name: Layer name
            visible: Initial visibility
            locked: Initial locked state
            color: Default color for layer
            opacity: Layer opacity
            description: Layer description
            
        Returns:
            Created layer
        """
        if name in self.layers:
            raise ValueError(f"Layer '{name}' already exists")
        
        order = max([layer.order for layer in self.layers.values()], default=0) + 1
        
        layer = Layer(
            name=name,
            visible=visible,
            locked=locked,
            color=color,
            opacity=opacity,
            description=description,
            order=order
        )
        
        self.layers[name] = layer
        return layer
    
    def get_layer(self, name: str) -> Optional[Layer]:
        """Get layer by name"""
        return self.layers.get(name)
    
    def delete_layer(self, name: str) -> bool:
        """
        Delete a layer
        
        Args:
            name: Layer name
            
        Returns:
            True if deleted, False if not found
        """
        if name in self.DEFAULT_LAYERS:
            raise ValueError(f"Cannot delete default layer '{name}'")
        
        if name in self.layers:
            del self.layers[name]
            if self.active_layer == name:
                self.active_layer = 'Measurements'
            return True
        return False
    
    def rename_layer(self, old_name: str, new_name: str) -> bool:
        """
        Rename a layer
        
        Args:
            old_name: Current layer name
            new_name: New layer name
            
        Returns:
            True if renamed, False if not found
        """
        if old_name not in self.layers:
            return False
        
        if new_name in self.layers:
            raise ValueError(f"Layer '{new_name}' already exists")
        
        layer = self.layers[old_name]
        layer.name = new_name
        self.layers[new_name] = layer
        del self.layers[old_name]
        
        if self.active_layer == old_name:
            self.active_layer = new_name
        
        return True
    
    def set_active_layer(self, name: str):
        """Set the active layer"""
        if name not in self.layers:
            raise ValueError(f"Layer '{name}' does not exist")
        self.active_layer = name
    
    def get_active_layer(self) -> Layer:
        """Get the active layer"""
        return self.layers[self.active_layer]
    
    def toggle_visibility(self, name: str) -> bool:
        """Toggle layer visibility"""
        if name in self.layers:
            self.layers[name].visible = not self.layers[name].visible
            return self.layers[name].visible
        return False
    
    def set_visibility(self, name: str, visible: bool):
        """Set layer visibility"""
        if name in self.layers:
            self.layers[name].visible = visible
    
    def lock_layer(self, name: str):
        """Lock a layer"""
        if name in self.layers:
            self.layers[name].locked = True
    
    def unlock_layer(self, name: str):
        """Unlock a layer"""
        if name in self.layers:
            self.layers[name].locked = False
    
    def toggle_lock(self, name: str) -> bool:
        """Toggle layer lock state"""
        if name in self.layers:
            self.layers[name].locked = not self.layers[name].locked
            return self.layers[name].locked
        return False
    
    def set_layer_opacity(self, name: str, opacity: float):
        """Set layer opacity (0.0 to 1.0)"""
        if name in self.layers:
            self.layers[name].opacity = max(0.0, min(1.0, opacity))
    
    def set_layer_order(self, name: str, order: int):
        """Set layer display order"""
        if name in self.layers:
            self.layers[name].order = order
    
    def move_layer_up(self, name: str):
        """Move layer up in display order"""
        if name in self.layers:
            self.layers[name].order += 1
    
    def move_layer_down(self, name: str):
        """Move layer down in display order"""
        if name in self.layers:
            self.layers[name].order = max(0, self.layers[name].order - 1)
    
    def get_all_layers(self) -> List[Layer]:
        """Get all layers sorted by order"""
        return sorted(self.layers.values(), key=lambda x: x.order)
    
    def get_visible_layers(self) -> List[Layer]:
        """Get all visible layers sorted by order"""
        return sorted(
            [layer for layer in self.layers.values() if layer.visible],
            key=lambda x: x.order
        )
    
    def hide_all_except(self, name: str):
        """Hide all layers except specified one"""
        for layer_name in self.layers:
            self.layers[layer_name].visible = (layer_name == name)
    
    def show_all(self):
        """Show all layers"""
        for layer in self.layers.values():
            layer.visible = True
    
    def hide_all(self):
        """Hide all layers"""
        for layer in self.layers.values():
            layer.visible = False
    
    def export_layers(self) -> List[Dict]:
        """Export all layers"""
        return [layer.to_dict() for layer in self.get_all_layers()]
    
    def import_layers(self, layers_data: List[Dict]):
        """Import layers from data"""
        for layer_data in layers_data:
            layer = Layer.from_dict(layer_data)
            self.layers[layer.name] = layer
    
    def get_layer_summary(self) -> Dict:
        """Get summary of all layers"""
        return {
            'total_layers': len(self.layers),
            'visible_layers': len(self.get_visible_layers()),
            'active_layer': self.active_layer,
            'layers': [
                {
                    'name': layer.name,
                    'visible': layer.visible,
                    'locked': layer.locked,
                    'order': layer.order
                }
                for layer in self.get_all_layers()
            ]
        }
