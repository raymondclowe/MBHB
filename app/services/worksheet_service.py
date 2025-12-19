"""Worksheet Service - Generates worksheets using Node.js generator"""

import subprocess
import os
import json
from datetime import datetime
from app import db
from app.models import Student, MistakeCategory, GeneratedWorksheet, PerformanceMetric


class WorksheetService:
    """Service for generating and managing worksheets"""
    
    @staticmethod
    def generate_worksheet_for_category(student_id, category_id):
        """
        Generate a worksheet for a specific student and mistake category
        Uses the existing Node.js worksheet generator
        """
        student = Student.query.get(student_id)
        category = MistakeCategory.query.get(category_id)
        
        if not student or not category:
            return {'success': False, 'error': 'Student or category not found'}
        
        # Get recent performance metric for pre-worksheet error rate
        metric = PerformanceMetric.query.filter_by(
            student_id=student_id,
            category_id=category_id
        ).order_by(PerformanceMetric.metric_date.desc()).first()
        
        pre_worksheet_error_rate = metric.moving_average if metric else 0
        
        # Map category to worksheet generator format
        worksheet_data = WorksheetService._category_to_worksheet_params(category)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"worksheet_{student.student_id}_{category.category_id}_{timestamp}.html"
        output_path = os.path.join('./generated_worksheets', output_filename)
        
        # Call Node.js generator
        success = WorksheetService._call_nodejs_generator(worksheet_data, output_path)
        
        if success:
            # Record in database
            worksheet = GeneratedWorksheet(
                student_id=student_id,
                category_id=category_id,
                file_path=output_path,
                status='generated',
                pre_worksheet_error_rate=pre_worksheet_error_rate
            )
            db.session.add(worksheet)
            db.session.commit()
            
            return {
                'success': True,
                'worksheet_id': worksheet.id,
                'file_path': output_path
            }
        else:
            return {'success': False, 'error': 'Failed to generate worksheet'}
    
    @staticmethod
    def _category_to_worksheet_params(category):
        """Convert mistake category to worksheet generator parameters"""
        # Map category to examples based on category_id
        examples_map = {
            'CAT001': {
                'bad_habit': 'Forgetting ± when solving equations',
                'example1': 'Solve: x² = 25. Correct: x = ±5. Common mistake: x = 5 only',
                'example2': 'Solve: x² = 16. Correct: x = ±4. Common mistake: x = 4 only',
                'problem': 'Solving quadratic equations with square roots'
            },
            'CAT002': {
                'bad_habit': 'Not changing sign when moving terms across equation',
                'example1': 'Solve: x + 5 = 10. Correct: x = 10 - 5 = 5. Common mistake: x = 10 + 5',
                'example2': 'Solve: 3x - 7 = 8. Correct: 3x = 8 + 7. Common mistake: 3x = 8 - 7',
                'problem': 'Rearranging algebraic equations'
            },
            'CAT011': {
                'bad_habit': 'Forgetting to distribute the negative sign when expanding -(a + b)',
                'example1': 'Simplify: -(3 + x). Correct: -3 - x. Common mistake: -3 + x',
                'example2': 'Simplify: -(5 - 2y). Correct: -5 + 2y. Common mistake: -5 - 2y',
                'problem': 'Expanding expressions with negative signs in front of parentheses'
            },
            'CAT012': {
                'bad_habit': 'Doing addition/subtraction before multiplication/division (ignoring PEMDAS)',
                'example1': 'Calculate: 3 + 4 × 2. Correct: 3 + 8 = 11. Common mistake: 7 × 2 = 14',
                'example2': 'Calculate: 12 ÷ 3 + 2. Correct: 4 + 2 = 6. Common mistake: 12 ÷ 5 = 2.4',
                'problem': 'Mixed operations requiring proper order of operations'
            },
            'CAT013': {
                'bad_habit': 'Adding fractions by adding numerators and denominators separately',
                'example1': 'Add: 1/2 + 1/3. Correct: 3/6 + 2/6 = 5/6. Common mistake: 2/5',
                'example2': 'Add: 2/5 + 1/4. Correct: 8/20 + 5/20 = 13/20. Common mistake: 3/9',
                'problem': 'Adding fractions with different denominators'
            },
            'CAT014': {
                'bad_habit': 'Thinking (a + b)² = a² + b² instead of a² + 2ab + b²',
                'example1': 'Expand: (x + 3)². Correct: x² + 6x + 9. Common mistake: x² + 9',
                'example2': 'Expand: (2y + 1)². Correct: 4y² + 4y + 1. Common mistake: 4y² + 1',
                'problem': 'Expanding squared binomial expressions'
            },
            'CAT015': {
                'bad_habit': 'Incorrectly canceling terms across addition',
                'example1': 'Simplify: (x+5)/x. Correct: Cannot simplify. Common mistake: 5',
                'example2': 'Simplify: (2x+4)/(2x). Correct: 1 + 2/x. Common mistake: 4 or 2',
                'problem': 'Simplifying algebraic fractions with addition in numerator'
            }
        }
        
        # Get mapping or use generic
        if category.category_id in examples_map:
            return examples_map[category.category_id]
        else:
            # Generic template
            return {
                'bad_habit': category.description or category.name,
                'example1': f'Example of {category.name}: [specific case]',
                'example2': f'Another example of {category.name}: [different case]',
                'problem': f'Practice problems for {category.name}'
            }
    
    @staticmethod
    def _call_nodejs_generator(worksheet_data, output_path):
        """Call the Node.js worksheet generator via subprocess"""
        try:
            # Create a temporary JSON file with the worksheet data
            temp_data_file = '/tmp/worksheet_data.json'
            with open(temp_data_file, 'w') as f:
                json.dump(worksheet_data, f)
            
            # Call Node.js script
            node_script = os.path.join(os.path.dirname(__file__), '..', '..', 'generate_worksheet.js')
            
            result = subprocess.run(
                ['node', node_script, temp_data_file, output_path],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Clean up temp file
            if os.path.exists(temp_data_file):
                os.remove(temp_data_file)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error calling Node.js generator: {e}")
            return False
    
    @staticmethod
    def mark_worksheet_completed(worksheet_id):
        """Mark a worksheet as completed and update metrics"""
        worksheet = GeneratedWorksheet.query.get(worksheet_id)
        if not worksheet:
            return False
        
        worksheet.completed_at = datetime.utcnow()
        worksheet.status = 'completed'
        
        # Calculate post-worksheet error rate
        metric = PerformanceMetric.query.filter_by(
            student_id=worksheet.student_id,
            category_id=worksheet.category_id
        ).order_by(PerformanceMetric.metric_date.desc()).first()
        
        if metric:
            worksheet.post_worksheet_error_rate = metric.moving_average
        
        db.session.commit()
        return True
    
    @staticmethod
    def generate_auto_worksheets():
        """
        Automatically generate worksheets for students based on priorities
        This can be called by a scheduler/cron job
        """
        from app.services.performance_service import PerformanceService
        
        students = Student.query.all()
        generated = []
        
        for student in students:
            # Get top priority that doesn't have a recent worksheet
            priorities = PerformanceService.get_top_priorities_for_student(student.id, limit=3)
            
            for metric in priorities:
                # Check if already generated worksheet in last 7 days
                recent_worksheet = GeneratedWorksheet.query.filter_by(
                    student_id=student.id,
                    category_id=metric.category_id
                ).filter(
                    GeneratedWorksheet.generated_at >= datetime.utcnow() - timedelta(days=7)
                ).first()
                
                if not recent_worksheet and metric.priority_score > 10:
                    result = WorksheetService.generate_worksheet_for_category(
                        student.id,
                        metric.category_id
                    )
                    if result['success']:
                        generated.append(result)
                        break  # Only generate one per student per run
        
        return generated
