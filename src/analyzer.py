
import google.generativeai as genai
import json
import streamlit as st
from .config import GENERATION_CONFIG

class AudioAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config=GENERATION_CONFIG
        )
    
    def analyze(self, letter: str, reference_audio: str, test_audio: str) -> dict:  # metod ismi değiştirildi
        try:
            prompt = f"""You will analyze two audio files for the pronunciation of the letter "{letter}".
            Audio files:
            1. Reference audio: {reference_audio}
            2. Test audio: {test_audio}
            
            Provide your analysis in the following JSON format only, with values in Turkish:
            {{
                "pronunciation_score": <0-100 arası sayısal değer>,
                "areas_of_improvement": "<iyileştirme alanlarını açıklayan Türkçe metin>",
                "detailed_feedback": {{
                    "vowel_sounds": "<ünlü sesler hakkında Türkçe geri bildirim>",
                    "consonant_sounds": "<ünsüz sesler hakkında Türkçe geri bildirim>",
                    "clarity": "<netlik hakkında Türkçe geri bildirim>"
                }},
                "confidence_score": <0-100 arası sayısal değer>
            }}
            
            Rules:
            1. Provide ONLY the JSON response, no additional text
            2. Ensure all text values are in Turkish
            3. Ensure all numeric values are between 0 and 100
            4. Do not include any explanations or notes outside the JSON structure
            """
            
            response = self.model.generate_content(
                prompt,
                stream=False
            )
            
            if response and response.text:
                return json.loads(response.text)
            else:
                raise ValueError("API yanıt vermedi")
                
        except Exception as e:
            st.error(f"Analiz sırasında hata: {str(e)}")
            return None