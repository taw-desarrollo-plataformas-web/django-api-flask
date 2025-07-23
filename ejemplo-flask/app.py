from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'una-clave-secreta-000001'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/los/estudiantes")
def los_estudiantes():
    """
    """
    r = requests.get("http://localhost:8000/api/estudiantes/",
            auth=('reroes', '1'))
    print("---------------------")
    print(r.content)
    print("---------------------")
    estudiantes = json.loads(r.content)['results']

    numero_estudiantes = json.loads(r.content)['count']
    return render_template("losestudiantes.html", estudiantes=estudiantes,
    numero_estudiantes=numero_estudiantes)


@app.route("/los/telefonos")
def los_telefonos():
    """
    """
    r = requests.get("http://localhost:8000/api/numerosts/",
            auth=('reroes', '1'))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    return render_template("lostelefonos.html", datos=datos,
    numero=numero)


@app.route("/los/telefonos/dos")
def los_telefonos_dos():
    """
    """
    r = requests.get("http://localhost:8000/api/numerosts/",
            auth=('reroes', '1'))
    datos = json.loads(r.content)['results']
    numero = json.loads(r.content)['count']
    datos2 = []
    for d in datos:
        datos2.append(

        {
        'telefono':d['telefono'],
        'tipo':d['tipo'],
        'estudiante': obtener_estudiante(d['estudiante'])}
        # http://127.0.0.1:8000/api/estudiantes/4/
        # René
        )
    return render_template("lostelefonosdos.html", datos=datos2,
    numero=numero)

# funciones ayuda

def obtener_estudiante(url):
    """
    http://127.0.0.1:8000/api/estudiantes/4/
    """
    r = requests.get(url, auth=('reroes', '1'))
    nombre_estudiante = json.loads(r.content)['nombre']
    return nombre_estudiante

@app.route("/crear_estudiante", methods=['GET', 'POST'])
def agregar_estudiante():
    """
    """
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        correo = request.form['correo']

        # Datos a enviar a la API de Django
        estudiante_data = {
            'nombre': nombre,
            'apellido': apellido,
            'cedula': cedula,
            'correo': correo
        }

        

        # Realizar la petición POST a la API de Django
        r = requests.post("http://localhost:8000/api/estudiantes/",
                              json=estudiante_data, # 'json' serializa el diccionario a JSON automáticamente
                              auth=('reroes', '1'))


        print(f"Status Code (Crear Estudiante): {r.status_code}")
        # Si todo fue bien (código 201 Created), la API devuelve el objeto creado
        nuevo_estudiante = json.loads(r.content)
        flash(f"Estudiante '{nuevo_estudiante['nombre']} {nuevo_estudiante['apellido']}' creado exitosamente!", 'success')
        return redirect(url_for('los_estudiantes')) # Redirigir a la lista de estudiantes

    # Si es una petición GET o si hubo un error en POST, muestra el formulario
    return render_template("crear_estudiante.html")

@app.route("/crear_numero_telefonico", methods=['GET', 'POST'])
def crear_numero_telefonico():
    """
    """
    estudiantes_disponibles = []

    r_estudiantes = requests.get("http://localhost:8000/api/estudiantes/", auth=('reroes', '1'))
    estudiantes_disponibles = json.loads(r_estudiantes.content)['results']

    if request.method == 'POST':
        telefono = request.form['telefono']
        tipo = request.form['tipo']

        estudiante_url = request.form['estudiante']

        numero_telefonico_data = {
            'telefono': telefono,
            'tipo': tipo,
            'estudiante': estudiante_url # Enviamos la URL del estudiante
        }

        r = requests.post("http://localhost:8000/api/numerosts/",
                              json=numero_telefonico_data,
                              auth=('reroes', '1'))

        print(f"Status Code (Crear Número): {r.status_code}")

        nuevo_numero = json.loads(r.content)
        flash(f"Número '{nuevo_numero['telefono']}' creado exitosamente para el estudiante!", 'success')
        return redirect(url_for('los_estudiantes')) # Redirigir a la lista principal o a una de números

    return render_template("crear_numero_telefonico.html",
                           estudiantes=estudiantes_disponibles,
                           )


if __name__ == "__main__":
    app.run(debug=True)
