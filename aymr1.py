# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 00:45:37 2024

@author: Abraxalandro
"""

#Nota Este es el esqueleto de la pagina de streamlit. se ira actualizando poco a poco. 

#Paso 1: Cargamos la libreria

import streamlit as st

st.title ("Esqueleto proyecto judicatura") #Para agregar un titulo.

st.image("judicatura.jpg", caption="ejemplo", use_column_width=True)

st.header("Este es el pirmer borrador de esqueleto del programa para la judidactura")

st.text("Aqui podria ir una pequeña descripción de que hace esta app") #st.text para escribir planamente

st.markdown("[Enlace al consejo de la judicatura] (https://www.cjf.gob.mx/)") #Poner un enlace