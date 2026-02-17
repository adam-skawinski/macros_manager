from sklearn.ensemble import RandomForestClassifier  # for generate tree clasyficator
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from logic.ML.features.CmdFeatures import CmdFeatures

def buildPipeline():
    tfidfVectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    featureUnion = FeatureUnion(
        [("tfidf", tfidfVectorizer), ("cmdFeatures", CmdFeatures())]
    )
    pipeline = Pipeline(
        [("features", featureUnion), ("clf", RandomForestClassifier(class_weight="balanced",random_state=42))]
    )
    return pipeline
