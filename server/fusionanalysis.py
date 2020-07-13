import pandas as pd
#from polyglot.text import Text
import json
import unicodedata
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from collections import Counter
import datetime


#def parse_field(typ, value):
#    if typ == "str":
#        return str(value)
#    elif typ == "int":
#        return int(value)
#    elif typ == "date":
#        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.000Z")
#    return None

# SENTIMENT STARTS HERE ----------------------------------------------

#def sentiment(messages):
#    # Polarities extraction
#    polarities = []
#    for message in messages:
#        preprocessed_message = pre_process(message)
#        text = Text(preprocessed_message)
#        text.language = "pt"
#        try:
#            polarities.append(text.polarity)
#        except:
#            polarities.append(0)
#    registers = {'text': messages, 'polarity': polarities}
#    df_sentiments = pd.DataFrame(data=registers)
#    # Counting polarities
#    polarities_list = df_sentiments.polarity.tolist()
#    negative = polarities_list.count(-1)
#    neg_medium = 0
#    neutral = polarities_list.count(0)
#    pos_medium = 0
#    positive = polarities_list.count(1)
#    for polarity in polarities_list:
#        if (polarity < 0 and polarity > -0.5 ):
#            neg_medium += 1
#        elif(polarity > 0 and polarity < 0.5):
#            pos_medium += 1
#    # generating results
#    results = {'negative': negative, 'negative_medium': neg_medium, 'neutral': neutral, 'positive_medium': pos_medium, 'positive': positive}
#    return(json.dumps(results))

# SENTIMENT ENDS HERE ------------------------------------------------

# PREPROCESS STARTS HERE ---------------------------------------------

nltk_stop = set(stopwords.words('portuguese'))
for word in ["2018","claro","oi","tim","vivo","dia","e","pois","r$"]:
    nltk_stop.add(word)

def pre_process(text):

    def removeURL(text):
        text = re.sub("http\\S+\\s*", "", text)
        return text

    # 'NFKD' is the code of the normal form for the Unicode input string.
    def remove_accentuation(text):
        text = unicodedata.normalize('NFKD', str(text)).encode('ASCII','ignore')
        return text.decode("utf-8")

    def remove_punctuation(text):
        # re.sub(replace_expression, replace_string, target)
        # new_text = re.sub(r"\.|,|;|!|\?|\(|\)|\[|\]|\$|\:|\\|\/", "", text)
        new_text = re.sub(r"\(|\)|\[|\]|\$|\:|\\|\/", "", text)
        return new_text

    def remove_numbers(text):
        # re.sub(replace_expression, replace_string, target)
        new_text = re.sub(r"[0-9]+", "", text)
        return new_text

    # Conver a text to lower case
    def lower_case(text):
        return text.lower()

    def remove_stop_words(text):
        for sw in nltk_stop:
            text = re.sub(r'\b%s\b' % sw, "", text)
        return text

    new_text = lower_case(text)
    new_text = removeURL(new_text)
    new_text = remove_stop_words(new_text)
    new_text = remove_numbers(new_text)
    new_text = remove_punctuation(new_text)
    new_text = remove_accentuation(new_text)
    return new_text

# PREPROCESS ENDS HERE -----------------------------------------------

# TOPICS STARTS HERE -------------------------------------------------

def topics(messages):
    result = []
    def top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            topic_words = " ".join(
                [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
            )
            result.append(topic_words)
        return(json.dumps(result))

    n_features = 2000 #len(messages)
    n_components = 5
    n_top_words = 10

    dataset = pd.DataFrame(messages)
    data_samples = dataset.iloc[0]
    df_pre_processed = data_samples.apply(pre_process)
    n_samples = len(df_pre_processed)
    # Use tf-idf features for LDA.
    # Extracting tf features and fitting models for LDA..."
    tf_vectorizer = TfidfVectorizer(max_features=n_features)
    tf = tf_vectorizer.fit_transform(df_pre_processed)
    # Fiting LDA model
    lda = LatentDirichletAllocation(
        n_components=n_components,
        max_iter=10,
        learning_method='online',
        learning_offset=50.,
        random_state=0
    )
    lda.fit(tf)
    # Return topics in LDA model
    tf_feature_names = tf_vectorizer.get_feature_names()
    return top_words(lda, tf_feature_names, n_top_words)

# TOPICS ENDS HERE ---------------------------------------------------

# COUNT_STATES STARTS HERE -------------------------------------------

def count_states(cities):
    values = [ x[-2:] for x in cities ]
    result = dict(Counter(values))
    return json.dumps(result)

# COUNT_STATES ENDS HERE ---------------------------------------------

# COUNT_MONTHS STARTS HERE -------------------------------------------

def count_months(input_dates):
    dates = [
        "{month}/{year}".format(
            month = x.month,
            year= x.year
        )
        for x in input_dates
    ]
    dates_counter = dict(Counter(dates))
    return json.dumps(dates_counter)

# COUNT_MONTHS ENDS HERE ---------------------------------------------

