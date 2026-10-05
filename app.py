import math
import random
import tkinter as tk
from tkinter import messagebox

# ---------------------------------------------------------
# 1. EMBEDDED IRIS DATASET (No external dataset files needed)
# ---------------------------------------------------------
# Features: [sepal_length, sepal_width, petal_length, petal_width], Label: Class Index
dataset = [
    # Setosa (0)
    ([5.1, 3.5, 1.4, 0.2], 0), ([4.9, 3.0, 1.4, 0.2], 0), ([4.7, 3.2, 1.3, 0.2], 0),
    ([4.6, 3.1, 1.5, 0.2], 0), ([5.0, 3.6, 1.4, 0.2], 0), ([5.4, 3.9, 1.7, 0.4], 0),
    ([4.6, 3.4, 1.4, 0.3], 0), ([5.0, 3.4, 1.5, 0.2], 0), ([4.4, 2.9, 1.4, 0.2], 0),
    ([4.9, 3.1, 1.5, 0.1], 0), ([5.4, 3.7, 1.5, 0.2], 0), ([4.8, 3.4, 1.6, 0.2], 0),
    # Versicolor (1)
    ([7.0, 3.2, 4.7, 1.4], 1), ([6.4, 3.2, 4.5, 1.5], 1), ([6.9, 3.1, 4.9, 1.5], 1),
    ([5.5, 2.3, 4.0, 1.3], 1), ([6.5, 2.8, 4.6, 1.5], 1), ([5.7, 2.8, 4.5, 1.3], 1),
    ([6.3, 3.3, 4.7, 1.6], 1), ([4.9, 2.4, 3.3, 1.0], 1), ([6.6, 2.9, 4.6, 1.3], 1),
    ([5.2, 2.7, 3.9, 1.4], 1), ([5.0, 2.0, 3.5, 1.0], 1), ([5.9, 3.0, 4.2, 1.5], 1),
    # Virginica (2)
    ([6.3, 3.3, 6.0, 2.5], 2), ([5.8, 2.7, 5.1, 1.9], 2), ([7.1, 3.0, 5.9, 2.1], 2),
    ([6.3, 2.9, 5.6, 1.8], 2), ([6.5, 3.0, 5.8, 2.2], 2), ([7.6, 3.0, 6.6, 2.1], 2),
    ([4.9, 2.5, 4.5, 1.7], 2), ([7.3, 2.9, 6.3, 1.8], 2), ([6.7, 2.5, 5.8, 1.8], 2),
    ([6.8, 3.0, 5.5, 2.1], 2), ([5.7, 2.5, 5.0, 2.0], 2), ([5.8, 2.8, 5.1, 2.4], 2)
]

target_names = ["Setosa", "Versicolor", "Virginica"]

# ---------------------------------------------------------
# 2. PURE PYTHON ML ALGORITHM (K-NEAREST NEIGHBORS - KNN)
# ---------------------------------------------------------
def euclidean_distance(point1, point2):
    """Calculates straight-line distance between two feature vectors."""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

def knn_predict(train_data, new_sample, k=3):
    """Finds the k closest dataset points and votes on the class."""
    distances = []
    for features, label in train_data:
        dist = euclidean_distance(features, new_sample)
        distances.append((dist, label))
    
    # Sort by distance and pick top K neighbors
    distances.sort(key=lambda x: x[0])
    k_neighbors = [label for _, label in distances[:k]]
    
    # Return the label with maximum occurrences
    return max(set(k_neighbors), key=k_neighbors.count)

def calculate_accuracy(data_list, k=3):
    """Evaluates accuracy using Leave-One-Out validation."""
    correct = 0
    for i in range(len(data_list)):
        # Unpack the features and true label directly
        features, true_label = data_list[i]
        
        # Create training subset excluding current test sample
        train_subset = data_list[:i] + data_list[i+1:]
        
        # Pass 'features' directly (NOT test_sample[0])
        predicted_label = knn_predict(train_subset, features, k)
        
        if predicted_label == true_label:
            correct += 1
    return (correct / len(data_list)) * 100

# Compute accuracy score at start
model_accuracy = calculate_accuracy(dataset, k=3)

# ---------------------------------------------------------
# 3. TKINTER UI & HANDLERS
# ---------------------------------------------------------
def predict_species():
    try:
        # Fetch inputs from UI text fields
        sepal_length = float(entry_sepal_length.get())
        sepal_width = float(entry_sepal_width.get())
        petal_length = float(entry_petal_length.get())
        petal_width = float(entry_petal_width.get())
        
        # Prepare test sample
        new_sample = [sepal_length, sepal_width, petal_length, petal_width]
        
        # Make Prediction via custom KNN
        prediction_index = knn_predict(dataset, new_sample, k=3)
        predicted_class = target_names[prediction_index]
        
        # Update output UI label
        lbl_result.config(text=f"Prediction: {predicted_class}", fg="#2E7D32")

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numerical values in all fields.")

def reset_fields():
    defaults = ["5.1", "3.5", "1.4", "0.2"]
    for ent, val in zip(entries, defaults):
        ent.delete(0, tk.END)
        ent.insert(0, val)
    lbl_result.config(text="Prediction: Ready", fg="#555555")

# Initialize Main Window
root = tk.Tk()
root.title("Custom ML Predictor - Iris Classification")
root.geometry("400x480")
root.config(padx=20, pady=20)

# Title Header
lbl_header = tk.Label(root, text="Iris Species Predictor", font=("Helvetica", 16, "bold"))
lbl_header.pack(pady=(5, 0))

# Model Accuracy Display Label
lbl_accuracy = tk.Label(
    root, 
    text=f"KNN Model Accuracy: {model_accuracy:.1f}%", 
    font=("Helvetica", 10, "italic"), 
    fg="#007ACC"
)
lbl_accuracy.pack(pady=(0, 15))

# Input Form Setup
fields = [
    ("Sepal Length (cm):", "5.1"),
    ("Sepal Width (cm):", "3.5"),
    ("Petal Length (cm):", "1.4"),
    ("Petal Width (cm):", "0.2")
]

entries = []
for label_text, default_val in fields:
    frame = tk.Frame(root)
    frame.pack(fill="x", pady=5)
    
    lbl = tk.Label(frame, text=label_text, width=18, anchor="w")
    lbl.pack(side="left")
    
    ent = tk.Entry(frame)
    ent.insert(0, default_val)
    ent.pack(side="right", expand=True, fill="x")
    entries.append(ent)

entry_sepal_length, entry_sepal_width, entry_petal_length, entry_petal_width = entries

# Button Frame
btn_frame = tk.Frame(root)
btn_frame.pack(fill="x", pady=15)

btn_predict = tk.Button(
    btn_frame, 
    text="Predict", 
    command=predict_species, 
    bg="#1976D2", 
    fg="white", 
    font=("Helvetica", 11, "bold"), 
    pady=5,
    width=14
)
btn_predict.pack(side="left", padx=(0, 5))

btn_reset = tk.Button(
    btn_frame, 
    text="Reset", 
    command=reset_fields, 
    bg="#757575", 
    fg="white", 
    font=("Helvetica", 11, "bold"), 
    pady=5,
    width=14
)
btn_reset.pack(side="right", padx=(5, 0))

# Output Result Display Label
lbl_result = tk.Label(root, text="Prediction: Ready", font=("Helvetica", 13, "bold"), fg="#555555")
lbl_result.pack(pady=10)

# Run Application Loop
root.mainloop()