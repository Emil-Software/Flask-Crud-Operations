from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/data.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


@app.route('/')
def home():
    users=User.query.all()
    return render_template('index.html',userList=users)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method =='POST':
        user = User(username=request.form['username'],email = request.form['email'])
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    user=User.query.get(id) #select * from User where id=2
    db.session.delete(user) # delete from User where id=2
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
  
    user=User.query.get(id)
    if request.method=='POST':
        
        newUsername=request.form['username']
        newEmail=request.form['email']
        user.username=newUsername
        user.email = newEmail
        db.session.merge(user) # update table User set username='' and email='' where id=1
        db.session.flush()
        db.session.commit()
        return redirect('/')
    else:
       
        return render_template('update.html',user=user)



if __name__ == '__main__':

    app.run(debug=True)
