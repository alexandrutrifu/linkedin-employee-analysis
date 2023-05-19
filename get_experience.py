from modules import *


def get_experience(company: str, driver: WebDriver, employee_data: dict):
	""" Parses employee experience data

	The function scrolls down the web page until the employee's 'Experience' sections becomes visible,
	then parses and extracts their current employment span in a time format.
	:param employee_data: Dictionary containing the values to be inserted into the employees table
	:param company:
	:param driver: Configured webdriver
	:return: Success code
	"""

	while 1:
		# While section has not become visible, scroll down
		driver.execute_script("window.scrollBy(0, 20)", "")
		try:
			driver.find_element(
				By.XPATH, '//span[@aria-hidden="true" and contains(text(), "Experience")]')
		except NoSuchElementException:
			time.sleep(2)
			continue
		else:
			# After finding the 'Experience' section, extract latest employment data
			current_job_info = driver.find_element(
				By.XPATH, '//span[contains(text(), "Present") and @aria-hidden="true"]').text
			current_job_info = current_job_info.split(" · ")[1]

			# Calculate employment span
			span = 0
			if current_job_info.find("mos") != -1:
				# Number of months specified
				index = current_job_info.find("mos")
				span += int(current_job_info[index-2])

			if current_job_info.find("yrs") != -1:
				# Number of years specified
				index = current_job_info.find("yrs")
				span += 12 * int(current_job_info[index-2])

			employee_data["Employment Span"] = span
			break
