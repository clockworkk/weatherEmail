#Philip Middleton
#Find Daily Weather

from bs4 import BeautifulSoup
import urllib
import smtplib
import re, os

def find_weather_information():
	#URL for houghton Michigan on www.weather.com
	url = 'http://www.weather.com/weather/today/Houghton+MI+USMI0405:1:US'

	soup = BeautifulSoup(urllib.urlopen(url).read())
	results = ''

	#Get the current Temperature from the url
	the_current_temperature = soup.find('span',{'itemprop' : 'temperature-fahrenheit'}).text
	results = ("The current temperature is " + the_current_temperature + ' degrees fahrenheit' + '\n')

	#Get the expected High for the day
	the_expected_high = soup.find("div",{"class" : "wx-temperature"}).text
	results = (results + "The expected High for today is " + the_expected_high)
	#Strip the degrees symbol from the string, smtplib freaks out about it.
	results = results[:-2]
	results = results + ' degrees fahrenheit' + '\n'

	#Get the expected low for the day
	count = 0
	close = False
	for wx_temp in soup.find_all("div",{"class" : "wx-temperature"}):
		count +=1
		if (count == 3):
			the_expected_low = wx_temp.text
			results = (results + "The expected Low for today is " + the_expected_low)
			#Strip the degrees symbol from the string, smtplib freaks out about it.
			results = results[:-1]
			results = results + ' degrees fahrenheit' + '\n'

	return results


def format_email(body):
	#Email information
	#Authetnication information with Google Mail
	username = ''
	passwd = ''
	fromaddr = ''
	toaddrs = ''

	SUBJECT = 'Todays Weather Report'
	Message = 'Subject: %s\n\n%s' % (SUBJECT, body)
	mailProcess = smtplib.SMTP('smtp.gmail.com:587')
	mailProcess.starttls()
	mailProcess.login(username,passwd)
	mailProcess.sendmail(fromaddr, toaddrs, Message)
	mailProcess.quit()	

#Main
def main():
	current_weather = find_weather_information()
	body = current_weather
	#Call format_body to send email
	format_email(body)
	
if __name__ == '__main__':
    main()
