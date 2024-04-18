import re
import logging

info_logger = logging.getLogger("info-logger")
info_logger.setLevel(logging.INFO)


def prepare_logger():
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler = logging.FileHandler(filename="logs/application.log", mode="w+")
    handler.setFormatter(formatter)
    info_logger.addHandler(handler)


with open(file='resources/example.txt', mode='r') as file:
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


if __name__ == "__main__":
    application_entrypoint()
