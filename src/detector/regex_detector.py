import re

class RegexDetector:
    def detect(self, text):
        result = []

        result.extend(self.find_emails(text))
        result.extend(self.find_phone_numbers(text))

        result.sort(key=lambda x: x["start"])

        return result

    def find_emails(self, text):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return [
            {
                "start": m.start(),
                "end": m.end(),
                "text": m.group(),
                "entity_type": "EMAIL"
            }
            for m in re.finditer(email_pattern, text)
        ]

    def find_phone_numbers(self, text):
        phone_number_pattern = r'(?:\+7|8|7)[\s\-\(\)]*(\d{3})[\s\-\(\)]*(\d{3})[\s\-\(\)]*(\d{2})[\s\-\(\)]*(\d{2})'
        matches = []
        for match in re.finditer(phone_number_pattern, text):
            full_match = match.group()
            matches.append({
                "start": match.start(),
                "end": match.end(),
                "text": full_match,
                "entity_type": "PHONE"
            })
        return matches
