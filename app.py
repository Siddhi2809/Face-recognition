from flask import Flask, render_template, redirect, url_for, request, jsonify, session
import attendance;
from flask_login import LoginManager, login_user, login_required, logout_user
import database
from datetime import datetime;
from werkzeug.utils import secure_filename;
import os

upload_folder = 'Raw_Dataset_Train'
allowed_extensions = set(['png','jpg','jpeg'])
    
app = Flask(__name__)
app.config['upload_folder'] = upload_folder
app.secret_key = 'FRAMS'   # Change this to a secure random key
login_manager = LoginManager()
login_manager.init_app(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def main_page():
    return render_template("index.html")

users = database.get_all_users()
# User loader function required by Flask-Login
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None  # return None if user is not found

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        userid = request.form['username']
        password = request.form['password']

        for user in users:
            if user.id == int(userid):
                if user and user.name == password:
                    login_user(user)
                    if user.type == 'User':
                        print("In the user")
                        session['user_name'] = user.password
                        session['user_id'] = userid
                        return redirect(url_for('dashboard', user_id=userid, user_name=user.password))
                    elif user.type == 'Admin':
                        print("In the admin")
                        session['user_name'] = user.password
                        session['user_id'] = userid
                        return redirect(url_for('admindash', user_id=userid, user_name=user.password))
                else:
                    return render_template('login.html', error="Invalid Credentials")

    return render_template('login.html')
        
@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)  # Remove username from session
    session.pop('user_name', None)
    print(session)
    logout_user() 
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
@login_required
def register():
    if request.method == "POST":
        user_id = request.form['userid']
        name = request.form['username']
        password = request.form['password']
        cpassword = request.form['cpassword']

        if password == cpassword:
            database.generate_new_user(user_id, password, name)
        
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_name = session['user_name']
        records = database.get_all_entries_by_user_id(user_id)
        return render_template('dashboard.html', user_id=user_id, user_name=user_name, records = records)
    else:
        return redirect(url_for('login'))

@app.route('/filter_records', methods=['POST'])
@login_required
def filter_records():
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')

    # Convert date strings to datetime objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Get records between the two dates
    filtered_records = database.get_records_between_dates(user_id, start_date, end_date)

    return render_template('filtered_records.html', user_id=user_id, user_name=user_name, records=filtered_records, s = start_date.date(), e = end_date.date())

@app.route('/admindash')
@login_required
def admindash():
    if 'user_id' in session:
        user_id = session['user_id']
        user_name = session['user_name']
        return render_template('admindash.html', user_id=user_id, user_name=user_name)
    else:
        return redirect(url_for('login'))

@app.route("/alldata")
@login_required
def alldata():
    user_id = session['user_id']
    user_name = session['user_name']

    records = database.get_all_attendance_records()

    return render_template('alldata.html', user_id=user_id, user_name=user_name, records = records)
        
@app.route("/dataofprticularemployee", methods = ['GET', 'POST'])
@login_required
def dataofprticularemployee():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user_name = request.form.get('user_name')

        user_id_emp = request.form.get('id')
        records = database.get_all_entries_by_user_id(user_id_emp)

        return render_template('dataofprticularemployee.html', user_id=user_id, user_name=user_name, records = records, id = user_id_emp)
   
@app.route("/addImage", methods=['POST'])
@login_required
def addImage():
    if 'file' not in request.files:
        return jsonify({'Error': 'Media not provided'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'Error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['upload_folder'], filename))
        return jsonify({'success': True, 'msg': 'Image uploaded successfully'})
    return jsonify({'Error': 'Invalid file format'}), 400

@app.route('/check_in', methods=['POST'])
def check_in():
    user_id = request.args.get('user_id')
    name = request.args.get('user_name')
    attendance.markCheckInAttendances(user_id, name)
    return jsonify({"message": 'Check In Attendance marked successfully'})

@app.route('/check_out', methods=['POST'])
def check_out():
    user_id = request.args.get('user_id')
    name = request.args.get('user_name')
    attendance.markCheckOutAttendances(user_id, name)
    return jsonify({"message": 'Check Out Attendance marked successfully'})
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)