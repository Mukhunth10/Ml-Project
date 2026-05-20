"""
PDF Handler - Process PDF drawings and extract information
"""
import io
from typing import List, Dict, Tuple, Optional
import PyPDF2
import pdfplumber
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
import numpy as np
import cv2


class PDFHandler:
    """Handle PDF document processing for quantity surveying"""
    
    def __init__(self, pdf_path: str = None, pdf_bytes: bytes = None):
        """
        Initialize PDF handler
        
        Args:
            pdf_path: Path to PDF file
            pdf_bytes: PDF as bytes (for uploaded files)
        """
        self.pdf_path = pdf_path
        self.pdf_bytes = pdf_bytes
        self.pages_count = 0
        self.metadata = {}
        self.images = []
        self.current_page = 0
        
        if pdf_path or pdf_bytes:
            self._load_pdf()
    
    def _load_pdf(self):
        """Load and analyze PDF"""
        try:
            if self.pdf_path:
                with open(self.pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    self.pages_count = len(pdf_reader.pages)
                    self.metadata = pdf_reader.metadata
            elif self.pdf_bytes:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(self.pdf_bytes))
                self.pages_count = len(pdf_reader.pages)
                self.metadata = pdf_reader.metadata
        except Exception as e:
            raise Exception(f"Error loading PDF: {str(e)}")
    
    def extract_text(self, page_num: int = None) -> Dict[int, str]:
        """
        Extract text from PDF pages
        
        Args:
            page_num: Specific page number (None for all pages)
            
        Returns:
            Dictionary of page number to text content
        """
        text_content = {}
        
        try:
            if self.pdf_path:
                with pdfplumber.open(self.pdf_path) as pdf:
                    if page_num is not None:
                        page = pdf.pages[page_num]
                        text_content[page_num] = page.extract_text() or ""
                    else:
                        for i, page in enumerate(pdf.pages):
                            text_content[i] = page.extract_text() or ""
            elif self.pdf_bytes:
                with pdfplumber.open(io.BytesIO(self.pdf_bytes)) as pdf:
                    if page_num is not None:
                        page = pdf.pages[page_num]
                        text_content[page_num] = page.extract_text() or ""
                    else:
                        for i, page in enumerate(pdf.pages):
                            text_content[i] = page.extract_text() or ""
        except Exception as e:
            raise Exception(f"Error extracting text: {str(e)}")
        
        return text_content
    
    def convert_to_images(self, dpi: int = 300, page_num: int = None) -> List[Image.Image]:
        """
        Convert PDF pages to images
        
        Args:
            dpi: Resolution for conversion
            page_num: Specific page number (None for all pages)
            
        Returns:
            List of PIL Images
        """
        try:
            if self.pdf_path:
                if page_num is not None:
                    images = convert_from_path(
                        self.pdf_path, 
                        dpi=dpi, 
                        first_page=page_num + 1, 
                        last_page=page_num + 1
                    )
                else:
                    images = convert_from_path(self.pdf_path, dpi=dpi)
            elif self.pdf_bytes:
                if page_num is not None:
                    images = convert_from_bytes(
                        self.pdf_bytes, 
                        dpi=dpi, 
                        first_page=page_num + 1, 
                        last_page=page_num + 1
                    )
                else:
                    images = convert_from_bytes(self.pdf_bytes, dpi=dpi)
            else:
                return []
            
            self.images = images
            return images
        except Exception as e:
            raise Exception(f"Error converting PDF to images: {str(e)}")
    
    def extract_drawing_info(self, page_num: int = 0) -> Dict:
        """
        Extract drawing information like scale, title block, etc.
        
        Args:
            page_num: Page number to analyze
            
        Returns:
            Dictionary with drawing information
        """
        drawing_info = {
            'page': page_num,
            'scale': None,
            'title': None,
            'drawing_number': None,
            'revision': None,
            'date': None,
            'dimensions': None
        }
        
        try:
            text_content = self.extract_text(page_num)
            page_text = text_content.get(page_num, "")
            
            # Extract scale information using pattern matching
            import re
            scale_patterns = [
                r'SCALE[:\s]+1:(\d+)',
                r'Scale[:\s]+1:(\d+)',
                r'1:(\d+)',
                r'@\s*1:(\d+)'
            ]
            
            for pattern in scale_patterns:
                match = re.search(pattern, page_text)
                if match:
                    drawing_info['scale'] = f"1:{match.group(1)}"
                    break
            
            # Extract drawing number
            dwg_patterns = [
                r'DWG\s*NO[.:]\s*([\w\-/]+)',
                r'DRAWING\s*NO[.:]\s*([\w\-/]+)',
                r'No[.:]\s*([\w\-/]+)'
            ]
            
            for pattern in dwg_patterns:
                match = re.search(pattern, page_text)
                if match:
                    drawing_info['drawing_number'] = match.group(1)
                    break
            
            # Get page dimensions
            if self.pdf_path:
                with pdfplumber.open(self.pdf_path) as pdf:
                    page = pdf.pages[page_num]
                    drawing_info['dimensions'] = {
                        'width': page.width,
                        'height': page.height
                    }
            elif self.pdf_bytes:
                with pdfplumber.open(io.BytesIO(self.pdf_bytes)) as pdf:
                    page = pdf.pages[page_num]
                    drawing_info['dimensions'] = {
                        'width': page.width,
                        'height': page.height
                    }
            
        except Exception as e:
            print(f"Warning: Could not extract all drawing info: {str(e)}")
        
        return drawing_info
    
    def detect_lines_and_shapes(self, page_num: int = 0) -> Dict:
        """
        Detect lines and shapes in drawing using computer vision
        
        Args:
            page_num: Page number to analyze
            
        Returns:
            Dictionary with detected elements
        """
        if not self.images:
            self.convert_to_images(page_num=page_num)
        
        if page_num >= len(self.images):
            return {}
        
        image = self.images[page_num]
        img_array = np.array(image)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        
        # Line detection using Hough Transform
        lines = cv2.HoughLinesP(
            edges, 
            rho=1, 
            theta=np.pi/180, 
            threshold=100,
            minLineLength=50,
            maxLineGap=10
        )
        
        # Contour detection for shapes
        contours, _ = cv2.findContours(
            edges, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        detected = {
            'lines': lines.tolist() if lines is not None else [],
            'contours': len(contours),
            'image_shape': img_array.shape
        }
        
        return detected
    
    def get_page_info(self) -> List[Dict]:
        """Get information about all pages"""
        pages_info = []
        
        for i in range(self.pages_count):
            info = {
                'page_number': i,
                'drawing_info': self.extract_drawing_info(i)
            }
            pages_info.append(info)
        
        return pages_info
