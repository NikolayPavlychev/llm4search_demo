import json

from classy_fastapi import Routable, post
from fastapi import FastAPI, File, UploadFile

from pydantic import BaseModel
from src.cores.common.web.api_paths import API_PATH
from src.service_modules.igla_chat_service.services.igla_chat_service import IglaChatService


class IglaChatController(Routable):
    CHAT_API_PATH = f"{API_PATH}/igla-chat"

    def __init__(self, chat_service: IglaChatService) -> None:
        super().__init__()
        self.__chat_service = chat_service
        
    class Item(BaseModel):
        question: str
        

     

    @post(f"{CHAT_API_PATH}/ask/", description="Ask chatbot", summary="Ask chatbot", status_code=200)

    def chat(self, item: Item):

        question = item.model_dump()['question']
        print(f'get: {question}')
        
        return self.__chat_service.ask(question=question)

    
    @post(f"{CHAT_API_PATH}/upload_file/", status_code=200)
    async def read_upload_file(self, file: UploadFile):
        json_data = [json.loads(line) for line in file.file]
        answer = 'RAG responces saved in ' + self.__chat_service.inference(data=json_data)
        return answer
    
