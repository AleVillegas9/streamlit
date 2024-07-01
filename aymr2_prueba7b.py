# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 20:52:14 2024

@author: javal
"""
#Objetivo: Con este codigo haré una app en streamlit que me permita interactuar con el LMM falcon 7b


#Paso 1: Montamos el LLM
#Nota: A veces se tienen problemas con el apitoken. Rehacerla en https://huggingface.co/settings/tokens


pip install huggingface_hub 
from langchain import HuggingFaceHub

huggingfacehub_api_token = "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" #mi API key

repo_id = "tiiuae/falcon-7b-instruct" #nombre del modelo que agarrare en este caso falcon 11b

llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token,
                     repo_id=repo_id,
                     model_kwargs={"temperature":0.1, "max_new_tokens":500}) #cargamos el modelo
#Averiguar que hace temperature: nivel de cratividad??????

#interactuamos con el de prueba
# print(llm('Haz un poema'))
# print(llm('Cuenta una historia corta'))


#Paso 2: Lo montamos en streamlit


import streamlit as st


st.title('Prueba')

st.write('Intenta hablar con el LLM Falcon 7b')



query = st.text_area('Di algo y el modelo te respondera')


st.write(llm(f'{query}'))

#Nota,creo que es ago de streamlit, porque este usuario, tambien tiene elmismo error https://docs.streamlit.io/develop/tutorials/llms/llm-quickstart
