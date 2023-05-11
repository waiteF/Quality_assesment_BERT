import torch
from transformers import BertTokenizer, BertModel
from scipy.spatial.distance import cosine

def execute_analysis(source_text, target_text):
    # Завантаження BERT-енкодера та токенайзера
    tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
    model = BertModel.from_pretrained('bert-base-multilingual-cased')

    # Функція для отримання векторного представлення тексту
    def get_bert_embedding(text):
        input_ids = torch.tensor([tokenizer.encode(text, add_special_tokens=True)])
        with torch.no_grad():
            last_hidden_states = model(input_ids)[0]
        return torch.mean(last_hidden_states, dim=1).squeeze().numpy()

    # Функція для обчислення схожості між текстами на основі BERT-енкодеру та косинусної близькості
    def compute_similarity(source_text, target_text):
        source_embedding = get_bert_embedding(source_text)
        target_embedding = get_bert_embedding(target_text)
        similarity = 1 - cosine(source_embedding, target_embedding)
        return similarity

    # Приклад порівняння векторних представлень текстів за допомогою косинусної схожості
    similarity = compute_similarity(source_text, target_text)
    print("Similarity score:", similarity)
    return similarity
