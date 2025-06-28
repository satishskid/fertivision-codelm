#!/usr/bin/env python3
"""
PDF Export Module for FertiVision
Generates comprehensive fertility reports in PDF format
"""

import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib.colors import HexColor
import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import seaborn as sns
import numpy as np

class FertilityReportPDF:
    """Generate comprehensive fertility reports in PDF format"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
        # Brand colors
        self.primary_color = HexColor('#667eea')
        self.secondary_color = HexColor('#764ba2')
        self.success_color = HexColor('#28a745')
        self.warning_color = HexColor('#ffc107')
        self.danger_color = HexColor('#dc3545')
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#667eea'),
            alignment=1  # Center alignment
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#333333'),
            borderWidth=1,
            borderColor=colors.HexColor('#667eea'),
            borderPadding=10,
            backColor=colors.HexColor('#f8f9fa')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=colors.HexColor('#333333')
        ))
        
        self.styles.add(ParagraphStyle(
            name='ScoreText',
            parent=self.styles['Normal'],
            fontSize=48,
            alignment=1,
            textColor=colors.HexColor('#28a745'),
            spaceAfter=10
        ))

    def generate_patient_report(self, patient_data, fertility_report, documents, output_path=None):
        """Generate a comprehensive patient fertility report"""
        
        if output_path is None:
            output_path = f"fertility_report_{patient_data['patient_id']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build story (content)
        story = []
        
        # Header
        story.extend(self._create_header(patient_data))
        
        # Patient Information
        story.extend(self._create_patient_info_section(patient_data))
        
        # Fertility Score Summary
        story.extend(self._create_fertility_score_section(fertility_report))
        
        # Domain Analysis
        story.extend(self._create_domain_analysis_section(fertility_report))
        
        # Document Summary
        story.extend(self._create_document_summary_section(documents))
        
        # Detailed Findings
        story.extend(self._create_detailed_findings_section(documents))
        
        # Recommendations
        story.extend(self._create_recommendations_section(fertility_report))
        
        # Footer
        story.extend(self._create_footer())
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_header(self, patient_data):
        """Create report header"""
        elements = []
        
        # Title
        title = Paragraph("🔬 FertiVision Comprehensive Fertility Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 20))
        
        # Report info table
        report_data = [
            ['Report Generated:', datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')],
            ['Patient ID:', patient_data['patient_id']],
            ['Medical ID:', patient_data.get('medical_id', 'N/A')],
            ['Report Type:', 'Comprehensive Fertility Assessment']
        ]
        
        table = Table(report_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_patient_info_section(self, patient_data):
        """Create patient information section"""
        elements = []
        
        # Section heading
        heading = Paragraph("Patient Information", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        # Calculate age
        if patient_data.get('date_of_birth'):
            dob = datetime.datetime.strptime(patient_data['date_of_birth'], '%Y-%m-%d')
            age = (datetime.datetime.now() - dob).days // 365
        else:
            age = 'N/A'
        
        # Patient info table
        patient_info = [
            ['Full Name:', patient_data['name']],
            ['Date of Birth:', patient_data.get('date_of_birth', 'N/A')],
            ['Age:', f"{age} years" if age != 'N/A' else 'N/A'],
            ['Gender:', patient_data.get('gender', 'N/A').title()],
            ['Contact:', patient_data.get('contact_number', 'N/A')],
            ['Email:', patient_data.get('email', 'N/A')],
            ['Registration Date:', patient_data.get('created_at', 'N/A')]
        ]
        
        table = Table(patient_info, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#495057')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_fertility_score_section(self, fertility_report):
        """Create fertility score summary section"""
        elements = []
        
        # Section heading
        heading = Paragraph("Fertility Score Summary", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        # Overall score
        overall_score = fertility_report.get('overall_score', 0)
        score_text = Paragraph(f"{overall_score:.1f}/100", self.styles['ScoreText'])
        elements.append(score_text)
        
        # Score interpretation
        if overall_score >= 80:
            interpretation = "Excellent fertility indicators"
            color = self.success_color
        elif overall_score >= 60:
            interpretation = "Good fertility potential with some areas for improvement"
            color = self.warning_color
        elif overall_score >= 40:
            interpretation = "Moderate fertility challenges identified"
            color = colors.orange
        else:
            interpretation = "Significant fertility concerns require attention"
            color = self.danger_color
        
        interp_style = ParagraphStyle(
            name='Interpretation',
            parent=self.styles['Normal'],
            fontSize=14,
            alignment=1,
            textColor=color,
            fontName='Helvetica-Bold'
        )
        
        interp_text = Paragraph(interpretation, interp_style)
        elements.append(interp_text)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_domain_analysis_section(self, fertility_report):
        """Create domain-specific analysis section"""
        elements = []
        
        # Section heading
        heading = Paragraph("Domain Analysis", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        domain_scores = fertility_report.get('domain_scores', {})
        
        if not domain_scores:
            no_data = Paragraph("No domain analysis available. Upload medical documents for detailed assessment.", 
                              self.styles['CustomNormal'])
            elements.append(no_data)
            elements.append(Spacer(1, 20))
            return elements
        
        # Create domain scores table
        domain_data = [['Domain', 'Score', 'Status']]
        
        for domain, score in domain_scores.items():
            domain_name = domain.replace('_', ' ').title()
            
            if score >= 80:
                status = "Excellent"
                status_color = colors.green
            elif score >= 60:
                status = "Good"
                status_color = colors.orange
            elif score >= 40:
                status = "Fair"
                status_color = colors.red
            else:
                status = "Concern"
                status_color = colors.red
            
            domain_data.append([domain_name, f"{score:.1f}", status])
        
        table = Table(domain_data, colWidths=[3*inch, 1*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_document_summary_section(self, documents):
        """Create document summary section"""
        elements = []
        
        # Section heading
        heading = Paragraph("Document Analysis Summary", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        if not documents:
            no_docs = Paragraph("No documents have been uploaded for analysis.", self.styles['CustomNormal'])
            elements.append(no_docs)
            elements.append(Spacer(1, 20))
            return elements
        
        # Document summary table
        doc_data = [['Document Type', 'Count', 'Latest Upload']]
        
        # Group documents by type
        doc_types = {}
        for doc in documents:
            doc_type = doc.get('document_type', 'unknown')
            if doc_type not in doc_types:
                doc_types[doc_type] = []
            doc_types[doc_type].append(doc)
        
        for doc_type, docs in doc_types.items():
            type_name = doc_type.replace('_', ' ').title()
            count = len(docs)
            latest = max([doc.get('created_at', '') for doc in docs])
            
            if latest:
                try:
                    latest_date = datetime.datetime.fromisoformat(latest.replace('Z', '+00:00'))
                    latest_formatted = latest_date.strftime('%m/%d/%Y')
                except:
                    latest_formatted = latest
            else:
                latest_formatted = 'N/A'
            
            doc_data.append([type_name, str(count), latest_formatted])
        
        table = Table(doc_data, colWidths=[3*inch, 1*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#dee2e6'))
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_detailed_findings_section(self, documents):
        """Create detailed findings section"""
        elements = []
        
        # Section heading
        heading = Paragraph("Detailed Document Findings", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        if not documents:
            return elements
        
        for i, doc in enumerate(documents[:10]):  # Limit to first 10 documents
            # Document header
            doc_type = doc.get('document_type', 'Unknown').replace('_', ' ').title()
            doc_title = f"{doc_type} - {doc.get('file_name', f'Document {i+1}')}"
            
            doc_heading_style = ParagraphStyle(
                name='DocHeading',
                parent=self.styles['Heading3'],
                fontSize=12,
                textColor=self.primary_color,
                spaceAfter=6
            )
            
            doc_heading = Paragraph(doc_title, doc_heading_style)
            elements.append(doc_heading)
            
            # Key findings
            findings = doc.get('key_findings', [])
            if findings:
                findings_text = "• " + "<br/>• ".join(findings[:5])  # Limit to 5 findings
                findings_para = Paragraph(f"<b>Key Findings:</b><br/>{findings_text}", self.styles['CustomNormal'])
                elements.append(findings_para)
            
            # Confidence score
            confidence = doc.get('confidence_score')
            if confidence is not None:
                confidence_text = f"<b>Analysis Confidence:</b> {confidence*100:.1f}%"
                confidence_para = Paragraph(confidence_text, self.styles['CustomNormal'])
                elements.append(confidence_para)
            
            elements.append(Spacer(1, 12))
        
        if len(documents) > 10:
            more_docs = Paragraph(f"... and {len(documents) - 10} more documents", 
                                self.styles['CustomNormal'])
            elements.append(more_docs)
        
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_recommendations_section(self, fertility_report):
        """Create recommendations section"""
        elements = []
        
        # Section heading
        heading = Paragraph("Clinical Recommendations", self.styles['CustomHeading'])
        elements.append(heading)
        elements.append(Spacer(1, 12))
        
        recommendations = fertility_report.get('recommendations', [])
        
        if not recommendations:
            # Generate basic recommendations based on score
            overall_score = fertility_report.get('overall_score', 0)
            
            if overall_score >= 80:
                recommendations = [
                    "Continue current lifestyle and health practices",
                    "Regular monitoring and check-ups",
                    "Consider pre-conception counseling if planning pregnancy"
                ]
            elif overall_score >= 60:
                recommendations = [
                    "Address identified areas for improvement",
                    "Consider lifestyle modifications",
                    "Follow up with fertility specialist",
                    "Regular monitoring of fertility parameters"
                ]
            else:
                recommendations = [
                    "Urgent consultation with fertility specialist recommended",
                    "Comprehensive fertility evaluation needed",
                    "Consider assisted reproductive technologies",
                    "Address underlying health conditions",
                    "Lifestyle and dietary modifications"
                ]
        
        # Create recommendations list
        rec_text = ""
        for i, rec in enumerate(recommendations[:8], 1):  # Limit to 8 recommendations
            rec_text += f"{i}. {rec}<br/>"
        
        rec_para = Paragraph(rec_text, self.styles['CustomNormal'])
        elements.append(rec_para)
        elements.append(Spacer(1, 30))
        
        return elements
    
    def _create_footer(self):
        """Create report footer"""
        elements = []
        
        # Disclaimer
        disclaimer_text = """
        <b>IMPORTANT DISCLAIMER:</b><br/>
        This report is generated by FertiVision AI-enhanced reproductive analysis system and is intended for 
        informational purposes only. It should not be considered as medical advice or a substitute for 
        professional medical consultation. Always consult with qualified healthcare providers for medical 
        decisions and treatment plans. The accuracy of this analysis depends on the quality and completeness 
        of the uploaded medical documents.
        """
        
        disclaimer_style = ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6c757d'),
            borderWidth=1,
            borderColor=colors.HexColor('#dee2e6'),
            borderPadding=10,
            backColor=colors.HexColor('#f8f9fa')
        )
        
        disclaimer = Paragraph(disclaimer_text, disclaimer_style)
        elements.append(disclaimer)
        elements.append(Spacer(1, 20))
        
        # Report footer
        footer_text = f"""
        <b>FertiVision - AI-Enhanced Reproductive Medicine</b><br/>
        Report generated on {datetime.datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
        © 2024 FertiVision. All rights reserved.
        """
        
        footer_style = ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=1,
            textColor=colors.HexColor('#6c757d')
        )
        
        footer = Paragraph(footer_text, footer_style)
        elements.append(footer)
        
        return elements

def export_patient_fertility_report(patient_data, fertility_report, documents, output_path=None):
    """
    Export a comprehensive patient fertility report to PDF
    
    Args:
        patient_data: Patient information dictionary
        fertility_report: Fertility analysis report dictionary
        documents: List of analyzed documents
        output_path: Optional output file path
    
    Returns:
        str: Path to generated PDF file
    """
    pdf_generator = FertilityReportPDF()
    return pdf_generator.generate_patient_report(patient_data, fertility_report, documents, output_path)

# Utility function for generating in-memory PDF
def generate_pdf_buffer(patient_data, fertility_report, documents):
    """Generate PDF report in memory buffer"""
    buffer = BytesIO()
    
    # Create temporary PDF generator
    pdf_generator = FertilityReportPDF()
    
    # Create document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Build story
    story = []
    story.extend(pdf_generator._create_header(patient_data))
    story.extend(pdf_generator._create_patient_info_section(patient_data))
    story.extend(pdf_generator._create_fertility_score_section(fertility_report))
    story.extend(pdf_generator._create_domain_analysis_section(fertility_report))
    story.extend(pdf_generator._create_document_summary_section(documents))
    story.extend(pdf_generator._create_detailed_findings_section(documents))
    story.extend(pdf_generator._create_recommendations_section(fertility_report))
    story.extend(pdf_generator._create_footer())
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer