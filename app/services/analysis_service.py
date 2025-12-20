"""Analysis Service - Processes homework submissions and extracts mistakes"""

import json
import os
from datetime import datetime, date
from app import db
from app.models import Student, HomeworkSubmission, Mistake, MistakeCategory


class AnalysisService:
    """Service for analyzing homework submissions"""
    
    @staticmethod
    def process_json_submission(file_path):
        """
        Process a JSON file containing AI-analyzed homework
        
        Expected JSON format:
        {
            "student_id": "12345",
            "homework_date": "2024-01-15",
            "questions": [
                {
                    "question_number": 1,
                    "topic": "Algebra",
                    "student_answer": "x = 5",
                    "correct_answer": "x = ±5",
                    "mistakes": [
                        {
                            "type": "missing_negative_root",
                            "description": "Student forgot negative solution",
                            "severity": "high"
                        }
                    ]
                }
            ]
        }
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            student_id = data.get('student_id')
            homework_date = datetime.strptime(data.get('homework_date'), '%Y-%m-%d').date()
            questions = data.get('questions', [])
            
            # Find or create student
            student = Student.query.filter_by(student_id=student_id).first()
            if not student:
                student = Student(
                    student_id=student_id,
                    name=data.get('student_name', f'Student {student_id}')
                )
                db.session.add(student)
                db.session.flush()
            
            # Create homework submission
            submission = HomeworkSubmission(
                student_id=student.id,
                submission_date=homework_date,
                file_path=file_path,
                analysis_status='processing',
                total_questions=len(questions)
            )
            db.session.add(submission)
            db.session.flush()
            
            # Process mistakes
            total_mistakes = 0
            for question in questions:
                question_mistakes = question.get('mistakes', [])
                total_mistakes += len(question_mistakes)
                
                for mistake_data in question_mistakes:
                    # Match mistake to category
                    category = AnalysisService._match_mistake_to_category(
                        mistake_data.get('type'),
                        mistake_data.get('description')
                    )
                    
                    if category:
                        mistake = Mistake(
                            submission_id=submission.id,
                            category_id=category.id,
                            question_number=question.get('question_number'),
                            description=mistake_data.get('description'),
                            severity=mistake_data.get('severity', 'medium'),
                            student_answer=question.get('student_answer'),
                            correct_answer=question.get('correct_answer')
                        )
                        db.session.add(mistake)
            
            # Update submission
            submission.total_mistakes = total_mistakes
            submission.analysis_status = 'complete'
            
            db.session.commit()
            
            # Trigger performance metric update
            from app.services.performance_service import PerformanceService
            PerformanceService.update_metrics_for_student(student.id)
            
            return {'success': True, 'submission_id': submission.id, 'mistakes': total_mistakes}
            
        except Exception as e:
            db.session.rollback()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _match_mistake_to_category(mistake_type, description):
        """Match a mistake to an existing category or create new one"""
        # Try exact match on category_id
        if mistake_type:
            # Convert mistake_type to category_id format
            category_id = mistake_type.upper().replace('_', '')
            if not category_id.startswith('CAT'):
                # Try to match by name similarity
                category = MistakeCategory.query.filter(
                    MistakeCategory.name.ilike(f'%{mistake_type.replace("_", " ")}%')
                ).first()
                if category:
                    return category
        
        # Keyword matching for common mistakes
        description_lower = description.lower() if description else ''
        
        keyword_mappings = {
            'CAT001': ['negative root', '±', 'positive and negative', 'forgot negative'],
            'CAT002': ['sign change', 'moving term', 'change sign'],
            'CAT003': ['unit', 'units', 'cm', 'm²', 'missing unit'],
            'CAT004': ['rounding', 'decimal places', 'significant figures'],
            'CAT005': ['domain', 'range', 'restriction'],
            'CAT006': ['integration constant', '+c', 'constant of integration'],
            'CAT007': ['chain rule', 'derivative'],
            'CAT008': ['trigonometric', 'trig identity', 'sin', 'cos', 'tan'],
            'CAT009': ['matrix', 'multiplication'],
            'CAT010': ['probability', 'notation', 'p('],
            'CAT011': ['negative sign', 'distribution', 'distribute negative'],
            'CAT012': ['order of operations', 'pemdas', 'bodmas'],
            'CAT013': ['fraction', 'add fractions', 'numerator', 'denominator'],
            'CAT014': ['binomial', '(a+b)²', 'expand', 'square'],
            'CAT015': ['cancel', 'cancellation', 'simplify fraction']
        }
        
        for category_id, keywords in keyword_mappings.items():
            if any(keyword in description_lower for keyword in keywords):
                category = MistakeCategory.query.filter_by(category_id=category_id).first()
                if category:
                    return category
        
        # If no match found, return a default "Other" category or create new
        return AnalysisService._get_or_create_other_category()
    
    @staticmethod
    def _get_or_create_other_category():
        """Get or create an 'Other' category for unclassified mistakes"""
        category = MistakeCategory.query.filter_by(category_id='CAT999').first()
        if not category:
            category = MistakeCategory(
                category_id='CAT999',
                name='Other/Unclassified',
                description='Mistakes that do not fit into existing categories',
                exam_weight=5
            )
            db.session.add(category)
            db.session.flush()
        return category
