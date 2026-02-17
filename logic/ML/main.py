from logic.ML.helpers.dataLoader import dataLoader
from logic.ML.models.classifier import buildPipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
import joblib

DATA_PATH = "./logic/ML/data/data.json"
DIR_SAVE_PATH = "./logic/ML/trainedModels/"
paramGrid = {
    "clf__n_estimators": [100, 200],
    "clf__max_depth": [None, 10, 20],
    "clf__min_samples_leaf": [1, 2, 4],
}

X, y = dataLoader(DATA_PATH)
print(X, y)
XTrain, XTest, yTrain, yTest = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline = buildPipeline()
print("test pipeline")
gridSearch = GridSearchCV(pipeline, paramGrid, cv=5, scoring="f1", n_jobs=-1)
gridSearch.fit(XTrain, yTrain)
print("test gride searxh")
yPred = gridSearch.predict(XTest)

print("\nParametry:", gridSearch.best_params_)
print("\nF1:", gridSearch.best_score_)
print(f"\nklasyfikacja:\n\n{classification_report(yTest, yPred)}")

trainedModel = gridSearch.best_estimator_
joblib.dump(trainedModel, DIR_SAVE_PATH + "randomforest_cmd_pipeline.joblib")
