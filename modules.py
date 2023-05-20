import requests
import os
import time
import json
from bs4 import BeautifulSoup
import pandas
from pandasql import sqldf
import random as rd
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium_stealth import stealth
from proxy_randomizer import RegisteredProviders
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent


def wait():
	""" Inserts time gaps between request operations
	"""

	time.sleep(3 + rd.randint(0, 5))

