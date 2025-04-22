import os
import joblib 
from dotenv import load_dotenv
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


load_dotenv(override=True)


APP_NAME = os.getenv("APP_NAME")
VERSION = os.getenv("VERSION")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")


src_folder_path = os.path.dirname(os.path.abspath(__file__))

ARTIFACTS_FOLDER_PATH = os.path.join(src_folder_path , "artifacts")


# Models
bow_vect = joblib.load(r"D:\AAAAAAA\NLP Course\NLP-Project\artifacts\bow_vectorizer.pkl")
svc_model = joblib.load(r"D:\AAAAAAA\NLP Course\NLP-Project\artifacts\svm_bow.pkl")
# glove_model = joblib.load(os.path.join(ARTIFACTS_FOLDER_PATH , "svc_glove_twitter.pkl"))




# Some constants
EMOTIOCS_MEANINGS = {
    ":)": "Happy",
    ":(": "Sad",
    ":D": "Very Happy",
    ":|": "Neutral",
    ":O": "Surprised",
    "<3": "Love",
    ";)": "Wink",
    ":P": "Playful",
    ":/": "Confused",
    ":*": "Kiss",
    ":')": "Touched",
    "XD": "Laughing",
    ":3": "Cute",
    ">:(": "Angry",
    ":-O": "Shocked",
    ":|]": "Robot",
    ":>": "Sly",
    "^_^": "Happy",
    "O_o": "Confused",
    ":-|": "Straight Face",
    ":X": "Silent",
    "B-)": "Cool",
    "<(‘.'<)": "Dance",
    "(-_-)": "Bored",
    "(>_<)": "Upset",
    "(¬‿¬)": "Sarcastic",
    "(o_o)": "Surprised",
    "(o.O)": "Shocked",
    ":0": "Shocked",
    ":*(": "Crying",
    ":v": "Pac-Man",
    "(^_^)v": "Double Victory",
    ":-D": "Big Grin",
    ":-*": "Blowing a Kiss",
    ":^)": "Nosey",
    ":-((": "Very Sad",
    ":-(": "Frowning",
}

# The mapping for the prediction
SENTIMENT_MAPPING = {
            0: "Negative",
            1: "Positive",
            2: "Neutral"
        }



class TextProcessor :
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))
        self.emotion_meanings = EMOTIOCS_MEANINGS


    def remove_pattern(self, text: str, pattern: str) -> str:
        return re.sub(pattern, '', text)
    

    def remove_excessive_chars(self, text: str, max_repeats: int = 2) -> str:
        pattern = f"(\\w)\\1{{{max_repeats},}}"
        return re.sub(pattern, r"\1", text)

    def convert_emoticons(self, text: str) -> str:
        for emoticon, meaning in self.emoticon_meanings.items():
            text = text.replace(emoticon, meaning)
        return text

    def remove_redundant_words(self, text: str) -> str:
        # Remove contractions
        text = re.sub(r"'\w+|\w+'\w+|\w+'", '', text)


    # Remove stopwords and extra spaces
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.stop_words]
        return ' '.join(filtered_words)

    def lemmatize_text(self, text: str) -> str:
        words = text.split()
        lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words]
        return ' '.join(lemmatized_words)

    def clean_text(self, text: str) -> str:
        # Apply all cleaning steps
        text = self.remove_pattern(text, r'@[\w]*')  # Remove mentions
        text = self.remove_pattern(text, r'https?://\S+|www\.\S+')  # Remove URLs
        text = self.remove_excessive_chars(text)  # Remove repeated chars
        text = self.convert_emoticons(text)  # Convert emoticons
        text = re.sub(r'[^a-zA-Z#]', ' ', text)  # Remove non-alphabetic chars
        text = ' '.join([w for w in text.split() if len(w) > 3])  # Remove short words
        text = self.remove_pattern(text, r'(?<=\w)\d+|\d+(?=\w)')  # Remove numbers
        text = self.remove_pattern(text, r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\|\/]')  # Remove special chars
        text = self.remove_redundant_words(text)  # Remove redundant words
        text = self.lemmatize_text(text)  # Lemmatize
        return text