import pandas as pd
from polyglot.text import Text
import json
import unicodedata
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from collections import Counter
import datetime
from wordcloud import WordCloud
from operator import itemgetter
from joblib import Parallel, delayed

# FUSIONANALYSIS STARTS HERE -----------------------------------------

def fusion_analysis(results_platforms, columns, language = "pt", company_stop_words = []):
    n_topics = 4

    # SENTIMENT STARTS HERE ----------------------------------------------

    def count_sentiments(messages, language = "pt"):
        # Polarities extraction
        polarities = []
        for message in messages:
            if message == None:
                polarities.append(0)
            else:
                preprocessed_message = pre_process(text = message, param_remove_punctuation = False, param_remove_accentuation = False, param_remove_stop_words = False)
                text = Text(preprocessed_message)
                text.language = language
                try:
                    polarities_sentences = [sentence.polarity for sentence in text.sentences]
                    polarities_sentences = list(filter(lambda x: x!=0,polarities_sentences))
                    mean_polarities = sum(polarities_sentences)/len(polarities_sentences)
                    polarities.append(mean_polarities)
                except:
                    polarities.append(0)
        registers = {'text': messages, 'polarity': polarities}
        df_sentiments = pd.DataFrame(data=registers)
        # Counting polarities
        polarities_list = df_sentiments.polarity.tolist()
        negative = polarities_list.count(-1)
        neg_medium = 0
        neutral = polarities_list.count(0)
        pos_medium = 0
        positive = polarities_list.count(1)
        for polarity in polarities_list:
            if (polarity < 0 and polarity > -1 ):
                neg_medium += 1
            elif(polarity > 0 and polarity < 1):
                pos_medium += 1
        # generating results
        results = {'negative': negative, 'negative_medium': neg_medium, 'neutral': neutral, 'positive_medium': pos_medium, 'positive': positive}
        return(json.dumps(results))

    # SENTIMENT ENDS HERE ------------------------------------------------

    # PREPROCESS STARTS HERE ---------------------------------------------

    nltk_stop = set(stopwords.words('portuguese'))
    for word in company_stop_words:
        nltk_stop.add(word)

    def pre_process(text = "", param_stemming = False, param_removeURL = True, param_remove_tags = True, param_remove_accentuation = True, param_remove_punctuation = True, param_remove_numbers = True, param_lower_case = True, param_remove_stop_words = True):
        stemmer = nltk.stem.RSLPStemmer()

        def tokenize(string, language = "pt"):
            text = Text(string, hint_language_code=language)
            text.language = language
            return text.words

        def stemming(text):
            words = tokenize(text)
            stemmer_words = [stemmer.stem(item) for item in words]
            return ' '.join(stemmer_words)
        
        def removeURL(text):
            text = re.sub("http\\S+\\s*", "", text)
            return text

        def remove_tags(text):
            cleanr = re.compile('<.*?>')
            text = re.sub(cleanr, '', text)
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

        new_text = str(text)
        if param_lower_case:
            new_text = lower_case(new_text)
        if param_remove_tags:
            new_text = remove_tags(new_text)
        if param_removeURL:
            new_text = removeURL(new_text)
        if param_remove_stop_words:
            new_text = remove_stop_words(new_text)
        if param_remove_numbers:
            new_text = remove_numbers(new_text)
        if param_remove_punctuation:
            new_text = remove_punctuation(new_text)
        if param_stemming:
            new_text = stemming(new_text)
        if param_remove_accentuation:
            new_text = remove_accentuation(new_text)
        return new_text

    # PREPROCESS ENDS HERE -----------------------------------------------

    # TOPICS STARTS HERE -------------------------------------------------

    def count_topics(messages):
        result = []
        def top_words(model, feature_names, n_top_words):
            result_top_words = []
            for topic_idx, topic in enumerate(model.components_):
                topic_words = " ".join(
                    [feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]
                )
                result_top_words.append(topic_words)
            return result_top_words

        n_features = None # 2000 #len(messages)
        n_components = n_topics
        n_top_words = 20

        dataset = pd.DataFrame(messages)
        data_samples = dataset.iloc[:,0]
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
        topics_words = top_words(lda, tf_feature_names, n_top_words)
        # WordCloud per topic:
        topics_word_cloud = []
        for n in range(n_topics):
            indexes = [index for (index,doc) in enumerate(lda.transform(tf)) if doc.argmax()==n]
            if len(indexes) > 0:
                string = ' '.join([df_pre_processed[i] for i in indexes])
                topic_word_cloud = WordCloud().generate(string).words_
                topics_word_cloud.append(topic_word_cloud)
            else:
                topics_word_cloud.append({})
        for i in range(n_topics):
            result.append(
                {
                    'words': topics_words[i],
                    'word_cloud': dict(sorted(topics_word_cloud[i].items(), key = itemgetter(1), reverse = True)[:20])
                }
            )
        return json.dumps(result)

    # TOPICS ENDS HERE ---------------------------------------------------

    # COUNT_STATES STARTS HERE -------------------------------------------

    def count_states(cities):
        values = [ x[-2:] for x in cities ]
        result = dict(Counter(values))
        return json.dumps(result)

    # COUNT_STATES ENDS HERE ---------------------------------------------

    # COUNT_MONTHS STARTS HERE -------------------------------------------

    def count_months(input_dates):

        def month_name(month_number):
            month_strings = {
                "1": "Janeiro",
                "2": "Fevereiro",
                "3": "Março",
                "4": "Abril",
                "5": "Maio",
                "6": "Junho",
                "7": "Julho",
                "8": "Agosto",
                "9": "Setembro",
                "10": "Outubro",
                "11": "Novembro",
                "12": "Dezembro"
            }
            month_string = month_strings[month_number]
            return month_string
        
        dates = [
            "{month}/{year}".format(
                month = month_name(
                    str(x.month)
                ),
                year= x.year
            )
            for x in input_dates
        ]
        dates_counter = dict(Counter(dates))
        return json.dumps(dates_counter)

    # COUNT_MONTHS ENDS HERE ---------------------------------------------

    result = {'success': True}
    
    amounts = {}
    for platform in results_platforms:
        amounts[platform] = len( results_platforms[platform] )
    result["amounts"] = amounts

    states = []
    for platform in results_platforms:
        parameter = columns['city'][platform]
        states.extend( [ x[parameter] for x in results_platforms[platform] ] )
    count_states_json = count_states( states )
    count_states = json.loads( count_states_json )
    result["count_states"] = count_states

    dates = {}
    count_dates_json = {}
    count_dates = {}
    for platform in results_platforms:
        parameter = columns['date'][platform]
        dates[platform] = [ x[parameter] for x in results_platforms[platform] ]
        count_dates_json[platform] = count_months( dates[platform] )
        count_dates[platform] = json.loads( count_dates_json[platform] )
    result["count_dates"] = count_dates

    topics = []
    for platform in results_platforms:
        parameter = columns['message'][platform]
        topics.extend( [ x[parameter] for x in results_platforms[platform] ] )
    topics_found_json = count_topics( topics )
    topics_found = json.loads( topics_found_json )
    result["topics"] = topics_found

    sentiments = []
    for platform in results_platforms:
        parameter = columns['evaluation'][platform]
        sentiments.extend( [ x[parameter] for x in results_platforms[platform] ] )
    sentiments_found_json = count_sentiments( sentiments, language = "pt" )
    sentiments_found = json.loads( sentiments_found_json )
    result["sentiments"] = sentiments_found

    return result

# FUSIONANALYSIS ENDS HERE -------------------------------------------

