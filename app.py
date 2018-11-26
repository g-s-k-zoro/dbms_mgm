from flask import Flask,render_template,url_for,flash,redirect, request
from queries_1 import *
import matplotlib.pyplot as plt

app = Flask(__name__)

#__________________Global variables_______________
usn_epic = None
sem_epic = 0
internal_status = None
target = None
arr = []
N = None
for_company_gpa = []
for_company_internal = []
flag1 = 0
#____________________Global variable ends___________________

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#__________________________________________________________________________
#IT'S DONE, DO NOT RE-EXECUTE:	only to be executed once, be careful!!!!!
#remove_func()
#create_db() 
#temp_placement()		#one time execution
#create_company_view()
# dele_details()
#create_trigger()
#alter_tables();
#drop_everything()
#select_regist()
#__________________________________________________________________________
print_additional()
def true_score(cgpa, code, hckr, clbsts, proj):
	return ((7*cgpa + 3*code + 2*hckr + 3*clbsts + 5*proj)*1.0)/20

def get_values():
	data, n = sorted_score()
	base_rating = 600
	avg_rating = (base_rating - (n+1) - 2)
	r = 1
	dat1 = []
	for row in data:
		nf = float(avg_rating*1.0*((base_rating - (r-1)*2) - avg_rating)/(base_rating - (r-1)*2))
		print(row[0])
		temp = row[1]
		temp = float(temp)
		temp = temp*nf
		dat1.append([row[0], temp])
		r+=1

	return dat1

#function for taking in the data from subject page from different sems
def sem_intake(sem_no):
	global usn_epic
	global sem_epic
	global internal_status
	global target
	global flag
	global arr
	usn = usn_epic
	print(usn)
	print(sem_epic)
	semester = int(sem_epic)	#has to be defined, and the further names have to be defined that way too
	sub_1 = request.form['1']
	sub_2 = request.form['2']
	sub_3 = request.form['3']
	sub_4 = request.form['4']
	sub_5 = request.form['5']
	sub_6 = request.form['6']
	internal_status = request.form['latest_internal']
	target = request.form['target']
	target=float(target)
	#credit_seq = '344444'#request.form['creditsq']	#instead it should be manually inserted
	#attend = request.form['attendance']	#lets see what to do about this
	#search if record already exists, if YES then update, else

	if(semester == 1):				#credit sequence for different sems
		credit_seq = "444442"
	elif(semester == 2):
		credit_seq = "444442"
	elif(semester == 3):
		credit_seq = "444443"
	elif(semester == 4):
		credit_seq = "444443"
	elif(semester == 5):
		credit_seq = "544344"
	elif(semester == 6):
		credit_seq = "454433"
	elif(semester == 7):
		credit_seq = "454333"

	sub_1 = float(sub_1)
	print("subj1 marks",sub_1)
	sub_2 = float(sub_2)
	sub_3 = float(sub_3)
	sub_4 = float(sub_4)
	sub_5 = float(sub_5)
	sub_6 = float(sub_6)
	internal_status = int(internal_status)
	#select_marks()
	chk_bit = chk_usn(usn)
	if(internal_status == 1 and chk_bit == 0):
		flag = 1
		insert_student_marks(usn,semester,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,credit_seq)
	else:
	 	data = get_marks(usn)
	 	if(internal_status == 1):
	 		update_marks(usn,semester,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,credit_seq)
	 	elif(internal_status == 2):
	 		arr = max_min(usn,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6)
	 		update_marks(usn,semester,(sub_1+data[0][2])/2,(sub_2+data[0][3])/2,(sub_3+data[0][4])/2,(sub_4+data[0][5])/2,(sub_5+data[0][6])/2,(sub_6+data[0][7])/2,credit_seq)
	 	elif(internal_status == 3):
	 		update_marks(usn,semester,sub_1,sub_2,sub_3,sub_4,sub_5,sub_6,credit_seq)

	return internal_status, target


#function for plotting the overall target goal-graph
def graph_plot(internal_status = 99, target = 99):
	global usn_epic
	global arr
	global for_company_gpa
	global for_company_internal
	global flag1
	data = plot_graph(usn_epic)
	internal = [1,2,3,4]
	gpa = []
	print("This is data")
	print(data)
	credits = data[0][8]
	sum1 = int(credits[0])*data[0][2]+int(credits[1])*data[0][3]+int(credits[2])*data[0][4]+int(credits[3])*data[0][5]+int(credits[4])*data[0][6]+int(credits[5])*data[0][7]
	denom = int(credits[0])+int(credits[1])+int(credits[2])+int(credits[3])+int(credits[4])+int(credits[5])
	sum1 = float(sum1)
	sum1 = sum1*10.0/(denom*25.0)
	if(internal_status!=3):
		for i in range(internal_status):
			gpa.append(sum1)
	else:
		data1 = great_two(usn_epic)
		sum1 = int(credits[0])*data1[0]+int(credits[1])*data1[1]+int(credits[2])*data1[2]+int(credits[3])*data1[3]+int(credits[4])*data1[4]+int(credits[5])*data1[5]
		sum1 = sum1*10.00/(denom*25.0)
		gpa.append(sum1)
		gpa.append(sum1)
		gpa.append(sum1)
		print("this is data gp")
		print(gpa)
		print(data1[0])
		print(data1[0],data1[1],data1[2],data1[3],data1[4],data1[5])
		print(gpa)

	rem = 4-internal_status

	if(sum1<target):
		delta = float(1.0*target-sum1)
		if(rem == 3):
			gpa.append(target+(1.0*delta/3))
			gpa.append(target-(1.0*delta/3))
			gpa.append(target)
		elif(rem == 2):
			sum1 = int(credits[0])*arr[0]+int(credits[1])*arr[1]+int(credits[2])*arr[2]+int(credits[3])*arr[3]+int(credits[4])*arr[4]+int(credits[5])*arr[5]
			sum1=(sum1*10.0)/(denom*25.0)
			delta = target - sum1
			if(sum1<target):
				if(target+delta<=10):
					gpa.append(target+(delta))
					gpa.append(target)
				else:
					gpa.append(target+(delta*2.0/3))
					gpa.append(target+(delta/3.0))
			else:
				gpa.append(target+.05)
				gpa.append(target-.05)

		elif(rem == 1):
			if(target+delta	<=10):
				gpa.append(target+delta)
			else:
				gpa.append(15)			#make this colour change to denote impossibility

	else:
		delta = sum1-target
		if(rem == 3):
			gpa.append(target-.05)
			gpa.append(target+.15)
			gpa.append(target-.05)
		elif(rem == 2):
			gpa.append(target+.05)
			gpa.append(target-.05)
		elif(rem == 1):
			gpa.append(target+.05)
	for_company_internal.append(0)
	for_company_gpa.append(0)
	for i in internal:
		for_company_internal.append(i)
	for i in gpa:
		for_company_gpa.append(i)
	print(internal)
	print(gpa)
	print(for_company_internal)
	print(for_company_gpa)
	#flag = 0
	for i in gpa:
		if i>10:
			flag1 = 1
			break
		else:
			flag1 = 0

	plt.plot(internal,gpa)
	plt.xlabel('Tests')
	plt.ylabel('GPA')
	plt.title('Test Performance')
	plt.savefig('./static/graph.png')
	plt.close()
	return True 					#purpose, for error correction: no return response
	#return render_template('gp_plot.html')	

def graph_subject(sub_no, internal_status, target):
	global usn_epic
	global arr
	data = plot_graph(usn_epic)
	internal = [1,2,3,4]
	gpa = []
	print("This is data")
	print(data)
	#credit = int(data[0][8][sub_no-1])
	sum1 = data[0][sub_no+1]
	sum1 = sum1*10/(25)
	if(internal_status!=3):
		for i in range(internal_status):
			gpa.append(sum1)
	else:
		sum1 = great_two_2(usn_epic, sub_no)
		sum1 = sum1*1.0/25
		gpa.append(sum1)
		gpa.append(sum1)
		gpa.append(sum1)

	rem = 4-internal_status

	if(sum1<target):
		delta = target-sum1
		if(rem == 3):
			gpa.append(target+(1.0*delta/3))
			gpa.append(target-(1.0*delta/3))
			gpa.append(target)
		elif(rem == 2):
			sum1 = arr[sub_no-1]
			sum1 = sum1*1.0/25
			delta = target-sum1
			if(sum1<target):
				if(target+delta<10):
					gpa.append(target+(delta))
					gpa.append(target)
				else:
					gpa.append(target+(delta*2.0/3))
					gpa.append(target+(delta/3.0))
			else:
				gpa.append(target+.05)
				gpa.append(target-.05)				
		elif(rem == 1):
			if(target+delta<=10):
				gpa.append(target+delta)
			else:
				gpa.append(15)			#make this colour change to denote impossibility

	else:
		delta = sum1-target
		if(rem == 3):
			gpa.append(target-.05)
			gpa.append(target+.15)
			gpa.append(target-.05)
		elif(rem == 2):
			gpa.append(target+.05)
			gpa.append(target-.05)
		elif(rem == 1):
			gpa.append(target+.05)
	#flag = 0
	for i in gpa:
		if i>=10:
			flag1=1
			break
		else:
			flag1=0

	plt.plot(internal,gpa)
	plt.xlabel('Tests')
	plt.ylabel('GPA')
	plt.title('Test Performance')
	plt.savefig('./static/graph.png')
	plt.close()
	return True 


@app.route("/")
def home():
	#internal_tab()
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
		pswd = str(pswd)

		pswd = pswd*2 + "3"

		insert_entry(usn, sem, email, pswd)

		return render_template('login.html')



#verifying the login function
@app.route("/loginform", methods = ['POST', 'GET'])				#from login.html
def check_credentials():
	global usn_epic
	global sem_epic

	if(request.method == 'POST'):
		usn1 = request.form['usn1']
		pswd1 = request.form['password1']
		usn1 = str(usn1)
		pswd1 = str(pswd1)
		pswd1 = pswd1*2 + "3"

		chk = check_password(usn1,pswd1)

		if(chk == 'valid'):
			#usn1 = usn1.lower()
			usn_epic = usn1
			sem_epic = obtain_sem(usn_epic)
			# Yaha par dhyan dena
			if(sem_epic == 1):
				return	render_template('1sem.html',result=[usn_epic,sem_epic])	
			elif(sem_epic == 2):
				return	render_template('2sem.html',result=[usn_epic,sem_epic])
			elif(sem_epic == 3):
				return	render_template('3sem.html',result=[usn_epic,sem_epic])
			elif(sem_epic == 4):
				return	render_template('4sem.html',result=[usn_epic,sem_epic])
			elif(sem_epic == 5):
				return	render_template('5sem.html',result=[usn_epic,sem_epic])
			elif(sem_epic == 6):
				return	render_template('6sem.html',result=[usn_epic,sem_epic])
			elif(sem_epic == 7):
				return	render_template('7sem.html',result=[usn_epic,sem_epic])
			
			return render_template('home.html')
		elif(chk == 'invalid'):
			return render_template('login.html',msg1="Wrong Password!!")
		else:
			return render_template('register1.html',msg2="Create Account!!")		#might have to change this, direct reference


@app.route("/additionalform", methods = ['POST', 'GET'])	#from additiponal.html
def insert_additional():
	global usn_epic
	global sem_epic
	global N
	if(request.method == 'POST'):
		cgpa = request.form['cgpa']
		code = request.form['coding']
		hckr = request.form['hackerrank']
		clbsts = request.form['membership_status']
		proj = request.form['projects']
		new_sem = request.form['update_sem']
		new_sem = int(new_sem)
		sem_epic = new_sem							#subtle motherfucker!!!
		cur_status = exist_check(usn_epic)

		normal = true_score(float(cgpa), int(code), int(hckr), int (clbsts), int(proj))
		print_additional()
		if(cur_status):
			insert_truepot(usn_epic, cgpa, code, hckr, clbsts, proj)
			insert_leaderboard(usn_epic,normal)
			print("insert leaderboard check")
		else:
			update_truepot(usn_epic, cgpa, code, hckr, clbsts, proj, new_sem)
			#additional_consequence(usn_epic, new_sem)
			update_leaderboard(usn_epic,normal)
			print("update leaderboard check")

		# return render_template('.html')		#same page rendering, lets see what happens
		if(sem_epic == 1):
			return	render_template('1sem.html',result=[usn_epic,sem_epic,"Click here"])	
		elif(sem_epic == 2):
			return	render_template('2sem.html',result=[usn_epic,sem_epic,"Click here"])
		elif(sem_epic == 3):
			return	render_template('3sem.html',result=[usn_epic,sem_epic,"Click here"])
		elif(sem_epic == 4):
			return	render_template('4sem.html',result=[usn_epic,sem_epic,"Click here"])
		elif(sem_epic == 5):
			return	render_template('5sem.html',result=[usn_epic,sem_epic,"Click here"])
		elif(sem_epic == 6):
			return	render_template('6sem.html',result=[usn_epic,sem_epic,"Click here"])
		elif(sem_epic == 7):
			return	render_template('7sem.html',result=[usn_epic,sem_epic,"Click here"])

		return render_template('home.html')		

@app.route("/subjectpage1", methods = ['POST', 'GET'])			#URL redirection to be changed and maybe copied 8 times.LETS see!
def insert_marks1():
	global usn_epic
	global sem_epic
	if(request.method == 'POST'):
		
		internal_status, target = sem_intake(1)
		graph_plot(internal_status, target)
		return render_template('additional.html',result=[usn_epic,sem_epic])

@app.route("/subjectpage2", methods = ['POST', 'GET'])			#URL redirection to be changed and maybe copied 8 times.LETS see!
def insert_marks2():
	global usn_epic
	global sem_epic
	if(request.method == 'POST'):

		internal_status, target = sem_intake(2)
		graph_plot(internal_status, target)
		return render_template('additional.html',result=[usn_epic,sem_epic])

@app.route("/subjectpage3", methods = ['POST', 'GET'])			#URL redirection to be changed and maybe copied 8 times.LETS see!
def insert_marks3():
	global usn_epic
	global sem_epic
	if(request.method == 'POST'):

		internal_status, target = sem_intake(3)
		graph_plot(internal_status, target)
		return render_template('additional.html',result=[usn_epic,sem_epic])

@app.route("/subjectpage4", methods = ['POST', 'GET'])			#URL redirection to be changed and maybe copied 8 times.LETS see!
def insert_marks4():
	global usn_epic
	global sem_epic
	if(request.method == 'POST'):

		internal_status, target = sem_intake(4)
		graph_plot(internal_status, target)
		return render_template('additional.html',result=[usn_epic,sem_epic])

@app.route("/subjectpage5", methods = ['POST', 'GET'])			#URL redirection to be changed and maybe copied 8 times.LETS see!
def insert_marks5():
	global usn_epic
	global sem_epic
	if(request.method == 'POST'):

		internal_status, target = sem_intake(5)
		graph_plot(internal_status, target)
		return render_template('additional.html',result=[usn_epic,sem_epic])

@app.route("/subjectpage6", methods = ['POST', 'GET'])			#URL redirection to be changed and maybe copied 8 times.LETS see!
def insert_marks6():
	global usn_epic
	global sem_epic
	if(request.method == 'POST'):

		internal_status, target = sem_intake(6)
		graph_plot(internal_status, target)
		return render_template('additional.html',result=[usn_epic,sem_epic])

@app.route("/subjectpage7", methods = ['POST', 'GET'])			#URL redirection to be changed and maybe copied 8 times.LETS see!
def insert_marks7():
	global usn_epic
	global sem_epic
	if(request.method == 'POST'):

		internal_status, target = sem_intake(7)
		graph_plot(internal_status, target)
		return render_template('additional.html',result=[usn_epic,sem_epic])

@app.route("/subj_plot", methods = ['POST', 'GET'])
def plot_sub():
	global usn_epic
	global sem_epic
	global flag1
	if(request.method == 'POST'):
		sub_no = request.form['sub']
		sub_no = int(sub_no)
		
		graph_subject(sub_no, internal_status, target)

		return render_template('gp_plot.html',result = flag1)

@app.route("/comp_plot", methods = ['POST', 'GET'])
def plot_comp():
	global usn_epic
	global sem_epic
	global for_company_gpa
	global for_company_internal
	if(request.method == 'POST'):
		c_name = request.form['cmp']
		c_name = str(c_name)

		c_gpa = obtain_cutoff(c_name)

		print(len(for_company_gpa))
		python_sux = [c_gpa, c_gpa, c_gpa, c_gpa]
		python_sux1 = [0,1,3,4]
		print(for_company_internal)
		print(for_company_gpa)

		plt.plot(python_sux1,python_sux,color = "red")
		plt.plot(for_company_internal, for_company_gpa, color = "blue")	#	subplot search write the html code for displaying table from backend
		plt.xlabel('Tests')
		plt.ylabel('GPA')
		plt.title('Test Performance')
		plt.savefig('./static/graph.png')
		plt.close()

	return render_template('gp_plot.html')
#---------------------Temp check : function to remove cache-----------------#


#-----------------Routes for "plot" button for the 7 pages-----------------------#

@app.route("/plot_b1", methods = ['POST', 'GET'])
def pltb1():
	global flag1
	return render_template('gp_plot.html',result = flag1)

@app.route("/plot_b2", methods = ['POST', 'GET'])
def pltb2():
	global flag1
	return render_template('gp_plot.html',result = flag1)

@app.route("/plot_b3", methods = ['POST', 'GET'])
def pltb3():
	global flag1
	return render_template('gp_plot.html',result = flag1)

@app.route("/plot_b4", methods = ['POST', 'GET'])
def pltb4():
	global flag1
	return render_template('gp_plot.html',result = flag1)	

@app.route("/plot_b5", methods = ['POST', 'GET'])
def pltb5():
	global flag1
	return render_template('gp_plot.html',result = flag1)

@app.route("/plot_b6", methods = ['POST', 'GET'])
def pltb6():
	global flag1
	return render_template('gp_plot.html',result = flag1)

@app.route("/plot_b7", methods = ['POST', 'GET'])
def pltb7():
	global flag1
	return render_template('gp_plot.html',result = flag1)

@app.route("/update_sem1", methods = ['POST', 'GET'])
def update_stud_sem():

	if(request.method == 'POST'):
		semester = request.form['update_sem']

		update_semester(usn_epic, semester)

@app.route("/logout_user",methods = ['POST','GET'])
def logout_function():
	global for_company_internal
	global for_company_gpa
	for_company_internal = []
	for_company_gpa = []
	return render_template('home.html')

@app.route("/leader",methods=['POST','GET'])
def leader():
	data = get_values()
	return render_template('leaderb.html',result = data, result2 = usn_epic)

@app.route("/testimonials",methods=['POST','GET'])
def testimonials():
	return render_template('testimonials.html')

@app.route("/testimonials1",methods=['POST','GET'])
def testimonials1():
	return render_template('testimonials1.html')

@app.route("/company",methods=['POST','GET'])
def company():
	conn, cur = connect()
	data = show_company_view()
	return render_template('table.html',result=data)

@app.route("/about")
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True)