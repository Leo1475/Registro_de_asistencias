import pdoc

def login(nombre,id):
    """
    Función que realiza un inicio de sesión para el estudiante que quiera usar la aplicación.
    Mediante un nombre y un número de cuenta determina si el estudiante esta autorizado para acceder.
    Los estudiantes autorizados se encuentran en un registro por defecto (estudiantes) donde se almacenan sus nombres y numeros de cuenta.

    Parametros: nombre: Nombre del estudiante.
                id: Número de cuenta del estudiante.
    
    Retorno: True: Si el estudiante esta autorizado será verdadero.
             False: Si el estudiante NO esta autorizado será falso.
    """
    if (nombre,id) in estudiantes:
        return True
    else:
        return False
    
def carrera(id):
    """
    Función que determina a que carrera pertenece el estudiante.
    Mediante el número de cuenta busca donde esta registrado.
    Las carreras se encuentran en un registro por defecto (carreras).

    Parametros: id: número de cuenta del estudiante.

    Retorno: carreras[id]: carrera correspondiente a donde pertenece el estudiante.
    """
    return carreras[id]

def navigate(page):
    """
    Función que permite navegar por páginas de la aplicación, esto facilita el acomodo del código y lo hace más ordenado.
    """
    st.session_state.page = page

def close_session(status):
    """
    Cierra la sesión y vuelve al inicio de la aplicación.

    Parametros: status: Si el estudiante finalizo el registro.
    """
    if status:
        st.session_state['logged_in']=False
        navigate('Inicio')

def crear_pdf(datos):
    """
    Genera un archivo .pdf con los datos registrados.

    Parametros: datos: Información de registro de profesores.
    """
    # Crear una instancia de FPDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Agregar una página
    pdf.add_page()

    # Establecer el tipo de fuente (Arial, negrita, tamaño 16)
    pdf.set_font('Arial', 'B', 16)

    # Título del reporte
    pdf.cell(0, 10, 'Reporte de Asistencia', 0, 1, 'C')

    # Espacio adicional
    pdf.ln(10)

    # Establecer el tipo de fuente para el contenido (Arial, tamaño 12)
    pdf.set_font('Arial', '', 12)

    # Encabezados de la tabla
    header = ['ID', 'Nombre', 'Fecha', 'Materia', 'Día', 'Horario', 'Asistencia', 'Carrera']
    widths = [10, 35, 20, 30, 20, 30, 20, 20]

    for i, heading in enumerate(header):
        pdf.cell(widths[i], 10, heading, 1)
    pdf.ln()

    # Agregar los registros de materias al PDF
    for dato in datos:
        pdf.cell(widths[0], 10, str(dato[0]), 1)
        pdf.cell(widths[1], 10, dato[1], 1)
        pdf.cell(widths[2], 10, dato[2], 1)
        pdf.cell(widths[3], 10, dato[3], 1)
        pdf.cell(widths[4], 10, dato[4], 1)
        pdf.cell(widths[5], 10, dato[5], 1)
        pdf.cell(widths[6], 10, dato[6], 1)
        pdf.cell(widths[7], 10, dato[7], 1)
        pdf.ln()

    # Guardar el archivo PDF
    pdf.output('reporte_asistencia.pdf')

def registrar_asistencia():
    """
    Registra la asistencia de un profesor, utiliza llenado de datos interactivos, asi que el estudiante no necesita ingresar información adicional.
    Determina el usuario elige que profesor impartio su clase, que dia y horario quiere registrar.
    No hay opciones de llenado de aistencia para fines de semana (sábado y domingo).
    Puede actualizar el registro sin necesidad de crear un apartado nuevo.
    """
    carrera=st.session_state['carrera']
    horarios=st.session_state['horario']
    profesores=st.session_state['profesores']
    st.title("Registro de asistencia")

    fecha = st.date_input("Fecha", min_value=datetime(2024, 11, 1), max_value=datetime(2024, 11, 30))
    if fecha.weekday() >= 5:  # Evitar Sábado y Domingo
        st.error("No hay clases programadas para fines de semana")
    else:
        dia_semana = fecha.strftime('%A')  # Convertir la fecha seleccionada al día de la semana
        horario = st.selectbox("Seleccione el Horario", list(horarios[dia_semana].keys()))
        materia = horarios[dia_semana][horario]
        nombre_profesor = st.selectbox("Seleccione el Profesor", profesores[materia])
        asistencia = st.radio("¿El profesor asistió?", ('Sí', 'No'))
        fecha_str = fecha.strftime('%Y-%m-%d')
        
        conn=sqlite3.connect('asistencia.db')
        c=conn.cursor()
        # Verificar si ya existe un registro para esta fecha, materia y horario
        c.execute('SELECT * FROM asistencia_profesores WHERE fecha = ? AND materia = ? AND horario = ? AND carrera = ?', (fecha_str, materia, horario, carrera))
        registro_existente = c.fetchone()

        if st.button("Registrar Asistencia"):
            if registro_existente:
                # Si existe, actualizamos la asistencia
                c.execute('UPDATE asistencia_profesores SET asistencia = ? WHERE fecha = ? AND materia = ? AND horario = ? AND carrera = ?',
                          (asistencia, fecha_str, materia, horario,carrera))
                st.success("Asistencia actualizada exitosamente")
            else:
                # Si no existe, insertamos un nuevo registro
                nuevo_registro = (nombre_profesor, fecha_str, materia, dia_semana, horario, asistencia,carrera)
                c.execute('INSERT INTO asistencia_profesores (nombre_profesor, fecha, materia, dia_semana, horario, asistencia,carrera) VALUES (?, ?, ?, ?, ?, ?, ?)', nuevo_registro)
                st.success("Asistencia registrada exitosamente")
            conn.commit()
            conn.close()
    
def mostrar_asistencia():
    """
    Aqui puede ver todos sus registros agregados.
    Una vez correctos lo datos puede imprimir los datos en un archivo .pdf.
    """
    st.title("Visualización de asistencia")
    carrera_filtro = st.session_state['carrera']
    conn = sqlite3.connect('asistencia.db')
    c = conn.cursor()
    if carrera_filtro:
        c.execute("SELECT * FROM asistencia_profesores WHERE carrera = ?", (carrera_filtro,))
    else:
        c.execute("SELECT * FROM asistencia_profesores")
    datos = c.fetchall()
    conn.close()

    if datos:
        st.write(pd.DataFrame(datos, columns=['ID', 'Nombre del Profesor', 'Fecha', 'Materia', 'Día de la Semana', 'Horario', 'Asistencia','Carrera']))
        if st.button("Descargar archivo .pdf"):
            crear_pdf(datos)
    else:
        st.write("No hay registros de asistencia")

def main(carrera):
    """
    Función principal para el registro de asistencia.
    Se crean la base de datos y la tabla donde se almacenaran los registros.
    Determina los horarios y profesores a mostrar mediante la carrera.
    Contiene un selectbox para que pueda navegar entre registrar y mostrar asistencias.
    Finaliza el registro mediante un botón.

    Parametros: carrera: Carrera a la que se le asignaran los registros.
    
    Retorno: True: Declara que el registro ha finalizado.
    """
    # Conexión a la base de datos
    conn = sqlite3.connect('asistencia.db')
    c = conn.cursor()
    # Crear tabla de asistencia si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS asistencia_profesores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_profesor TEXT,
        fecha TEXT,
        materia TEXT,
        dia_semana TEXT,
        horario TEXT,
        asistencia TEXT,
        carrera TEXT
    )''')

    st.session_state['carrera']=carrera
    match carrera:
        case 'ICI':
            st.session_state['horario']=info.horario_ici
            st.session_state['profesores']=info.profesores_ici
        case 'IME':
            st.session_state['horario']=info.horario_ime
            st.session_state['profesores']=info.profesores_ime
        case 'IM':
            st.session_state['horario']=info.horario_im
            st.session_state['profesores']=info.profesores_im
        case 'ISET':
            st.session_state['horario']=info.horario_iset
            st.session_state['profesores']=info.profesores_iset
    st.header(carrera)
    opcion = st.sidebar.selectbox("Seleccione una opción", ["Registrar Asistencia", "Mostrar Asistencia"])
    if opcion == "Registrar Asistencia":
        registrar_asistencia()
    elif opcion == "Mostrar Asistencia":
        mostrar_asistencia()

    # Regresar al inicio
    if st.button("Finalizar registro"):
        return True
    # Guardar y cerrar la conexión a la base de datos
    conn.commit()
    conn.close()