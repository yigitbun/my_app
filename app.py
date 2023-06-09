

# Set up OpenAI API key
#openai.api_key = "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"

from flask import Flask
import requests
from bs4 import BeautifulSoup
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

# Load the links from the text file into a list
with open('medium_links.txt', 'r') as file:
    links = [line.strip() for line in file]

# Initialize the summarization model and tokenizer
model = T5ForConditionalGeneration.from_pretrained('t5-small')
tokenizer = T5Tokenizer.from_pretrained('t5-small')

@app.route('/')
def summarize_articles():
    summaries = {}
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('article')
        if article:
            # Get the article content
            content = article.get_text(separator='\n')
            # Generate a summary using the T5 model
            input_ids = tokenizer.encode('summarize: ' + content, return_tensors='pt', max_length=512, truncation=True)
            summary_ids = model.generate(input_ids, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            # Store the summary and original article URL in a dictionary
            summaries[link] = {'summary': summary, 'url': link}
    # Write the summaries to a text file
    with open('article_summaries.txt', 'w') as file:
        for summary in summaries.values():
            file.write(f"{summary['summary']}\n\nOriginal Article: {summary['url']}\n\n")
    return 'Article summaries generated and saved to file.'

if __name__ == '__main__':
    app.run(debug=True)
