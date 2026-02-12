import json
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path
from config import settings

class DataProcessor:
    """
    Process the JSONL medical education dataset
    """
    
    def __init__(self, jsonl_path: str = None):
        self.jsonl_path = jsonl_path or settings.JSONL_DATA_PATH
        self.data: List[Dict[str, Any]] = []
        self.subjects: set = set()
        self.topics: set = set()
    
    def load_data(self) -> List[Dict[str, Any]]:
        """
        Load and parse JSONL file
        """
        print(f"Loading data from {self.jsonl_path}")
        
        try:
            with open(self.jsonl_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            self.data.append(entry)
                            
                            # Extract subjects and topics
                            if 'subject' in entry:
                                self.subjects.add(entry['subject'])
                            if 'topic' in entry:
                                self.topics.add(entry['topic'])
                                
                        except json.JSONDecodeError as e:
                            print(f"Error parsing line: {e}")
                            continue
            
            print(f"Loaded {len(self.data)} questions")
            print(f"Found {len(self.subjects)} subjects: {list(self.subjects)[:5]}...")
            print(f"Found {len(self.topics)} topics")
            
            return self.data
            
        except FileNotFoundError:
            print(f"Error: File not found at {self.jsonl_path}")
            return []
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return []
    
    def get_subjects(self) -> List[str]:
        """Get list of unique subjects"""
        return sorted(list(self.subjects))
    
    def get_topics(self, subject: str = None) -> List[str]:
        """Get list of topics, optionally filtered by subject"""
        if subject:
            topics = {
                entry['topic'] 
                for entry in self.data 
                if entry.get('subject') == subject and entry.get('topic')
            }
            return sorted(list(topics))
        return sorted(list(self.topics))
    
    def format_qa_for_embedding(self, entry: Dict[str, Any]) -> str:
        """
        Format a QA entry into text for embedding
        """
        question = entry.get('question', '')
        options = entry.get('options', {})
        explanation = entry.get('explanation', '')
        subject = entry.get('subject', '')
        topic = entry.get('topic', '')
        
        # Format options
        options_text = ""
        if options:
            options_text = "\n".join([
                f"{key}. {value}" 
                for key, value in options.items()
            ])
        
        # Combine into searchable text
        text = f"""Subject: {subject}
Topic: {topic}
Question: {question}
Options:
{options_text}
Explanation: {explanation}"""
        
        return text
    
    def get_correct_answer(self, entry: Dict[str, Any]) -> str:
        """
        Get the correct answer text from entry
        """
        options = entry.get('options', {})
        correct_index = entry.get('correct_answer_index', 0)
        
        # Convert index to letter key (0='A', 1='B', etc.)
        option_keys = list(options.keys())
        if correct_index < len(option_keys):
            correct_key = option_keys[correct_index]
            return options.get(correct_key, "")
        
        return ""
    
    def filter_by_subject(self, subject: str) -> List[Dict[str, Any]]:
        """Get all questions for a subject"""
        return [
            entry for entry in self.data 
            if entry.get('subject', '').lower() == subject.lower()
        ]
    
    def filter_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Get all questions for a topic"""
        return [
            entry for entry in self.data 
            if entry.get('topic', '').lower() == topic.lower()
        ]
    
    def get_random_questions(self, n: int = 10, subject: str = None, topic: str = None) -> List[Dict[str, Any]]:
        """
        Get random questions, optionally filtered by subject and topic
        """
        import random
        
        pool = self.data
        
        if subject:
             pool = [q for q in pool if q.get('subject', '').lower() == subject.lower()]
             
        if topic:
             pool = [q for q in pool if q.get('topic', '').lower() == topic.lower()]
        
        if len(pool) <= n:
            return pool
        
        return random.sample(pool, n)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about the dataset
        """
        return {
            "total_questions": len(self.data),
            "total_subjects": len(self.subjects),
            "total_topics": len(self.topics),
            "subjects": self.get_subjects(),
            "questions_per_subject": {
                subject: len(self.filter_by_subject(subject))
                for subject in self.subjects
            }
        }

# Global data processor instance
data_processor = DataProcessor()
