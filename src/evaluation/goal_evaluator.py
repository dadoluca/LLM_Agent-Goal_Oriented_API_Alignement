from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk
import numpy as np
from sklearn.metrics import auc

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

    def evaluate(self, generated_goals, reference_goals, threshold=0.9, similarities=False):
        """
        Evaluate the effectiveness of the generated goals.
        """
        # Compute cosine similarity between generated and reference goals
        if type(similarities) == bool:
            similarities = self.compute_similarity(generated_goals, reference_goals)
            
        rate_table =  np.empty((len(generated_goals), len(reference_goals)), dtype=object)
        
        # Initialize counters for TP, FP, TN, FN
        tp = 0  # True Positives
        fp = 0  # False Positives
        tn = 0  # True Negatives
        fn = 0  # False Negatives

        matched_refs = set()

        # Loop through generated goals and check their matches with reference goals
        for gen_idx, gen_goal in enumerate(generated_goals):
            # Find the best match for the current generated goal
            best_match_score = similarities[gen_idx].max()

            for ref_idx, ref_goal in enumerate(reference_goals):
                similarity_cell = similarities[gen_idx, ref_idx]
                current_eval = ""
                if  similarity_cell >= threshold:
                    if similarity_cell == best_match_score and ref_idx not in matched_refs: #if it is the best match, it is above t and we haven't used the reference goal yet
                        tp += 1  # Correctly matched goal
                        current_eval = "TP"
                        matched_refs.add(ref_idx)
                    else:
                        fp += 1  # Incorrectly matched goal
                        current_eval = "FP"
                else:
                    if similarity_cell == best_match_score:
                        fn += 1 # If the best match doesn't meet the threshold, it's a false negative
                        current_eval = "FN"
                    else:
                        tn += 1
                        current_eval = "TN"

                rate_table[gen_idx, ref_idx] =f"({current_eval})" +f" {similarity_cell:.2f}"
        
        # Precision: TP / (TP + FP)
        precision = tp / (tp + fp + 1e-9)

        # Recall: TP / (TP + FN)
        recall = tp / (tp + fn + 1e-9)
        
        # F1 Score: 2 * (Precision * Recall) / (Precision + Recall)
        f1_score = 2 * (precision * recall) / (precision + recall + 1e-9)
        
        # False Positive Rate: FP / (FP + TN)
        fpr = fp / (fp + tn + 1e-9) 
        
        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "fpr": fpr,
            "similarities": similarities,
            "rate_table": rate_table
        }
        
    def print_roc_prec_rec_curve(self, generated_goals, reference_goals, hide_roc=False,   hide_prec_rec=False, save_to_file=False, output_file="output.txt"):     
        """
        Plot the ROC and Precision-Recall curves for the generated goals.
        """           
        recall_arr = []
        precision_arr = []
        fpr_arr = []
        summary = []

        similarities = self.compute_similarity(generated_goals, reference_goals)
        
        for th in np.arange(0.01, 1, 0.01):
            # Computes the Similarities Matrix
            results = self.evaluate(generated_goals, reference_goals, th, similarities=similarities)

            recall_arr.append(results["recall"])
            fpr_arr.append(results["fpr"])
            precision_arr.append(results["precision"])
            
            summary.append(f"{th} {results["recall"]} {results['fpr']} {results['f1_score']} {results["precision"]}")
            
            if save_to_file:
                with open(output_file, "a") as f:
                    f.write(f"{th} {results["recall"]} {results['fpr']} {results['f1_score']} {results["precision"]}\n")

        auc_roc = auc(fpr_arr, recall_arr) 
        auc_prec_rec = auc(recall_arr, precision_arr)
        
        if not hide_prec_rec:
            # Plot della Precision-Recall Curve
            plt.figure(figsize=(8, 6))
            plt.plot(precision_arr, recall_arr, marker='o', linestyle='-', color='b', label="Precision-Recall Curve")
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            plt.title("Precision-Recall Curve")
            plt.legend()
            plt.grid()
            plt.show()
            
        if not hide_roc:
            # Plot della ROC Curve
            plt.figure(figsize=(8, 6))
            plt.plot(fpr_arr, recall_arr, marker='o', linestyle='-', color='b', label="ROC")
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.title("ROC Curve")
            plt.legend()
            plt.grid()
            plt.show()
            
        return auc_roc, auc_prec_rec, summary