#natural language processing toolkit (nltk)
from nltk.corpus import PlaintextCorpusReader
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk import FreqDist
from nltk import NaiveBayesClassifier
# from nltk.util import ngrams

#library to dump data in arff file
import arff


class CorpusHandler:
    tokens = []     #list of all token
    tagged_dataset = [] #list of tagged dataset tokens
    featured_tokens = []    #list of most informative features

    def __init__(self, corpus_root, pattern):
        self.init_corpus_params(corpus_root, pattern)

    def init_corpus_params(self, corpus_root, pattern):
        self.wordlists = PlaintextCorpusReader(corpus_root, pattern)    #read the corpus

        for file in self.wordlists.fileids():
            raw_text_per_file = self.wordlists.raw(file)    #get raw content of file

            for line in raw_text_per_file.split('\n'):
                line = word_tokenize(line)
                sentiment_tokens = line[1:] #get tokens and category
                category = ''.join(line[:1])

                self.tokens = self.tokens + sentiment_tokens
                self.tagged_dataset = self.tagged_dataset + [(sentiment_tokens, category)]

        #calculate frequency distribution
        frequency_distribution = self.frequency_distribution([token.lower() for token in self.tokenize()])
        tokens = [tup[0] for tup in frequency_distribution]
        self.featured_tokens = tokens[:1000]

    #function to remove stop words and non-informative words
    def tokenize(self):
        stop_words = stopwords.words('english')
        tokens = [token for token in self.tokens if token not in stop_words and len(token) > 1]
        return tokens

    #function to obtain stem of tokens
    def stem(self, tokens):
        stemmer = SnowballStemmer('english', ignore_stopwords=True)
        tokens = [stemmer.stem(token) for token in tokens]
        return tokens

    def get_dataset_from_corpus(self):
        return self.tagged_dataset

    #function to calculate frequency distribution in most common order
    def frequency_distribution(self, tokens):
        return FreqDist(tokens).most_common()

    #function to calculate n-grams from tokens
    def get_ngrams(self, tokens, n):
        # grams = list(ngrams(tokens, n))
        grams = [tuple(tokens[i:i+n]) for i in range(len(tokens) - n)]
        return grams

    #function to write data into arff file
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

    #function to extract features from a document/input text
    def feature_extractor(self, document):
        document_words = set([word.lower() for word in document])
        features = {}

        for word in self.featured_tokens:
            features['contains({})'.format(word.encode('utf8'))] = (word in document_words)

        return features

    #function to train a classifier using naive bayes algorithm
    def trained_classifier(self, training_set):
        classifier = NaiveBayesClassifier.train(training_set)
        return classifier


if __name__ == "__main__":
    corpus_root = 'Dataset2_SMS_Spam_Collection'
    corpus_handler = CorpusHandler(corpus_root, '.*')

    #obtain normal and stem tokens
    tokens = corpus_handler.tokenize()
    stem_tokens = corpus_handler.stem(tokens)

    bigrams = corpus_handler.get_ngrams(stem_tokens, 2)
    trigrams = corpus_handler.get_ngrams(stem_tokens, 3)
    four_grams = corpus_handler.get_ngrams(stem_tokens, 4)

    bigrams_frequency_distribution = corpus_handler.frequency_distribution(bigrams)
    trigrams_frequency_distribution = corpus_handler.frequency_distribution(trigrams)
    four_grams_frequency_distribution = corpus_handler.frequency_distribution(four_grams)

    corpus_handler.dump_to_arff('A2D22G_saimouli.arff', bigrams_frequency_distribution, 'Frequency Distribution', ['Bigram', 'Count'])
    corpus_handler.dump_to_arff('A2D23G_saimouli.arff', trigrams_frequency_distribution, 'Frequency Distribution', ['Trigram', 'Count'])
    corpus_handler.dump_to_arff('A2D24G_saimouli.arff', four_grams_frequency_distribution, 'Frequency Distribution',
                                ['Four_gram', 'Count'])

    # corpus_handler.dump_to_arff('A2D22G_yourLastName.arff', bigrams, 'Bigrams', ['Bigram_0', 'Bigram_1'])
    # corpus_handler.dump_to_arff('A2D23G_yourLastName.arff', trigrams, 'Trigrams', ['Trigram_0', 'Trigram_1', 'Trigram_2'])
    # corpus_handler.dump_to_arff('A2D24G_yourLastName.arff', four_grams, 'Four_grams',
    #                             ['Four_gram_0', 'Four_gram_1', 'Four_gram_2', 'Four_gram_3'])

