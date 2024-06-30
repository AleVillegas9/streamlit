# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 22:36:46 2024

@author: javal
"""

#Paso 1: Instalamos  / cargamos streamlit

# &&&& pip install streamlit &&&&

import streamlit as st

#Paso 2: Ponemos titulo y una descripcion

st.title ('Mi primera aplicacion')
st.write ('Esta es una prueba')

#Con input

nombre = st.text_input ('Ingresa tu nombre: ')
if nombre:
    st.write(f'Hola, {nombre}')