"""
BOQ Generator - Generate Bill of Quantities from measurements
"""
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class BOQItem:
    """Represents a single BOQ item"""
    item_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    item_number: str = ""
    description: str = ""
    unit: str = ""
    quantity: float = 0.0
    rate: float = 0.0
    amount: float = 0.0
    
    # Standard reference
    standard_code: Optional[str] = None
    work_section: str = ""
    category: str = ""
    
    # Additional details
    notes: str = ""
    drawing_reference: str = ""
    specification: str = ""
    
    # Hierarchy
    level: int = 1  # For grouping and sub-items
    parent_id: Optional[str] = None
    
    def calculate_amount(self):
        """Calculate amount from quantity and rate"""
        self.amount = self.quantity * self.rate
        return self.amount
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'item_id': self.item_id,
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
            'drawing_reference': self.drawing_reference,
            'specification': self.specification,
            'level': self.level,
            'parent_id': self.parent_id
        }


class BOQGenerator:
    """Generate Bill of Quantities from measurements"""
    
    def __init__(self, project_name: str = "Untitled Project"):
        """
        Initialize BOQ generator
        
        Args:
            project_name: Name of the project
        """
        self.project_name = project_name
        self.items: List[BOQItem] = []
        self.metadata = {
            'project_name': project_name,
            'created_date': datetime.now().isoformat(),
            'version': '1.0',
            'currency': 'GBP',
            'vat_rate': 0.20  # 20% VAT
        }
    
    def add_item(self, item: BOQItem) -> BOQItem:
        """Add a BOQ item"""
        if not item.item_number:
            item.item_number = self._generate_item_number()
        self.items.append(item)
        return item
    
    def create_item(
        self,
        description: str,
        unit: str,
        quantity: float,
        rate: float = 0.0,
        **kwargs
    ) -> BOQItem:
        """
        Create and add a BOQ item
        
        Args:
            description: Item description
            unit: Unit of measurement
            quantity: Quantity
            rate: Unit rate
            **kwargs: Additional item properties
            
        Returns:
            Created BOQ item
        """
        item = BOQItem(
            description=description,
            unit=unit,
            quantity=quantity,
            rate=rate,
            **kwargs
        )
        item.calculate_amount()
        return self.add_item(item)
    
    def create_section_header(self, title: str, level: int = 1) -> BOQItem:
        """Create a section header"""
        item = BOQItem(
            description=title,
            unit="",
            quantity=0.0,
            level=level
        )
        return self.add_item(item)
    
    def _generate_item_number(self) -> str:
        """Generate sequential item number"""
        return f"{len(self.items) + 1:03d}"
    
    def import_from_measurements(self, measurements: List[Dict]):
        """
        Import measurements and create BOQ items
        
        Args:
            measurements: List of measurement dictionaries
        """
        # Group measurements by category
        grouped = {}
        for measurement in measurements:
            category = measurement.get('category', 'General')
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(measurement)
        
        # Create BOQ items by category
        for category, items in grouped.items():
            # Add section header
            self.create_section_header(category, level=1)
            
            # Add items
            for measurement in items:
                unit = measurement.get('units', 'nr')
                
                # Determine quantity based on measurement type
                if measurement.get('area'):
                    quantity = measurement['area']
                    unit = 'm²'
                elif measurement.get('length'):
                    quantity = measurement['length']
                    unit = 'm'
                elif measurement.get('count'):
                    quantity = measurement['count']
                    unit = 'nr'
                else:
                    quantity = 1.0
                
                self.create_item(
                    description=measurement.get('description', measurement.get('label', 'Item')),
                    unit=unit,
                    quantity=quantity,
                    category=category,
                    drawing_reference=measurement.get('drawing_ref', ''),
                    notes=measurement.get('notes', ''),
                    level=2
                )
    
    def get_item_by_id(self, item_id: str) -> Optional[BOQItem]:
        """Get item by ID"""
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None
    
    def update_item(self, item_id: str, **updates) -> bool:
        """Update an item's properties"""
        item = self.get_item_by_id(item_id)
        if item:
            for key, value in updates.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            if 'quantity' in updates or 'rate' in updates:
                item.calculate_amount()
            return True
        return False
    
    def delete_item(self, item_id: str) -> bool:
        """Delete an item"""
        item = self.get_item_by_id(item_id)
        if item:
            self.items.remove(item)
            return True
        return False
    
    def get_items_by_section(self, section: str) -> List[BOQItem]:
        """Get all items in a work section"""
        return [item for item in self.items if item.work_section == section]
    
    def get_items_by_category(self, category: str) -> List[BOQItem]:
        """Get all items in a category"""
        return [item for item in self.items if item.category == category]
    
    def calculate_totals(self) -> Dict:
        """Calculate BOQ totals"""
        subtotal = sum(item.amount for item in self.items)
        vat = subtotal * self.metadata.get('vat_rate', 0.20)
        total = subtotal + vat
        
        return {
            'subtotal': subtotal,
            'vat': vat,
            'vat_rate': self.metadata.get('vat_rate', 0.20),
            'total': total,
            'currency': self.metadata.get('currency', 'GBP'),
            'item_count': len(self.items)
        }
    
    def get_summary_by_section(self) -> Dict[str, float]:
        """Get cost summary by work section"""
        summary = {}
        for item in self.items:
            section = item.work_section or 'Unclassified'
            summary[section] = summary.get(section, 0.0) + item.amount
        return summary
    
    def get_summary_by_category(self) -> Dict[str, float]:
        """Get cost summary by category"""
        summary = {}
        for item in self.items:
            category = item.category or 'General'
            summary[category] = summary.get(category, 0.0) + item.amount
        return summary
    
    def renumber_items(self):
        """Renumber all items sequentially"""
        for i, item in enumerate(self.items, start=1):
            if item.level > 1:  # Don't number section headers
                item.item_number = f"{i:03d}"
    
    def sort_items(self, by: str = 'item_number'):
        """Sort items"""
        if by == 'item_number':
            self.items.sort(key=lambda x: x.item_number)
        elif by == 'category':
            self.items.sort(key=lambda x: (x.category, x.item_number))
        elif by == 'amount':
            self.items.sort(key=lambda x: x.amount, reverse=True)
    
    def to_dict(self) -> Dict:
        """Convert entire BOQ to dictionary"""
        return {
            'metadata': self.metadata,
            'items': [item.to_dict() for item in self.items],
            'totals': self.calculate_totals()
        }
