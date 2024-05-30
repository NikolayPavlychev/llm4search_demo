import itertools
import numpy as np

from torchmetrics.text import TranslationEditRate
from nltk.translate.bleu_score import SmoothingFunction, corpus_bleu, sentence_bleu

def bleu(ref, gen, level='corpus'):
  
  ''' 
  calculate pair wise bleu score. uses nltk implementation
  Args:
      references : a list of reference sentences 
      candidates : a list of candidate(generated) sentences
  Returns:
      bleu score(float)
  '''
  #https://www.nltk.org/_modules/nltk/translate/bleu_score.html
  
  if level=='corpus':
    ref_bleu = []
    gen_bleu = []
    for l in gen:
        gen_bleu.append(l.split())
    for i,l in enumerate(ref):
        ref_bleu.append([l.split()])
    cc = SmoothingFunction()
    score_bleu = corpus_bleu(ref_bleu, gen_bleu, weights=(0.25, 0.5, 0.25, 0), smoothing_function=cc.method4)
  elif level=='sentence':
    bleu_list =[]
    for i, j in zip(ref, gen):
      bleu_list.append(sentence_bleu([i.split()], j.split(), weights=(0.5, 0.5, 0, 0)))
    score_bleu = np.mean(bleu_list)

  return score_bleu


#rouge scores for a reference/generated sentence pair

#supporting function
def _split_into_words(sentences):
  """Splits multiple sentences into words and flattens the result"""
  return list(itertools.chain(*[_.split(" ") for _ in sentences]))

#supporting function
def _get_word_ngrams(n, sentences):
  """Calculates word n-grams for multiple sentences.
  """
  assert len(sentences) > 0
  assert n > 0

  words = _split_into_words(sentences)
  return _get_ngrams(n, words)

#supporting function
def _get_ngrams(n, text):
  """Calcualtes n-grams.
  Args:
    n: which n-grams to calculate
    text: An array of tokens
  Returns:
    A set of n-grams
  """
  ngram_set = set()
  text_length = len(text)
  max_index_ngram_start = text_length - n
  for i in range(max_index_ngram_start + 1):
    ngram_set.add(tuple(text[i:i + n]))
  return ngram_set

def rouge_n(reference_sentences, evaluated_sentences, n=2):
  """
  Computes ROUGE-N of two text collections of sentences.
  Source: http://research.microsoft.com/en-us/um/people/cyl/download/
  papers/rouge-working-note-v1.3.1.pdf
  Args:
    evaluated_sentences: The sentences that have been picked by the summarizer
    reference_sentences: The sentences from the referene set
    n: Size of ngram.  Defaults to 2.
  Returns:
    recall rouge score(float)
  Raises:
    ValueError: raises exception if a param has len <= 0
  """
  if len(evaluated_sentences) <= 0 or len(reference_sentences) <= 0:
    raise ValueError("Collections must contain at least 1 sentence.")

  evaluated_ngrams = _get_word_ngrams(n, evaluated_sentences)
  reference_ngrams = _get_word_ngrams(n, reference_sentences)
  reference_count = len(reference_ngrams)
  evaluated_count = len(evaluated_ngrams)

  # Gets the overlapping ngrams between evaluated and reference
  overlapping_ngrams = evaluated_ngrams.intersection(reference_ngrams)
  overlapping_count = len(overlapping_ngrams)

  # Handle edge case. This isn't mathematically correct, but it's good enough
  if evaluated_count == 0:
    precision = 0.0
  else:
    precision = overlapping_count / evaluated_count

  if reference_count == 0:
    recall = 0.0
  else:
    recall = overlapping_count / reference_count

  f1_score = 2.0 * ((precision * recall) / (precision + recall + 1e-8))

  #just returning recall count in rouge, useful for our purpose
  return recall

def ter(ref, gen):
    '''
    Args:
        ref - reference sentences - in a list
        gen - generated sentences - in a list
    Returns:
        averaged TER score over all sentence pairs
    '''
    ter = TranslationEditRate()
    ter_list =[]
    
    for i, j in zip(ref, gen):
      ter_list.append(ter(j, [i]))
    score_ter = np.mean(ter_list)
    return score_ter



def evaluation_metrics(ref_file_path, gen_file_path,  level='corpus', n_for_rouge = 2):
    '''
    Args:
        ref_file_path (string) : reference file path -> file containing the reference sentences on each line
        gen_file_path (string) : model generated file path -> containing corresponding generated sentences(to reference sentences) on each line
    
    Returns:
        A list containing [bleu, rouge, meteor, ter]
    '''
    file_ref = open(ref_file_path, 'r')
    ref = file_ref.readlines()

    file_gen = open(gen_file_path, 'r')
    gen = file_gen.readlines()

    for i,l in enumerate(gen):
        gen[i] = l.strip()

    for i,l in enumerate(ref):
        ref[i] = l.strip()
    
    ter_score = ter(ref, gen)
    bleu_score = bleu(ref, gen, level=level)
    rouge_score = rouge_n(ref, gen, n=n_for_rouge)
    return [bleu_score, rouge_score, ter_score]
