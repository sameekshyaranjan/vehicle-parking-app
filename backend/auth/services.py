import re
from typing import Dict, Any
class AuthService:
    def validate_registration_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        ""
        username = data.get('username', '').strip()
        if len(username) < 3 or len(username) > 50:
            return {'valid': False, 'message': 'Username must be between 3 and 50 characters'}
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return {'valid': False, 'message': 'Username can only contain letters, numbers, and underscores'}
        email = data.get('email', '').strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return {'valid': False, 'message': 'Invalid email format'}
        password = data.get('password', '')
        if not self.validate_password_strength(password):
            return {'valid': False, 'message': 'Password must be at least 6 characters long'}
        fullname = data.get('fullname', '').strip()
        if len(fullname) < 2 or len(fullname) > 100:
            return {'valid': False, 'message': 'Full name must be between 2 and 100 characters'}
        pin_code = data.get('pin_code', '').strip()
        if not re.match(r'^\d{6}$', pin_code):
            return {'valid': False, 'message': 'Pin code must be exactly 6 digits'}
        address = data.get('address', '').strip()
        if len(address) < 10 or len(address) > 500:
            return {'valid': False, 'message': 'Address must be between 10 and 500 characters'}
        return {'valid': True, 'message': 'Validation successful'}
    def validate_password_strength(self, password: str) -> bool:
        if len(password) < 6:
            return False
        return True
    def sanitize_user_input(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize user input data"""
        sanitized = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                # Strip whitespace and convert to appropriate case
                if key in ['username', 'email']:
                    sanitized[key] = value.strip().lower()
                else:
                    sanitized[key] = value.strip()
            else:
                sanitized[key] = value
        
        return sanitized
