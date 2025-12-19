"""Initialize default mistake categories for IB HL AA Mathematics"""

from app import db
from app.models.mistake_category import MistakeCategory


DEFAULT_CATEGORIES = [
    {
        'category_id': 'CAT001',
        'name': 'Missing Negative Roots',
        'description': 'Forgetting ± when solving equations like x² = 25, giving only positive solution',
        'exam_weight': 8
    },
    {
        'category_id': 'CAT002',
        'name': 'Sign Change Error',
        'description': 'Not changing sign when moving terms across equation (e.g., x + 5 = 10 → x = 10 + 5)',
        'exam_weight': 9
    },
    {
        'category_id': 'CAT003',
        'name': 'Unit Omission',
        'description': 'Missing units in final answer (cm, m², radians, etc.)',
        'exam_weight': 5
    },
    {
        'category_id': 'CAT004',
        'name': 'Rounding Error',
        'description': 'Incorrect number of decimal places or significant figures',
        'exam_weight': 4
    },
    {
        'category_id': 'CAT005',
        'name': 'Domain/Range Restriction',
        'description': 'Forgetting to state domain or range restrictions (e.g., x ≠ 0 for 1/x)',
        'exam_weight': 7
    },
    {
        'category_id': 'CAT006',
        'name': 'Missing Integration Constant',
        'description': 'Forgetting +C in indefinite integrals',
        'exam_weight': 8
    },
    {
        'category_id': 'CAT007',
        'name': 'Chain Rule Error',
        'description': 'Incorrect application of chain rule in differentiation',
        'exam_weight': 9
    },
    {
        'category_id': 'CAT008',
        'name': 'Trigonometric Identity',
        'description': 'Wrong trigonometric identity or simplification',
        'exam_weight': 6
    },
    {
        'category_id': 'CAT009',
        'name': 'Matrix Operation Error',
        'description': 'Incorrect matrix multiplication or operations',
        'exam_weight': 6
    },
    {
        'category_id': 'CAT010',
        'name': 'Probability Notation',
        'description': 'Missing P() or incorrect probability notation',
        'exam_weight': 3
    },
    {
        'category_id': 'CAT011',
        'name': 'Negative Sign Distribution',
        'description': 'Forgetting to distribute negative sign: -(a+b) should be -a-b not -a+b',
        'exam_weight': 8
    },
    {
        'category_id': 'CAT012',
        'name': 'Order of Operations',
        'description': 'Doing addition/subtraction before multiplication/division (ignoring PEMDAS)',
        'exam_weight': 7
    },
    {
        'category_id': 'CAT013',
        'name': 'Fraction Addition',
        'description': 'Adding fractions by adding numerators and denominators separately',
        'exam_weight': 8
    },
    {
        'category_id': 'CAT014',
        'name': 'Binomial Expansion',
        'description': 'Thinking (a+b)² = a²+b² instead of a²+2ab+b²',
        'exam_weight': 8
    },
    {
        'category_id': 'CAT015',
        'name': 'Incorrect Cancellation',
        'description': 'Canceling terms across addition (e.g., (x+3)/x ≠ 3)',
        'exam_weight': 7
    }
]


def initialize_default_categories():
    """Initialize database with default mistake categories"""
    for cat_data in DEFAULT_CATEGORIES:
        category = MistakeCategory(**cat_data)
        db.session.add(category)
    
    try:
        db.session.commit()
        print(f"Initialized {len(DEFAULT_CATEGORIES)} default mistake categories")
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing categories: {e}")
