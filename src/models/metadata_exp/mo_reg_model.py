import sys
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# Preprocessing
def load_and_preprocess():
    train_data = pd.read_csv('train.csv')
    val_data = pd.read_csv('val.csv')
    test_data = pd.read_csv('test.csv')

    # get rid of years missing features/labels
    train_data = train_data.dropna()
    val_data = val_data.dropna()
    test_data = test_data.dropna()

    for dataset in [train_data, val_data, test_data]:
        dataset['text'] = dataset['lyrics'] + " " + dataset['tags']

    # define targets, get year for visualization
    target_cols = ['AVERAGE_APPROVAL_Pres', 'AVERAGE_APPROVAL_Congress', 'AVERAGE_GDP', 'EF_Summary_Index']
    year_col = train_data.columns[0]
    X_train, y_train, years_train = train_data['text'], train_data[target_cols].values, train_data[year_col].values
    X_val, y_val, years_val = val_data['text'], val_data[target_cols].values, val_data[year_col].values
    X_test, y_test, years_test = test_data['text'], test_data[target_cols].values, test_data[year_col].values

    # TF-IDF to vectorize text content
    vectorizer = TfidfVectorizer(max_features=300)
    X_train_tfidf = vectorizer.fit_transform(X_train).toarray()
    X_val_tfidf = vectorizer.transform(X_val).toarray()
    X_test_tfidf = vectorizer.transform(X_test).toarray()

    # scale inputs & outputs
    scaler = StandardScaler()
    X_train_tfidf = scaler.fit_transform(X_train_tfidf)
    X_val_tfidf = scaler.transform(X_val_tfidf)
    X_test_tfidf = scaler.transform(X_test_tfidf)
    target_scaler = MinMaxScaler()
    y_train = target_scaler.fit_transform(y_train)
    y_val = target_scaler.transform(y_val)
    y_test = target_scaler.transform(y_test)

    return X_train_tfidf, y_train, years_train, X_val_tfidf, y_val, years_val, X_test_tfidf, y_test, years_test, vectorizer, scaler, target_scaler

# plotting functions, metrics

# visualize preds v true vals
def plot_predictions(predictions, true_values, years_test):
    features = ['Presidential Approval', 'Congressional Approval', 'GDP', 'Economic Freedom']
    num_features = len(features)

    for i in range(num_features):
        plt.figure(figsize=(8, 6))
        plt.scatter(true_values[:, i], predictions[:, i], alpha=0.7)
        plt.plot([min(true_values[:, i]), max(true_values[:, i])],
                 [min(true_values[:, i]), max(true_values[:, i])], color='red', linestyle='--')
        plt.title(f"Predicted vs. True Values for {features[i]}")
        plt.xlabel("True Values")
        plt.ylabel("Predicted Values")
        plt.show()

# over time
def plot_over_time(predictions, true_values, years_test):
    features = ['Presidential Approval', 'Congressional Approval', 'GDP', 'Economic Freedom']
    num_features = len(features)

    for i in range(num_features):
        plt.figure(figsize=(10, 6))
        plt.plot(years_test, true_values[:, i], label="True Values", marker='o')
        plt.plot(years_test, predictions[:, i], label="Predictions", marker='x')
        plt.title(f"{features[i]} Over Time")
        plt.xlabel("Year")
        plt.ylabel(features[i])
        plt.legend()
        plt.show()
# get r^2 metric
def compute_r2_score(predictions, true_values):
    r2_per_feature = r2_score(true_values, predictions, multioutput='raw_values')
    print("R-squared for each feature:")
    for i, feature in enumerate(['Presidential Approval', 'Congressional Approval', 'GDP', 'Economic Freedom']):
        print(f"{feature}: {r2_per_feature[i]}")

# Model!
class MultiOutputRegressionModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(MultiOutputRegressionModel, self).__init__()
        self.hidden1 = nn.Linear(input_dim, 128)
        self.hidden2 = nn.Linear(128, 64)
        self.output = nn.Linear(64, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.hidden1(x))
        x = self.relu(self.hidden2(x))
        x = self.output(x)
        return x

def train_model(model, X_train, y_train, X_val, y_val, epochs=100, lr=0.001):
    X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32)
    X_val_tensor = torch.tensor(X_val, dtype=torch.float32)
    y_val_tensor = torch.tensor(y_val, dtype=torch.float32)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        predictions = model(X_train_tensor)
        loss = criterion(predictions, y_train_tensor)
        loss.backward()
        optimizer.step()

        if epoch % 10 == 0:
            model.eval()
            with torch.no_grad():
                val_predictions = model(X_val_tensor)
                val_loss = criterion(val_predictions, y_val_tensor)
            print(f"Epoch {epoch}/{epochs}, Train Loss: {loss.item()}, Val Loss: {val_loss.item()}")

    return model

def evaluate_model(model, X_test, y_test, target_scaler):
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

    model.eval()
    with torch.no_grad():
        test_predictions = model(X_test_tensor).numpy()
        test_predictions_original_scale = target_scaler.inverse_transform(test_predictions)
        y_test_original_scale = target_scaler.inverse_transform(y_test)

    mse_per_feature = np.mean((test_predictions_original_scale - y_test_original_scale) ** 2, axis=0)
    print("MSE for each feature:")
    for i, feature in enumerate(['Presidential Approval', 'Congressional Approval', 'GDP', 'Economic Freedom']):
        print(f"{feature}: {mse_per_feature[i]}")

    return mse_per_feature


if __name__ == "__main__":
    X_train, y_train, years_train, X_val, y_val, years_val, X_test, y_test, years_test, vectorizer, scaler, target_scaler = load_and_preprocess()

    input_dim = X_train.shape[1]
    output_dim = y_train.shape[1]
    model = MultiOutputRegressionModel(input_dim, output_dim)

    model = train_model(model, X_train, y_train, X_val, y_val)
    evaluate_model(model, X_test, y_test, target_scaler)

    # predict
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    model.eval()
    with torch.no_grad():
        predictions = model(X_test_tensor).numpy()
        predictions_original_scale = target_scaler.inverse_transform(predictions)

    # we got years earlier, print for manual review
    predictions_with_years = pd.DataFrame(
        np.hstack((years_test.reshape(-1, 1), predictions_original_scale)),
        columns=['Year', 'Presidential Approval', 'Congressional Approval', 'GDP', 'Economic Freedom']
    )
    print("first 5 predictions with corresponding years:")
    print(predictions_with_years.head())

    # visualizations
    print("getting scatter plots for predictions vs true values, pls wait")
    plot_predictions(predictions_original_scale, target_scaler.inverse_transform(y_test), years_test)
    print("getting plot over time, pls wait")
    plot_over_time(predictions_original_scale, target_scaler.inverse_transform(y_test), years_test)

    compute_r2_score(predictions_original_scale, target_scaler.inverse_transform(y_test))
