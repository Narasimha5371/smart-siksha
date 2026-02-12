import httpx
from typing import Optional
from config import settings

class TranslationService:
    """
    Translation service using LibreTranslate (free and open source)
    """
    
    def __init__(self):
        self.base_url = settings.LIBRETRANSLATE_URL
        self.api_key = settings.LIBRETRANSLATE_API_KEY
    
    async def translate(
        self,
        text: str,
        source_lang: str = "en",
        target_lang: str = "hi"
    ) -> Optional[str]:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'en')
            target_lang: Target language code (e.g., 'hi')
        
        Returns:
            Translated text or None if translation fails
        """
        if source_lang == target_lang:
            return text
        
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "q": text,
                    "source": source_lang,
                    "target": target_lang,
                    "format": "text"
                }
                
                # Add API key if configured
                if self.api_key:
                    payload["api_key"] = self.api_key
                
                response = await client.post(
                    self.base_url,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("translatedText", text)
                else:
                    print(f"Translation error: {response.status_code} - {response.text}")
                    return text  # Return original text on error
                    
        except Exception as e:
            print(f"Translation exception: {str(e)}")
            return text  # Return original text on exception
    
    async def detect_language(self, text: str) -> str:
        """
        Detect language of text
        
        Args:
            text: Text to detect language
        
        Returns:
            Language code (e.g., 'en', 'hi')
        """
        try:
            async with httpx.AsyncClient() as client:
                payload = {
                    "q": text
                }
                
                if self.api_key:
                    payload["api_key"] = self.api_key
                
                response = await client.post(
                    self.base_url.replace("/translate", "/detect"),
                    json=payload,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    detections = result.get("detections", [])
                    if detections and len(detections) > 0:
                        return detections[0].get("language", "en")
                
                return "en"  # Default to English
                
        except Exception as e:
            print(f"Language detection exception: {str(e)}")
            return "en"
    
    def get_supported_languages(self) -> dict:
        """
        Returns supported language codes and names
        """
        return {
            "en": "English",
            "hi": "Hindi - हिंदी",
            "ta": "Tamil - தமிழ்",
            "te": "Telugu - తెలుగు",
            "bn": "Bengali - বাংলা",
            "mr": "Marathi - मराठी",
            "gu": "Gujarati - ગુજરાતી",
            "kn": "Kannada - ಕನ್ನಡ",
            "ml": "Malayalam - മലയാളം",
            "pa": "Punjabi - ਪੰਜਾਬੀ"
        }

# Global translation service instance
translation_service = TranslationService()
