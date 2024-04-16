import re
import logging
import extraction as ext

info_logger = logging.getLogger("info-logger")
info_logger.setLevel(logging.INFO)


def prepare_logger():
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler(filename="logs/application.log", mode="w+")
    handler.setFormatter(formatter)
    info_logger.addHandler(handler)


with open(file='resources/example-3.txt', mode='r') as file:
    file_content = file.read()

punctuation_marks = [".", ",", ":", ";", "?", "!", "\"", "'", "«", "»", "–", "-"]
regex = "[" + ''.join(punctuation_marks) + "]"


def prepare_file_content_for_processing(*, file_content: str) -> str:
    info_logger.info(f"Processing for regex: {regex}")
    return re.sub(regex, " ", file_content).lower()


def application_entrypoint():
    prepare_logger()

    prepared_file_content = prepare_file_content_for_processing(file_content=file_content)
    info_logger.info(f"Result of processing:\n\n{prepared_file_content}")

    preprocessed_text = ext.preprocess_text(text=prepared_file_content)

    raked_keywords = ext.extract_keywords_with_rake(text=prepared_file_content)
    yaked_keywords = ext.extract_keywords_with_yake(text=preprocessed_text)
    tfidf_keywords = ext.extract_keywords_with_tf_idf(text=preprocessed_text)

    print("Raked algorithm result")
    print(raked_keywords)
    print("Yake! algorithm result")
    print(yaked_keywords)
    print("Tf-Idf algorithm result")
    print(tfidf_keywords)


if __name__ == "__main__":
    application_entrypoint()
