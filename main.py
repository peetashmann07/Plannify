from flask import Flask, render_template, request, session, redirect
import json
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

p = open('data.json')
data = json.load(p)
new = open('weekly.json')
data_pending  = json.load(new)
names = []
usernames = []
passwords = []
week_maths = []
week_sci = []
week_sst = []
week_eng = []
types = []
child_name = []
attendance_monthly = []
attendance_yearly = []
transport = []
avg_transport = []
monthlyp = []
hw = []
yearly = []
target = []
achieved = []

for i in data['students']:
    passwords.append(i['password'])
    usernames.append(i['username'])
    types.append(i['type'])
    names.append(i['name'])
    if i['type'] == 'parent':
        attendance_monthly.append(i['attendance_monthly'])
        attendance_yearly.append(i['attendance_yearly'])
        transport.append(i['transport'])
        avg_transport.append(i['average_t'])
        monthlyp.append(i['monthly_p'])
        hw.append(i['hw'])
        yearly.append(i['yearly'])
        target.append(i['target'])
        achieved.append(i['achievied'])
@app.route('/studenthome')
def home():
    if not session.get('verified'):
        return redirect('/login', code=302)
    
    else:
        if types[session['number']] == 'student':
            return render_template('index.html',name=session['name'])
        elif types[session['number']] == 'teacher':
            return redirect('/adminhome',code=302)
        elif types[session['number']] == 'parent':
            return redirect('/parenthome', code=302)
@app.route('/parenthome')
def parenthome():
    if not session.get('verified'):
        return redirect('/login', code=302)
    
    else:
        if types[session['number']] == 'student':
            return redirect('/studenthome', code=302)
        elif types[session['number']] == 'teacher':
            return redirect('/adminhome',code=302)
        elif types[session['number']] == 'parent':
            session['am'] = int(attendance_monthly[0])*3
            session['am_a'] = 100 - session['am'] 
            session['ay'] = int(attendance_yearly[0])
            session['ay_a'] = 100 - int(session['ay'])
            session['transport'] = transport[0]
            session['avg_t'] = list(avg_transport[0].split(','))
            session['hw'] = hw[0]
            session['hw_p'] = 100 - int(session['hw'])
            session['monthly_p'] = list(monthlyp[0].split(','))
            session['yearly'] = list(yearly[0].split(','))
            session['target'] = list(target[0].split(','))
            session['achieved'] = list(achieved[0].split(','))
            print(session['transport'])
            return render_template('parent_home.html')
@app.route('/adminhome')
def admin():
    if not session.get('verified'):
        return redirect('/login', code=302)
    
    else:
        if types[session['number']] == 'student':
            return redirect('/studenthome', code=302)
        elif types[session['number']] == 'teacher':
            return render_template('admin.html')
        elif types[session['number']] == 'parent':
            return redirect('/parenthome',code=302)
@app.route('/login', methods=['POST', 'GET'])
def login():
    c = 1
    session['subjects'] = []
    session['week_science'] = []
    session['week_maths'] = []
    session['week_sst'] = []
    session['week_english'] = []
    session['username'] = None
    session['incorrect_username'] = False
    session['incorrect_pass'] = False
    if request.method == 'POST':
        session['username'] = request.form.get("username")
        session['password'] = request.form.get('password')
        session['verified'] = None
        if type(session['username']) == str:
            if session['username'] in usernames:
                print('Username exists')
                session['number'] = usernames.index(session['username'])
                if session['password'] == passwords[session['number']]: 
                    print("Correct Information, Redirecting")
                    session['verified'] = True
                    session['name'] = names[session['number']]
                    for x in data['students']:
                        if session['name'] == x['name']:
                            for y in x['weekly_test_marks']:
                                for z in y['science']:
                                    session['week_science'].append(z)
                                    if z == ",":
                                        session['week_science'].remove(',')

                                for z in y['maths']:
                                    session['week_maths'].append(z)
                                    if z == ",":
                                        session['week_maths'].remove(',')
                    

                                for z in y['social_science']:
                                    session['week_sst'].append(z)
                                    if z == ",":
                                        session['week_sst'].remove(',')
                    

                                for z in y['english']:
                                    session['week_english'].append(z)
                                    if z == ",":
                                        session['week_english'].remove(',')
                    session['week_english_final'] = [eval(h) for h  in session['week_english']]
                    session['week_science_final'] = [eval(j) for j  in session['week_science']]
                    session['week_sst_final'] = [eval(ch) for ch in session['week_sst']]
                    session['week_maths_final'] = [eval(k) for k in session['week_maths']]
                    session['week_full'] = session['week_science_final'][-1] + session['week_english_final'][-1] + session['week_sst_final'][-1] + session['week_maths_final'][-1]
                    if types[session['number']] == 'student':
                        return redirect('/studenthome', code=302)
                    if types[session['number']] == 'parent':
                        return redirect('/parenthome', code=302)
                    if types[session['number']] == 'teacher':
                        return redirect('/adminhome', code=302)
                else:
                    print('Incorrect pass')
                    session['incorrect_pass'] = True
                    return render_template('login.html', incorrect_pass=session['incorrect_pass'])
            else: 
                session['incorrect_username'] = True
                print(session['incorrect_username'])
                return render_template('login.html', username=session['incorrect_username'])
    return render_template('login.html')


@app.route('/maps')
def maps():
    return render_template('map-google.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('404-page.html')
if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0")