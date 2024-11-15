from flask import Flask, request, jsonify
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
import torch

tokenizer = XLMRobertaTokenizer.from_pretrained('classla/xlm-roberta-base-multilingual-text-genre-classifier')
model = XLMRobertaForSequenceClassification.from_pretrained('classla/xlm-roberta-base-multilingual-text-genre-classifier')

GENRE_LABELS = [
    "Other", "Information", "News", "Instruction", "Argumentation", 
    "Forum", "Fiction", "Legal", "Promotion"
]

app = Flask(__name__)

@app.route('/classify_genre', methods=['POST'])
def classify_genre():

    data = request.json
    text = data.get("text", "")
    

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
    
    probabilities = torch.nn.functional.softmax(logits, dim=-1)
    
    probs = probabilities.squeeze().tolist()
    predicted_genre_index = probs.index(max(probs))
    predicted_genre = GENRE_LABELS[predicted_genre_index]
    
    return jsonify({
        "predicted_genre": predicted_genre,
        "probabilities": probs
    })

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
