import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load data from CSV file
data = pd.read_csv('reduced_dataset.csv')

# Convert string representations of lists to actual lists of length 2
data['initial_hand'] = data['initial_hand'].apply(lambda x: [int(i) for i in x.strip('[]').split(',')])

# Extract the two cards in the initial_hand list and create a new DataFrame
initial_cards = pd.DataFrame(data['initial_hand'].tolist(), columns=['initial_card1', 'initial_card2'], index=data.index)

# Function to check if the initial hand contains an Ace
def has_ace(hand):
    return int(1 in hand)

# Create the has_ace column
initial_cards['has_ace'] = initial_cards[['initial_card1', 'initial_card2']].apply(has_ace, axis=1)

# Concatenate the new DataFrame with the existing DataFrame
data = pd.concat([data, initial_cards], axis=1)

# Drop the original initial_hand column
data.drop('initial_hand', axis=1, inplace=True)

# Create a new column for the total initial hand value
data['initial_total'] = data['initial_card1'] + data['initial_card2']

# Split data into training and testing sets
X = data[['dealer_up', 'initial_total', 'has_ace']]
y = data['actions_taken']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# Train a decision tree classifier on the training set
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Predict actions on the testing set and calculate accuracy
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Print the accuracy score
print(f"Accuracy: {accuracy:.2f}")

# Test the model
dealer_up = int(input("What is the Dealer's Face Up Card?: "))
initial_total = int(input("What is the Player's Sum of Cards"))
predicted_action = clf.predict([[dealer_up, initial_total, 0]])[0]
print(f"Predicted action for dealer_up={dealer_up} and initial_total={initial_total}: {predicted_action}")


import joblib

# Save the model to an H5 file
joblib.dump(clf, 'decision_tree_model.h5')
