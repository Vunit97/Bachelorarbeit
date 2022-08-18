from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV

from utils import load_data

# Load Data
X_train, X_test, y_train, y_test = load_data(test_size=0.25)


# Just to initialize a model
model = MLPClassifier(max_iter=100)

# Define an Area for parameters
parameter = {
    'hidden_layer_sizes': [(50,50,50), (50,100,50), (100,), (100, 100), (200,), (300,)],
    'activation': ['tanh', 'relu'],
    'solver': ['sgd', 'adam'],
    'batch_size': [128, 256, 512, 1024],
    'alpha': [0.0001, 0.001, 0.005 , 0.05, 0.01],
    'learning_rate': ['constant','adaptive'],
    'max_iter': [200, 300, 400, 500, 700]
}

# Starting GridSearch: Training
grid_search_parameters = GridSearchCV(model, parameter, n_jobs=-1, cv=3)
grid_search_parameters.fit(X_train, y_train)


# Printing best parameters found
print('Best parameters found:\n', grid_search_parameters.best_params_)

"""
After more than 4 hours GridSearchSV:

Best parameter: {
'activation': 'tanh', 
'alpha': 0.001, 
'batch_size': 256, 
'hidden_layer_sizes': (300,), 
'learning_rate': 'constant', 
'max_iter': 500, 
'solver': 'adam'}
}

"""