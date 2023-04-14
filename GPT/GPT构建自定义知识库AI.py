# -*- codeing = utf-8 -*-
# @Time :2023/3/22 15:02
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://blog.acwinds.com/%E7%BC%96%E7%A8%8B%E7%AC%94%E8%AE%B0/2023/03/12/Use-ChatGPT.html
# @Link : https://colab.research.google.com/drive/1PQXcM_jhN6QJ7uTkxvNbxoI54r03uSr3?usp=sharing#scrollTo=6LL4rxT6_W7h&uniqifier=1
# @File :  GPT构建自定义知识库AI.py

import os

from langchain import OpenAI
from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper

os.environ["OPENAI_API_KEY"] = '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'
from IPython.display import Markdown, display


def construct_index(directory_path):
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 2000
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(
        documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    index.save_to_disk('index.json')

    return index


def ask_ai():
    index = GPTSimpleVectorIndex.load_from_disk('index.json')
    while True:
        query = input("What do you want to ask? ")
        response = index.query(query, response_mode="compact")
        display(Markdown(f"Response: <b>{response.response}</b>"))

# construct_index("./data")

ask_ai()
