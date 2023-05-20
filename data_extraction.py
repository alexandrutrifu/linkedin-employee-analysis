from modules import *
from start_search import *
from db_operations import *


def extraction():
	""" Progressively extracts employee data from company's profile

	The function signs into LinkedIn, browsing lists of employees until finding enough to add to the database table
	"""

	url = "https://www.linkedin.com/voyager/api/search/dash/clusters?decorationId=com.linkedin.voyager.dash.deco.search" \
		".SearchClusterCollection-190&count=50&origin=FACETED_SEARCH&q=all&query=(" \
		"flagshipSearchIntent:ORGANIZATIONS_PEOPLE_ALUMNI,queryParameters:(currentCompany:List(9707),resultType:List(" \
		"ORGANIZATION_ALUMNI)),includeFiltersInResponse:true)&start=350"

	payload = {}
	headers = {
		'Cookie': os.environ["linkedin_cookie"],
		'Csrf-Token': 'ajax:4403627024508559140'
	}

	# TODO: this changes depending on company
	company_name = "Endava"

	# TODO: create separate function for extracting the company's name
	# TODO: request -> company profile -> parse HTML (main section "Organization page for ...")
	create_employees_table()

	# List of employee data to insert into database once a certain number of values is reached
	employees_to_add = []

	# Login to LinkedIn
	driver = login(company_name, employees_to_add)

	# Progressively sending the GET Requests to the LinkedIn server
	while 1:
		response = requests.request("GET", url, headers=headers, data=payload)

		# Parsing JSON response into Python dictionary
		dic = json.loads(response.text)

		for element in dic["elements"][0]["items"]:

			# Extracting employee name
			employee_name = element["itemUnion"]["entityResult"]["title"]["text"]
			print(employee_name)

			# Company role
			position = element["itemUnion"]["entityResult"]["primarySubtitle"]["text"]
			role = position.split("at")[0]

			# Extracting employee profile link
			if "navigationUrl" in element["itemUnion"]["entityResult"]:

				# Parses profile URL
				navigation_url = element["itemUnion"]["entityResult"]["navigationUrl"]
				end_mark = navigation_url.find("?")
				navigation_url = navigation_url[:end_mark]

				# Checks if the employee is already enlisted in database
				profile_tag = navigation_url.split("/")[-1]

				employee = {
					"Name": employee_name,
					"Role": role,
					"Employment Tenure": 0,
					"Profile Tag": profile_tag,
					"CompanyID": 9707,
					"CompanyName": "Endava",
					"Profile Link": navigation_url
				}

				if check_employees(profile_tag) == 1:
					continue
				if employee not in employees_to_add:
					employees_to_add.append(employee)

				# Once we have more than 50 employees to add to the company's database,
				# we begin parsing their profiles
				if len(employees_to_add) >= 30:
					parse_profiles(driver, company_name, employees_to_add)
					employees_to_add = []

		# Updating request's URL start-point
		current_index = int(url.split("start=")[1])
		url = f'{url.split("start=")[0]}start={current_index + 50}'
		print(url)

		# Break condition after a percentage of employees have been added
		if current_index >= 500:
			break

		# Request cooldown
		time.sleep(10)

	# Close WebDriver
	driver.close()
