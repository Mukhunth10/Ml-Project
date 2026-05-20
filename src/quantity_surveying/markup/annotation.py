"""
Annotation - Text annotations and callouts
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import Tuple, Dict, Optional
import uuid
import json
from datetime import datetime


class AnnotationType(Enum):
    """Types of annotations"""
    TEXT = "text"
    CALLOUT = "callout"
    CLOUD = "cloud"
    ARROW = "arrow"
    STAMP = "stamp"
    NOTE = "note"
    DIMENSION = "dimension"


@dataclass
class Annotation:
    """Represents an annotation on a drawing"""
    
    annotation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    annotation_type: AnnotationType = AnnotationType.TEXT
    position: Tuple[float, float] = (0, 0)
    text: str = ""
    color: str = "#000000"
    font_size: int = 12
    font_family: str = "Arial"
    
    # For callouts and arrows
    leader_points: list = field(default_factory=list)
    
    # Visual properties
    background_color: str = "#FFFFFF"
    border_color: str = "#000000"
    border_width: float = 1.0
    opacity: float = 1.0
    
    # Layer and visibility
    layer: str = "annotations"
    visible: bool = True
    locked: bool = False
    
    # Metadata
    author: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'annotation_id': self.annotation_id,
            'annotation_type': self.annotation_type.value,
            'position': self.position,
            'text': self.text,
            'color': self.color,
            'font_size': self.font_size,
            'font_family': self.font_family,
            'leader_points': self.leader_points,
            'background_color': self.background_color,
            'border_color': self.border_color,
            'border_width': self.border_width,
            'opacity': self.opacity,
            'layer': self.layer,
            'visible': self.visible,
            'locked': self.locked,
            'author': self.author,
            'created_at': self.created_at,
            'modified_at': self.modified_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Annotation':
        """Create from dictionary"""
        data = data.copy()
        if 'annotation_type' in data:
            data['annotation_type'] = AnnotationType(data['annotation_type'])
        return cls(**data)
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Annotation':
        """Create from JSON string"""
        return cls.from_dict(json.loads(json_str))
