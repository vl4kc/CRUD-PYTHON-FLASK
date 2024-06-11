from flask import Flask,render_template,redirect,request,url_for
import os
import database as db

#para encontrar la ruta absoluta donde se encuentra el archivo
teamplade_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) #para extraer la ubicacion de arcivo padre de la aplicación que seria la carpeta principal del proyecto
teamplade_dir = os.path.join(teamplade_dir,'src' ,'templates') #combinamos la ruta templade_dir con src\teamplates

#creacion de la instancia Flask
app = Flask(__name__, template_folder= teamplade_dir)


#ruta de la aplicación
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute('SELECT * FROM user')#ejecuta una consulta SQL que obtiene todo los datos que esta en la tabla user
    myresult = cursor.fetchall()#recupera los datos de la consulta y lo almacena en la variable myresult
    #Convertir los datos a diccionario
    insertObject = [] #creamos el diccionario donde se guardaran los datos
    columName = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columName, record)))
    cursor.close()
    return render_template('index.html', data= insertObject)

#Ruta para guradar usuarios en la bd
@app.route('/user', methods = ['post'])
def addUser():
    
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']

    if username and name and password:
        cursor = db.database.cursor()
        sql = 'INSERT INTO USER (username, name, password) VALUES (%s,%s,%s)'
        data = (username, name, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

#Ruta para editar usuarios en la bd
@app.route('/edit/<string:id>', methods=['post'])
def edit(id):
    #extraemos el valor del campo del formulario 
    username = request.form['username'] 
    name = request.form['name']
    password = request.form['password']

    #evaluamos que username, name y password no estén vacías
    if username and name and password:
        cursor = db.database.cursor()
        sql = 'UPDATE user SET username = %s, name = %s, password = %s WHERE id = %s'
        data = (username,name,password,id)
    else:
        sql = "UPDATE user SET username = %s, name = %s, password = %s WHERE id = %s"
        data = (username, name, password, id)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

#Ruta para eliminar usuario en la bd
@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = 'DELETE FROM user WHERE id=%s'
    data = (id,)
    cursor.execute(sql,data)
    db.database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)