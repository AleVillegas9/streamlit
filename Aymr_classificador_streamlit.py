# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 19:31:53 2024

@author: Abraxalandro


Código completo del clasificador. 

Ver: Amry_borrador4_limipio
"""

# #Paso 1: Extraemos el texto de los PDF's
# import os #para manipular cosas de mi directorio, y sistema
# import PyPDF2 #para manejar pdf's

# #creamos función que extraiga texto de los pdf's de un directorio

# def extract_text_from_pdfs(pdf_folder_path):
#     pdf_texts = {}  #aqui dcimos que es un diccionario por que aun no se si funciona mejor con diccionarios o listas. 
#     for pdf_file in os.listdir(pdf_folder_path):
#         if pdf_file.endswith('.pdf'):
#             with open(os.path.join(pdf_folder_path, pdf_file), 'rb') as file:
#                 reader = PyPDF2.PdfReader(file)
#                 text = ''
#                 for page in reader.pages:
#                     text += page.extract_text()
#                 pdf_texts[pdf_file] = text
#     return pdf_texts

# #optenemos el path del directorio
# pdf_folder_path = (r"C:\Users\javal\OneDrive\Desktop\judicatura\Con LLM\pruebas")


# # #aplicamos la funcion
# normas_prueba = extract_text_from_pdfs(pdf_folder_path)  

# #-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


# #Paso 2: Troceamos la información en fragmentador para que sea más manejable. 

# from langchain.text_splitter import CharacterTextSplitter #para hacer los fragmetnadores. 

# #hacemos el fragmentador. Ahora que lo pienso, puede haber varios separadores. y usarlos en contextos distintos ....
# text_splitter = CharacterTextSplitter(separator = ' ', chunk_size = 1000, chunk_overlap = 50) 

# # #hacemos un dicionario vacio, odio trabajar con diccionarios. 
# normas_trozadas = {} #te va a regresar otro diccionario

# #iteramos para cada norma

# for norma, contenido in normas_prueba.items(): #recuerda que es un diccionario, donde norma es la key, y el contenido pues el value.
#     fragmentos = text_splitter.split_text(contenido) #el contenido es un string, pues es el value del diccionario
#     normas_trozadas[norma] = fragmentos #recuerda que es un diccionario.

#-*-*-*-*-*-*-*-*-*-*-*-*

#Paso 3: Preparar los fragmentos en algo que pueda subir a Pieccone. 

# #Primero cargamos la funcion vectorizadora
# from openai import OpenAI


# #cargamos la apikey
# usuario = OpenAI(api_key = 'sk-proj-twIXfKBO4Lvfa5NEY8pVT3BlbkFJ6S9Pcbh3Gued8oHSHx6i')

# #definimos la funcion embeddignadora o convierte en vector todo lo que le ponga
# def get_embedding (text, model = "text-embedding-ada-002"):
#     text = text.replace('\n', " ")
#     return usuario.embeddings.create(input = [text], model = model). data[0].embedding


# #Despues aplicamos la funcion en cada fragmento

# data = [] #en este caso, lo que resulta son tuples *******

# # Convertir los trozos de texto a vectores y crear identificadores únicos
# for doc_id, chunks in normas_trozadas.items():
#     for i, chunk in enumerate(chunks):
#         chunk_id = f"{doc_id}_chunk_{i}"
#         vector = get_embedding(chunk)  # Convertir el trozo de texto a vector
#         data.append((chunk_id, vector))


#-*-*-*-*--*-*-*-*-*-**-


#Paso 4: Creamos al index en pinecone para chatear

#Primero creamos el índex

from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(
      api_key="7332013f-ef1d-4436-a29a-80e430b549b3", environment="us-west1-gcp")

# #&&&&&

# # # creo un index un index en pinecone


# pc.create_index(
#     name="index",
#     dimension=1536, # este deve ser del mismo tamanio del modelo de embedding que uso
#     metric="euclidean", # Remplazar con la metrica que queremos
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     ) 
# ) 

# #Iniciamos el index
# index = pc.Index('index') #esto se puede verificar desde mi cuenta en pinecone.com

#-**-*-*-*-*-*-*-*-*

#Paso 5 : Subimos la tuple al index

# index.upsert(vectors = data) #Salen 15 vectores uno por cada lista de fragmentos. Si reqquiero mas, necesito hacerlo en batches. https://docs.pinecone.io/guides/data/upsert-data

#-*-*-*-*-*-*-*-**--*-

# #Paso 6: Actualizamos con los metadatos necesarios para la funcion de chat

# #Los metadatos son esnciales para que todo funcione. El chiste es poner los contenidos originales de los fragmentos en los metadatos del index de pinecone

# #Primero extraemos los nombres de los fragmentos de normas. Estos deben ser extraido de DATA es decir, de la lista de donde se subio el index de pinecone.

# nombres = []

# for tupla in data:
#     nombre = tupla[0]
#     nombres.append(nombre)
    
# # #Despues extraemos los contenidos de los fragmentos. Estos estan dentro de la variable diccionarios.

# contenidos = []
# for key, lista in normas_trozadas.items():
#     for string in lista:
#         contenidos.append(string)
        

# # #Tercero, creamos un diccionario con los metadatos. 

# metadatos_dicc ={nombres:value for nombres, value in zip(nombres,contenidos)}

# # #Lo bueno es que el orden matchea. 


# # #Por ultimo, actualizamos el index

# for key, value in metadatos_dicc.items():
#     index.update(id = key, set_metadata = {'contenido': f'{value}' })

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

#Paso 7: Creamos un index gemelo, donde los metadatos solo contengan las fuentes


# pc.create_index(
#     name="indexfuentes",
#     dimension=1536, # este deve ser del mismo tamanio del modelo de embedding que uso
#     metric="euclidean", # Remplazar con la metrica que queremos
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     ) 
# ) 

# # #Iniciamos el index
indexfuentes = pc.Index('indexfuentes') #esto se puede verificar desde mi cuenta en pinecone.com

# # #Le ponemos contenido al index gemelo. es cgemelo porque tiene los mismos vectores. 

# indexfuentes.upsert(vectors = data) 


# #NOTA IMPORTANTE: Si no hago la parte de los index gemelos. cuanto aplique el retriever, me soltara todos los metadatos. tanto los de la fuente, como los de contenido. y sera inteligible. 
# #-*-*-*-*-*-*-*-*-*

# #Paso 7: Actualizo los metadatos necesarios para la funcionde clasificacion de textos. 

# #En este caso necesito que el mismo index ya usado, tenga otro campo de metadatos que me diga el documento origen de los fragmentos. En este caso pondre un nombre, pero tambien se puede poner un link. 

# #Al igual que el anterior necesito hacer un diccionaro. La primera parte ya la tengo pues es la lista de nombres de los frgamentos. Ahora necesito una lista que matchee en orden, que a cada fragmento le asocie un string donde diga de qu[e documento viene.

# #Primero hacemos un diccionario, con las asociaciones entre los ID de las normas, y la fuente que queremos que aparezca en los metadados. Aqui cuidado, porque el key, debe de ser algo que identifique el nombre de cada norma. En este caso puse las primeras 6 letras de los filosofos. pero puede ser otra cosa. Incluso este se pued sacar  de listas. 

# asociaciones_fuente ={
#    'Schope':'Biografia Schopenhauer',
#    'Seneca': 'Biografica Seneca',
#    'Voltai': 'Biografia Voltaire'}

# #Creamos una lista de fuentes que tenga el mismo orden que los ID (queen este codigo se llama nombres, ver linea 130)

# lista_fuentes = []

# for nombre in nombres:
#     prefijo = nombre[:6]  #esta linea me dira cual sera el criterio para clasificar el nombre asociado. EN este caso las primeras seis letras. 
#     if prefijo in asociaciones_fuente:
#         lista_fuentes.append(asociaciones_fuente[prefijo])

# #creamos el diccionario con las fuentes y los nombres de los fragmentos asociados. 
# metadatos_fuentes ={nombres:value for nombres, value in zip(nombres,lista_fuentes)}


# #Actualizamos nuestro index 

# for key, value in metadatos_fuentes.items():
#     indexfuentes.update(id = key, set_metadata = {'fuente': f'{value}' }) #PON MUCHA ATENCION COMO LLAMAS AL CAMPO DE LOS METADATOS, PORQUE SERVIRA PARA HACER EL VECTORSTORE PARA CLASIFICAR. 

#verificamos en : https://app.pinecone.io/organizations/-O0GfPwgVtMaldW2mBha/projects/c86b0676-8a7d-4cd2-a6f6-03b6c43e7c9c/indexes/index/browser

#-*-*-*-*-*-**-*-*-*-*-

#Paso 8: Creamos un vectorstore para clasificar

#es decir, que me regrese los metadatos del campo de fuente. 

from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

#Primero, creamos el embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key= 'sk-proj-twIXfKBO4Lvfa5NEY8pVT3BlbkFJ6S9Pcbh3Gued8oHSHx6i')


# #Despues Hacemos el vectorstore
vector_store_clasificador = PineconeVectorStore(index = indexfuentes, embedding= embeddings, text_key= 'fuente') #NOTA NIVEL 9: el text_key, es el campo de metadatos que quieres que consulte. ASEGURATE QUE TODO EL TEXTO ESTE EN ESTE CAMPO DE LOS METADATOS

#nota2: fijate que en el parametro de index, viene el que creaste para clasificar. 

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

#Paso 9: Creamos un vectorstore para chatear, es decir que me de los metadatos contenidos en el campo de contenido. 

# vector_store_chat = PineconeVectorStore(index = index, embedding= embeddings, text_key= 'contenido')

#-*-*-*-*-*-*-*-*-*-*--*-*-*

                                #Clasificador
#Paso 10: convertimos el vectorstore clasificador en un retriever:

#Teoría: https://python.langchain.com/v0.2/docs/how_to/vectorstore_retriever/

# El retriever me permite usar un vector store para darme documentos relacionados con la query que haga. Osea, es lo que me va a clasificar. 

# retriever = vector_store_clasificador.as_retriever(search_type = 'similarity_score_threshold', search_kwargs = {"score_threshold": 0.67}) #Aqui puedo manejar el porcentaje de similitud que servira para saber que textos me dara. 


retrieverk  = vector_store_clasificador.as_retriever(search_kwargs={"k": 1})

#Nota: Otra opcion es especificar top K. pero siento que esto podria dar mucha basura. o dejar fuera documentos que pueden ser importantes. Una segunda opcion es aplicar maximum marginal relevance. Metodo que trata de equilibrar la relevancia de los textods dados, con la diversodad de documentos. Es decir, presenta resultados similares y diversos. En las pruebvas la diversidad me parecia excesiva. Ademas, se tiene poco control sobre los documentos que regresa. 

#-*-*-*-*-*-*-*-*-*-*--*-*-*

#Paso 11: Lo aplicamos

# query = '¿Qué documentos tratan sobre filósofos franceses?'


# #Primero el que cñasifica con probabilidad
# docs = retriever.invoke(query)

# print(docs)


# #vemos que nos da documentos que no concuerdan


# #despues como como sabemos que solo hay una bibliografia que hablar de cada filosofo. y cada filosofo es de nacionalidad diferente. aplicamos el metodo k = n, en este caso k= 1

# docs2 = retrieverk.invoke(query)


#-*-*-*-*-*-*-*-*-*-*


# #Paso 12: Limpiamos la respuesta

# print(docs2[0]) #este es lo que me da mas cercano a un nombre claro de fuente. 

# #lo convertimos a string

# respuesta_class_sucia= str(docs2[0]) 

# print(respuesta_class_sucia)


# #limpiamos el string quitanto lo de page_content

# respuesta_class_limpia = respuesta_class_sucia.replace('page_content=', '').strip()

# print(respuesta_class_limpia)

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*

                                #CHAT
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

                            #Montarlo en streamlit
                            
                            
                            #Streamlit clasificacion
                                    
#Paso 13: Importamos libreria

import streamlit as st

#-*-*-*-*-*-*-*-*-*-*-*-*-*

#Paso 14: Datos generales de la pagina

st.image("judicatura.jpg", use_column_width=True) #Quizá también añadir un logotipo del proyecto. Que lo haga la IA xd. Acomodar despues. 

st.title('Asistente jurídico Aymr') #Cambiar el nombre cuando se decida uno

st.subheader("Aymr es un asistente jurídico, impulsado con inteligencia artificial, que te ayudará en la busqueda de normas que sean relevantes para tu caso. Además de que te permitirá interactuar con dichas normas. Su funcionamiento es muy sencillo. Primero debes de seleccionar la categoria en la que se enmarca tu caso en cuestión. Aymr te dará una lista de las normas con una mayor posibilidad de relacionarse con tu caso. Segundo, elije una norma con la que quieras chatear, y hazle preguntas.")  #Mejorar descripción

st.text("Esta herramienta es sólo de apoyo para la labor de los abogados. DE NINGUNA MANERA SUSTITUYE LA LABOR DE INVESTIGACIÓN Y AUTONOMÍA DEL ABOGADO") #Pesar en más advertencias. 

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


#Paso 15: Informacion e instrucciones del calsificador. 
    
st.header('Clasificador de textos filosoficos por paises')
st.text('Selecciona un pais, y te dira que texto es sobre el filósofo de ese país')

#-*-*-*-*-*-


#Paso 16: Aplicar

query_categoria = st.selectbox('Elije el país del que quieres el texto', ['Francia', 'Alemania', 'Hispania']) #el usuario elije una categoria
    

query_clasificacion = (f'¿Qué documentos tratan sobre filósofos nacidos en {query_categoria}?')  #se crea una query en funcion de esa categoria. 


respuesta_classificacion = retrieverk(query_clasificacion) #aqui usamos el retriever para tener la respuesta

#limpiamos la respuesta

#convertimos a string
texto_class_sucio = str(respuesta_classificacion[0]) 

#limpiamos el string quitanto lo de page_content

texto_class_limpio = texto_class_sucio.replace('page_content=', '').strip()

st.write(f'haz seleccionado {query_categoria} El nombre de los textos que tratan sobre filosofos de ese país son {texto_class_limpio}')

#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-

                                #Streamlit chat
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*


#Paso 17: Referencias

st.markdown("[Enlace al consejo de la judicatura] (https://www.cjf.gob.mx/)") #Poner un enlace
st.markdown("[Enlace a la normativa aplicable] (https://apps.cjf.gob.mx/normativa/Index)") #Aqui poner los links al repositorio de normas.

st.markdown("[Enlace CIDE], (https://www.cide.edu/)")





