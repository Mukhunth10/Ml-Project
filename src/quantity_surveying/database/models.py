"""
Database Models using SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Project(Base):
    """Project model"""
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    location = Column(String(200))
    client = Column(String(200))
    standard_type = Column(String(50))  # NRM2, CESMM4, ARM
    currency = Column(String(10), default='GBP')
    vat_rate = Column(Float, default=0.20)
    
    # Relationships
    measurements = relationship('Measurement', back_populates='project', cascade='all, delete-orphan')
    boq_items = relationship('BOQItem', back_populates='project', cascade='all, delete-orphan')
    drawings = relationship('Drawing', back_populates='project', cascade='all, delete-orphan')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'client': self.client,
            'standard_type': self.standard_type,
            'currency': self.currency,
            'vat_rate': self.vat_rate,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Drawing(Base):
    """Drawing/PDF model"""
    __tablename__ = 'drawings'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    filename = Column(String(200), nullable=False)
    file_path = Column(String(500))
    drawing_number = Column(String(100))
    revision = Column(String(50))
    scale = Column(String(50))
    pages_count = Column(Integer, default=1)
    
    # Relationships
    project = relationship('Project', back_populates='drawings')
    measurements = relationship('Measurement', back_populates='drawing')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'filename': self.filename,
            'drawing_number': self.drawing_number,
            'revision': self.revision,
            'scale': self.scale,
            'pages_count': self.pages_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Measurement(Base):
    """Measurement shape model"""
    __tablename__ = 'measurements'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    drawing_id = Column(Integer, ForeignKey('drawings.id'))
    
    shape_id = Column(String(100), unique=True, nullable=False)
    shape_type = Column(String(50), nullable=False)  # line, polyline, rectangle, etc.
    points = Column(JSON)  # Store points as JSON
    
    category = Column(String(100), default='General')
    label = Column(String(200))
    description = Column(Text)
    
    # Measurements
    length = Column(Float)
    area = Column(Float)
    volume = Column(Float)
    count = Column(Integer)
    units = Column(String(20), default='mm')
    
    # Visual properties
    color = Column(String(20))
    layer = Column(String(100))
    visible = Column(Boolean, default=True)
    locked = Column(Boolean, default=False)
    
    # Relationships
    project = relationship('Project', back_populates='measurements')
    drawing = relationship('Drawing', back_populates='measurements')
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'drawing_id': self.drawing_id,
            'shape_id': self.shape_id,
            'shape_type': self.shape_type,
            'points': self.points,
            'category': self.category,
            'label': self.label,
            'description': self.description,
            'length': self.length,
            'area': self.area,
            'volume': self.volume,
            'count': self.count,
            'units': self.units,
            'color': self.color,
            'layer': self.layer,
            'visible': self.visible,
            'locked': self.locked,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BOQItem(Base):
    """Bill of Quantities item model"""
    __tablename__ = 'boq_items'
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    item_number = Column(String(50))
    description = Column(Text, nullable=False)
    unit = Column(String(20))
    quantity = Column(Float, default=0.0)
    rate = Column(Float, default=0.0)
    amount = Column(Float, default=0.0)
    
    standard_code = Column(String(50))
    work_section = Column(String(100))
    category = Column(String(100))
    
    notes = Column(Text)
    specification = Column(Text)
    
    level = Column(Integer, default=1)
    parent_id = Column(Integer, ForeignKey('boq_items.id'))
    
    # Relationships
    project = relationship('Project', back_populates='boq_items')
    children = relationship('BOQItem', backref='parent', remote_side=[id])
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'item_number': self.item_number,
            'description': self.description,
            'unit': self.unit,
            'quantity': self.quantity,
            'rate': self.rate,
            'amount': self.amount,
            'standard_code': self.standard_code,
            'work_section': self.work_section,
            'category': self.category,
            'notes': self.notes,
            'level': self.level,
            'parent_id': self.parent_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
