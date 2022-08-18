from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import os
import pickle

from utils import load_data

# Best parameter by grid_search.py
best_parameters = {
    'activation': 'tanh',
    'alpha': 0.001,
    'batch_size': 256,
    'hidden_layer_sizes': (300,),
    'learning_rate': 'constant',
    'max_iter': 500,
    'solver': 'adam',
    'verbose': 'true',
}

# load Dataset, 75% train 25% test (Ravdess and TESS)
X_train, X_test, y_train, y_test = load_data(test_size=0.25)

# Initialize the model
model = MLPClassifier(**best_parameters)

# train, predict the model
print("Start training the model")
model.fit(X_train, y_train)
prediction = model.predict(X_test)

# Loss Function Value
loss_value = model.loss_curve_
plt.ylabel('loss')
plt.xlabel('iteration')
plt.title("MlpClassifier")
plt.plot(loss_value)
plt.show()

# Create a confusion matrix to visualize the performance
cm = confusion_matrix(y_test, prediction, labels=["happy", "sad", "angry", "neutral"])
cm_display = ConfusionMatrixDisplay(cm, display_labels=["happy", "sad", "angry", "neutral"]).plot()
plt.show()

#Calculate accuracy
accuracy = accuracy_score(y_test, prediction)
print("Accuracy: {:.2f}%".format(accuracy * 100))

# Saving the model with pickle
if not os.path.isdir("result"):
    os.mkdir("result")

pickle.dump(model, open("result/mlp_classifier", "wb"))
