from flask import Flask, render_templates

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_templates("inicio.html")

@app.route("/quienes-somos")
def quienes_somos():
    return render_templates("quienes.html")

@app.route("/servicios")
def servicios():
    return render_templates("servicios.html")

@app.route("/proyectos")
def proyectos():
    return render_templates("proyectos.html")

@app.route("/contactos")
def contactos():
    return render_template("contactos.html")

if __name__ == "__main__":
    app.run(debug=True)
