from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')

# configuring database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'

db = SQLAlchemy(app)

# User model

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(200))
    password = db.Column(db.String(10))
    
    
    def __init__(self, username, email, password, confirm_password):
        self.username = username
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
    
    
    def __repr__(self):
        return f'<Member {self.username}>'

# Create all tables
with app.app_context():
    db.create_all()

# home route

@app.route('/')

def home():
    # retrive all the members 
    members = Member.query.all()
    
    return render_template('home.html', members=members)


@app.route('/signup', methods=['GET','POST'])
def signup_page():
    
    if request.method == 'POST':
        
        if not request.form['username']:
            flash('Please enter your username')
            return redirect(url_for('signup_page'))
        else:
            # username = request.form['username']
            # email = request.form['email']
            # password = request.form['password']
            # confirm_password= request.form['confirm_password']
            
            member = Member(request.form['username'], request.form['email'], request.form['password'], request.form['confirm_password'])
            
            db.session.add(member)
            db.session.commit()
        # Further processing
            return redirect(url_for('home'))
    return render_template('signup.html',)
  
# Delete member 
@app.route('/delete/<int:id>')
def delete(id):
    member = Member.query.get(id)
    db.session.delete(member)
    db.session.commit()
    
    return redirect(url_for('home'))


# update member

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Member.query.get(id)
    
    if request.method == 'POST':
        member.username = request.form['username']
        member.email = request.form['email']
        member.password = request.form['password']
        
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template('edit.html', member=member)

if __name__ == '__main__':
  
    app.run(debug=True)
    