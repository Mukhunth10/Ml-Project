"""
Standards Manager - Unified interface for all standards
"""
from typing import Dict, List, Optional, Union
from enum import Enum
from .nrm2_standard import NRM2Standard, NRM2Item
from .cesmm4_standard import CESMM4Standard, CESMM4Item
from .arm_standard import ARMStandard, ARMItem


class StandardType(Enum):
    """Types of measurement standards"""
    NRM2 = "nrm2"
    CESMM4 = "cesmm4"
    ARM = "arm"


class StandardsManager:
    """Manage multiple measurement standards"""
    
    def __init__(self, default_standard: StandardType = StandardType.NRM2):
        """
        Initialize standards manager
        
        Args:
            default_standard: Default standard to use
        """
        self.nrm2 = NRM2Standard()
        self.cesmm4 = CESMM4Standard()
        self.arm = ARMStandard()
        self.active_standard = default_standard
    
    def set_active_standard(self, standard_type: StandardType):
        """Set the active measurement standard"""
        self.active_standard = standard_type
    
    def get_active_standard(self) -> Union[NRM2Standard, CESMM4Standard, ARMStandard]:
        """Get the active standard object"""
        if self.active_standard == StandardType.NRM2:
            return self.nrm2
        elif self.active_standard == StandardType.CESMM4:
            return self.cesmm4
        elif self.active_standard == StandardType.ARM:
            return self.arm
        else:
            return self.nrm2
    
    def search_all_standards(self, keyword: str) -> Dict[str, List]:
        """
        Search across all standards
        
        Args:
            keyword: Search keyword
            
        Returns:
            Dictionary with results from each standard
        """
        results = {}
        
        # Search NRM2
        nrm2_results = self.nrm2.search_items(keyword)
        if nrm2_results:
            results['NRM2'] = nrm2_results
        
        # Search CESMM4
        cesmm4_results = [
            item for item in self.cesmm4.items.values()
            if keyword.lower() in item.description.lower()
        ]
        if cesmm4_results:
            results['CESMM4'] = cesmm4_results
        
        # Search ARM
        arm_results = [
            item for item in self.arm.items.values()
            if keyword.lower() in item.description.lower()
        ]
        if arm_results:
            results['ARM'] = arm_results
        
        return results
    
    def get_standard_info(self, standard_type: StandardType) -> Dict:
        """Get information about a specific standard"""
        info = {
            StandardType.NRM2: {
                'name': 'New Rules of Measurement 2',
                'region': 'UK',
                'application': 'Building works',
                'publisher': 'RICS'
            },
            StandardType.CESMM4: {
                'name': 'Civil Engineering Standard Method of Measurement, 4th Edition',
                'region': 'UK',
                'application': 'Civil engineering works',
                'publisher': 'ICE'
            },
            StandardType.ARM: {
                'name': 'Agreed Rules of Measurement',
                'region': 'Ireland',
                'application': 'Building works',
                'publisher': 'SCSI/CIF'
            }
        }
        
        return info.get(standard_type, {})
    
    def recommend_standard(self, project_type: str, region: str) -> StandardType:
        """
        Recommend a standard based on project type and region
        
        Args:
            project_type: 'building', 'civil', or 'infrastructure'
            region: 'uk' or 'ireland'
            
        Returns:
            Recommended standard type
        """
        region = region.lower()
        project_type = project_type.lower()
        
        if region == 'ireland':
            return StandardType.ARM
        elif project_type in ['civil', 'infrastructure']:
            return StandardType.CESMM4
        else:
            return StandardType.NRM2
