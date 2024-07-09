from flask import Flask, render_template, request, redirect , url_for

import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM usuarios")
    miResultado = cursor.fetchall()
    
    insertarObjectos = [] 
    nombreDeColumnas = [columna[0] for columna in cursor.description]
    
    for unRegistro in miResultado:
         insertarObjectos.append(dict(zip(nombreDeColumnas, unRegistro)))
      
    cursor.close()
    return render_template('index.html', data=insertarObjectos)

@app.route('/usuarios', methods=['POST'])
def addUser():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    usuario = request.form['usuario']
    

    if nombre and apellido and email and usuario:
       cursor = db.database.cursor()
       sql = "INSERT INTO usuarios ( nombre, apellido, email, usuario) VALUES ( %s, %s, %s, %s)"
       data = (nombre, apellido, email, usuario)
       cursor.execute(sql, data)
       db.database.commit()
    return redirect(url_for('home'))

@app.route('/eliminar/<string:id>')
def eliminar(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM usuarios WHERE id= %s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/editar/<string:id>', methods=['POST'])
def edit(id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    usuario = request.form['usuario']

    if nombre and apellido and email and usuario:
        cursor = db.database.cursor()
        sql = "UPDATE usuarios SET nombre = %s, apellido = %s, email = %s, usuario = %s WHERE id = %s"
        data = (nombre, apellido, email, usuario, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))



#puerto
if __name__ == '__main__':
    app.run(debug=True, port=4000)

