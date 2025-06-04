import groq as gr
import streamlit as st
st.set_page_config("MI CHAT BOX")

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def configurar_pagina():
    st.title("Mi chat IA")

    nombre = st.text_input("¿Cuál es tu nombre? ")
    if st.button("Saludar"):
        st.write(f"Hola {nombre}")
    st.sidebar.title("Configuración modelos")
    modelo_elegido = st.sidebar.selectbox("Modelos", MODELOS, index=0)

    return modelo_elegido

def crear_usuario():
    clave_secreta = st.secrets['CLAVE_API']
    return gr.Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensaje_entrada):
    return cliente.chat.completions.create(model = modelo, messages = [{"role" : "user", "content" : mensaje_entrada}], stream = False)

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol,contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar = mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedor = st.container(height=400, border=True)
    with contenedor : mostrar_historial()

def generar_respuesta(respuesta_ia):
    respuesta_completa = ""
    for frase in respuesta_ia:
        if frase.choices(0).delta.content:
            respuesta_completa += frase.choices(0).delta.content
            yield frase.choices(0).delta.content
    return respuesta_completa

usuario_groq = crear_usuario()
inicializar_estado()
modelo_actual = configurar_pagina()
area_chat()
def main():

    mensaje_usuario = st.chat_input("Ingrese su prompt")

    if mensaje_usuario:
        actualizar_historial("user", mensaje_usuario, "🐔")
        respuesta_ia = configurar_modelo(usuario_groq, modelo_actual, mensaje_usuario)
        print(mensaje_usuario)
        if respuesta_ia:
            contenido_respuesta = respuesta_ia.choices[0].message.content  # Solo el texto
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(contenido_respuesta)
            actualizar_historial("assistant", contenido_respuesta, "🤖")
            st.rerun()
    
if __name__ == "__main__":
    main()