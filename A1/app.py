from flask import Flask,render_template,request,redirect,session
from pymongo import MongoClient
client=MongoClient('127.0.0.1',27017)
db=client['shri']
c=db['flaskapp']
app=Flask(__name__)
app.secret_key='shri1234'
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')


@app.route('/dashboard')
def dashboardpage():
    owner=session['username']
    return render_template('dashboard.html',owner=owner)


@app.route('/formdata',methods=['post'])
def formdata():
    name=request.form['name']
    email=request.form['email']
    phone=request.form['phone']
    password=request.form['password']
    print(name,email,phone,password)

    data=[]
    for i in c.find():
        if i['phone']==phone:
            return render_template('index.html',err='you have already registered')
    k={}
    k['name']=name
    k['email']=email
    k['phone']=phone
    k['password']=password
    c.insert_one(k)
    return render_template('index.html',res='you have registered successfully')

@app.route('/logindata',methods=['post'])
def logindata():
    phone=request.form['phone']
    password=request.form['password']
    print(phone,password)
    for i in c.find():
        if i['phone']==phone and i['password']==password:
            session['username']=phone
            return redirect('/dashboard')
            return render_template('login.html',res1='valid credentials')
    return render_template('login.html',err1='invalid credentials')

@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/')

@app.route('/viewnotes')
def viewnotes():
    c1=db['notes']
    data=[]
    for i in c1.find():
        if i['owner']==session['username']:
            data.append(i['notes'])
    print(data)
    return render_template('viewnotes.html',data=data,l=len(data))

@app.route('/insertnotes')
def insert():
    return render_template('insertnotes.html')

@app.route('/insertnotesdata',methods=['post'])
def insertnotesdata():
    notes=request.form['notes']
    owner=session['username']
    print(notes,owner)
    c1=db['notes']
    k={}
    k['owner']=owner
    k['notes']=notes
    c1.insert_one(k)
    return render_template('insertnotes.html',res2='notes saved')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)