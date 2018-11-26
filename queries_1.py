import sqlite3

def create_db():
	#one time execution function
	#all required tables have been created here, some may noit have gsk's entry
	conn, cur = connect()
	#cur.execute("create table stud_marks (usn varchar(10) primary key, semester int, sub_1 DECIMAL(2,4), sub_2 DECIMAL(2,4), sub_3 DECIMAL(2,4), sub_4 DECIMAL(2,4), sub_5 DECIMAL(2,4), sub_6 DECIMAL(2,4), credit_seq varchar(6))")
	#cur.execute("insert into stud_marks values(?, ?, ?, ?, ?, ?, ?, ?, ?)", ["4NI16CS036", 5, 21, 25, 25, 17.5, 23, 18, "344444"])
	#cur.execute("create table true_pot (usn varchar(10) primary key, cgpa DECIMAL(2,2), number_of_coding_comp_won int, hackerrank_score int, club_membership_status int, no_of_projects int)")
	#cur.execute("create table placement_info (company_name varchar(30), tier int, cut_off DECIMAL(2,2), avg_number_placed int, internship_status int)")
	#cur.execute("create table leaderboard (usn varchar(10), true_pot_score DECIMAL(2,4))")
	#cur.execute("create table account_detail (usn varchar(10), semester int, email varchar(50), password varchar(100))")	#remember what you did here
	#cur.execute("CREATE INDEX acc_index ON account_detail(usn);")		##most searches in these days
	#cur.execute("CREATE INDEX stud_marks_index ON stud_marks(usn);")
	#cur.execute("CREATE INDEX internal_index ON internal_table(usn);")
	#conn.commit()
	conn.close()


def connect():

	conn = sqlite3.connect("./ePerform.db")
	cur = conn.cursor()

	return conn, cur

#entering the login details of the registered students
def drop_trigger():
	conn, cur = connect()
	cur.execute("drop trigger delete_trigger")
	conn.commit()
	conn.close()

def temp_placement():
	conn, cur = connect()
	cur.execute("insert into placement_info values('BOSCH',3,7.75,18,0),('HP',2,7,7,0),('CISCO',1,7,4,0),('INTUIT',1,7.5,1,0),('DELL',2,7.75,3,0),('SHELL',1,7,3,0),('SAP_LABS',1,7.5,2,0),('AMAZON',1,7.5,7,0),('HCL_TECHNOLOGIES',2,7,2,0),('ORACLE_SOLUTIONS',2,7.5,5,0),('NOKIA_INDIA_LTD',2,7.85,8,0);")
	conn.commit()
	conn.close()

def insert_entry(usn1 = 'null', semester1 = 'null', email1 = 'null', password1 = 'null'):
	conn, cur = connect()
	cur.execute('insert into account_detail values (?, ?, ?, ?)', [usn1, semester1, email1, password1])
	conn.commit()
	conn.close()
	#select_regist()

#function for checking the password

def check_password(usn1, password1):
	conn, cur = connect()
	cur.execute('select password from account_detail where usn = ?', (usn1, ))		#write the OTP function later
	data = cur.fetchone()
	conn.close()
	if(data):
			if(data[0] == password1):
				return "valid"				#in app.py check the return string for valid or invalid
			else:
				return "invalid"
	else:
		return "absent_record"

def get_marks(usn):
	conn, cur = connect()
	cur.execute("select * from stud_marks where usn = ?", (usn, ))
	data = cur.fetchall()
	conn.close()
	return data
#function for entering the marks of a student for the first time

def insert_student_marks(usn = 'null', semester = 'null', sub_1 = 'null', sub_2='null' , sub_3 = 'null', sub_4= 'null', sub_5 = 'null', sub_6 = 'null', credit_seq = 'null'):

	conn, cur = connect()
	cur.execute('insert into stud_marks values(?, ?, ?, ?, ?, ?, ?, ?, ?)', [usn, semester, sub_1, sub_2, sub_3, sub_4, sub_5, sub_6, credit_seq])
	conn.commit()
	conn.close()
	return True

def max_min(usn1, sub1, sub2, sub3, sub4, sub5, sub6):
	conn, cur = connect()
	cur.execute("select usn from internal_table where usn = ?",(usn1, ))
	dat = cur.fetchall()
	if(dat):
		cur.execute("delete from internal_table where usn=?", (usn1, ))
		conn.commit()

	cur.execute("select sub_1, sub_2, sub_3, sub_4, sub_5, sub_6 from stud_marks where usn = ?", (usn1, ))
	data = cur.fetchall()
	cur.execute("insert into internal_table values(?,?,?,?,?,?,?,?,?,?,?,?,?)", [usn1, max(data[0][0],sub1), min(data[0][0],sub1), max(data[0][1],sub2), min(data[0][1],sub2), max(data[0][2],sub3), min(data[0][2],sub3), max(data[0][3],sub4), min(data[0][3],sub4), max(data[0][4],sub5), min(data[0][4],sub5), max(data[0][5],sub6), min(data[0][5],sub6)])
	conn.commit()
	conn.close()
	arr1 = [max(data[0][0],sub1),max(data[0][1],sub2),max(data[0][2],sub3),max(data[0][3],sub4),max(data[0][4],sub5),max(data[0][5],sub6)]
	select_max()
	return arr1

def great_two(usn1):						#JOINS USED
	conn, cur = connect()
	cur.execute("select * from internal_table,stud_marks where internal_table.usn = stud_marks.usn and stud_marks.usn = ?",(usn1, ))
	data = cur.fetchall()
	best = []
	best.append((max(float(data[0][2]),float(data[0][15]))+float(data[0][1]))/2.0)
	best.append((max(float(data[0][4]),float(data[0][16]))+float(data[0][3]))/2.0)
	best.append((max(float(data[0][6]),float(data[0][17]))+float(data[0][5]))/2.0)
	best.append((max(float(data[0][8]),float(data[0][18]))+float(data[0][7]))/2.0)
	best.append((max(float(data[0][10]),float(data[0][19]))+float(data[0][9]))/2.0)
	best.append((max(float(data[0][12]),float(data[0][20]))+float(data[0][11]))/2.0)

	print(float(data[0][2]),float(data[0][14]), float(data[0][1]))
	print(float(data[0][4]),float(data[0][15]), float(data[0][3]))
	print(float(data[0][6]),float(data[0][16]), float(data[0][5]))
	print(float(data[0][8]),float(data[0][17]), float(data[0][7]))
	print(float(data[0][10]),float(data[0][18]), float(data[0][9]))
	print(float(data[0][12]),float(data[0][19]), float(data[0][11]))

	print(best)
	conn.close()
	return best

def great_two_2(usn1, sub_no):						#JOINS USED
	conn, cur = connect()
	cur.execute("select * from internal_table,stud_marks where internal_table.usn = stud_marks.usn and stud_marks.usn = ?",(usn1, ))
	data = cur.fetchall()
	best = (max(data[0][2*sub_no],data[0][sub_no+13])+data[0][2*sub_no-1])/2.0
	conn.close()
	return best

#select_all_students()
#update the value of marks
def update_marks(usn1 = 'null', semester = 'null', sub_1 = 'null', sub_2='null' , sub_3 = 'null', sub_4= 'null', sub_5 = 'null', sub_6 = 'null', credit_seq = 'null'):

	conn, cur = connect()
	cur.execute('update stud_marks set semester = ?, sub_1 = ?, sub_2 = ?, sub_3 = ?, sub_4 = ?, sub_5 = ?, sub_6 = ?, credit_seq = ? where usn = ?', (semester, sub_1, sub_2, sub_3, sub_4, sub_5, sub_6, credit_seq, usn1,))
	conn.commit()
	conn.close()
	select_marks()

#checking if entry for truepot exists
def exist_check(usn1):
	conn, cur = connect()
	cur.execute('select * from true_pot where usn = ?', (usn1, ))
	data = cur.fetchall()
	conn.close()
	if(data):
		return 0
	else:
		return 1

#additional details for true potential calculation
def insert_truepot(usn = 'null', cgpa = 'null', number_of_coding_comp_won = 'null', hackerrank_score = 'null', club_membership_status = 'null', no_of_projects = 'null'):
	
	conn, cur = connect()
	cur.execute('insert into true_pot values(?, ?, ?, ?, ?, ?)',[usn, cgpa, number_of_coding_comp_won, hackerrank_score, club_membership_status, no_of_projects])
	conn.commit()
	conn.close()

#function for updating details for evaluation of truepot
def update_truepot(usn = 'null', cgpa = 'null', number_of_coding_comp_won = 'null', hackerrank_score = 'null', club_membership_status = 'null', no_of_projects = 'null', new_sem = 'null'):
	conn, cur = connect()
	cur.execute('update true_pot set cgpa = ?, number_of_coding_comp_won = ?, hackerrank_score = ?, club_membership_status = ?, no_of_projects = ? where usn = ?', (cgpa, number_of_coding_comp_won, hackerrank_score, club_membership_status, no_of_projects, usn,))
	cur.execute('update account_detail set semester = ? where usn =? and semester != ?',(new_sem, usn, new_sem,))
	conn.commit()
	conn.close()

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

def update_leaderboard(usn = 'null', true_pot_score = 'null'):	#maybe remove the N
	conn, cur = connect()
	cur.execute('update leaderboard set true_pot_score = ? where usn = ?', (true_pot_score, usn,))
	conn.commit()
	conn.close()
	

def sorted_score():
	conn, cur = connect()
	cur.execute("select * from leaderboard order by true_pot_score desc")
	data = cur.fetchall();
	cur.execute("select count(usn) from leaderboard")
	n = cur.fetchall()
	n1 = int(n[0][0])
	conn.close()
	return data, n1

def obtain_cutoff(name):
	conn, cur = connect()
	cur.execute("select cut_off from placement_info where company_name = ?", (name, ))
	data = cur.fetchall()
	conn.close()
	c_off = data[0][0]
	c_off = float(c_off)
	return c_off

#---------------DELETE records....Admin Function----#
def delete_stud (usn):
	conn, cur = connect()
	cur.execute('select * from stud_marks where usn=?', (usn, ))
	d = cur.fetchall()
	cur.execute('delete from stud_marks where usn = ?', (usn, ))
	conn.commit()
	conn.close()

def obtain_sem(usn1):
	conn, cur = connect()
	cur.execute('select semester from account_detail where usn = ?', (usn1, ))
	data = cur.fetchall()
	temp = data[0][0]
	conn.commit()
	conn.close()
	return temp

def chk_usn(usn1):
	conn, cur = connect()
	cur.execute('select * from stud_marks where usn = ?', (usn1, ))
	data = cur.fetchall()
	conn.close()
	if(data):
		return 1
	else:
		return 0

#------------------Functions for debugging----------------------------------------#
def drop_everything():
	conn, cur = connect()
	cur.execute("delete from account_detail")
	cur.execute("delete from leaderboard")
	cur.execute("delete from stud_marks")
	cur.execute("delete from internal_table")
	cur.execute("delete from true_pot")
	conn.commit()
	conn.close

def remove_func():
	conn, cur = connect()
	cur.execute("drop table leaderboard")
	cur.execute("drop table account_detail")
	conn.commit()
	conn.close()

def select_regist():
	conn, cur = connect()
	cur.execute("select * from account_detail")
	data = cur.fetchall()
	conn.close()
	for i in data:
		print(i)
	return data
#######
def alter_tables():
	conn, cur = connect()
	cur.execute("alter table leaderboard add primary key(?)",[usn])
	cur.execute("alter table account_detail add primary key(?)",[usn])
	conn.commit()
	conn.close()

def select_marks():
	conn, cur = connect()
	print("Marks")
	cur.execute("select * from stud_marks")
	data = cur.fetchall()
	conn.close()
	for i in data:
		print(i)
	return data

def select_max():
	conn, cur = connect()
	cur.execute("select * from internal_table")
	data = cur.fetchall()
	conn.close()
	for i in data:
		print(i)
	return True

#______________________________________________________________________________________________________________________________
	#views
def create_company_view():
	conn, cur = connect()
	cur.execute(''' create view disp_company as
					select company_name,
					tier,
					avg_number_placed
					from placement_info;''')
	conn.commit()
	conn.close()

def show_company_view():
	conn, cur = connect()
	cur.execute('select * from disp_company')
	data=cur.fetchall()
	conn.close()
	return data		

def dele_details():
	conn, cur = connect()
	cur.execute('delete from placement_info')
	conn.commit()
	conn.close()

#______________________________________________________________________________________________________________________________

#triggers

def create_trigger():
	conn, cur = connect()

	cur.execute(''' create trigger del_trigger
					after update
					on account_detail
					when new.semester >= 8

					BEGIN
						delete from stud_marks where stud_marks.usn = old.usn;
						delete from true_pot where true_pot.usn = old.usn;
						delete from leaderboard where leaderboard.usn = old.usn;
						delete from account_detail where usn = old.usn;

					END;

					''')
	conn.commit()
	conn.close()


##_______________________Transactions_____________________________
# def leader_transact():
# 	conn, cur = connect()
# 	cur.execute('''
# 				BEGIN TRANSACTION;

# 				UPDATE leaderboard
# 				   SET diff = true_pot_score - prev_score
# 				 WHERE account_no = 100;
				 
				 
# 				COMMIT;
# 		''')
	#----------------------------------------------------------------------------------------------------------------------------#
	#GRAPH STUFF#

def plot_graph(usn1):
	conn, cur = connect()
	cur.execute("select * from stud_marks where usn =?", (usn1, ))
	data = cur.fetchall()
	conn.commit()
	conn.close()
	print("This is data 2")
	print(data)
	return data

def print_additional():
	conn, cur = connect()
	cur.execute("select * from true_pot")
	data=cur.fetchall()
	conn.close()
	print("This is additional data")
	print(data)