from flask import Flask, request, jsonify
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import torch

# Load the pre-trained model and tokenizer
tokenizer = XLMRobertaTokenizer.from_pretrained('classla/xlm-roberta-base-multilingual-text-genre-classifier')
model = XLMRobertaForSequenceClassification.from_pretrained('classla/xlm-roberta-base-multilingual-text-genre-classifier')

# Define the genre labels as per the model's training
GENRE_LABELS = [
    "Other", "Information/Explanation", "News", "Instruction", "Opinion/Argumentation", 
    "Forum", "Prose/Lyrical", "Legal", "Promotion"
]

app = Flask(__name__)

@app.route('/classify_genre', methods=['POST'])
def classify_genre():
    # Get the input text from the request
    data = request.json
    text = data.get("text", "")
    
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    # Run the model to get the logits
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    # Apply softmax to get probabilities
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    
    # Get the genre with the highest probability
    predicted_genre_index = torch.argmax(probabilities, dim=-1).item()
    predicted_genre = GENRE_LABELS[predicted_genre_index]
    
    # Return the genre and the probabilities
    return jsonify({
        "predicted_genre": predicted_genre,
        "probabilities": probabilities.squeeze().tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
