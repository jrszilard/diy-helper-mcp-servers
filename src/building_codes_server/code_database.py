"""
Code Database - In-memory database for building codes
For MVP, uses JSON file. Later: migrate to Pinecone/PostgreSQL with pgvector
"""

import json
import os
from typing import Optional, List, Dict
from pathlib import Path

class CodeDatabase:
    """Manages building code data and search"""
    
    def __init__(self, data_file: str = None):
        """Initialize database"""
        if data_file is None:
            # Look for codes.json in same directory
            data_file = Path(__file__).parent / "codes.json"
        
        self.data_file = data_file
        self.codes = []
        self.load_codes()
    
    def load_codes(self):
        """Load codes from JSON file"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.codes = json.load(f)
        else:
            # Initialize with empty database
            self.codes = []
            print(f"Warning: Code database not found at {self.data_file}")
            print("Starting with empty database. Add codes to codes.json")
    
    async def search(
        self, 
        query: str, 
        jurisdiction: str = "National",
        code_type: Optional[str] = None,
        top_k: int = 3
    ) -> List[Dict]:
        """
        Search codes by query
        For MVP: simple keyword matching
        TODO: Replace with vector similarity search
        """
        query_lower = query.lower()
        results = []
        
        for code in self.codes:
            # Filter by jurisdiction
            if code.get('jurisdiction') != jurisdiction:
                continue
            
            # Filter by code type if specified
            if code_type and code.get('category') != code_type:
                continue
            
            # Simple keyword matching (replace with vector search later)
            score = 0
            searchable_text = (
                f"{code.get('title', '')} "
                f"{code.get('summary', '')} "
                f"{' '.join(code.get('common_questions', []))}"
            ).lower()
            
            # Count matching words
            for word in query_lower.split():
                if word in searchable_text:
                    score += 1
            
            if score > 0:
                results.append({
                    **code,
                    'relevance_score': score
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results[:top_k]
    
    async def get_section(
        self, 
        section_reference: str, 
        jurisdiction: str = "National"
    ) -> Optional[Dict]:
        """Get specific code section by reference"""
        for code in self.codes:
            if (code.get('code_ref') == section_reference and 
                code.get('jurisdiction') == jurisdiction):
                return code
        
        return None
    
    def get_categories(self) -> Dict:
        """Get all code categories and their questions"""
        categories = {}
        
        for code in self.codes:
            category = code.get('category', 'general')
            if category not in categories:
                categories[category] = {
                    'count': 0,
                    'sample_questions': []
                }
            
            categories[category]['count'] += 1
            
            # Add first 3 common questions
            questions = code.get('common_questions', [])
            if questions and len(categories[category]['sample_questions']) < 3:
                categories[category]['sample_questions'].extend(
                    questions[:3 - len(categories[category]['sample_questions'])]
                )
        
        return categories