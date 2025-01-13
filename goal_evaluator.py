from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch

from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk

# Download the punkt tokenizer and other required resources
nltk.download('punkt')  # Tokenizer for splitting text into words/sentences
nltk.download('punkt_tab')  # Tokenizer for splitting text into words/sentences
nltk.download('wordnet')  # WordNet lemmatizer data
nltk.download('omw-1.4')  # Open Multilingual WordNet data (optional for lemmatization)
class GoalEvaluator:
    def __init__(self, model_name="bert-base-uncased", preprocess=True):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        if not preprocess:
            self.preprocess_text = lambda text: text
    

    def preprocess_text(self, text):
        """
        Preprocess the input text using stemming and lemmatization.
        """
        # Tokenize the text
        tokens = word_tokenize(text)
        # Apply stemming and lemmatization
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens] #to reduce words to their base forms (e.g., "running" → "run").
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in stemmed_tokens] #to normalize words to their dictionary forms (e.g., "ran" → "run").
        # Reconstruct the text
        preprocessed_text = " ".join(lemmatized_tokens)
        return preprocessed_text

    def encode_texts(self, texts):
        """
        Encode a list of texts using BERT with preprocessing.
        """
        # Preprocess each text
        preprocessed_texts = [self.preprocess_text(text) for text in texts]
        # Tokenize and encode with BERT
        inputs = self.tokenizer(preprocessed_texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
        return embeddings

    def compute_similarity(self, generated_goals, reference_goals):
        """
        Compute cosine similarity between generated and reference goals.

        Each column corresponds to a manual goal and each row corresponds to a generated goal.
        """
        gen_embeddings = self.encode_texts(generated_goals)
        ref_embeddings = self.encode_texts(reference_goals)
        similarities = cosine_similarity(gen_embeddings, ref_embeddings)
        return similarities

    def evaluate(self, generated_goals, reference_goals, threshold=0.9):
        """
        Evaluate the effectiveness of the generated goals.
        """
        # Compute cosine similarity between generated and reference goals
        similarities = self.compute_similarity(generated_goals, reference_goals)
        
        # Initialize counters for TP, FP, TN, FN
        tp = 0  # True Positives
        fp = 0  # False Positives
        tn = 0  # True Negatives
        fn = 0  # False Negatives

        # Loop through generated goals and check their matches with reference goals
        for gen_idx, gen_goal in enumerate(generated_goals):
            # Find the best match for the current generated goal
            best_match_score = similarities[gen_idx].max()
            best_match_idx = similarities[gen_idx].argmax()
            
            # Determine if it meets the threshold
            if best_match_score >= threshold:
                # Check if the match is a true positive
                if gen_idx == best_match_idx:  # Assuming perfect one-to-one mapping for ground truth
                    tp += 1  # Correctly matched goal
                else:
                    fp += 1  # Incorrectly matched goal
            else:
                # If no match meets the threshold, it's a false negative
                fn += 1
            
            # Precision: TP / (TP + FP)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0

            # Recall: TP / (TP + FN)
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0

            # F1 Score: 2 * (Precision * Recall) / (Precision + Recall)
            f1_score = 2 * (precision * recall) / (precision + recall + 1e-9) if (precision + recall) > 0 else 0
        
        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "similarities": similarities
        }











'''
        similarities = self.compute_similarity(generated_goals, reference_goals)
        matches = (similarities.max(axis=1) > threshold).astype(int)
        TP = sum(matches)
        total_number_of_generated_goals = len(generated_goals) #as every generated goal is considered a prediction
        precision = TP / total_number_of_generated_goals #TP / TP + FP
        recall = TP / len(reference_goals)  #TP / TP + FN
        f1_score = 2 * (precision * recall) / (precision + recall + 1e-9)
'''