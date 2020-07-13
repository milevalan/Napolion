""" Using Word Embedding to Attempt to understand the topic of text """
from collections import defaultdict
from functools import reduce
from App.utilities import format_sent

import numpy as np
import spacy

nlp = spacy.load('en_core_web_lg')


class Semantic_Extractor:
    def __init__(self, text):
        self.corpus = []
        self.doc = nlp(text)
        self.sents = [format_sent(sent.text) for sent in self.doc.sents]
        self.filter = []

        self.__corpus()
        self.__topic_words()
        self.__score_sent()

    def __corpus(self, stopwords=False, punctuation=False):
        for _sent in self.sents:
            sent_doc = nlp(_sent)
            __sent = set()
            for token in sent_doc:
                if not stopwords and token.is_stop:
                    continue
                if not punctuation and self.punctuation(token):
                    continue
                if token.text.strip() == '':
                    continue
                __sent.add(token)
            self.corpus.append(__sent)
        self.filter = list(np.ones((len(self.corpus),)))

    def __topic_words(self):
        _tokens = reduce(lambda x, y: x + y, [[token for token in sent] for sent in self.corpus])
        freq_table = defaultdict(lambda: 0)
        for token in _tokens:
            freq_table[token.lemma_] += 1
        ordered_freq_table = sorted(freq_table.items(), key=lambda x: x[1])
        line = np.array([i for i in set(term[1] for term in ordered_freq_table)])
        integrated_eq = self.integrate(line)
        index = np.where(integrated_eq > integrated_eq.mean())[0][0]
        self.topic_words = [s[0] for s in freq_table.items() if s[1] > line[index]]
        if len(self.topic_words) == 0:
            self.topic_words = [s[0] for s in ordered_freq_table[-10:]]

    def __score_sent(self):
        key_words = [token for token in nlp(' '.join(self.topic_words))]
        similarity_matrix = []
        for sent in self.corpus:
            term_similarity = []
            for term in sent:
                if term.has_vector:
                    for token in key_words:
                        if token.has_vector:
                            term_similarity.append(token.similarity(term))

            if term_similarity:
                similarity_matrix.append(np.nanmean(np.array(term_similarity)))
            else:
                similarity_matrix.append(0.0)

        self.sent_similarity = np.array(similarity_matrix)
        print(self.sent_similarity)

    def __percentage_compression(self):
        return (1 - np.array(self.filter).mean()) * 100

    def layer_one(self):
        for i, score in enumerate(self.sent_similarity):
            if score < self.sent_similarity.mean() * .7:
                self.filter[i] = 0.0
        print('Layer One : {pc} % compression'.format(pc=self.__percentage_compression()))

    def layer_two(self):
        self.layer_one()
        integrate = self.integrate(self.sent_similarity)
        boundaries = [k + 2 for k in np.where(integrate > integrate.mean())[0]] + [-1]
        _start = 0
        for boundary in boundaries:
            _stop = boundary
            cluster, cluster_mask = self.sent_similarity[_start:_stop], np.array(self.filter[_start:_stop])
            if len(cluster) > 2 and cluster_mask.mean() > 0:
                ordered = np.array(list(set(sorted(cluster))))
                integrate = self.integrate(ordered)
                index = list(integrate).index(integrate.max())
                filtered_out = np.where(cluster < ordered[index])[0] + _start
                for sent in filtered_out:
                    self.filter[sent] = 0.0
            _start = _stop
        print('Layer Two: {pc} % compression'.format(pc=self.__percentage_compression()))

    def write_to_file(self, filename, folder=r'Output/'):
        if np.array(self.filter).mean() < 1.0:
            path = folder + filename if 'txt' in filename else filename + '.txt'
            outfile = open(path, mode='wt', encoding='utf-8')
            for sent in self.summary():
                outfile.write(sent)
            outfile.close()
        else:
            print('Error: No Summary Done Yet!')

    # TODO change the default value of debug to false
    def summary(self, debug=False):
        out = []
        for (filtered, sent) in zip(self.filter, self.sents):
            if debug:
                out.append('{filtered} |- {sent}'.format(filtered=filtered, sent=sent))
            else:
                if filtered:
                    out.append(sent)
        return out

    @staticmethod
    def diff(vals):
        if len(vals) > 2:
            return abs(vals[1::] - vals[:-1:])
        else:
            return vals

    @staticmethod
    def integrate(vals):
        return Semantic_Extractor.diff(Semantic_Extractor.diff(vals))

    @staticmethod
    def punctuation(token):
        return token.pos_ == 'PUNCT'
