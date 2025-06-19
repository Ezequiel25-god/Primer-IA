#importar  y renombrar Streamlit
import streamlit as st
import groq

#Modelos 
Modelos = ['llama3-8b-8192','llama3-70b-8192','mixtral-8x7b-32768']

#Configuracion de la pagina(Titulos)
def configurar_pagina():
    st.set_page_config(page_title="Primer Chat Bot")
    st.title("Bienvenido a mi Chat Bot")

#Crea Cliente en Groq segun la API
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"]
    return groq.Groq(api_key=groq_api_key)

#Muestra Barra Laterral 
def mostrar_sitebar():
    st.sidebar.title("Eleji Modelo De IA")
    modelo = st.sidebar.selectbox('Eleji tu Modelo  ',Modelos,index=0)
    st.write(f'**Elegiste el modelo** {modelo}')
    return modelo 

def inicializar_estado_chat():
   if "mensajes" not in st.session_state:
       st.session_state.mensajes = []

def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje ["role"]):  
            st.markdown(mensaje ["content"]) 
                     
def obtener_mensaje_Usuario():
    return st.chat_input("Envia tu mensaje")

def agregar_mensajes_previos(role,content):
    st.session_state.mensajes.append({"role": role , "content": content})

def mostrar_mensaje(role,content):
    with st.chat_message(role):
        st.markdown(content)   
        
def obtener_respuesta_modelo(cliente,modelo,mensaje):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=mensaje,
        stream=False
    )        
    return respuesta.choices[0].message.content    
        
def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sitebar()
    
    inicializar_estado_chat()
    mensaje_usuario = obtener_mensaje_Usuario()
    obtener_mensajes_previos()
    
    if mensaje_usuario:
        agregar_mensajes_previos("user",mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)
        respuesta_modelo = obtener_respuesta_modelo(cliente,modelo,st.session_state.mensajes)
        
        agregar_mensajes_previos("assistant",respuesta_modelo)
        mostrar_mensaje("assistant",respuesta_modelo)
    
    print(mensaje_usuario)
    
    
if __name__ == '__main__':
    ejecutar_chat()