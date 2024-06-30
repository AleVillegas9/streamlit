# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 00:45:37 2024

@author: Abraxalandro
"""

#Nota Este es el esqueleto de la pagina de streamlit. se ira actualizando poco a poco. 

#Paso 1: Cargamos la libreria

import streamlit as st


#Paso 2: Le agregamos cositas

st.title ("Esqueleto proyecto judicatura") #Para agregar un titulo.

st.image("judicatura.jpg", caption="ejemplo", use_column_width=True) 

st.header("Este es el pirmer borrador de esqueleto del programa para la judidactura")

st.text("Aqui podria ir una pequeña descripción de que hace esta app") #st.text para escribir planamente


#Cosas que debe de poner el usuario: De qué categoria es su caso

#Opcion 1: Caja de opcion simple

categoria1 = st.selectbox('Selecciona la categoria de la que es tu caso', ['administrativo', ' acuerdos organizacionales', 'juridiccionales']) #como la guarda en una variable, ya la puedo usar en el codigo

st.write(f'haz seleccionado {categoria1}')


categoria2 = st.multiselect('Selecciona las categorias con las que se relaciona tu caso', ['perritos', 'gatitos', 'MAPPaches', ' delfines', 'abejas', 'caballos']) #la variable es una lista. OJO. 

st.write(f'Haz seleccionado las categorias {categoria2}')

 



query = st.text_input("¿De qué va tu caso?") 

st.write(f'Tu caso va de {query}') #en este caso, la variable de aqui sera la respuesta que da el modelo

#Nota: El primer paso es que el usuario tenga una clasificación de normas relevantes. ¿Conviene que esto se haga preguntando en una query, y que el modelo diga a qué clasificación pertenece? o mejor ponemos una caja de opcion y que el usuario elija la clase a la que pertenece su caso? 

#Nota 2: En caso de que sea la segunda opcion. ¿Ponemos que se pueda elegir una opcion, o dos opciones


#Nota 3: Tambien existe la opcion st.file_uploader("Subir archivo"), osea, se podria implementar que el usuario suba un pdf con su caso, y que el modelo le diga de qué categoria es su caso. 
    #Pero no sé, ¿No sería hacerles demasiado la chamba? ¿Qué tan bueno sería que el LLM decidiera de que tipo es? 

#Links relevantes
st.markdown("[Enlace al consejo de la judicatura] (https://www.cjf.gob.mx/)") #Poner un enlace
st.markdown("[Enlace a la normativa aplicable] (https://apps.cjf.gob.mx/normativa/Index)")