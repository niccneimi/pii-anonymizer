import re

def find_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return [{"start": m.start(), "end": m.end(), "label": "EMAIL"} for m in re.finditer(email_pattern, text)]

def find_phone_numbers(text):
    phone_number_pattern = r'(?:\+7|8|7)[\s\-\(\)]*(\d{3})[\s\-\(\)]*(\d{3})[\s\-\(\)]*(\d{2})[\s\-\(\)]*(\d{2})'
    return [{"start": m.start(), "end": m.end(), "label": "PHONE_NUMBER"} for m in re.finditer(phone_number_pattern, text)]

def find_pii(text):
    result = []

    [result.append(el) for el in find_emails(text)] 
    [result.append(el) for el in find_phone_numbers(text)]

    result.sort(key=lambda x: x["start"], reverse=True)
    
    return result