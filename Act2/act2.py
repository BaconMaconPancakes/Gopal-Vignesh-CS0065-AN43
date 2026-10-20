import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# 1. Load the dataset
data = pd.read_csv('student_performance_knime.csv')

# 2. Set X to the four academic input columns
X = data[['attendance', 'quiz_score', 'assignment_score', 'exam_score']]

# 3. Set y to the target
y = data['risk_status']

# 4. Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 5. Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 6. Train the model
model.fit(X_train, y_train)

# 7. Make predictions
y_pred = model.predict(X_test)

# 8. Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, pos_label='At Risk')
recall = recall_score(y_test, y_pred, pos_label='At Risk')
f1 = f1_score(y_test, y_pred, pos_label='At Risk')

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 9. Save the trained model
joblib.dump(model, 'student_performance_model.joblib')

print("\nModel saved as student_performance_model.joblib")