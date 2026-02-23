from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')

@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

@app.route('/quienes')
def quienes():
    return render_template('quienes.html')

if __name__ == '__main__':
    app.run(debug=True)
