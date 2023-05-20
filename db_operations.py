import sqlite3


def view_table(cursor: object, company: str, table: str):
	""" Prints table rows

	:param company: Database name
	:param table: Table name
	:return: None
	"""

	cursor.execute("SELECT * FROM employees")

	rows = cursor.fetchall()

	for row in rows:
		print(row)


def create_employees_table(database="employee_analysis"):
	""" Creates a database table for the specified company

	:param database: Database name
	:return: None
	"""

	create_command = f""" CREATE TABLE IF NOT EXISTS employees (
		ID INTEGER PRIMARY KEY,
		Name TEXT NOT NULL,
		Role TEXT NOT NULL,
		"Employment Tenure" INTEGER NOT NULL,
		"Profile Tag" TEXT NOT NULL,
		"CompanyID" INTEGER NOT NULL DEFAULT 9707,
		"CompanyName" TEXT NOT NULL DEFAULT "Endava"
	)		
	"""

	con = sqlite3.connect(f"{database}.sqlite3")

	# Creating database cursor to execute SQL instructions
	cursor = con.cursor()

	# Creating the actual company database
	cursor.execute(create_command)

	con.close()


def insert_employees(employee: dict, database="employee_analysis"):
	""" Updates specified table with new information

	:param database: Database name
	:param employee: Values to be inserted (dictionary)
	:return: None
	"""

	# Establishing database connection
	con = sqlite3.connect(f"{database}.sqlite3")

	cursor = con.cursor()

	tuple_values = tuple(list(employee.values())[:-1])

	# Inserting new values
	cursor.execute(f"INSERT INTO employees ('Name', 'Role', 'Employment Tenure', 'Profile Tag', 'CompanyID', 'CompanyName') "
					f"VALUES {tuple_values}")

	con.commit()
	cursor.close()


def check_employees(employee_tag: str, database="employee_analysis"):
	""" Checks if the employee is already listed in the company's database

	:param database: Database name
	:param employee_tag: Employee profile tag
	:return: 0/1
	"""

	con = sqlite3.connect(f"{database}.sqlite3")

	cursor = con.cursor()

	cursor.execute(f'SELECT * FROM employees WHERE "Profile Tag" = "{employee_tag}"')

	results = cursor.fetchall()

	cursor.close()
	if len(results) != 0:
		return 1
	else:
		return 0
