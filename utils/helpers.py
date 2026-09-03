import re

def valider_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def valider_telephone(telephone):
    pattern = r'^(\+[0-9]{1,3})?[0-9]{9,12}$'
    return re.match(pattern, telephone) is not None