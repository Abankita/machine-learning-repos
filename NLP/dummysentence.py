import os
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = 'all-MiniLM-L6-v2'
MODEL_FOLDER = 'model'

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

def load_or_download_model():
    model_path = os.path.join(MODEL_FOLDER, MODEL_NAME)
    if os.path.exists(model_path):
        print(f"Loading model from {model_path}")
        return SentenceTransformer(model_path)
    else:
        print(f"Downloading model {MODEL_NAME}")
        model = SentenceTransformer(MODEL_NAME)
        os.makedirs(MODEL_FOLDER, exist_ok=True)
        model.save(model_path)
        print(f"Model saved to {model_path}")
        return model

def find_similar_sentences(query, file_path, top_n=5):
    # Load the pre-trained model
    model = load_or_download_model()

    # Load and encode the sentences from the file
    sentences = load_file(file_path)
    sentence_embeddings = model.encode(sentences)

    # Encode the query
    query_embedding = model.encode([query])

    # Calculate cosine similarities
    cosine_scores = util.pytorch_cos_sim(query_embedding, sentence_embeddings)[0]

    # Get top N results
    top_results = sorted(zip(sentences, cosine_scores), key=lambda x: x[1], reverse=True)[:top_n]

    return top_results

def main():
    print("Welcome to the Sentence Similarity Search Tool!")
    
    # Get user input for query
    query = input("Enter your query: ")
    
    # Get user input for file path
    file_name = input("Enter the name of your text file (without .txt extension): ")
    file_path = f"{file_name}.txt"

    try:
        results = find_similar_sentences(query, file_path)

        print(f"\nTop 5 similar sentences for query: '{query}'\n")
        for sentence, score in results:
            print(f"Similarity: {score:.4f}")
            print(f"Sentence: {sentence}\n")
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file name and try again.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()