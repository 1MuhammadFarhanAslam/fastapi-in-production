import requests
from transformers import pipeline


class MLModelService:
    def __init__(self, use_api=True):
        self.use_api = use_api
        self.api_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
        self.classifier = None
    
    def load_model(self):
        if not self.use_api:
            self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
    
    def unload_model(self):
        self.classifier = None
    
    def predict(self, payload):
        from fastapi_mlops_template.schemas.response import TextPredictionResponse
        
        text = payload.text if hasattr(payload, 'text') else str(payload)
        
        if self.use_api:
            return self._predict_api(text)
        else:
            return self._predict_local(text)
    
    def _predict_api(self, text):
        from fastapi_mlops_template.schemas.response import TextPredictionResponse
        
        try:
            response = requests.post(self.api_url, json={"inputs": text})
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return TextPredictionResponse(prediction=result[0])
                else:
                    return TextPredictionResponse(prediction={"error": f"Unexpected response: {result}"})
            else:
                return TextPredictionResponse(prediction={"error": f"API error {response.status_code}: {response.text}"})
        except Exception as e:
            return TextPredictionResponse(prediction={"error": f"Request failed: {str(e)}"})
    
    def _predict_local(self, text):
        from fastapi_mlops_template.schemas.response import TextPredictionResponse
        
        if not self.classifier:
            self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        
        result = self.classifier(text)
        return TextPredictionResponse(prediction=result[0])