from flask import Flask, request, jsonify
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification, GPT2LMHeadModel, GPT2Tokenizer
import torch

tokenizer = XLMRobertaTokenizer.from_pretrained('classla/xlm-roberta-base-multilingual-text-genre-classifier')
model = XLMRobertaForSequenceClassification.from_pretrained('classla/xlm-roberta-base-multilingual-text-genre-classifier')

GENRE_LABELS = [
    "Other", "Information", "News", "Instruction", "Argumentation", 
    "Forum", "Fiction", "Legal", "Promotion"
]

tokenizer_2 = GPT2Tokenizer.from_pretrained('gpt2')
model_2 = GPT2LMHeadModel.from_pretrained('gpt2', pad_token_id=tokenizer.eos_token_id)

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

@app.route('/generate_suggestions', methods=['POST'])
def generate_suggestions():
    data = request.json
    input_text = data.get("text", "")

    inputs = tokenizer_2.encode(input_text, return_tensors='pt')
    outputs = model_2.generate(inputs, max_length=1000, do_sample=True, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)

    text = tokenizer_2.decode(outputs[0], skip_special_tokens=True)

    final = str(text).replace(input_text,  "")

    return jsonify({ "suggestions": final  })



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
