import streamlit as st
import actions as act
import registro as reg

# Centrar el header con Markdown y agregar emojis
st.markdown("<h1 style='text-align: center;'>Registro de Asistencia de 3 grado FIME 📒✏️🤖</h1>", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'Inicio' 

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'carrera' not in st.session_state:
    st.session_state['carrera'] = "None"

if st.session_state.page == 'Inicio':
    pagina = st.sidebar.selectbox("Ir a:", ["Inicio", "Iniciar sesión"])
    match pagina:
        case 'Inicio':
            st.image("https://media.licdn.com/dms/image/D4E12AQHYxLvWyjmgoQ/article-cover_image-shrink_720_1280/0/1715103390362?e=2147483647&v=beta&t=908mbmzEFh8xU7tcZwT7_4ikLQrxnUhH8t3dQtG_JZ4", caption="Registro de Asistencia")
            
            # Textos más grandes
            st.markdown("<h2>Bienvenido a la página de registro de asistencia</h2>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 20px;'>En esta página podrás registrar las asistencias de los profesores que imparten tus materias en el tercer grado de las carreras que existen en FIME.</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size: 20px;'>También podrás obtener datos referente a la asistencia de todos los profesores en el mes.</p>", unsafe_allow_html=True)

            # Lista de pasos a seguir
            st.markdown("<h3>Pasos a seguir:</h3>", unsafe_allow_html=True)
            st.markdown("""
                1. Selecciona la opción "Iniciar sesión" en el menú lateral.
                2. Ingresa tu nombre y número de cuenta.
                3. Haz clic en el botón "Iniciar sesión".
                4. Accede a tu carrera y registra las asistencias de tus profesores.
                5. Completa la información requerida.
                6. Revisa tus registros y asegúrate de que todo esté correcto.
            """, unsafe_allow_html=True)

            st.markdown("<p style='font-size: 20px;'>PD: No nos hacemos responsables por quejas de maestros.</p>", unsafe_allow_html=True)

        case 'Iniciar sesión':
            if st.session_state['logged_in']:
                act.navigate('Registro')
            else:
                st.title("Iniciar sesión")
                nombre = st.text_input("Nombre")
                id = st.text_input("Número de cuenta")
                if st.button("Iniciar sesión"):
                    status = act.login(nombre, id)
                    if status:
                        st.session_state['logged_in'] = True
                        st.session_state['carrera'] = act.carrera(id)
                    else:
                        st.error("Nombre o Número de cuenta incorrecto")

                
                st.image("https://i0.wp.com/imgs.hipertextual.com/wp-content/uploads/2023/05/robot-ia-aprende-a-leer.jpg?fit=1200%2C750&quality=70&strip=all&ssl=1")

if st.session_state.page == 'Registro':
    carrera = st.session_state['carrera']
    match carrera:
        case "ICI":
            status = reg.main('ICI')
            act.close_session(status)
        case "IME":
            status = reg.main('IME')
            act.close_session(status)
        case "IM":
            status = reg.main('IM')
            act.close_session(status)
        case "ISET":
            status = reg.main('ISET')
            act.close_session(status)
