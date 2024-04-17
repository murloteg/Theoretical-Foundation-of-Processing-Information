import spacy
import nltk

from nltk.corpus import stopwords as sw
from rake_nltk import Rake
from yake import KeywordExtractor
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nltk.download('stopwords')

ru_pipeline = spacy.load("ru_core_news_lg")
useless_symbols = set(sw.words('russian')).union(set(ru_pipeline.Defaults.stop_words))


def preprocess_text(*, text: str) -> str:
    doc = ru_pipeline(text)
    preprocessed_text = " ".join([token.lemma_ for token in doc if token.text not in useless_symbols])
    return preprocessed_text


def extract_keywords_with_rake(*, text: str) -> list[str]:
    rake_extractor = Rake(stopwords=useless_symbols, max_length=1, language='ru', include_repeated_phrases=False)
    rake_extractor.extract_keywords_from_text(text)

    keywords_with_score = rake_extractor.get_ranked_phrases_with_scores()
    keywords_with_score.sort()
    return [t[1] for t in keywords_with_score[:8]]


def extract_keywords_with_yake(*, text: str) -> list:
    yake_extractor = KeywordExtractor(lan='ru', n=1, stopwords=useless_symbols)
    keywords_with_score = yake_extractor.extract_keywords(text)
    keywords_with_score.sort(key=lambda a: a[1])
    return [t[0] for t in keywords_with_score[:8]]


def extract_keywords_with_tf_idf(*, text: str) -> list[str]:
    raw_docs = text.split('\n')

    tfidf_vectorizer = TfidfVectorizer(stop_words=list(useless_symbols))
    values = tfidf_vectorizer.fit_transform(raw_docs)

    keywords_with_score = [[word, score] for word, score in zip(tfidf_vectorizer.get_feature_names_out(), values.toarray()[0])]
    keywords_with_score.sort(key=lambda a: a[1], reverse=True)
    return [t[0] for t in keywords_with_score[:8]]