#!/usr/bin/env python3
import numpy as np
from hmm_loader import Loader
from collections import defaultdict


class HMM:
    def __init__(self, tag_vocab):
        self.emissions = None
        self.transitions = None
        # self.states contains one-tag states (bigram)
        self.states = list(tag_vocab)

    def train(self, train_x, train_y, smooth, lambdas=None):
        '''
        Train HMM with ML estimations. 
        Store results in self.emissions and self.transitions.
        Args:
            train_x: List[List[str]], observations
            train_y: List[List[str]], tags
            smooth: str, smoothing method for transition estimations
                    'add_one' or 'linear_interpolate'
        '''
        self.emissions = self._emisson_probs(train_x, train_y)
        self.transitions = self._transition_probs(train_y, smooth, lambdas)

    def _emisson_probs(self, train_x, train_y):
        '''
        Calculate ML estimations to construct emission probability table.
        Args: 
            train_x: List[List[str]], observations
            train_y: List[List[str]], tags
        Returns:
            emissions: dict[(str, str)], emission probabilities, i.e. P(word | tag)
        '''
        emissions = defaultdict(lambda: float('-inf'))
        emission_count = defaultdict(int)
        tag_count = defaultdict(int)
        for sentence, tags in zip(train_x, train_y):
            for word, tag in zip(sentence, tags):
                if tag == '*':
                    continue
                emission_count[(word, tag)] += 1
                tag_count[tag] += 1
        for word, tag in emission_count.keys():
            # only count existing probabilities
            # for later use, missing P(word | tag) will be viewed as -inf in log space
            emissions[(word, tag)] = np.log(emission_count[(word, tag)] / tag_count[tag])
        return emissions

    def _transition_probs(self, train_y, smooth, lambdas):
        if smooth == 'add_one':
            return self._transition_add_one(train_y)
        elif smooth == 'linear_interpolate':
            assert lambdas is not None
            return self._transition_linear_interpolate(train_y, lambdas)

    def _transition_linear_interpolate(self, train_y, lambdas):
        transitions = defaultdict(float)
        nomin1 = defaultdict(int)
        denom1 = defaultdict(int)
        nomin0 = defaultdict(int)
        for tags in train_y:
            for i, tag in enumerate(tags):
                if tag == '*':
                    continue
                N, V = tags[i], tags[i - 1]
                nomin1[(N, V)] += 1
                denom1[V] += 1
                nomin0[N] += 1
        tag_pairs = [(N, V) for N in self.states
                            for V in self.states]
        for pair in tag_pairs:
            N, V = pair
            if (N, V) in nomin1:
                transitions[(N, V)] += lambdas[1] * nomin1[(N, V)] / denom1[V]
            if N in nomin0:
                transitions[(N, V)] += lambdas[0] * nomin0[N] / len(nomin0)
            if (N, V) not in transitions:
                transitions[(N, V)] = float('-inf')
            else:
                transitions[(N, V)] = np.log(transitions[(N, V)])
        return transitions 

    def _transition_add_one(self, train_y):
        transitions = {}
        nomin_count = defaultdict(int)
        denom_count = defaultdict(int)
        for tags in train_y:
            for i, tag in enumerate(tags):
                if tag == '*':
                    continue
                N, V = tags[i], tags[i - 1]
                nomin_count[(N, V)] += 1
                denom_count[V] += 1
        tag_pairs = [(N, V) for N in self.states 
                            for V in self.states]
        for pair in tag_pairs:
            N, V = pair
            if (N, V) in nomin_count:
                transitions[(N, V)] = np.log((nomin_count[(N, V)] + 1) / (denom_count[V] + len(denom_count)))
            else:
                transitions[(N, V)] = np.log(1 / (denom_count[V] + len(denom_count)))
        return transitions 

    def inference(self, x, decode, k=None, verbose=False):
        if decode == 'beam':
            assert k is not None
            pred_y = self._beam(x, k, verbose)
        elif decode == 'viterbi':
            pred_y = self._viterbi(x, verbose)
        else:
            raise NotImplementedError('Decode method not implemented.')
        return pred_y

    def _beam(self, x, k, verbose):
        pred_y = []
        for c, sentence in enumerate(x):
            seqs = [['*'] for _ in range(k)]
            total_scores = [0] * k
            for i, word in enumerate(sentence):
                if word == '*':
                    continue
                topk_scores = [float('-inf')] * k
                topk_backpointers = [(0, '')] * k # [(k_, N), ...]
                for k_ in range(k):
                    for state in self.states:
                        N = state
                        if self.emissions[(word, N)] == float('-inf'):
                            continue
                        if seqs[k_][-1] == '':
                            continue
                        V = seqs[k_][-1]
                        score = self.emissions[(word, N)] + self.transitions[(N, V)] + total_scores[k_]
                        min_score = min(topk_scores)
                        if score > min_score and score not in topk_scores and (k_, N) not in topk_backpointers:
                            min_idx = topk_scores.index(min_score)
                            topk_scores[min_idx] = score
                            topk_backpointers[min_idx] = (k_, N)
                new_seqs = []
                new_total_scores = []
                for score, bp in zip(topk_scores, topk_backpointers):
                    k_, N = bp
                    new_seqs.append(seqs[k_] + [N])
                    new_total_scores.append(score)
                seqs = new_seqs
                total_scores = new_total_scores
            if verbose and c % 50 == 0:
                print('%dth sentence:' % c)
                for seq in seqs:
                    print(seq)
            max_score_idx = total_scores.index(max(total_scores))
            pred_y.append(seqs[max_score_idx])
        return pred_y

    def _viterbi(self, x, verbose):
        pred_y = []
        for c, sentence in enumerate(x):
            pi = {state: float('-inf') for state in self.states}
            pi['*'] = 0
            back_pointer = {}
            bp_idx = 0
            for word in sentence:
                if word == '*':
                    continue
                new_pi = {state: float('-inf') for state in self.states}
                for N in self.states:
                    if self.emissions[(word, N)] == float('-inf'):
                        continue
                    for V in self.states:
                        score = pi[V] + self.transitions[(N, V)] + self.emissions[(word, N)]
                        if score > new_pi[N]:
                            new_pi[N] = score
                            back_pointer[(bp_idx, N)] = V # bp_idx starts from 0
                pi = new_pi
                bp_idx += 1
            # generate sequence from back pointer
            last_state = max(pi, key=pi.get) # get last state with the highest score
            seq = [last_state]               # put last tag into the sequence
            bp_idx -= 1                      # set bp_idx to the right ending position
            while bp_idx >= 0:
                N = seq[-1]
                tag = back_pointer[(bp_idx, N)]
                seq.append(tag)
                bp_idx -= 1
            pred_y.append(seq[::-1])
            if verbose and c % 50 == 0:
                print('%dth sentence:' % c)
                print(seq[::-1])
        return pred_y

    def accuracy(self, dev_x, dev_y, decode, k=None, verbose=False):
        pred_y = self.inference(dev_x, decode, k, verbose)
        num_correct = 0
        total = 0
        for pred_seq, dev_seq in zip(pred_y, dev_y):
            for y_, y in zip(pred_seq, dev_seq):
                if y == '*' or y == '<STOP>':
                    continue
                if y_ == y:
                    num_correct += 1
                total += 1
        return num_correct / total

    def find_suboptimal_sequences(self, x, y, decode, k=None, verbose=False):
        pred_y = self.inference(x, decode, k, verbose)
        num_suboptimal = 0
        num_completely_correct = 0
        num_other = 0
        for sentence, pred_seq, gold_seq in zip(x, pred_y, y):
            pred_score = 0
            gold_score = 0
            for i in range(len(sentence)):
                if gold_seq[i] == '*':
                    continue
                pred_score += (self.transitions[(pred_seq[i], pred_seq[i - 1])] 
                              + self.emissions[(sentence[i], pred_seq[i])])
                gold_score += (self.transitions[(gold_seq[i], gold_seq[i - 1])]
                              + self.emissions[(sentence[i], gold_seq[i])])
            if gold_score > pred_score:
                num_suboptimal += 1
#                print('Predicted seq:', pred_seq)
#                print('Gold seq:     ', gold_seq)
            if gold_score == pred_score:
                num_completely_correct += 1
        return num_suboptimal / len(x), num_completely_correct / len(x)

def generate_submission(pred_sequences, filename='hmm_bigram_sample'):
    with open('./results/' + filename + '.csv', 'w') as f:
        f.write('id,tag\n')
        idx = 0
        for seq in pred_sequences:
            for tag in seq:
                if tag == '*' or tag == '<STOP>':
                    continue
                f.write('{},"{}"\n'.format(idx, tag))
                idx += 1


if __name__ == '__main__':
    loader = Loader(ngram=2)
    train_x, train_y = loader.load_data('train')
    dev_x, dev_y = loader.load_data('dev')
    test_x, _ = loader.load_data('test')
    print('Done loading data.')

    hmm = HMM(tag_vocab=loader.tag_vocab)
    # smooth = ['add_one', 'linear_interpolate']
#    hmm.train(train_x, train_y, smooth='linear_interpolate', lambdas=(0.8, 0.2))
    hmm.train(train_x, train_y, smooth='add_one')
    print('Done training.')

    sample_size = 2000

    # inference
    dev_acc = hmm.accuracy(dev_x[:sample_size], dev_y[:sample_size], decode='viterbi', verbose=False)
    print('Dev accuracy (viterbi):', dev_acc)
    dev_acc = hmm.accuracy(dev_x[:sample_size], dev_y[:sample_size], decode='beam', k=3, verbose=False)
    print('Dev accuracy (beam):', dev_acc)

    # analysis
    viterbi_sub_rate, viterbi_correct_rate = hmm.find_suboptimal_sequences(dev_x[:sample_size], dev_y[:sample_size], decode='viterbi')
    print('Suboptimal sequence rate (viterbi):', viterbi_sub_rate)
    print('Correct sequence rate (viterbi):   ', viterbi_correct_rate)
    beam_sub_rate, beam_correct_rate = hmm.find_suboptimal_sequences(dev_x[:sample_size], dev_y[:sample_size], decode='beam', k=3)
    print('Suboptimal sequence rate (beam):', beam_sub_rate)
    print('Correct sequence rate (beam):   ', beam_correct_rate)

    # generate submission .csv file
#    pred_y = hmm.inference(test_x, decode='viterbi') # decode = ['beam', 'viterbi']
#    generate_submission(pred_y, filename='hmm_trigram_add_one_viterbi')

