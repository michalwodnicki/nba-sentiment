import pandas as pd
import datetime
import pytz
import nltk
import re
import os

nltk.download("vader_lexicon")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


nltk.download("stopwords")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download("omw-1.4")


def get_datetime(utctime):
    utc_datetime = datetime.datetime.utcfromtimestamp(utctime)
    desired_time_zone = pytz.timezone("America/Chicago")
    converted_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(
        desired_time_zone
    )
    formatted_datetime = converted_datetime.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    return formatted_datetime


def preprocess_text(text, method="lemmatization"):
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)

    # Remove new lines and extra whitespace
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # Convert to lowercase
    text = text.lower()

    # Remove numbers
    text = re.sub(r"\d+", "", text)

    # Remove punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Tokenization
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]

    # Apply chosen method
    if method == "stemming":
        stemmer = PorterStemmer()
        processed_tokens = [stemmer.stem(token) for token in tokens]
    elif method == "lemmatization":
        lemmatizer = WordNetLemmatizer()
        processed_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    else:
        raise ValueError("Invalid method. Choose either 'stemming' or 'lemmatization'.")

    # Join the tokens back into a single string
    preprocessed_text = " ".join(processed_tokens)

    return preprocessed_text


# Takes a list of game DataFrames (games) and applies
def process_text(game_df):
    # Apply pre-processing
    game_df["pre-processed"] = game_df["body"].apply(
        lambda x: preprocess_text(x, method="lemmatization")
    )

    # Apply utc -> DateTime
    game_df["dataTime"] = game_df["utc"].apply(lambda x: get_datetime(x))

    return game_df


def get_csv_files(foldername):
    folder_path = f"data/{foldername}"
    files = os.listdir(folder_path)
    csv_files = [file for file in files if file.endswith(".csv")]
    return csv_files


def main(foldername):
    csv_list = get_csv_files(foldername)

    for csv in csv_list:
        filepath = f"data/{foldername}/{csv}"
        df = pd.read_csv(filepath)
        df = process_text(df)
        output_path = filepath
        df.to_csv(output_path)


x = main("MIAvBOS")
print("test stop")


# get_comments returns csvs in my data folder
# this function will take a csv, read it in as a df, process comment body, apply game number, and get datetime
