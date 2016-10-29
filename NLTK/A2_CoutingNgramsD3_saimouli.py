from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import FreqDist
from nltk import NaiveBayesClassifier
from nltk import classify
# from nltk.util import ngrams
import arff
import re
from bs4 import BeautifulSoup
import random


class CorpusHandler:
    tokens = []
    tagged_dataset = []
    featured_tokens = []

    def __init__(self, corpus_root, pattern):
        self.init_corpus_params(corpus_root, pattern)

    def init_corpus_params(self, corpus_root, pattern):
        self.wordlists = PlaintextCorpusReader(corpus_root, pattern)

        ai_files = [fileid for fileid in self.wordlists.fileids() if re.compile('AI*').match(fileid)]
        dt_files = [fileid for fileid in self.wordlists.fileids() if re.compile('DT*').match(fileid)]
        el_files = [fileid for fileid in self.wordlists.fileids() if re.compile('EL*').match(fileid)]

        for file in ai_files:
            soup = BeautifulSoup(self.wordlists.raw(file), "lxml")

            for element in soup.find_all(['script', 'style']):
                element.decompose()

            raw_text_per_file = soup.get_text()
            sentiment_tokens = word_tokenize(raw_text_per_file)
            category = 'AI'
            self.tokens = self.tokens + sentiment_tokens
            self.tagged_dataset = self.tagged_dataset + [(sentiment_tokens, category)]

        for file in dt_files:
            soup = BeautifulSoup(self.wordlists.raw(file), "lxml")

            for element in soup.find_all(['script', 'style']):
                element.decompose()

            raw_text_per_file = soup.get_text()
            sentiment_tokens = word_tokenize(raw_text_per_file)
            category = 'DT'
            self.tokens = self.tokens + sentiment_tokens
            self.tagged_dataset = self.tagged_dataset + [(sentiment_tokens, category)]

        for file in el_files:
            soup = BeautifulSoup(self.wordlists.raw(file), "lxml")

            for element in soup.find_all(['script', 'style']):
                element.decompose()

            raw_text_per_file = soup.get_text()
            sentiment_tokens = word_tokenize(raw_text_per_file)
            category = 'EL'
            self.tokens = self.tokens + sentiment_tokens
            self.tagged_dataset = self.tagged_dataset + [(sentiment_tokens, category)]

        random.shuffle(self.tagged_dataset)

        frequency_distribution = self.frequency_distribution([token.lower() for token in self.tokenize()])
        tokens = [tup[0] for tup in frequency_distribution]
        self.featured_tokens = tokens[:1000]

    def tokenize(self):
        stop_words = stopwords.words('english')
        tokens = [token for token in self.tokens if token not in stop_words and len(token) > 1]
        return tokens

    def stem(self, tokens):
        stemmer = SnowballStemmer('english', ignore_stopwords=True)
        tokens = [stemmer.stem(token) for token in tokens]
        return tokens

    def get_dataset_from_corpus(self):
        return self.tagged_dataset

    def frequency_distribution(self, tokens):
        return FreqDist(tokens).most_common()

    def get_ngrams(self, tokens, n):
        # grams = list(ngrams(tokens, n))
        grams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n)]
        return grams

    def dump_to_arff(self, filename, data, relation, attribute_names):

        encoded_data = []

        for tup in data:
            elements = []
            for element in tup:
                if type(element) is tuple:
                    element = ' '.join([entry for entry in element])

                if type(element) is unicode:
                    element = element.encode('utf8')

                elements.append(element)

            encoded_data.append(tuple(elements))

        # encoded_data.append(tuple([tup[0].encode('utf8'), tup[1]]))
        arff.dump(filename, encoded_data, relation=relation, names=attribute_names)
        print "Dumped data to arff file : ", filename

    def feature_extractor(self, document):
        document_words = set([word.lower() for word in document])
        features = {}

        for word in self.featured_tokens:
            features['contains({})'.format(word.encode('utf8'))] = (word in document_words)

        return features

    def trained_classifier(self, training_set):
        classifier = NaiveBayesClassifier.train(training_set)
        return classifier


if __name__ == "__main__":
    corpus_root = 'Dataset3_Classification_Algorithms'
    corpus_handler = CorpusHandler(corpus_root, '.*\.html')

    tokens = corpus_handler.tokenize()
    stem_tokens = corpus_handler.stem(tokens)

    bigrams = corpus_handler.get_ngrams(stem_tokens, 2)
    trigrams = corpus_handler.get_ngrams(stem_tokens, 3)
    four_grams = corpus_handler.get_ngrams(stem_tokens, 4)

    bigrams_frequency_distribution = corpus_handler.frequency_distribution(bigrams)
    trigrams_frequency_distribution = corpus_handler.frequency_distribution(trigrams)
    four_grams_frequency_distribution = corpus_handler.frequency_distribution(four_grams)

    corpus_handler.dump_to_arff('A2D32G_saimouli.arff', bigrams_frequency_distribution, 'Frequency Distribution', ['Bigram', 'Count'])
    corpus_handler.dump_to_arff('A2D33G_saimouli.arff', trigrams_frequency_distribution, 'Frequency Distribution', ['Trigram', 'Count'])
    corpus_handler.dump_to_arff('A2D34G_saimouli.arff', four_grams_frequency_distribution, 'Frequency Distribution',
                                ['Four_gram', 'Count'])

    # corpus_handler.dump_to_arff('A2D32G_yourLastName.arff', bigrams, 'Bigrams', ['Bigram_0', 'Bigram_1'])
    # corpus_handler.dump_to_arff('A2D33G_yourLastName.arff', trigrams, 'Trigrams', ['Trigram_0', 'Trigram_1', 'Trigram_2'])
    # corpus_handler.dump_to_arff('A2D34G_yourLastName.arff', four_grams, 'Four_grams',
    #                             ['Four_gram_0', 'Four_gram_1', 'Four_gram_2', 'Four_gram_3'])

