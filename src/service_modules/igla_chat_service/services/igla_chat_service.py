import logging
import json
from tqdm import tqdm

import pandas as pd

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.runnable import RunnableLambda
from src.cores.common.elastic.stores.elastic_vector_store_factory import ElasticVectorStoreFactory
from src.cores.igla.models.aliases import ELASTIC_ALIAS_IGLA
from langchain_community.llms import HuggingFaceEndpoint

from src.service_modules.igla_chat_service.chat_models.chat_model_factory import ChatModelFactory


class IglaChatService:
    def __init__(self, store_factory: ElasticVectorStoreFactory, chat_model_factory: ChatModelFactory) -> None:
        self.__store_factory = store_factory
        self.__chat_model = chat_model_factory.create()
        self.__template = "Ты — русскоязычный автоматический ассистент оператора колл центра. Ответь на вопрос, основываясь только на следующем контексте: {context} Вопрос: {question}. Ответ:"
        self.__prompt = ChatPromptTemplate.from_template(self.__template)
        

    def ask(self, question: str, metadata_flg=True) -> str:
        try:
            logging.info(f"question: {question}")

            context, metadata = self.add_context(question)
            query = {"context": context, "question": question} 
   


            chain = (self.__prompt | self.__chat_model
                    | StrOutputParser())

            res = chain.invoke(query)
            if 'bot\n' in res:
                output_clear = res.split('bot\n')[0]
            else:
                output_clear = res
            question_answer_source = 'Вопрос: ' + output_clear.split('Вопрос: ')[1]
            sources = output_clear.split('Вопрос: ')[0]
            sources = sources.split('основываясь только на следующем контексте: ')[1]
            

            
            page_list = []
            
            for p in metadata:
                page_list.append(p['page'])
                                
            source_output= ' Ответ основан на следующей информации из документа Igla_X_clear.pdf: ' + sources
            pages = 'Cписок страниц: ' + str(page_list)


            if metadata_flg==True:
                return question_answer_source + source_output + pages
            else:
                return question_answer_source
            
        except Exception as e:
            logging.error(e, exc_info=True)
            raise e


    
    def add_context(self, question: str) -> str:
        vector_store = self.__store_factory.create(ELASTIC_ALIAS_IGLA)
        r = vector_store.similarity_search(query=question, k=4)
        context = ". ".join(x.page_content for x in r)

    
        return context, [x.metadata for x in r]
    
    def inference(self, data) -> str:
        responce_list = []
        for item in tqdm(data):

            
            answer_rag = self.ask(item['question'], metadata_flg=False)
            item.update({'answer_rag': answer_rag})
            responce_list.append(item)
            
        df_responce = pd.DataFrame(responce_list)
        path = '/home/nikolaypavlychev/llm4search_dev/llm4search_dev/llm4search/references/dataset_val_rag_exp_ind_release.csv'
        df_responce.to_csv(path, sep='\t',index=False)    
        return path

