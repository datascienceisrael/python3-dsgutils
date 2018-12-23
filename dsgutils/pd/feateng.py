import numpy as np
import pandas as pd
import re
from collections import defaultdict
from collections import Counter
import nltk


def alphanumeric_feature(df, text_column):
    """
    Convert text column to alpha numeric column, replacing non alpha numeric with a space.
    :param df : Dataframe
    :param text_column : the column containing text.
    :return df_new : The new Dataframe
    """
    df_new = df.copy()
    alphanumeric_feature_column = 'alpha_num_'+ text_column
    df_new[alphanumeric_feature_column] = ''
    for sentence in df_new[text_column]:
        if pd.isnull(sentence) is not True:
            df_new.loc[df[text_column] == sentence, alphanumeric_feature_column] = re.sub('[^A-Za-z0-9 ]+', ' ', sentence)
    
    print('Finish writing the new alpha numeric column : alpha_num_', str(text_column))
    return(df_new)


def one_hot_encode(df, feature_name, prefix="CAT_", is_list=False, delim=",", cat_amount=0):
    """
    Gets a DataFrame and a categorical column, and replace the
    column with one hot encoded vectors. If the values in the
    column are a list of categories, then the values are split
    according to the given delimiter. The user has an option of
    selecting cat_amount most frequent categories to take into
    consideration (limiting the amount of categories / vectors)
    :param df: DataFrame to create one hot encoded vectors for
    :param feature_name: Categorical feature to turn to one hot vectors
    :param prefix: Prefix to attach to the one-hot vector names
    :param is_list: Flag to indicate whether the values in
                    feature_name are a list of categories
    :param delim: If the values are a list, the delimiter to split the categories
    :param cat_amount: Number of most frequent categories to turn to one-hot vectors
                        Default is o, meaning one-hot encode all categories
    :return: None
    """

    if not isinstance(df, pd.core.frame.DataFrame):
        raise ValueError('df must be a pandas DataFrame')

    if not feature_name:
        raise ValueError('feature_name parameter must be provided')

    elif not feature_name in df.keys():
        raise ValueError(feature_name + ' column does not exist in the given DataFrame')

    if is_list:
        # Split the categories by delimiter
        df[feature_name] = [x.split(delim) if str(x) != 'nan' else "" for x in df[feature_name]]

        if cat_amount > 0:
            # Limit number of vectors created
            one_hot_vals = set(pd.Series([item for sublist in df[feature_name] for item in sublist]) \
                               .value_counts()[:cat_amount].index.values)

        else:
            # Choose all categories
            one_hot_vals = set([item for sublist in df[feature_name] for item in sublist])

        # Create one-hot vectors
        for col in one_hot_vals:
            df[prefix + feature_name + "_" + str(col)] = [int(col in x) for x in df[feature_name]]

        del df[feature_name]

        return

    if cat_amount > 0:
        # Limit number of vectors created
        one_hot_vals = set(df[feature_name].value_counts()[:cat_amount].index.values)

    else:
        # Choose all categories
        one_hot_vals = set(df[feature_name])

    # Create one-hot vectors
    for col in one_hot_vals:
        df[prefix + feature_name + "_" + str(col)] = [1 if x == col else 0 for x in df[feature_name]]

    del df[feature_name]
    return

# def create_top_gram(df, sentence_column, gram_range=(1, 2, 3, 4, 5)):
#     """
    
#     """
#     n_grams_dic = defaultdict(Counter)
#     words_tags_dic = Counter()
#     lemma_dic = Counter()
#     stem_dic = Counter()

#     # Swap nulls with empty strings
#     text = df.drop_duplicates(subset=sentence_column, keep='first', inplace=False)[sentence_column]
    
#     for sentence in text:
#         if pd.isnull(sentence) == False :
#             alpha_numeric_sentence = re.sub('[^A-Za-z0-9 ]+', ' ', str(sentence).lower())
#             tokens = nltk.word_tokenize(alpha_numeric_sentence)
#             tokens_no_stop_words = [t for t in tokens if t not in stopwords.words('english')]
#             for n in gram_range:
#                     if n == 1:
#                         n_grams_dic[n].update(tokens_no_stop_words)
#                     else:
#                         n_grams_dic[n].update(nltk.ngrams(tokens, n))  # N-Gram counts
#                 words_tags_dic.update(nltk.pos_tag(tokens_no_stop_words))  # Word tag counts
#                 lemma_dic.update([w.lemma_ for w in nlp(alpha_numeric_sentence) if w.lemma_ not in stopwords.words('english')])
#                 stem_dic.update([ps.stem(token) for token in tokens_no_stop_words])

#                 if (i % 10000) == 0:
#                     #print(i)
#                     #print(sentence)
#                     ioprint(sentence, level=10)
#                     ioprint(str(i), level=10)
#                 i = i + 1
#         else:
#             break

#     return n_grams_dic, words_tags_dic, lemma_dic, stem_dic