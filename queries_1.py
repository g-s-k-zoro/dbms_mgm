import sqlite3

def create_db():
	#one time execution function
	#all required tables have been created here, some may noit have gsk's entry
	conn, cur = connect()
	cur.execute("create table stud_marks (usn varchar(10) primary key, semester int, sub_1 DECIMAL(2,4), sub_2 DECIMAL(2,4), sub_3 DECIMAL(2,4), sub_4 DECIMAL(2,4), sub_5 DECIMAL(2,4), sub_6 DECIMAL(2,4), credit_seq varchar(6))")
	cur.execute("insert into stud_marks values(?, ?, ?, ?, ?, ?, ?, ?, ?)", ["4NI16CS036", 21, 25, 25, 17.5, 23, 18, "444443"])
	cur.execute("create table true_pot (usn varchar(10) primary key, cgpa DECIMAL(2,2), number_of_coding_comp_won int, hackerrank_score int, club_membership_status int, no_of_projects int)")
	cur.execute("create table placement_info (company_name varchar(30), tier int, cut_off DECIMAL(2,2), avg_number_placed int, internship_status int)")
	cur.execute("create table leaderboard (usn varchar(10), true_pot_score DECIMAL(2,4))")
	cur.execute("create table account_detail (usn varchar(10), semester int, email varchar(50), password varchar(100))")
	conn.commit()
	conn.close()

def connect():

	conn = sqlite3.connect("./ePerform.db")
	cur = conn.cursor()

	return conn, cur

#entering the login details of the registered students

def insert_entry(usn1 = 'null', semester1 = 'null', email1 = 'null', password1 = 'null'):
	conn, cur = connect()

	cur.execute('insert into account_detail values (?, ?, ?, ?)', [usn1, semester1, email1, password1])
	conn.commit()
	conn.close()
	select_regist()

#function for checking the password

def check_password(usn1, password1):
	conn, cur = connect()
	cur.execute('select password from account_detail where usn = ?', (usn1, ))		#write the OTP function later
	data = cur.fetchall()
	if(data):
			if(data[0] == password1):
				return "valid"				#in app.py check the return string for valid or invalid
			else:
				return "invalid"
	else:
		return "absent_record"
	conn.commit()
	conn.close()

#function for entering the marks of a student for the first time

def insert_student_marks(usn = 'null', semester = 'null', sub_1 = 'null', sub_2='null' , sub_3 = 'null', sub_4= 'null', sub_5 = 'null', sub_6 = 'null', credit_seq = 'null'):

	conn, cur = connect()
	cur.execute('insert into stud_marks values(?, ?, ?, ?, ?, ?, ?)', [usn, semester, sub_1, sub_2, sub_3, sub_4, sub_5, sub_6, credit_seq])
	conn.commit()
	conn.close()

#select_all_students()
#update the value of marks
def update_marks(usn1 = 'null', semester = 'null', sub_1 = 'null', sub_2='null' , sub_3 = 'null', sub_4= 'null', sub_5 = 'null', sub_6 = 'null', credit_seq = 'null'):

	conn, cur = connect()
	cur.execute('update stud_marks set semester = ?, sub_1 = ?, sub_2 = ?, sub_3 = ?, sub_4 = ?, sub_5 = ?, sub_6 = ?, credit_seq = ? where usn = ?', [semester, sub_1, sub_2, sub_3, sub_4, sub_5, sub_6, credit_seq, usn1])
	conn.commit()
	conn.close()

#additional details for true potential calculation
def insert_truepot(usn = 'null', cgpa = 'null', number_of_coding_comp_won = 'null', hackerrank_score = 'null', club_membership_status = 'null', no_of_projects = 'null'):
	
	conn, cur = connect()
	cur.execute('insert into true_pot values(?, ?, ?, ?, ?, ?)',[usn, cgpa, number_of_coding_comp_won, hackerrank_score, club_membership_status, no_of_projects])
	conn.commit()
	conn.close()

#function for updating details for evaluation of truepot
def update_truepot(usn = 'null', cgpa = 'null', number_of_coding_comp_won = 'null', hackerrank_score = 'null', club_membership_status = 'null', no_of_projects = 'null')
	conn, cur = connect()
	cur.execute('update truepot set cgpa = ?, number_of_coding_comp_won = ?, hackerrank_score = ?, club_membership_status = ?, no_of_projects = ?, where usn = ?', [cgpa, number_of_coding_comp_won, hackerrank_score, club_membership_status, no_of_projects])
	cur.execute('update account_detail set semester = ?, where usn =? and semester != new_sem',[new_sem, usn])
	conn.commit()
	conn.close()
	conn, cur = connect()
	cur.execute('select semester')
	data = cur.fetchall()
	if(data):

def insert_company_det(company_name, tier, cut_off, avg_number_placed, internship_status):
	#one time execution function, that is, when the data from the placement office is collected
	conn, cur = connect()
	cur.execute('insert into placement_info values(?, ?, ?, ?, ?)',[company_name, tier, cut_off, avg_number_placed, internship_status])
	conn.commit()
	conn.close()


def insert_leaderboard(usn = 'null', true_pot_score = 'null'):
	conn, cur = connect()
	cur.execute('insert into leaderboard values(?, ?)', [usn, true_pot_score])
	conn.commit()
	conn.close()


def delete_stud (usn):
	conn, cur = connect()
	cur.execute('select * from stud_marks where usn=?', (usn, ))
	d = cur.fetchall()

	if(d and d[1]>6):
			cur.execute('delete from stud_marks where usn = ?', (usn, ))
			cur.execute('delete from true_pot where usn = ?', (usn, ))
			cur.execute('delete from leaderboard where usn = ?', (usn, ))
	else:
		print('INVALID STUDENT USN')

	conn.commit()
	conn.close()

def obtain_sem(usn1):
	conn, cur = connect()
	cur.execute('select semester from account_detail where usn1 = ?', (usn1, ))
	data = cur.fetchall()
	conn.commit()
	conn.close()
	return data[0]

def update_semester(usn, semester = 'null'):

	conn, cur = connect()
	cur.execute('update account_detail set semester = ?, where usn = ?', (semester, usn))
	cur.execute('update truepot set ')


def select_regist():
	conn, cur = connect()
	cur.execute("select * from account_detail")
	data = cur.fetchall()
	conn.close()
	for i in data:
		print(i)
	return data

	
