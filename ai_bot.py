from openai import OpenAI
import pandas as pd
from tqdm import tqdm

client = OpenAI(
    base_url= 'http://localhost:11434/v1',
    api_key='ollama', # required, but unused
)

# Function to extract keywords
def extract_keywords(client, text):
    prompt = f"""
    Extract 5-10 important keywords from the following text:
    "{text}"
    Keywords:"""
    response = client.chat.completions.create(
        model="gemma2:9b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Function to analyze sentiment
def analyze_sentiment(client, text):
    prompt = f"""
    Analyze the sentiment (Positive, Neutral, Negative) of the following text:
    "{text}"
    Sentiment:"""
    response = client.chat.completions.create(
        model="gemma2:9b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Load data
data = pd.read_json('news_data_final_1116.json')
# Keep only the title and summary
data = data[["title", "summary"]]

# Initialize results
results = []

# Process each article
for _, row in tqdm(data.iterrows(), total=len(data), desc="Processing Articles"):
    # Combine title and summary for analysis
    title_summary = f"{row['title']}. {row['summary']}"
    
    # Extract keywords
    keywords = extract_keywords(client, title_summary)
    
    # Analyze sentiment
    sentiment = analyze_sentiment(client, title_summary)
    
    # Append results
    results.append({
        "title": row["title"],
        "summary": row["summary"],
        "keywords": keywords,
        "sentiment": sentiment
    })

# Save results to a CSV file
output = pd.DataFrame(results)
output.to_csv("processed_articles.csv", index=False)

print("Processing complete. Results saved to 'processed_articles.csv'.")