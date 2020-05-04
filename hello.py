from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/waterplant')
def waterPlant():
    return "You have accessed waterplant"
@app.route('/airhumidity')
def getAirHumidity():
    return "You have accessed air humidity"
@app.route('/airtemperature')
def getAirTemp():
    return "You have accessed air temperature"
@app.route('/viewcamera')
def viewCameraFeed():
    return render_template("camera.html")
if __name__ == "__main__":
    app.run(debug=True)