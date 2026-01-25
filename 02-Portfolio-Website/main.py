from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/projects")
def projects():
    return render_template("projects.html")

@app.get("/certificates")
def certificates():
    return render_template("certificates.html")


if __name__ == "__main__":
    app.run(debug=True)
