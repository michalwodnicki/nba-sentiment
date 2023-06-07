from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline


def textblob_sentiment(comment):
    blob = TextBlob(comment)
    sentiment = blob.sentiment
    return sentiment.polarity


# initializing BERTA sentiment pipeline
model_path = "cardiffnlp/twitter-roberta-base-sentiment-latest"
sentiment_pipeline = pipeline(
    "sentiment-analysis", model=model_path, tokenizer=model_path
)


def berta_sentiment(comment):
    return sentiment_pipeline(comment)[0]


def process_text(games):
    sia = SentimentIntensityAnalyzer()

    # Apply NLTK sentiment socring
    game["compound_ss"] = game["pre-processed"].apply(
        lambda x: sia.polarity_scores(x)["compound"]
    )
    game["positive_ss"] = game["pre-processed"].apply(
        lambda x: sia.polarity_scores(x)["pos"]
    )
    game["negative_ss"] = game["pre-processed"].apply(
        lambda x: sia.polarity_scores(x)["neg"]
    )
    game["neutral_ss"] = game["pre-processed"].apply(
        lambda x: sia.polarity_scores(x)["neu"]
    )

    # Apply TextBlob Sentiment Scoring
    game["textblob_ss"] = game["pre-processed"].apply(lambda x: textblob_sentiment(x))

    # Applying BERTA Sentiment Scoring
    game["BERTA"] = game["pre-processed"].apply(lambda x: berta_sentiment(x))

    print(game_number)
    game_number += 1
