from typing import List , Dict
from src.helper import TextProcessor
from src.helper import bow_vect , svc_model
from src.helper import SENTIMENT_MAPPING



class TextClassifier:
    def __init__(self):
        self.processor = TextProcessor()
        self.vectorizer = bow_vect
        self.model = svc_model
        self.sentiment_mapping = SENTIMENT_MAPPING

    def predict(self, texts: List[str]) -> List[Dict[str, str]]:
        # Clean and preprocess texts
        cleaned_texts = [self.processor.clean_text(text) for text in texts]
        
        # Vectorize
        vectors = self.vectorizer.transform(cleaned_texts).toarray()
        
        # Predict
        raw_predictions = self.model.predict(vectors)
        
        # Create sentiment predictions as list of dictionaries
        predictions = []
        for text, label in zip(texts, raw_predictions):
            prediction_dict = {
                "text": text,
                "sentiment": self.sentiment_mapping[int(label)]
            }
            predictions.append(prediction_dict)
        
        return predictions