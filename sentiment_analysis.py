from mingpt.model import GPT
from mingpt.bpe import BPETokenizer
import re
import torch

model_type = 'gpt2'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_path = 'models/gpt2_classification'
model = GPT.from_pretrained(model_type, model_path=model_path)
tokenizer = BPETokenizer()

# ship model to device and set to eval mode
model.to(device)
model.eval();

def sentiment_analysis_model(text):
    # check if text is empty
    if text == "":
        return 0

    text = text + " " # the model has difficulties if there is only one token in the input

    inputs = tokenizer(text).to(device)

    response = model.generate(inputs, max_new_tokens=50, temperature=0.7, top_k=40, do_sample=True)

    response = tokenizer.decode(response[0][:-1].cpu().squeeze()) # remove the <|endoftext|> token and decode
    response = response[len(text):] # remove the input text

    print(response)
    
    match = re.search(r'Sentiment: (\d)', response)
    sentiment_value = 0
    if match:
        sentiment_value = int(match.group(1))
    
    return sentiment_value