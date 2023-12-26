from flask import Flask, render_template
import sqlite3
import socket

app = Flask(__name__)

def get_worker_data():
    conn = sqlite3.connect('hospital.db')  
    cursor = conn.cursor()
    cursor.execute('SELECT name, surname, floor, room_num FROM patients')
    data = cursor.fetchall()

    print(data)
    conn.close()
    return data

@app.route('/')
def display_workers():
    worker_data = get_worker_data()
    return render_template('./index.html', patients=worker_data)

if __name__ == '__main__':
    ip = socket.gethostbyname(socket.gethostname())
    app.run(host=ip, port=80, debug=True)
