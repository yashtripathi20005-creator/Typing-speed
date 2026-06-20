"""
Word Generator - Provides words and sentences for the typing test
"""

import random
from typing import List


class WordGenerator:
    """Generates random words and paragraphs for typing tests"""
    
    # Common English words for typing practice
    COMMON_WORDS = [
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
        "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
        "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
        "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
        "people", "into", "year", "your", "good", "some", "could", "them", "see", "other",
        "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
        "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
        "is", "was", "were", "are", "am", "been", "being", "has", "had", "did",
        "programming", "python", "code", "algorithm", "function", "variable", "method",
        "class", "object", "inheritance", "polymorphism", "encapsulation", "abstraction",
        "developer", "application", "software", "system", "network", "database", "server",
        "client", "interface", "module", "library", "framework", "component", "design",
        "pattern", "architecture", "security", "performance", "optimization", "debugging",
        "testing", "deployment", "integration", "version", "control", "repository", "commit",
        "branch", "merge", "pull", "push", "clone", "fork", "issue", "pull", "request"
    ]
    
    # Words for more variety
    ADDITIONAL_WORDS = [
        "beautiful", "wonderful", "amazing", "extraordinary", "fantastic",
        "incredible", "magnificent", "spectacular", "remarkable", "outstanding",
        "brilliant", "excellent", "superb", "terrific", "awesome",
        "quick", "brown", "lazy", "sleepy", "happy",
        "sad", "angry", "excited", "calm", "peaceful",
        "mountain", "ocean", "forest", "desert", "island",
        "galaxy", "planet", "star", "moon", "sun",
        "technology", "science", "innovation", "discovery", "invention",
        "creative", "artistic", "imaginative", "innovative", "progressive"
    ]
    
    def __init__(self):
        self.words = self.COMMON_WORDS + self.ADDITIONAL_WORDS
    
    def get_random_word(self) -> str:
        """Get a single random word"""
        return random.choice(self.words)
    
    def generate_sentence(self, word_count: int = 10) -> List[str]:
        """Generate a sentence with specified number of words"""
        words = [self.get_random_word() for _ in range(word_count)]
        # Capitalize first word
        words[0] = words[0].capitalize()
        return words
    
    def generate_paragraph(self, sentence_count: int = 5, words_per_sentence: int = 8) -> List[str]:
        """Generate a paragraph with multiple sentences"""
        all_words = []
        
        for _ in range(sentence_count):
            sentence_words = self.generate_sentence(words_per_sentence)
            all_words.extend(sentence_words)
            # Add a period at the end of each sentence
            all_words[-1] = all_words[-1] + "."
        
        return all_words
    
    def generate_custom_text(self, word_count: int = 50) -> List[str]:
        """Generate custom text with specified number of words"""
        return [self.get_random_word() for _ in range(word_count)]
