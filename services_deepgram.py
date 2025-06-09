import asyncio
import json
import httpx
from utils import DEEPGRAM_API_KEY, DEEPGRAM_MODEL, DEEPGRAM_LANGUAGE

class DeepgramService:
    def __init__(self):
        self.api_key = DEEPGRAM_API_KEY
        self.base_url = "https://api.deepgram.com/v1"
        
    async def transcribe(self, audio_data):
        """Transcribe audio using Deepgram API"""
        try:
            url = f"{self.base_url}/listen"
            
            headers = {
                "Authorization": f"Token {self.api_key}",
                "Content-Type": "audio/wav"
            }
            
            params = {
                "model": DEEPGRAM_MODEL,
                "language": DEEPGRAM_LANGUAGE,
                "smart_format": "true",
                "punctuate": "true"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    headers=headers,
                    params=params,
                    content=audio_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if "results" in result and "channels" in result["results"]:
                        alternatives = result["results"]["channels"][0]["alternatives"]
                        if alternatives:
                            transcript = alternatives[0]["transcript"]
                            return transcript.strip()
                    return ""
                else:
                    print(f"Deepgram API error: {response.status_code} - {response.text}")
                    return ""
                    
        except Exception as e:
            print(f"Deepgram transcription error: {e}")
            return ""
