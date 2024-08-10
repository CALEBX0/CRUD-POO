import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app=Flask(__name__)

#Mysqlconnection
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', '11071726')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'escuela')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))
mysql = MySQL(app)

#settings
app.secret_key  = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', personas=data)

# TABLA PERSONAS
@app.route('/add_persona', methods=['POST'])
def add_persona():
    if request.method == 'POST':
        # Recibir datos del formulario
        nombre = request.form['Nombre']
        apellido_p = request.form['Apellido paterno']
        apellido_m = request.form['Apellido materno']
        matricula = request.form['Matricula']

        # Imprimir datos recibidos para depuración
        print(f"Nombre: {nombre}, Apellido Paterno: {apellido_p}, Apellido Materno: {apellido_m}, Matricula: {matricula}")

        # Insertar datos en la base de datos
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO personas (nombre, apellido_p, apellido_m, matricula) VALUES (%s, %s, %s, %s)',
                    (nombre, apellido_p, apellido_m, matricula))
        mysql.connection.commit()
        flash("Se agregó la persona exitosamente")
        return redirect(url_for('index')) #index PQ en @app.route('/'), la función es index :)



@app.route('/edit_persona/<id>')
def get_persona(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM personas WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('Edit_personas.html', persona=data[0])


@app.route('/update_persona/<id>', methods=['POST'])
def update_persona(id):
    if request.method == 'POST':
        # Print the received form data
        print(request.form)

        # Extract form data
        nombre = request.form['Nombre']
        apellido_p = request.form['Apellido paterno']
        apellido_m = request.form['Apellido materno']
        matricula = request.form['Matricula']

        # Update the database
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE personas
        SET nombre = %s, apellido_p = %s, apellido_m = %s, matricula = %s
        WHERE id = %s
        """, (nombre, apellido_p, apellido_m, matricula, id))
        mysql.connection.commit()
        flash("La persona ha sido actualizada ;)")
        return redirect(url_for('index'))

@app.route('/delete_persona/<string:id>')
def borrar(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM personas WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash("Se eliminó la persona exitosamente")
    return redirect(url_for('index'))



#ESTUDIANTES

@app.route('/estudiantes')
def estudiantes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estudiantes')
    estudiantes_data = cur.fetchall()

    cur.execute('SELECT id, nombre, apellido_p, apellido_m FROM personas')
    personas_data = cur.fetchall()

    return render_template('Estudiantes.html', estudiantes=estudiantes_data, personas=personas_data)



@app.route('/add_estudiante', methods=['POST'])
def add_estudiante():
    if request.method == 'POST':
        persona_id = request.form ['persona_id']
        Grado = request.form['Grado']
        Grupo = request.form['Grupo']
        Fecha_registro = request.form['Fecha_registro']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO estudiantes (persona_id, Grado, Grupo, Fecha_registro) VALUES (%s, %s, %s, %s)',
                    (persona_id, Grado, Grupo, Fecha_registro))
        mysql.connection.commit()
        flash("Se agregó al estudiante exitosamente")
        return redirect(url_for('estudiantes')) #estudiantes PQ en @app.route('/estudiantes'), la función es estudiantes :)



@app.route('/edit_estudiante/<id>')
def get_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM estudiantes WHERE id = %s', [id])
    estudiante = cur.fetchone()

    cur.execute('SELECT * FROM personas')
    personas = cur.fetchall()

    return render_template('Edit_estudiantes.html', estudiante=estudiante, personas=personas)



@app.route('/update_estudiante/<id>', methods=['POST'])
def update_estudiante(id):
    if request.method == 'POST':
        # pa ver que datos jaló
        print(request.form)

        # para extraerle los datos al form del html
        persona_id = request.form['persona_id']
        Grado = request.form['Grado']
        Grupo = request.form['Grupo']
        Fecha_registro = request.form['Fecha_registro']

        # para actualizar la BD uwu
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE estudiantes
        SET persona_id = %s, Grado = %s, Grupo = %s, Fecha_registro = %s
        WHERE id = %s
        """, (persona_id, Grado, Grupo, Fecha_registro, id))
        mysql.connection.commit()
        flash("El estudiante ha sido actualizado ;)")
        return redirect(url_for('estudiantes'))

@app.route('/delete_estudiante/<string:id>')
def borrar_estudiante(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM estudiantes WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash("Se eliminó el estudiante exitosamente")
    return redirect(url_for('estudiantes'))


# Profesores
@app.route('/profesores')
def profesores():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM profesores')
    profesores_data = cur.fetchall()

    cur.execute('SELECT id, nombre, apellido_p, apellido_m FROM personas')
    personas_data = cur.fetchall()

    return render_template('profesores.html', profesores=profesores_data, personas=personas_data)

@app.route('/add_profesor', methods=['POST'])
def add_profesor():
    if request.method == 'POST':
        persona_id = request.form['persona_id']
        Especialidad = request.form['Especialidad']
        Fecha_contratacion = request.form['Fecha_contratacion']

        # Comprobar en la consola que se han ingresado esos datillos xd
        print(f"Persona ID: {persona_id}, Especialidad: {Especialidad}, Fecha de Contratación: {Fecha_contratacion}")

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO profesores (persona_id, Especialidad, Fecha_contratacion) VALUES (%s, %s, %s)',
                    (persona_id, Especialidad, Fecha_contratacion))
        mysql.connection.commit()
        flash("Se agregó al profesor exitosamente")
        return redirect(url_for('profesores'))

@app.route('/edit_profesores/<id>')
def get_profesor(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM profesores WHERE id = %s', [id])
    profesor = cur.fetchone()

    cur.execute('SELECT * FROM personas')
    personas = cur.fetchall()

    return render_template('Edit_profesores.html', profesor=profesor, personas=personas)


@app.route('/update_profesor/<id>', methods=['POST'])
def update_profesor(id):
    if request.method == 'POST':
        # pa ver que datos jaló
        print(request.form)

        # para extraerle los datos al form del html
        persona_id = request.form['persona_id']
        Especialidad = request.form['Especialidad']
        Fecha_contratacion = request.form['Fecha_contratacion']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE profesores
        SET persona_id = %s, Especialidad = %s, Fecha_contratacion = %s
        WHERE id = %s
        """, (persona_id, Especialidad, Fecha_contratacion, id))
        mysql.connection.commit()
        flash("El profesor ha sido actualizado ;)")
        return redirect(url_for('profesores'))

@app.route('/delete_profesor/<string:id>')
def borrar_profesor(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM profesores WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash("Se eliminó al profesor exitosamente")
    return redirect(url_for('profesores'))



# Materias
@app.route('/materias')
def materias():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materias')
    materias_data = cur.fetchall()

    cur.execute('''
        SELECT profesores.id, personas.nombre, personas.apellido_p, personas.apellido_m, profesores.Especialidad, profesores.Fecha_contratacion
        FROM profesores
        INNER JOIN personas ON profesores.persona_id = personas.id
        ORDER BY profesores.id, personas.nombre, personas.apellido_p, personas.apellido_m, profesores.Especialidad, profesores.Fecha_contratacion
    ''')
    profesores_data=cur.fetchall()
    return render_template('materias.html', materias=materias_data, profesores=profesores_data)

@app.route('/add_materia', methods=['POST'])
def add_materia():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Descripcion = request.form['Descripcion']
        Profesor_id = request.form['Profesor_id']

        # Comprobar en la consola que se han ingresado esos datillos xd
        print(f"Persona ID: {Nombre}, Especialidad: {Descripcion}, Fecha de Contratación: {Profesor_id}")

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO materias (Nombre, Descripcion, Profesor_id) VALUES (%s, %s, %s)',
                    (Nombre, Descripcion, Profesor_id))
        mysql.connection.commit()
        flash("Se agregó la materia exitosamente")
        return redirect(url_for('materias'))

@app.route('/edit_materias/<id>')
def get_materia(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materias WHERE id = %s', [id])
    materia = cur.fetchone()
    cur.execute('''
        SELECT profesores.id, personas.nombre, personas.apellido_p, personas.apellido_m, profesores.Especialidad, profesores.Fecha_contratacion
        FROM profesores
        INNER JOIN personas ON profesores.persona_id = personas.id
        ORDER BY profesores.id, personas.nombre, personas.apellido_p, personas.apellido_m, profesores.Especialidad, profesores.Fecha_contratacion
    ''')
    profesores = cur.fetchall()
    return render_template('Edit_materias.html', materia=materia, profesores=profesores)

@app.route('/update_materia/<id>', methods=['POST'])
def update_materia(id):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Descripcion = request.form['Descripcion']
        Profesor_id = request.form['Profesor_id']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE materias
        SET Nombre = %s, Descripcion = %s, Profesor_id = %s
        WHERE id = %s
        """, (Nombre, Descripcion, Profesor_id, id))
        mysql.connection.commit()
        flash("La materia ha sido actualizado ;)")
        return redirect(url_for('materias'))

@app.route('/delete_materias/<string:id>')
def borrar_materia(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM materias WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash("Se eliminó la materia exitosamente")
    return redirect(url_for('materias'))


# Aulas
@app.route('/aulas')
def aulas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM aulas')
    data = cur.fetchall()
    return render_template('aulas.html', aulas=data)

@app.route('/add_aula', methods=['POST'])
def add_aula():
    if request.method == 'POST':
        Nombre = request.form['Nombre']

        # Comprobar en la consola que se han ingresado esos datillos xd
        print(f"Nombre: {Nombre}")

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO aulas (Nombre) VALUES (%s)', (Nombre,))
        mysql.connection.commit()
        flash("Se agregó la aula exitosamente")
        return redirect(url_for('aulas'))


@app.route('/edit_aulas/<id>')
def get_aula(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM aulas WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('Edit_aulas.html', aula=data[0])

@app.route('/update_aula/<id>', methods=['POST'])
def update_aula(id):
    if request.method == 'POST':
        Nombre = request.form['Nombre']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE aulas
        SET Nombre = %s
        WHERE id = %s
        """, (Nombre, id))
        mysql.connection.commit()
        flash("la aula ha sido actualizada ;)")
        return redirect(url_for('aulas'))

@app.route('/delete_aulas/<string:id>')
def borrar_aula(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM aulas WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash("Se eliminó la aulas exitosamente")
    return redirect(url_for('aulas'))


@app.route('/calificaciones')
def calificaciones():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM calificaciones')
    calificaciones_data = cur.fetchall()

    #Para agarrarnos los del estudiante
    cur.execute('''
        SELECT estudiantes.id, personas.nombre, personas.apellido_p, personas.apellido_m, personas.matricula
        FROM estudiantes
        INNER JOIN personas ON estudiantes.persona_id = personas.id
        ORDER BY personas.nombre, personas.apellido_p, personas.apellido_m, personas.matricula
    ''')
    estudiantes_data = cur.fetchall()

    #Para agarrarnos los de la materia
    cur.execute('SELECT id, Nombre, Descripcion, Profesor_id FROM materias')
    materias_data = cur.fetchall()

    return render_template('calificaciones.html', calificaciones=calificaciones_data, estudiantes=estudiantes_data, materias=materias_data)

@app.route('/add_calificacion', methods=['POST'])
def add_calificacion():
    if request.method == 'POST':
        Estudiante_id = request.form['Estudiante_id']
        Materia_id = request.form['Materia_id']
        Fecha = request.form['Fecha']
        Calificacion = request.form['Calificacion']

        # Comprobar en la consola que se han ingresado esos datillos xd
        print(f"Estudiante_id: {Estudiante_id}, Materia_id: {Materia_id}, Fecha: {Fecha}, Calificacion: {Calificacion}")

        cur = mysql.connection.cursor()
        try:
            cur.execute('INSERT INTO calificaciones (Estudiante_id, Materia_id, Fecha, Calificacion) VALUES (%s, %s, %s, %s)',
                        (Estudiante_id, Materia_id, Fecha, Calificacion))
            mysql.connection.commit()
            flash("Se agregó la calificación exitosamente")
        except MySQLdb.IntegrityError as e:
            flash("Error al agregar la calificación. Verifique que el Estudiante y la Materia existan.")
            print(f"Error: {e}")
        return redirect(url_for('calificaciones'))

@app.route('/edit_calificaciones/<id>')
def get_calificacion(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM calificaciones WHERE id = %s', [id])
    calificacion = cur.fetchone()

    #Para agarrarnos los del estudiante again
    cur.execute('''
        SELECT estudiantes.id, personas.nombre, personas.apellido_p, personas.apellido_m, personas.matricula
        FROM estudiantes
        INNER JOIN personas ON estudiantes.persona_id = personas.id
        ORDER BY estudiantes.id, personas.nombre, personas.apellido_p, personas.apellido_m, personas.matricula
    ''')
    estudiantes = cur.fetchall()

    #Para agarrarnos los de la materia again
    cur.execute('SELECT id, Nombre, Descripcion, Profesor_id FROM materias')
    materias = cur.fetchall()

    return render_template('Edit_calificaciones.html', calificacion=calificacion, materias=materias, estudiantes=estudiantes)

@app.route('/update_calificacion/<id>', methods=['POST'])
def update_calificacion(id):
    if request.method == 'POST':
        Estudiante_id = request.form['Estudiante_id']
        Materia_id = request.form['Materia_id']
        Fecha = request.form['Fecha']
        Calificacion = request.form['Calificacion']

        cur = mysql.connection.cursor()
        try:
            cur.execute("""
            UPDATE calificaciones
            SET Estudiante_id = %s, Materia_id = %s, Fecha = %s, Calificacion = %s
            WHERE id = %s
            """, (Estudiante_id, Materia_id, Fecha, Calificacion, id))
            mysql.connection.commit()
            flash("La calificación ha sido actualizada ;)")
        except MySQLdb.IntegrityError as e:
            flash("Error al actualizar la calificación. Verifique que el Estudiante y la Materia existan.")
            print(f"Error: {e}")
        return redirect(url_for('calificaciones'))

@app.route('/delete_calificaciones/<string:id>')
def borrar_calificacion(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM calificaciones WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash("Se eliminó la calificación exitosamente")
    return redirect(url_for('calificaciones'))



# Horarios
@app.route('/horarios')
def horarios():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM horarios')
    horarios_data = cur.fetchall()

    cur.execute('''
        SELECT profesores.id, personas.nombre, personas.apellido_p, personas.apellido_m, profesores.Especialidad, profesores.Fecha_contratacion
        FROM profesores
        INNER JOIN personas ON profesores.persona_id = personas.id
        ORDER BY profesores.id, personas.nombre, personas.apellido_p, personas.apellido_m, profesores.Especialidad, profesores.Fecha_contratacion
    ''')
    profesores_data=cur.fetchall()

    cur.execute('SELECT id, Nombre, Descripcion, Profesor_id FROM materias')
    materias_data = cur.fetchall()

    cur.execute('SELECT id, Nombre FROM aulas')
    aulas_data = cur.fetchall()

    return render_template('horarios.html', horarios=horarios_data, profesores=profesores_data, materias=materias_data, aulas=aulas_data)

@app.route('/add_horario', methods=['POST'])
def add_horario():
    if request.method == 'POST':
        Profesor_id = request.form['Profesor_id']
        Materia_id = request.form['Materia_id']
        Aula_id = request.form['Aula_id']
        Dia = request.form['Dia']
        Hora_inicio = request.form['Hora_inicio']
        Hora_fin = request.form['Hora_fin']

        # Comprobar en la consola que se han ingresado esos datillos xd
        print(f"Profesor_id: {Profesor_id}, Materia_id: {Materia_id}, Aula_id: {Aula_id}, Dia: {Dia}, Hora_inicio: {Hora_inicio}, Hora_fin: {Hora_fin}")

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO horarios (Profesor_id, Materia_id, Aula_id, Dia, Hora_inicio, Hora_fin) VALUES (%s, %s, %s, %s, %s, %s)',
                    (Profesor_id, Materia_id, Aula_id, Dia, Hora_inicio, Hora_fin))
        mysql.connection.commit()
        flash("Se agregó el horario exitosamente")
        return redirect(url_for('horarios'))

@app.route('/edit_horarios/<id>')
def get_horario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM horarios WHERE id = %s', [id])
    horario = cur.fetchone()

    cur.execute('''
        SELECT profesores.id, personas.nombre, personas.apellido_p, personas.apellido_m, profesores.Especialidad, profesores.Fecha_contratacion
        FROM profesores
        INNER JOIN personas ON profesores.persona_id = personas.id
        ORDER BY profesores.id, personas.nombre, personas.apellido_p, personas.apellido_m, profesores.Especialidad, profesores.Fecha_contratacion
    ''')
    profesores = cur.fetchall()

    cur.execute('SELECT id, Nombre, Descripcion, Profesor_id FROM materias')
    materias = cur.fetchall()

    cur.execute('SELECT id, Nombre FROM aulas')
    aulas = cur.fetchall()


    return render_template('Edit_horarios.html', horario=horario, profesores=profesores, materias=materias, aulas=aulas)

@app.route('/update_horario/<id>', methods=['POST'])
def update_horario(id):
    if request.method == 'POST':
        Profesor_id = request.form['Profesor_id']
        Materia_id = request.form['Materia_id']
        Aula_id = request.form['Aula_id']
        Dia = request.form['Dia']
        Hora_inicio = request.form['Hora_inicio']
        Hora_fin = request.form['Hora_fin']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE horarios
        SET Profesor_id = %s, Materia_id = %s, Aula_id = %s, Dia = %s, Hora_inicio = %s, Hora_fin = %s
        WHERE id = %s
        """, (Profesor_id, Materia_id, Aula_id, Dia, Hora_inicio, Hora_fin, id))
        mysql.connection.commit()
        flash("El horario ha sido actualizado ;)")
        return redirect(url_for('horarios'))

@app.route('/delete_horarios/<string:id>')
def borrar_horario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM horarios WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash("Se eliminó el horario exitosamente")
    return redirect(url_for('horarios'))



# Materias-Estudiantes (Para asignarle las materias pues xd)
@app.route('/materias_estudiantes')
def materias_estudiantes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materias_estudiantes')
    materias_estudiantes_data = cur.fetchall()

    cur.execute('''
        SELECT estudiantes.id, personas.nombre, personas.apellido_p, personas.apellido_m, personas.matricula
        FROM estudiantes
        INNER JOIN personas ON estudiantes.persona_id = personas.id
        ORDER BY personas.nombre, personas.apellido_p, personas.apellido_m, personas.matricula
    ''')
    estudiantes_data = cur.fetchall()

    cur.execute('SELECT * FROM horarios')
    horarios_data = cur.fetchall()

    return render_template('materias_estudiantes.html', materias_estudiantes=materias_estudiantes_data, estudiantes=estudiantes_data, horarios=horarios_data)


@app.route('/add_materia_estudiante', methods=['POST'])
def add_materia_estudiante():
    if request.method == 'POST':
        Estudiante_id = request.form['Estudiante_id']
        Horario_id = request.form['Horario_id']

        # Comprobar en la consola que se han ingresado esos datillos xd
        print(f"Estudiante_id: {Estudiante_id}, Horario_id: {Horario_id}")

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO materias_estudiantes (Estudiante_id, Horario_id) VALUES (%s, %s)',
                    (Estudiante_id, Horario_id))
        mysql.connection.commit()
        flash("Se agregó materia-estudiante exitosamente")
        return redirect(url_for('materias_estudiantes'))

@app.route('/edit_materias_estudiantes/<id>')
def get_materia_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materias_estudiantes WHERE id = %s', [id])
    materia_estudiante = cur.fetchone()

    cur.execute('''
        SELECT estudiantes.id, personas.nombre, personas.apellido_p, personas.apellido_m, personas.matricula
        FROM estudiantes
        INNER JOIN personas ON estudiantes.persona_id = personas.id
        ORDER BY estudiantes.id, personas.nombre, personas.apellido_p, personas.apellido_m, personas.matricula
    ''')
    estudiantes = cur.fetchall()

    cur.execute('SELECT id, Profesor_id, Materia_id, Aula_id, Dia, Hora_inicio, Hora_fin FROM horarios')
    horarios = cur.fetchall()

    return render_template('Edit_materias_estudiantes.html', materia_estudiante=materia_estudiante, estudiantes=estudiantes, horarios=horarios)

@app.route('/update_materia_estudiante/<id>', methods=['POST'])
def update_materia_estudiante(id):
    if request.method == 'POST':
        Estudiante_id = request.form['Estudiante_id']
        Horario_id = request.form['Horario_id']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE materias_estudiantes
        SET Estudiante_id = %s, Horario_id = %s
        WHERE id = %s
        """, (Estudiante_id, Horario_id, id))
        mysql.connection.commit()
        flash("materia-estudiante ha sido actualizado ;)")
        return redirect(url_for('materias_estudiantes'))

@app.route('/delete_materias_estudiantes/<string:id>')
def borrar_materia_estudiante(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM materias_estudiantes WHERE id={0}'.format(id))
    mysql.connection.commit()
    flash("Se eliminó materia-estudiante exitosamente")
    return redirect(url_for('materias_estudiantes'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)