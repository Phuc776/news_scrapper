import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas as pd

def clean_data(data_json):
    data = pd.DataFrame(data_json)
    data.dropna(subset=['title', 'summary', 'author'], inplace=True)  
    return data

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'\W+', ' ', text.lower())  
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)