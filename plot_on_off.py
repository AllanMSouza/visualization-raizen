import pandas as pd
import matplotlib.pyplot as plt
plt.rc('axes', axisbelow=True)


def plot_conn():

	df = pd.DataFrame(pd.read_csv('log_plot_raizen.txt', sep='\t', names=['id', 'Status Online com atraso menor que 10s', 'Status Offline com atraso menor que 10s', 'Status Online com atraso maior que 1min', 'Status offline com atraso maior que 1min']))
	df.set_index('id', inplace=True)

	for attribute in ('Status Online com atraso menor que 10s', 'Status Offline com atraso menor que 10s', 'Status Online com atraso maior que 1min', 'Status offline com atraso maior que 1min'):

		df[attribute].plot.bar(color='blue', edgecolor='k')

		plt.title(attribute, size=14)
		plt.ylabel('Dados transmitidos', size=12)
		plt.xlabel('ID do equipamento', size=12)
		plt.grid(True, linestyle='--')
		plt.savefig(f'Plots/{attribute}.jpeg', bbox_inches='tight')

		plt.show()


def plot_time():

	df = pd.DataFrame(pd.read_csv('avg_time.txt', sep='\t', names=['id', 'Status Online com atraso menor que 10s', 'Status Offline com atraso menor que 10s', 'Status Online com atraso maior que 1min', 'Status offline com atraso maior que 1min']))
	df.set_index('id', inplace=True)

	for attribute in ('Status Online com atraso menor que 10s', 'Status Offline com atraso menor que 10s', 'Status Online com atraso maior que 1min', 'Status offline com atraso maior que 1min'):

		df[attribute].plot.bar(color='red', edgecolor='k')

		plt.title(attribute, size=14)
		plt.ylabel('Atraso medio (segundos)', size=12)
		plt.xlabel('ID do equipamento', size=12)
		plt.grid(True, linestyle='--')
		plt.savefig(f'Plots/{attribute}_time.jpeg', bbox_inches='tight')

		plt.show()

def get_equipments_with_error():
	df = pd.DataFrame(pd.read_csv('log_plot_raizen.txt', sep='\t', names=['id', 'Status Online com atraso menor que 10s', 'Status Offline com atraso menor que 10s', 'Status Online com atraso maior que 1min', 'Status offline com atraso maior que 1min']))
	# df.set_index('id', inplace=True)

	for idx, row in df.iterrows():
		if int(row['Status Offline com atraso menor que 10s']) > int(row['Status Online com atraso menor que 10s']):
			print(f'OFF > ON: {row}')

		elif int(row['Status Online com atraso maior que 1min']) > int(row['Status offline com atraso maior que 1min']):
			print(f'ON > OFF: {row}')


get_equipments_with_error()
# plot_conn()
# plot_time()