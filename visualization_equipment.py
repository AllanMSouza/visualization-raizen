import folium
import pandas as pd
import random
from folium.plugins import FastMarkerCluster
from optparse import OptionParser

def get_data(id_equipment):
	'''
		Obtem os dados do equipamento passado por parametro
		Cria e ordena um dataframe indexado pelo timestamp do dado DT_HR_LOCAL
		Retorna o dataframe criado
	'''

	data = pd.read_csv(f'colhedoras/{id_equipment}.csv', sep=',', names=["VL_ALARME","STATUS","FG_TP_COMUNICACAO","CD_EQUIPAMENTO","VL_LATITUDE","VL_LONGITUDE","DT_HR_LOCAL","DT_HR_SERVIDOR","DIFERENCA"])
	data = pd.DataFrame(data)
	
	data['DT_HR_LOCAL'] = pd.to_datetime(data['DT_HR_LOCAL'], format='%d/%m/%Y %H:%M:%S')

	#Ordena os dados de acordo com o timestamp
	data.set_index('DT_HR_LOCAL', inplace=True)

	return data

def get_minutes(string_time):
	'''
		Retorna os minutos do timestamp recebido como parametro
	'''

	minutes = string_time.strip().split(':')[1]

	return int(minutes)

def get_random_point(data):

	'''
		Retorna um ponto aleatorio do conjunto de pontos recebido como parametro 
		para centralizar a visualizacao a ser gerada
	'''

	random_lat = random.choice(data['VL_LATITUDE'].values)
	random_lon = random.choice(data['VL_LONGITUDE'].values)

	return (random_lat, random_lon)

def create_map(random_point):
	'''
		Cria o mapa inicial da visualização baseado na localização recebida como parametro
	'''

	maps = folium.Map(location=random_point, zoom_start=13, prefer_canvas=True)

	return maps


def add_points_latency(maps, data, delay):

	'''
		Adiciona os pontos ao mapa de acordo com a latencia da transmissao,
		recebe como parametros o mapa, o conjutno de dados e o atraso maximo a ser considerado (e.g., online)
		Retorna dois layer de visualizacao, sendo um com os pontos verdes representando dados com conexao
		e outra com os pontos vermelhos representando os dados sem conexao
	'''

	WITH_CONNECTION    = folium.FeatureGroup(name='With Connection')
	WITHOUT_CONNECTION = folium.FeatureGroup(name='Without Connection')

	for index, row in data.iterrows():
		
		if get_minutes(row['DIFERENCA']) < delay:
			color = 'green'
			folium.CircleMarker(location=[row['VL_LATITUDE'], row['VL_LONGITUDE']], color=color, radius=2, fill=True, popup=create_pop_up(row)).add_to(WITH_CONNECTION)

		else:
			color = 'red'
			folium.CircleMarker(location=[row['VL_LATITUDE'], row['VL_LONGITUDE']], color=color, radius=2, fill=True, popup=create_pop_up(row)).add_to(WITHOUT_CONNECTION)

	return WITH_CONNECTION, WITHOUT_CONNECTION


def create_pop_up(row):

	'''
		Gera o texto a ser mostrado na janela ne popup de cada ponto
	'''

	pop_up_string = f'Equipamento:{row["CD_EQUIPAMENTO"]} \n' + \
					f'Latencia:{row["DIFERENCA"]} \n' +\
					f'Comunicacao:{row["FG_TP_COMUNICACAO"]}'

	return pop_up_string

def add_points_status(maps, data):

	'''
		Adiciona os pontos ao mapa de acordo com a latencia da transmissao,
		recebe como parametros o mapa e o conjutno de dados 
		Retorna dois layer de visualizacao, sendo um com os pontos verdes representando dados com status online
		e outra com os pontos vermelhos representando os dados com status offline
	'''

	WITH_CONNECTION    = folium.FeatureGroup(name='With Connection')
	WITHOUT_CONNECTION = folium.FeatureGroup(name='Without Connection')

	for index, row in data.iterrows():
		
		if int(row['STATUS']) == 1:
			color = 'green'
			folium.CircleMarker(location=[row['VL_LATITUDE'], row['VL_LONGITUDE']], color=color, radius=2, fill=True, popup=create_pop_up(row)).add_to(WITH_CONNECTION)

		else:
			color = 'red'
			folium.CircleMarker(location=[row['VL_LATITUDE'], row['VL_LONGITUDE']], color=color, radius=2, fill=True, popup=create_pop_up(row)).add_to(WITHOUT_CONNECTION)

	return WITH_CONNECTION, WITHOUT_CONNECTION


def filter_data_by_communication_type(data, communication_type):

	'''
		Filtra o conjunto de dados baseado no tipo de communicacao desejada
		recebe como parametro o conjunto de dados e o tipo de comunicacao desejado
	'''

	list_of_indexs = data['FG_TP_COMUNICACAO'] == communication_type

	return data[list_of_indexs]

def filter_data_by_date(data, start_date, end_date):
	'''
		Filtra o conjunto de dados baseado no periodo desejado,
		recebe como parametro data de inicio e data final do periodo em questao
	'''

	return data[start_date:end_date]

def make_visualization(id_equipment, communication_type, status, delay, start_date, end_date, output_dir):

	'''
		Gera a visualizaco desejaba baseado nos parametros recebidos por linha de comando
	'''

	#Leitura dos dados de acordo com o equipamento
	print(f'Coletando dados equipamento {id_equipment} ...')
	data = get_data(id_equipment)

	#Filtragem dos dados de acordo com o tipo de comunicacao
	print(f'Filtrando dados pelo tipo de comunicacao {communication_type} ...')
	data = filter_data_by_communication_type(data, 'G')

	#Filtragem dos dados de acordo com o periodo desejado
	print(f'Filtrando dados com inicio em {start_date} ate {end_date} ...')
	data = filter_data_by_date(data, start_date, end_date)


	#Obtem ponto aleatorio no mapa para centralizar a visualizacao
	#Gera o mapa da visualização
	random_point = get_random_point(data)
	maps         = create_map(random_point)

	# These two lines should create FastMarkerClusters
	# FastMarkerCluster(name='Clustering Example', data=list(zip(data['VL_LATITUDE'].values, data['VL_LONGITUDE'].values))).add_to(maps)


	if status == True:
		#Gera visualizacao baseada em status
		print(f'Gerando visualizacao baseada em status ...')
		WITH_CONNECTION, WITHOUT_CONNECTION = add_points_status(maps, data)
		end_of_file = 'status'

	else:
		#Gera visualizacao baseada em latencia
		print(f'Gerando visualizacao baseada em latencia com delay maximo de {delay} minuto...')
		WITH_CONNECTION, WITHOUT_CONNECTION = add_points_latency(maps, data, delay)
		end_of_file = 'latency'


	#adiciona os layers ao mapa de visualizacao
	WITH_CONNECTION.add_to(maps)
	WITHOUT_CONNECTION.add_to(maps)	

	#adiciona interface para gerenciar os layers
	folium.LayerControl().add_to(maps)

	#Salva visualizacao no arquivo desejado
	print(f'Salvando arquivo de visualizacao ...')
	maps.save(f'{output_dir}/{id_equipment}_{communication_type}_{end_of_file}.html')

	return

def main():

	parser = OptionParser()
	parser.add_option('-o', '--output',             dest='output_dir',         help='Nome do diretorio para salvar a visualizacao',              metavar='STRING')
	parser.add_option('-i', '--id-equipment',       dest='id_equipment',       help='Identificador do equipamento para gerar a visualizacao', metavar='INT')
	parser.add_option('-t', '--communication_type', dest='communication_type', help='Tipo de comunicacao a ser considerada na visualizacao',  metavar='STRING')
	parser.add_option('-s', '--status',             dest='status',             help='Gerar visualizacao baseada no status',                   action="store_true")
	parser.add_option('-l', '--latency',            dest='status',             help='Gerar visualizacao baseada na  latencia',                action="store_false")
	parser.add_option('-d', '--delay',              dest='delay', type='int',  help='Atraso maximo para considerar o online ou offiline',     metavar='INT')
	parser.add_option('',   '--start-date',         dest='start_date',         help='Data de inicio para filtragem dos dados',                metavar='DATE')
	parser.add_option('',   '--end-date',           dest='end_date',           help='Data de final para filtragem dos dados',                 metavar='DATE')


	(opt, args) = parser.parse_args()

	make_visualization(opt.id_equipment, opt.communication_type, opt.status, opt.delay, opt.start_date, opt.end_date, opt.output_dir)

if __name__ == '__main__':
	main()