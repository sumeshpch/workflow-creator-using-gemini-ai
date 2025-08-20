from enum import Enum
from typing import Optional, List
import google.generativeai as genai
import re
import json

class LanguageSelection(Enum):
    MALAYALAM = "malayalam"
    HINDI = "hindi"
    ARABIC = "arabic"
    ENGLISH = "english"

class GeminiModel:
    def __init__(self, api_key: str, selected_language: LanguageSelection):
        # Configure the API key first
        genai.configure(api_key=api_key)
        
        self.api_key = api_key
        self.selected_language = selected_language
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 10240,
            "response_mime_type": "application/json"
        }
        
        self.chat = None
        self.history = []
        self.prompts = self._load_prompts()

        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config=self.generation_config,
            system_instruction=self.get_system_instruction()
        )

    def _load_prompts(self) -> dict:
        prompts = {}
        try:
            with open('prompts.txt', 'r', encoding='utf-8') as file:
                current_section = None
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if ':' in line:
                        key, value = line.split(':', 1)
                        prompts[key.strip()] = value.strip()
        except FileNotFoundError:
            print("Warning: prompts.txt not found. Using default prompts.")
            # Default prompts if file not found
            prompts = {
                'ai_prompt': 'Default English prompt',
                'ai_additional_consideration': 'Default additional consideration',
                'required_english': 'Default English requirement',
                'ai_ml_prompt': 'Default Malayalam prompt',
                'ml_additional_translation': 'Default Malayalam translation',
                'required_malayalam': 'Default Malayalam requirement',
                'ai_hindi_prompt': 'Default Hindi prompt',
                'hindi_additional_translation': 'Default Hindi translation',
                'required_hindi': 'Default Hindi requirement',
                'ai_arabic_prompt': 'Default Arabic prompt',
                'arabic_additional_translation': 'Default Arabic translation',
                'required_arabic': 'Default Arabic requirement'
            }
        return prompts

    def get_system_instruction(self) -> str:
        if self.selected_language == LanguageSelection.MALAYALAM:
            return f"{self.prompts['ai_ml_prompt']} {self.prompts['ml_additional_translation']} {self.prompts['required_malayalam']}"
        elif self.selected_language == LanguageSelection.HINDI:
            return f"{self.prompts['ai_hindi_prompt']} {self.prompts['hindi_additional_translation']} {self.prompts['required_hindi']}"
        elif self.selected_language == LanguageSelection.ARABIC:
            return f"{self.prompts['ai_arabic_prompt']} {self.prompts['arabic_additional_translation']} {self.prompts['required_arabic']}"
        else:  # ENGLISH
            return f"{self.prompts['ai_prompt']} {self.prompts['ai_additional_consideration']} {self.prompts['required_english']}"

    def start_chat(self, history: Optional[List] = None):
        if history is None:
            history = []
        self.history = history
        self.chat = self.model.start_chat(history=self.history)
        return self.chat

    def send_message(self, user_input: str):
        if not self.chat:
            self.start_chat()
        
        # Add JSON formatting instruction to the prompt
        formatted_input = f"""Please provide your response in valid JSON format. The response should be a JSON object with the following structure:
        {{
            "response": "your actual response here",
            "details": {{
                "explanation": "additional explanation if needed",
                "suggestions": ["suggestion1", "suggestion2"]
            }}
        }}

        User message: {user_input}"""
        
        response = self.chat.send_message(formatted_input)
        
        try:
            # Try to parse the response as JSON
            # First, clean the response text by removing markdown code blocks
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            json_response = json.loads(clean_text)
            return json_response
        except json.JSONDecodeError:
            # If parsing fails, return a structured error response
            return {
                "response": response.text,
                "details": {
                    "error": "Response could not be parsed as JSON",
                    "original_response": response.text
                }
            } 