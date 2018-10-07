from flask import Flask,render_template,url_for,flash,redirect, request
from queries_1 import *

app = Flask(__name__)

global usn_epic
global sem_epic

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

#create_db()		#IT'S DONE, DO NOT RE-EXECUTE:	only to be executed once, be careful!!!!! 

@app.route("/")
def home():
	return render_template('home.html')

@app.route("/login",methods=['POST','GET'])
def login():
	return render_template('login.html',title='Login')

@app.route("/register",methods=['POST','GET'])
def register():   
		return render_template('register1.html',title='Register')

@app.route("/details",methods=['POST','GET'])
def details():
	return render_template('additional.html',title='Details')

#entering the record of a new student
@app.route("/registerform", methods = ['POST', 'GET'])			#from register1.html
def insert_new_stud():

	if(request.method == 'POST'):
		usn = request.form['usn']
		sem = request.form['sem']
		email = request.form['email']
		pswd = request.form['confirm_password']

		insert_entry(usn, sem, email, pswd)

		return render_template('login.html')

#verifying the login function
@app.route("/loginform", methods = ['POST', 'GET'])				#from login.html
def check_credentials():

	if(request.method == 'POST'):
		usn1 = request.form['usn1']
		pswd1 = request.form['password1']

		chk = check_password(usn1,pswd1)

		if(chk == 'valid'):
			usn_epic = usn1
			sem_epic = obtain_sem(usn_epic)

			return render_template('home.html')
		elif(chk == 'invalid'):
			flash('Incorrect password, Re-Enter')
			return render_template('additional.html')
		else:
			flash('Account does not exist, register now!')
			return render_template('register1.html')		#might have to change this, direct reference


@app.route("/additionalform", methods = ['POST', 'GET'])	#from additiponal.html
def insert_additional():

	if(request.method == 'POST'):
		cgpa = request.form['cgpa']
		code = request.form['coding']
		hckr = request.form['hackerrank']
		clbsts = request.form['membership_status']
		proj = request.form['projects']
		new_sem = request.form['update_sem']

		cur_status = exist_check(usn_epic)
		if(cur_status):
			insert_truepot(usn_epic, cgpa, code, hckr, clbsts, proj, new_sem)
		else:
			update_truepot(usn_epic, cgpa, code, hckr, clbsts, proj, new_sem)

		return render_template('main_page.html')		#same page rendering, lets see what happens

@app.route("/from_the_subject_page", methods = ['POST', 'GET'])			#URL redirection to be changed and maybe copied 8 times.LETS see!
def insert_marks():

	if(request.method == 'POST'):
		usn = usn_epic
		semester = sem_epic	#has to be defined, and the further names have to be defined that way too
		sub_1 = request.form['sub_1']
		sub_2 = request.form['sub_2']
		sub_3 = request.form['sub_3']
		sub_4 = request.form['sub_4']
		sub_5 = request.form['sub_5']
		sub_6 = request.form['sub_6']
		internal_status = request.form['latest_internal']
		target = request.form['target']
		credit_seq = request.form['creditsq']

		#search if record already exists, if YES then update, else 
		if(internal_status == 1):
			insert_student_marks(usn,semester,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,credit_seq)
		else:
			update_marks(usn,semester,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,credit_seq)

		return render_template('main_page.html')		#or additional.html, lets see.


@app.route("/update_sem1", methods = ['POST', 'GET'])
def update_stud_sem():

	if(request.method == 'POST'):
		semester = request.form['update_sem']

		update_semester(usn_epic, semester)

if __name__ == '__main__':
	app.run(debug=True)