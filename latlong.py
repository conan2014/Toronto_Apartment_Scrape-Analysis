from selenium import webdriver
import pandas as pd
import numpy as np

driver = webdriver.Chrome('/Users/conan/chromedriver')
driver.get("https://www.latlong.net/Show-Latitude-Longitude.html")

df = pd.read_csv("toronto_apartments_aug_16_2019.csv")
df['address'] = ''

for i in range(df.shape[0]):
	
	latitude = driver.find_element_by_name("latitude")
	latitude.send_keys(str(df.iloc[i]['latitude']))

	longitude = driver.find_element_by_name("longitude")
	longitude.send_keys(str(df.iloc[i]['longitude']))

	driver.find_element_by_xpath("//button[@title='Show Lat Long converted address on Map']").click()

	address_list = []
	address = driver.find_elements_by_id("address")
	for location in address:
		address_list.append(location.text)
	df.at[i, 'address'] = address_list[0]
	
	latitude = driver.find_element_by_name("latitude").clear()

	longitude = driver.find_element_by_name("longitude").clear()

	print(address_list)
	print('\n')

df.to_csv("toronto_apartments_aug_16_2019_address.csv")
