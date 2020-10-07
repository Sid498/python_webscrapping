import os
import csv
import prettytable
import pandas as pd
import requests as re
from bs4 import BeautifulSoup as bs

ipl_dict = {}

def get_data():
	url = "https://www.iplt20.com/points-table/2020"
	page = re.get(url)
	soup = bs(page.text, 'html.parser')
	table = soup.find('table',class_='standings-table standings-table--full')
	team_table = table.find_all('tr')
	for teams in team_table:
	    team_name = teams.find('span', class_='standings-table__team-name js-team')
	    matches_played = teams.find('td', class_='standings-table__padded')
	    matches_won = teams.find_all('td', class_='standings-table__optional')
	    net_rr = teams.find('td', class_='')
	    team_points = teams.find('td', class_='standings-table__highlight js-points')
	    form = teams.find('ul', class_='standings-table__form')

	    if team_name:
	    	ipl_dict.update({team_name.text:{
	    				'played': matches_played.text.strip(),
	    			    'won': matches_won[0].text,
	    			    'lost': matches_won[1].text,
	    			    'tied':matches_won[2].text,
	    			    'n/r':matches_won[3].text,
	    			    'net-run-rate': net_rr.text,
	    			    'for': matches_won[4].text,
	    			    'against': matches_won[5].text,
	    			    'points': team_points.text,
	    			    'form': ",".join(form.text.strip().replace('\n',",").split(","))}})
	return ipl_dict


def create_table(data_dict):
	table = prettytable.PrettyTable()
	table.field_names = ['name', 'played', 'won', 'lost', 'tied', 'N/R', 'net-rr', 'for', 'against', 'points', 'form']

	for key,val in data_dict.items():
		table.add_row([key, val.get('played'),
							val.get('won'),
							val.get('lost'),
							val.get('tied'),
							val.get('n/r'),
							val.get('net-run-rate'),
							val.get('for'),
							val.get('against'),
							val.get('points'),
							val.get('form')])
	print(table)


def save_csv():
	path = os.path.join(os.getcwd(), 'ipl.csv')
	data = get_data()
	df = pd.DataFrame.from_dict(data, orient='index')
	df.to_csv(path)
	create_table(data)
	print(f"File saved at {path}")


if __name__ == '__main__':
	save_csv()

