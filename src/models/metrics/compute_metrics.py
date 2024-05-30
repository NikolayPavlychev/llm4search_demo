import os
import sys

import json

from dotenv import load_dotenv
from dotenv import dotenv_values

load_dotenv('/home/namenode/llm4search_repo/llm4search/.env')

config = dotenv_values()
sys.path.append(config['HOME'])
sys.path.append(config['SRC'])

import pandas as pd
from src.models.metrics.evaluate import *

df_responces = pd.read_csv('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/references/dataset_val_rag.csv',sep='\t')
df_responces['answer_rag']= df_responces['answer_rag'].apply(lambda x: x.split('Ответ: ')[1])
ref = df_responces['answer'].to_list()
gen = df_responces['answer_rag'].to_list()

ter_score = ter(ref, gen)
bleu_score_corpus = bleu(ref, gen, level='corpus')
bleu_score_sentence = bleu(ref, gen, level='sentence')
rouge_score = rouge_n(ref, gen, n=2)
metrics ={'ter_score': round(ter_score, 3), 'bleu_score_corpus': round(bleu_score_corpus, 3),
          'bleu_score_sentence': round(bleu_score_sentence, 3), 'rouge_score': round(rouge_score, 3)}

with open ('/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/src/models/metrics/metrics_dataset_val.json', 'w') as f:
    f.write(json.dumps(str(metrics)))
