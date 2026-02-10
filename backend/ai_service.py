"""
AI Service Module for Student Discussion Forum
Provides AI-powered features: Answer Assistant, Moderation, Summarization, and Question Enhancement
"""

import os
from typing import Dict, Any

class AIService:
    """AI service with multiple providers support"""
    
    def __init__(self, provider='mock', api_key=None, model='gpt-3.5-turbo'):
        self.provider = provider
        self.api_key = api_key
        self.model = model
        
        if provider == 'openai' and api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=api_key)
            except ImportError:
                print("OpenAI library not installed. Falling back to mock.")
                self.provider = 'mock'
    
    def get_answer_for_discussion(self, title: str, content: str, subject: str) -> Dict[str, Any]:
        """
        Generate an AI answer for a discussion topic
        
        Args:
            title: Discussion title
            content: Discussion content
            subject: Subject/tag
        
        Returns:
            Dict with 'success' and 'answer' keys
        """
        if self.provider == 'openai':
            return self._openai_answer(title, content, subject)
        else:
            return self._mock_answer(title, content, subject)
    
    def moderate_content(self, content: str) -> Dict[str, Any]:
        """
        Check content for spam, abuse, or inappropriate material
        
        Args:
            content: Text content to moderate
        
        Returns:
            Dict with 'is_safe', 'reason', 'confidence' keys
        """
        if self.provider == 'openai':
            return self._openai_moderate(content)
        else:
            return self._mock_moderate(content)
    
    def summarize_thread(self, title: str, content: str, comments: list) -> Dict[str, Any]:
        """
        Generate a summary of a discussion thread
        
        Args:
            title: Post title
            content: Post content
            comments: List of comment texts
        
        Returns:
            Dict with 'success' and 'summary' keys
        """
        if self.provider == 'openai':
            return self._openai_summarize(title, content, comments)
        else:
            return self._mock_summarize(title, content, comments)
    
    def enhance_question(self, question: str) -> Dict[str, Any]:
        """
        Improve the clarity and quality of a student question
        
        Args:
            question: Original question text
        
        Returns:
            Dict with 'success', 'enhanced_question', 'improvements' keys
        """
        if self.provider == 'openai':
            return self._openai_enhance(question)
        else:
            return self._mock_enhance(question)
    
    # Mock implementations (work without API key)
    
    def _mock_answer(self, title: str, content: str, subject: str) -> Dict[str, Any]:
        """Mock AI answer generation"""
        answer = f"""**AI-Generated Answer for "{title}"**

Based on the question about {subject.lower()}, here are some key points to consider:

1. **Understanding the Core Concept**: The topic requires careful analysis of the fundamental principles involved.

2. **Relevant Information**: Consider reviewing related materials in your {subject} textbook, particularly chapters that discuss similar concepts.

3. **Practical Application**: Think about how this concept applies to real-world scenarios and examples.

4. **Further Resources**: I recommend checking online educational resources like Khan Academy, Coursera, or your institution's library for more detailed explanations.

*Note: This is an AI-generated response. Please verify information with your instructor or reliable sources.*
"""
        return {'success': True, 'answer': answer}
    
    def _mock_moderate(self, content: str) -> Dict[str, Any]:
        """Mock content moderation"""
        # Simple keyword-based detection for demo
        spam_keywords = ['buy now', 'click here', 'limited offer', 'FREE MONEY']
        abuse_keywords = ['idiot', 'stupid', 'hate', 'dumb']
        
        content_lower = content.lower()
        
        for keyword in spam_keywords:
            if keyword.lower() in content_lower:
                return {
                    'is_safe': False,
                    'reason': 'Potential spam detected',
                    'confidence': 0.85
                }
        
        for keyword in abuse_keywords:
            if keyword.lower() in content_lower:
                return {
                    'is_safe': False,
                    'reason': 'Potentially abusive language detected',
                    'confidence': 0.75
                }
        
        return {
            'is_safe': True,
            'reason': 'Content appears appropriate',
            'confidence': 0.90
        }
    
    def _mock_summarize(self, title: str, content: str, comments: list) -> Dict[str, Any]:
        """Mock thread summarization"""
        comment_count = len(comments)
        summary = f"""**Thread Summary: {title}**

📊 **Overview**: This discussion has {comment_count} comment(s) and covers important aspects of the topic.

🎯 **Main Question**: {content[:150]}{'...' if len(content) > 150 else ''}

💬 **Discussion Highlights**:
- Active participation from {comment_count} response(s)
- Multiple perspectives shared
- Key insights contributed by community members

📝 **Key Takeaways**: The discussion explores various viewpoints and provides valuable learning opportunities for students interested in this topic.
"""
        return {'success': True, 'summary': summary}
    
    def _mock_enhance(self, question: str) -> Dict[str, Any]:
        """Mock question enhancement"""
        enhanced = question.strip()
        improvements = []
        
        # Add question mark if missing
        if not enhanced.endswith('?'):
            if not enhanced.endswith('.'):
                enhanced += '?'
            improvements.append("Added question mark for clarity")
        
        # Capitalize first letter
        if enhanced and not enhanced[0].isupper():
            enhanced = enhanced[0].upper() + enhanced[1:]
            improvements.append("Capitalized first letter")
        
        # Add context suggestion
        if len(enhanced) < 20:
            improvements.append("Consider adding more context to your question")
        
        if not improvements:
            improvements.append("Question looks good! No major improvements needed")
        
        return {
            'success': True,
            'enhanced_question': enhanced,
            'improvements': improvements
        }
    
    # OpenAI implementations (requires API key)
    
    def _openai_answer(self, title: str, content: str, subject: str) -> Dict[str, Any]:
        """OpenAI-powered answer generation"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are a helpful academic tutor specializing in {subject}. Provide clear, educational answers to student questions."},
                    {"role": "user", "content": f"Question: {title}\n\nDetails: {content}\n\nProvide a helpful, educational answer."}
                ],
                temperature=0.7,
                max_tokens=500
            )
            answer = response.choices[0].message.content
            return {'success': True, 'answer': answer}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _openai_moderate(self, content: str) -> Dict[str, Any]:
        """OpenAI-powered content moderation"""
        try:
            response = self.client.moderations.create(input=content)
            result = response.results[0]
            
            if result.flagged:
                categories = [cat for cat, flagged in result.categories if flagged]
                return {
                    'is_safe': False,
                    'reason': f"Content flagged for: {', '.join(categories)}",
                    'confidence': 0.95
                }
            else:
                return {
                    'is_safe': True,
                    'reason': 'Content is appropriate',
                    'confidence': 0.95
                }
        except Exception as e:
            # Fall back to mock on error
            return self._mock_moderate(content)
    
    def _openai_summarize(self, title: str, content: str, comments: list) -> Dict[str, Any]:
        """OpenAI-powered thread summarization"""
        try:
            thread_text = f"Title: {title}\n\nOriginal Post: {content}\n\nComments:\n"
            thread_text += "\n".join([f"- {comment}" for comment in comments[:10]])  # Limit to 10 comments
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes discussion threads concisely."},
                    {"role": "user", "content": f"Summarize this discussion thread:\n\n{thread_text}"}
                ],
                temperature=0.5,
                max_tokens=300
            )
            summary = response.choices[0].message.content
            return {'success': True, 'summary': summary}
        except Exception as e:
            return self._mock_summarize(title, content, comments)
    
    def _openai_enhance(self, question: str) -> Dict[str, Any]:
        """OpenAI-powered question enhancement"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful writing assistant. Improve student questions to make them clearer and more specific while maintaining the original intent. Respond with the enhanced question only."},
                    {"role": "user", "content": f"Improve this question: {question}"}
                ],
                temperature=0.7,
                max_tokens=200
            )
            enhanced = response.choices[0].message.content
            return {
                'success': True,
                'enhanced_question': enhanced,
                'improvements': ['AI-enhanced for clarity and specificity']
            }
        except Exception as e:
            return self._mock_enhance(question)
