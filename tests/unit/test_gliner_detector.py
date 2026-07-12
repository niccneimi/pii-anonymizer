from src.detector.gliner_detector import gliner_predict

class TestGlinerDetector:
    def test_model_loading(self):
        result = gliner_predict("Test text", ["PERSON"])
        
        assert isinstance(result, list), "Model should return a list of predictions"
        
        empty_result = gliner_predict("", ["PERSON"])
        assert isinstance(empty_result, list), "Model should handle empty text"

    def test_prediction_on_short_text(self):
        short_text = "Почта Марины Степановны marianskaya_vpadina@gmail.com"
        labels = ["PERSON", "EMAIL"]
        
        predictions = gliner_predict(short_text, labels)
        
        assert isinstance(predictions, list), "Predictions should be returned as a list"

        if len(predictions) > 0:
            first_pred = predictions[0]
            assert "text" in first_pred, "Prediction should contain extracted text"
            assert "label" in first_pred, "Prediction should contain label"
            assert "score" in first_pred, "Prediction should contain confidence score"
            assert isinstance(first_pred["score"], float), "Score should be a float"
            assert 0 <= first_pred["score"] <= 1, "Score should be between 0 and 1"
