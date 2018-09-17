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