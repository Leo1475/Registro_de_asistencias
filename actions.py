import streamlit as st

carreras={
    "20208468":"ICI",
    "15244862":"IME",
    "20185645":"IM",
    "82248795":"ISET"
    }

estudiantes=[
    ("Miguel Ortiz Torres","20208468"),
    ("Cristian Orlando","15244862"),
    ("Ricky Martin","20185645"),
    ("Elalba Sierra","82248795")
    ]

def login(nombre,id):
    if (nombre,id) in estudiantes:
        return True
    else:
        return False
    
def carrera(id):
    return carreras[id]

def navigate(page):
    st.session_state.page = page

def close_session(status):
    if status:
        st.session_state['logged_in']=False
        navigate('Inicio')