import fasttext
import wget
import os
import string
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

# Patch to stop fasttext.load_model warning saying 'FastText' objects are returned now
fasttext.FastText.eprint = lambda x: None


class LangIdentificationException(Exception):
    pass


class LangIdentification:
    def __init__(self, model_type='augmented'):
        dir_path = os.path.join(os.path.dirname(__file__),
                                'models')
        if model_type in ['original', 'augmented']:
            file_path = os.path.join(dir_path,
                                     f'langdetect_{model_type}.ftz')
            if Path(file_path).exists():
                logging.info(f'Loading model langdetect_{model_type}.ftz...\n')
                self.model = fasttext.load_model(file_path)
            else:
                logging.info(f'Model langdetect_{model_type}.ftz was not found. Checking for models directory '
                             f'and creating if not available...\n')
                os.makedirs(dir_path, exist_ok=True)
                try:
                    logging.info(f'Downloading langdetect_{model_type}.ftz...\n')
                    url = f'https://github.com/absu5530/langidentification/releases/latest/download/' \
                          f'langdetect_{model_type}.ftz'
                    wget.download(url, file_path)
                    logging.info(f'Loading model langdetect_{model_type}.ftz...\n')
                    self.model = fasttext.load_model(file_path)
                except Exception as e:
                    raise LangIdentificationException(f'Error in getting model: {str(e)}')
        else:
            raise LangIdentificationException(f'Given model_type {model_type} is invalid. Valid model types are: '
                                              f'"original" and "augmented".')

        self.punct_table = str.maketrans(dict.fromkeys(string.punctuation))

    def preprocess_text(self, text='test_string'):
        if isinstance(text, str):
            preprocessed_text = text.translate(self.punct_table)
        elif isinstance(text, list):
            if all(isinstance(item, str) for item in text):
                preprocessed_text = [t.translate(self.punct_table) for t in text]
            else:
                raise LangIdentificationException('Not all objects in given input list are strings.')
        else:
            raise LangIdentificationException('Given text is neither a str nor a list.')
        return preprocessed_text

    def predict_lang(self, text):
        preprocessed_text = self.preprocess_text(text)
        return self.model.predict(preprocessed_text)
