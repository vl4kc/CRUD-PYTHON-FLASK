from flask import Flask,render_template
import os

#para encontrar la ruta absoluta donde se encuentra el archivo
teamplade_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__))) #para extraer la ubicacion de arcivo padre de la aplicación que seria la carpeta principal del proyecto
teamplade_dir = os.path.join(teamplade_dir,'src' ,'templates') #combinamos la ruta templade_dir con src\teamplates

#creacion de la instancia Flask
app = Flask(__name__, template_folder= teamplade_dir)


#ruta de la aplicación
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)