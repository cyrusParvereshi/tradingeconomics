import tradingeconomics as te
import pdb
import pandas as pd 
import requests
import pprint
import matplotlib.pyplot as plt
import configparser

def read_api_key():
	configParser = configparser.RawConfigParser()   
	configFilePath = './.api_key.txt'
	configParser.read(configFilePath)
	details_dict = dict(configParser.items('api-key'))
	return details_dict['api_key']

def obtain_data(api_key):
	url_mfgGDP = f'https://api.tradingeconomics.com/historical/country/mexico/indicator/GDP%20from%20Manufacturing?c={api_key}&f=json'
	url_mx_unemp = f'https://api.tradingeconomics.com/historical/country/Mexico/indicator/Unemployment%20Rate?c={api_key}&f=json'
	# first clean mex gdp to the columns we want
	mfg_mex_gdp = requests.get(url_mfgGDP).json()
	mx_unemp = requests.get(url_mx_unemp).json()
	return (mfg_mex_gdp, mx_unemp)

def clean_data(mfg_mex_gdp, mx_unemp):
	mfg_mex_gdp = [{k: v for k, v in x.items() if k.startswith('Value') or k.startswith("DateTime")} for x in mfg_mex_gdp]
	mx_unemp = [{k: v for k, v in x.items() if k.startswith('Value') or k.startswith("DateTime")} for x in mx_unemp]
	gdp_df = pd.DataFrame(mfg_mex_gdp)
	gdp_df = gdp_df.rename(columns={"Value": "MFG_GDP"})
	unemp_df = pd.DataFrame(mx_unemp)
	unemp_df = unemp_df.rename(columns={ "Value": "UnemploymentRate"})

	df_combo = pd.merge(gdp_df, unemp_df, on="DateTime", how='inner')
	df_combo['DateTime'] = pd.to_datetime(df_combo['DateTime'])
	df_combo = df_combo[(df_combo['DateTime'] > '2012-01-01')]
	return df_combo

def plot_data(df_combo, main_file=True):
	figure, axis = plt.subplots(1, 2) 
	figure.set_size_inches(15, 7)
	axis[0].plot(df_combo['DateTime'], df_combo['MFG_GDP'], color='green')
	axis[0].set_title("Mex MFG GDP/Time")
	axis[0].set_xlabel("Year")
	axis[0].set_ylabel("Manufacturing GDP ($m)")
	axis[1].plot(df_combo['DateTime'], df_combo['UnemploymentRate'], color='red')
	axis[1].set_title("Mex Unemp Rate/Time")
	axis[1].set_xlabel("Year")
	axis[1].set_ylabel("Mexican Unemployment Rate (%)")
	if main_file:
		plt.show()
	plt.close(figure) 	
	return figure

def main():
	api_key = read_api_key()
	(mfg_mex_gdp, mx_unemp) = obtain_data(api_key)
	df_combo = clean_data(mfg_mex_gdp, mx_unemp)
	plot_data(df_combo)

if __name__ == '__main__':
	main()