from modules import *
from get_experience import get_experience
from db_operations import *


# Specifying LinkedIn credentials
username = "andronescuestera@gmail.com"
password = os.environ["linkpass"]


def start_driver() -> WebDriver:
	""" Configures the Chrome driver

	:return: Driver config
	"""

	Cookies = os.environ["linkedin_cookie"]

	# Adding Browser options in order to maximize stealth level
	chrome_options = Options()

	chrome_options.add_argument(f'user-agent={UserAgent().random}')
	chrome_options.add_argument("start-maximized")
	# chrome_options.add_argument("--headless")
	chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
	chrome_options.add_experimental_option('useAutomationExtension', False)
	chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
	chrome_options.add_argument('--no-sandbox')

	# Instantiate Chrome driver
	driver = webdriver.Chrome(service=Service(
		ChromeDriverManager().install()), chrome_options=chrome_options)

	stealth(driver,
			user_agent=UserAgent().random,
			languages=["en-US", "en"],
			vendor="Google Inc.",
			platform="Win32",
			webgl_vendor="Intel Inc.",
			renderer="Intel Iris OpenGL Engine",
			fix_hairline=True,
			)

	driver.get_cookies()

	return driver


def send_credentials(driver: WebDriver):
	""" Inserts user credentials

	:param driver: Configured WebDriver
	:return:
	"""
	driver.find_element(By.XPATH, '//input[@name="session_key"]').send_keys(username)
	wait()
	driver.find_element(By.XPATH, '//input[@name="session_password"]').send_keys(password)
	wait()
	driver.find_element(
		By.XPATH, '//button[contains(text(), "Sign in") and @data-id="sign-in-form__submit-btn"]').click()


def login(company: str, employees: list) -> WebDriver:
	""" Parses the HTML source-code of the provided page and extracts employment date

	:param company: Company name
	:param employees: List of employees to add to the company's database
	:return: Configured WebDriver instance
	"""

	# Configure webdriver
	driver = start_driver()

	linkedin_url = "https://linkedin.com"

	driver.get_cookies()
	# Sending GET request
	try:
		driver.get(linkedin_url)
	except ConnectionError:
		print("Error: Failed to fetch main LinkedIn page")
		return -1

	wait()
	# Wait for the 'Sign In' box to be detected
	cooldown = WebDriverWait(driver, 30).until(ec.presence_of_element_located((
		By.XPATH, '//button[contains(text(), "Sign")]')))

	wait()
	# Try to identify the credential input boxes
	try:
		driver.find_element(By.XPATH, '//input[@name="session_key"]')
	except NoSuchElementException:
		print('Error: Could not sign in')
		return -1
	else:
		# Once clicked, try to log-in
		try:
			send_credentials(driver)
		except NoSuchElementException:
			print('Error: Could not find credential boxes')
		else:
			# Fetch employee profiles
			try:
				wait()
				driver.find_element(By.XPATH, '//a[@title="continue anyway"]').click()
			except NoSuchElementException:
				pass

	return driver


def parse_profiles(driver: WebDriver, company: str, employees: list):
	""" Gets employee profiles and starts parsing process

	:param driver: Pre-configured WebDriver instance
	:param company: Company name
	:param employees: List of employees to add to the company's database
	:return: None
	"""

	for employee in employees:

		profile_link = employee["Profile Link"]

		# Sending GET request
		try:
			driver.get(profile_link)
		except ConnectionError:
			print("Error: Failed to fetch profile")
			return -1
		else:
			# TODO: check if it asks you to login again
			try:
				driver.find_element(By.XPATH, '//input[@name="session_key"]')
			except NoSuchElementException:
				pass
			else:
				send_credentials(driver)
			finally:
				wait()
				get_experience(company, driver, employee)
				wait()

	for employee in employees:
		insert_employees(employee)

