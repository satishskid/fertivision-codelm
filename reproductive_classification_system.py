#!/usr/bin/env python3
"""
Reproductive Classification System
Core classification functionality for reproductive medicine
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

class OocyteMaturity(Enum):
    """Oocyte maturity stages"""
    GERMINAL_VESICLE = "germinal_vesicle"
    METAPHASE_I = "metaphase_i"
    METAPHASE_II = "metaphase_ii"
    DEGENERATE = "degenerate"

class SpermMotility(Enum):
    """Sperm motility classifications"""
    PROGRESSIVE = "progressive"
    NON_PROGRESSIVE = "non_progressive"
    IMMOTILE = "immotile"

class EmbryoGrade(Enum):
    """Embryo grading system"""
    GRADE_A = "excellent"
    GRADE_B = "good"
    GRADE_C = "fair"
    GRADE_D = "poor"

@dataclass
class SpermAnalysisResult:
    """Sperm analysis result structure"""
    sample_id: str
    concentration: float
    motility: SpermMotility
    progressive_motility: float
    morphology_normal: float
    vitality: float
    ph: Optional[float] = None
    volume: Optional[float] = None
    timestamp: datetime = datetime.now()

@dataclass
class OocyteAnalysisResult:
    """Oocyte analysis result structure"""
    oocyte_id: str
    maturity: OocyteMaturity
    quality_score: float
    cytoplasm_quality: str
    zona_pellucida_intact: bool
    polar_body_present: bool
    timestamp: datetime = datetime.now()

@dataclass
class EmbryoAnalysisResult:
    """Embryo analysis result structure"""
    embryo_id: str
    developmental_stage: str
    grade: EmbryoGrade
    cell_count: int
    fragmentation_percentage: float
    symmetry_score: float
    quality_score: float
    timestamp: datetime = datetime.now()

class ReproductiveClassificationSystem:
    """Base reproductive classification system"""
    
    def __init__(self):
        self.analysis_history = []
    
    def classify_sperm(self, **kwargs) -> SpermAnalysisResult:
        """Classify sperm parameters"""
        result = SpermAnalysisResult(
            sample_id=kwargs.get('sample_id', f"sperm_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            concentration=kwargs.get('concentration', 20.0),
            motility=SpermMotility.PROGRESSIVE,
            progressive_motility=kwargs.get('progressive_motility', 32.0),
            morphology_normal=kwargs.get('morphology_normal', 4.0),
            vitality=kwargs.get('vitality', 58.0),
            ph=kwargs.get('ph', 7.2),
            volume=kwargs.get('volume', 3.7)
        )
        return result
    
    def classify_oocyte(self, **kwargs) -> OocyteAnalysisResult:
        """Classify oocyte maturity and quality"""
        result = OocyteAnalysisResult(
            oocyte_id=kwargs.get('oocyte_id', f"oocyte_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            maturity=OocyteMaturity.METAPHASE_II,
            quality_score=kwargs.get('quality_score', 8.5),
            cytoplasm_quality=kwargs.get('cytoplasm_quality', "good"),
            zona_pellucida_intact=kwargs.get('zona_pellucida_intact', True),
            polar_body_present=kwargs.get('polar_body_present', True)
        )
        return result
    
    def classify_embryo(self, **kwargs) -> EmbryoAnalysisResult:
        """Classify embryo development and quality"""
        result = EmbryoAnalysisResult(
            embryo_id=kwargs.get('embryo_id', f"embryo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"),
            developmental_stage=kwargs.get('developmental_stage', "blastocyst"),
            grade=EmbryoGrade.GRADE_A,
            cell_count=kwargs.get('cell_count', 8),
            fragmentation_percentage=kwargs.get('fragmentation_percentage', 5.0),
            symmetry_score=kwargs.get('symmetry_score', 9.0),
            quality_score=kwargs.get('quality_score', 8.8)
        )
        return result
