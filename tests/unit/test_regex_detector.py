from src.detector.regex_detector import RegexDetector

class TestRegexDetector:
    def setup_method(self):
        self.detector = RegexDetector()
    
    def test_email_detection(self):
        text = "Клиент отменил заказ. Контакты: foti_95@example.com"
        results = self.detector.detect(text)
        
        email_entities = [ent for ent in results if ent["label"] == "EMAIL"]
        assert len(email_entities) > 0, "No email entities detected"
        
        detected_emails = [ent["text"] for ent in email_entities]
        expected_emails = ["foti_95@example.com"]
        
        for email in expected_emails:
            assert email in detected_emails, f"Expected email {email} not found in detection results"
    
    def test_phone_detection(self):
        text = "Клиент отменил заказ. Контакты: 8 208 159 91 19."
        results = self.detector.detect(text)
        
        phone_entities = [ent for ent in results if ent["label"] == "PHONE"]
        assert len(phone_entities) > 0, "No phone entities detected"
        
        detected_phones = [ent["text"] for ent in phone_entities]
        expected_phones = ["8 208 159 91 19"]
        
        for phone in expected_phones:
            assert phone in detected_phones, f"Expected phone {phone} not found in detection results"