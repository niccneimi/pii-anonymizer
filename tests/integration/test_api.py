import requests
from unittest.mock import patch
from src.api.main import app
from fastapi.testclient import TestClient

class TestAnonymizeEndpoint:
    def setup_method(self):
        self.client = TestClient(app)
        self.anonymize_url = "/api/anonymize"
        
    @patch('src.detector.ensemble_detector.detect_pii')
    def test_anonymize_ensemble_mode(self, mock_gliner_predict):
        mock_gliner_predict.return_value = [
            {"text": "Сергеев Епифан Трифонович", "label": "PERSON", "start": 22, "end": 48},
            {"text": "tamaraisakova@example.net", "label": "EMAIL", "start": 58, "end": 83},
            {"text": "+7 895 570 25 61", "label": "PHONE_NUMBER", "start": 93, "end": 111},
            {"text": "с. Ребриха, ул. Большая", "label": "ADDRESS", "start": 121, "end": 145},
        ]

        test_data = {
            "text": "Поддержка, помогите! Я Сергеев Епифан Трифонович, мой email tamaraisakova@example.net, телефон +7 895 570 25 61, адрес с. Ребриха, ул. Большая",
            "mode": "ensemble"
        }

        response = self.client.post(
            self.anonymize_url,
            json=test_data
        )

        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        
        result = response.json()
        assert "anonymized_text" in result, "Response should contain anonymized_text field"
        
        anonymized_text = result["anonymized_text"]
        assert "[PERSON]" in anonymized_text, "Anonymized text should contain [PERSON] placeholder"
        assert "[EMAIL]" in anonymized_text, "Anonymized text should contain [EMAIL] placeholder"
        assert "[PHONE_NUMBER]" in anonymized_text, "Anonymized text should contain [PHONE] placeholder"
        assert "[ADDRESS]" in anonymized_text, "Anonymized text should contain [ADDRESS] placeholder"
        
        original_pii = [
            "Сергеев Епифан Трифонович",
            "tamaraisakova@example.net",
            "+7 895 570 25 61",
            "с. Ребриха, ул. Большая"
        ]
        
        for pii in original_pii:
            assert pii not in anonymized_text, f"Original PII '{pii}' should not be present in anonymized text"