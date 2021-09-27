from __future__ import unicode_literals

import json

from datetime import date
import locale
import frappe
import random
import string
import requests
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def random_string(string_length=8):
	letters = string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(string_length))

@frappe.whitelist()
def get_exchange_rate(**args):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	exchange_date = args.get('exchange_date')
	from_currency = args.get('from_currency')
	to_currency = args.get('to_currency')

	yyyymmdd = exchange_date[0:10]
	print(yyyymmdd)
	yyyy = exchange_date[0:4]
	mm = exchange_date[5:7]
	dd = exchange_date[8:10]
	print(yyyy + mm + dd)


	url1 = 'https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do'
	data = {
		'ajax': 'true',
		'curCd': from_currency,
		'tmpInqStrDt': yyyymmdd,
		'pbldDvCd': '1',
		'pbldSqn': '',
		'inqStrDt': yyyy + mm + dd,
		'inqKindCd': '1',
		'requestTarget': 'searchContentDiv'
	}
	res1 = requests.post(url1, data=data)
	html = res1.content
	soup = BeautifulSoup(html, 'lxml')
	exchange_rate = 0.0
	list_td = soup.find_all(name="td", attrs={"class": "txtAr"})
	exchange_rate = list_td[8].text.strip()
	if locale.atof(exchange_rate) > 0:
		exchange_doc = frappe.new_doc('Currency Exchange')
		exchange_doc.date = exchange_date
		exchange_doc.from_currency = from_currency
		exchange_doc.to_currency = to_currency
		if from_currency == "JPY" or from_currency == "VND" or from_currency == "IDR":
			exchange_doc.exchange_rate = locale.atof(exchange_rate)/100
		else:
			exchange_doc.exchange_rate = locale.atof(exchange_rate)
		exchange_doc.for_buying = 1
		exchange_doc.for_selling = 1

#		create_exchange_rate(yyyymmdd, currency_cd, exchange_rate)
#	for td_tag in list_td:
#		print(td_tag.text.strip())

#		exchange_rate = td_tag.text.strip()

	print(args)
	print(exchange_doc)
	return exchange_doc

@frappe.whitelist()
def get_exchange_rate_all(**args):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	exchange_date = args.get('exchange_date')
	list_currency = ['USD', 'JPY', 'EUR', 'CNY', 'HKD', 'THB', 'TWD', 'PHP', 'SGD', 'AUD', 'VND', 'GBP', 'CAD', 'MYR',
					 'RUB', 'ZAR', 'NOK', 'NZD', 'DKK', 'MXN', 'MNT', 'BHD', 'BDT', 'BRL', 'BND', 'SAR', 'LKR', 'SEK',
					 'CHF', 'AED', 'DZD', 'OMR', 'JOD', 'ILS', 'EGP', 'INR', 'IDR', 'CZK', 'CLP', 'KZT', 'QAR', 'KES',
					 'COP', 'KWD', 'TZS', 'TRY', 'PKR', 'PLN', 'HUF']

	yyyymmdd = exchange_date[0:10]
	yyyy = exchange_date[0:4]
	mm = exchange_date[5:7]
	dd = exchange_date[8:10]

	for currency_cd in list_currency:
		url1 = 'https://www.kebhana.com/cms/rate/wpfxd651_01i_01.do'
		data = {
			'ajax': 'true',
			'curCd': currency_cd,
			'tmpInqStrDt': yyyymmdd,
			'pbldDvCd': '1',
			'pbldSqn': '',
			'inqStrDt': yyyy + mm + dd,
			'inqKindCd': '1',
			'requestTarget': 'searchContentDiv'
		}
		res1 = requests.post(url1, data=data)
		html = res1.content
		soup = BeautifulSoup(html, 'lxml')
		exchange_rate = 0.0
		list_td = soup.find_all(name="td", attrs={"class": "txtAr"})
		exchange_rate = list_td[8].text.strip()
		if locale.atof(exchange_rate) > 0:
			create_exchange_rate(yyyymmdd, currency_cd, exchange_rate)
#	for td_tag in list_td:
#		print(td_tag.text.strip())

#		exchange_rate = td_tag.text.strip()

	print(args)
	return True

def create_exchange_rate(curr_date , currency_cd , mrate):
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
	ex_exists = frappe.db.exists({
		'doctype': 'Currency Exchange',
		'date': curr_date,
		'from_currency': currency_cd,
		'to_currency': 'KRW'
	})
	if not ex_exists:
		print("create  " + curr_date + " " + currency_cd + " " + mrate)
		exchange_doc = frappe.new_doc('Currency Exchange')
		exchange_doc.date = curr_date
		exchange_doc.from_currency = currency_cd
		exchange_doc.to_currency = "KRW"
		if currency_cd == "JPY" or currency_cd == "VND" or currency_cd == "IDR":
			exchange_doc.exchange_rate = locale.atof(mrate)/100
		else:
			exchange_doc.exchange_rate = mrate
		exchange_doc.for_buying = 1
		exchange_doc.for_selling = 1
		exchange_doc.insert()
