from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app=Flask(__name__)

#Mysqlconnection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '110717'
app.config['MYSQL_DB'] = 'escuela'
app.config['MYSQL_PORT'] = 3306
mysql =MySQL(app)

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
    data = cur.fetchall()
    print(data)
    return render_template('Estudiantes.html', estudiantes=data)


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
    data = cur.fetchall()
    return render_template('Edit_estudiantes.html', estudiante=data[0])


@app.route('/update_estudiante/<id>', methods=['POST'])
def update_estudiante(id):
    if request.method == 'POST':
        # Print the received form data
        print(request.form)

        # Extract form data
        persona_id = request.form['persona_id']
        Grado = request.form['Grado']
        Grupo = request.form['Grupo']
        Fecha_registro = request.form['Fecha_registro']

        # Update the database
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
    data = cur.fetchall()
    return render_template('profesores.html', profesores=data)

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
    data = cur.fetchall()
    return render_template('Edit_profesores.html', profesor=data[0])

@app.route('/update_profesor/<id>', methods=['POST'])
def update_profesor(id):
    if request.method == 'POST':
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
    data = cur.fetchall()
    return render_template('materias.html', materias=data)

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
    data = cur.fetchall()
    return render_template('Edit_materias.html', materia=data[0])

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







if __name__ == '__main__':
    app.run(port=5000, debug=True)