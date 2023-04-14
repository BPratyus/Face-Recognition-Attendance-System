from flask import *
from distutils.log import debug
from fileinput import filename
import csv

app = Flask(__name__)

@app.route('/')
def index():
    # Read the CSV file
    with open('Attendance.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    # Render the template with the data
    return render_template('./index.html', data=data)

@app.route('/download')
def download():
    # Return the CSV file as a download attachment
    return send_file('Attendance.csv', as_attachment=True)

@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        return redirect(request.referrer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
