#!/usr/bin/env python3
"""
PDF Export Module for FertiVision-CodeLM System
Generates professional medical reports in PDF format
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.colors import black, blue, grey, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
import os
import datetime
from typing import Dict, Any
import base64
from io import BytesIO
from PIL import Image as PILImage

class PDFReportGenerator:
    def __init__(self, output_folder: str = "exports"):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for medical reports"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.darkblue,
            alignment=TA_CENTER
        ))
        
        # Subheader style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue,
            alignment=TA_LEFT
        ))
        
        # Analysis text style
        self.styles.add(ParagraphStyle(
            name='AnalysisText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=8,
            leftIndent=20
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
    
    def create_info_table(self, info_data):
        """Create simple info table with key-value pairs"""
        table = Table(info_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        return table
    
    def create_header_table(self, analysis_data: Dict[str, Any]):
        """Create header table with patient and analysis info"""
        # Patient info data
        data = [
            ['Analysis ID:', analysis_data.get('analysis_id', 'N/A'), 
             'Date:', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Analysis Type:', analysis_data.get('analysis_type', 'N/A').title(), 
             'System:', 'FertiVision-CodeLM AI'],
            ['Classification:', analysis_data.get('classification', 'N/A'), 
             'Status:', 'Completed']
        ]
        
        table = Table(data, colWidths=[1.2*inch, 2.3*inch, 1*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        return table
    
    def add_image_to_report(self, image_path: str, max_width: float = 4*inch):
        """Add image to report with proper sizing"""
        try:
            if os.path.exists(image_path):
                # Open and resize image if needed
                pil_img = PILImage.open(image_path)
                
                # Calculate dimensions maintaining aspect ratio
                width, height = pil_img.size
                aspect_ratio = height / width
                
                if width > max_width:
                    new_width = max_width
                    new_height = max_width * aspect_ratio
                else:
                    new_width = width
                    new_height = height
                
                # Create ReportLab image
                img = Image(image_path, width=new_width, height=new_height)
                return img
        except Exception as e:
            print(f"Error adding image: {e}")
        
        return None
    
    def generate_follicle_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate follicle analysis PDF report"""
        filename = f"follicle_analysis_{analysis_data.get('scan_id', 'unknown')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Header
        story.append(Paragraph("FOLLICLE SCAN ANALYSIS REPORT", self.styles['CustomHeader']))
        story.append(Spacer(1, 20))
        
        # Patient/Scan Info
        info_data = [
            ['Scan ID:', analysis_data.get('scan_id', 'N/A')],
            ['Analysis Date:', analysis_data.get('timestamp', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))],
            ['Classification:', analysis_data.get('classification', 'N/A')],
        ]
        info_table = self.create_info_table(info_data)
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # AI Analysis
        if 'image_analysis' in analysis_data:
            story.append(Paragraph("AI ANALYSIS", self.styles['CustomSubHeader']))
            analysis_text = analysis_data['image_analysis']
            story.append(Paragraph(analysis_text, self.styles['AnalysisText']))
            story.append(Spacer(1, 20))
        
        # Footer
        footer_text = f"""
        <para align="center">
        Generated by FertiVision-CodeLM AI-Enhanced Reproductive Classification System<br/>
        Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
        This report is for clinical reference only.
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['Footer']))
        
        doc.build(story)
        return filepath

    def generate_oocyte_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate oocyte analysis PDF report"""
        filename = f"oocyte_analysis_{analysis_data.get('oocyte_id', 'unknown')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        story.append(Paragraph("OOCYTE GRADING REPORT", self.styles['CustomHeader']))
        story.append(Spacer(1, 20))
        
        info_data = [
            ['Oocyte ID:', analysis_data.get('oocyte_id', 'N/A')],
            ['Classification:', analysis_data.get('classification', 'N/A')],
        ]
        info_table = self.create_info_table(info_data)
        story.append(info_table)
        
        doc.build(story)
        return filepath

    def generate_embryo_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate embryo analysis PDF report"""
        filename = f"embryo_analysis_{analysis_data.get('embryo_id', 'unknown')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        story.append(Paragraph("EMBRYO CLASSIFICATION REPORT", self.styles['CustomHeader']))
        story.append(Spacer(1, 20))
        
        info_data = [
            ['Embryo ID:', analysis_data.get('embryo_id', 'N/A')],
            ['Classification:', analysis_data.get('classification', 'N/A')],
        ]
        info_table = self.create_info_table(info_data)
        story.append(info_table)
        
        doc.build(story)
        return filepath

    def generate_hysteroscopy_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate hysteroscopy analysis PDF report"""
        filename = f"hysteroscopy_analysis_{analysis_data.get('procedure_id', 'unknown')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        story.append(Paragraph("HYSTEROSCOPY ANALYSIS REPORT", self.styles['CustomHeader']))
        story.append(Spacer(1, 20))
        
        info_data = [
            ['Procedure ID:', analysis_data.get('procedure_id', 'N/A')],
            ['Classification:', analysis_data.get('classification', 'N/A')],
        ]
        info_table = self.create_info_table(info_data)
        story.append(info_table)
        
        doc.build(story)
        return filepath

    def generate_sperm_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate sperm analysis PDF report"""
        filename = f"sperm_analysis_{analysis_data.get('sample_id', 'unknown')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        title = Paragraph("SPERM ANALYSIS REPORT", self.styles['CustomHeader'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Header table
        header_table = self.create_header_table(analysis_data)
        story.append(header_table)
        story.append(Spacer(1, 20))
        
        # Add image if available
        if 'image_path' in analysis_data:
            img = self.add_image_to_report(analysis_data['image_path'])
            if img:
                story.append(Paragraph("Sample Image:", self.styles['CustomSubHeader']))
                story.append(img)
                story.append(Spacer(1, 15))
        
        # Analysis Results
        story.append(Paragraph("ANALYSIS RESULTS", self.styles['CustomSubHeader']))
        
        # Parse and format analysis text
        analysis_text = analysis_data.get('image_analysis', '')
        if analysis_text:
            # Split by sections
            sections = analysis_text.split('\n\n')
            for section in sections:
                if section.strip():
                    lines = section.split('\n')
                    for line in lines:
                        if line.strip():
                            if line.strip().endswith(':'):
                                # Section header
                                p = Paragraph(f"<b>{line.strip()}</b>", self.styles['Normal'])
                            else:
                                # Regular content
                                p = Paragraph(line.strip(), self.styles['AnalysisText'])
                            story.append(p)
                    story.append(Spacer(1, 10))
        
        # Parameters table if available
        if hasattr(analysis_data, 'get') and analysis_data.get('parameters'):
            story.append(Paragraph("MEASURED PARAMETERS", self.styles['CustomSubHeader']))
            params = analysis_data['parameters']
            param_data = [['Parameter', 'Value', 'Reference Range']]
            
            if 'concentration' in params:
                param_data.append(['Concentration', f"{params['concentration']} million/mL", "15-200 million/mL"])
            if 'progressive_motility' in params:
                param_data.append(['Progressive Motility', f"{params['progressive_motility']}%", "≥32%"])
            if 'normal_morphology' in params:
                param_data.append(['Normal Morphology', f"{params['normal_morphology']}%", "≥4%"])
            
            param_table = Table(param_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
            param_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            story.append(param_table)
            story.append(Spacer(1, 20))
        
        # Footer
        footer_text = f"""
        <para align="center">
        Generated by FertiVision-CodeLM AI-Enhanced Reproductive Classification System<br/>
        Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
        This report is for clinical reference only. Results should be interpreted by qualified medical professionals.
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['Footer']))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def generate_embryo_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate embryo analysis PDF report"""
        filename = f"embryo_analysis_{analysis_data.get('embryo_id', 'unknown')}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        title = Paragraph("EMBRYO ANALYSIS REPORT", self.styles['CustomHeader'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Header table
        header_table = self.create_header_table(analysis_data)
        story.append(header_table)
        story.append(Spacer(1, 20))
        
        # Add image if available
        if 'image_path' in analysis_data:
            img = self.add_image_to_report(analysis_data['image_path'])
            if img:
                story.append(Paragraph("Embryo Image:", self.styles['CustomSubHeader']))
                story.append(img)
                story.append(Spacer(1, 15))
        
        # Analysis Results
        story.append(Paragraph("MORPHOLOGICAL ASSESSMENT", self.styles['CustomSubHeader']))
        
        # Parse and format analysis text
        analysis_text = analysis_data.get('image_analysis', '')
        if analysis_text:
            sections = analysis_text.split('\n\n')
            for section in sections:
                if section.strip():
                    lines = section.split('\n')
                    for line in lines:
                        if line.strip():
                            if line.strip().endswith(':'):
                                p = Paragraph(f"<b>{line.strip()}</b>", self.styles['Normal'])
                            else:
                                p = Paragraph(line.strip(), self.styles['AnalysisText'])
                            story.append(p)
                    story.append(Spacer(1, 10))
        
        # Footer
        footer_text = f"""
        <para align="center">
        Generated by FertiVision-CodeLM AI-Enhanced Reproductive Classification System<br/>
        Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
        This report is for clinical reference only. Results should be interpreted by qualified embryologists.
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['Footer']))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def generate_general_report(self, analysis_data: Dict[str, Any]) -> str:
        """Generate general analysis PDF report for follicle/hysteroscopy/oocyte"""
        analysis_type = analysis_data.get('analysis_type', 'general')
        analysis_id = analysis_data.get('analysis_id', 'unknown')
        
        filename = f"{analysis_type}_analysis_{analysis_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=A4,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        title = Paragraph(f"{analysis_type.upper()} ANALYSIS REPORT", self.styles['CustomHeader'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Header table
        header_table = self.create_header_table(analysis_data)
        story.append(header_table)
        story.append(Spacer(1, 20))
        
        # Add image if available
        if 'image_path' in analysis_data:
            img = self.add_image_to_report(analysis_data['image_path'])
            if img:
                story.append(Paragraph("Analysis Image:", self.styles['CustomSubHeader']))
                story.append(img)
                story.append(Spacer(1, 15))
        
        # Analysis Results
        story.append(Paragraph("ANALYSIS RESULTS", self.styles['CustomSubHeader']))
        
        # Parse and format analysis text
        analysis_text = analysis_data.get('image_analysis', '')
        if analysis_text:
            sections = analysis_text.split('\n\n')
            for section in sections:
                if section.strip():
                    lines = section.split('\n')
                    for line in lines:
                        if line.strip():
                            if line.strip().endswith(':'):
                                p = Paragraph(f"<b>{line.strip()}</b>", self.styles['Normal'])
                            else:
                                p = Paragraph(line.strip(), self.styles['AnalysisText'])
                            story.append(p)
                    story.append(Spacer(1, 10))
        
        # Footer
        footer_text = f"""
        <para align="center">
        Generated by FertiVision-CodeLM AI-Enhanced Reproductive Classification System<br/>
        Report Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
        This report is for clinical reference only. Results should be interpreted by qualified medical professionals.
        </para>
        """
        story.append(Paragraph(footer_text, self.styles['Footer']))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def generate_report(self, analysis_type: str, analysis_data: Dict[str, Any]) -> str:
        """Generate PDF report for any analysis type"""
        try:
            if analysis_type == 'sperm':
                return self.generate_sperm_report(analysis_data)
            elif analysis_type == 'oocyte':
                return self.generate_oocyte_report(analysis_data)
            elif analysis_type == 'embryo':
                return self.generate_embryo_report(analysis_data)
            elif analysis_type == 'follicle':
                return self.generate_follicle_report(analysis_data)
            elif analysis_type == 'hysteroscopy':
                return self.generate_hysteroscopy_report(analysis_data)
            else:
                raise ValueError(f"Unsupported analysis type: {analysis_type}")
        except Exception as e:
            print(f"Error generating PDF report: {e}")
            raise
    
    def generate_batch_report(self, analysis_ids: list) -> str:
        """Generate combined PDF report for multiple analyses"""
        filename = f"batch_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_folder, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Title page
        story.append(Paragraph("BATCH ANALYSIS REPORT", self.styles['CustomHeader']))
        story.append(Spacer(1, 20))
        
        # Summary table
        summary_data = [['Analysis ID', 'Type', 'Date', 'Classification']]
        for analysis_id in analysis_ids:
            # This would need to be implemented to fetch actual data
            summary_data.append([analysis_id, 'Mixed', datetime.datetime.now().strftime('%Y-%m-%d'), 'Varies'])
        
        summary_table = Table(summary_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 30))
        
        # Individual reports would be added here
        story.append(Paragraph("DETAILED REPORTS", self.styles['CustomSubHeader']))
        story.append(Paragraph("Individual analysis reports would be included here in the full implementation.", self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filepath
