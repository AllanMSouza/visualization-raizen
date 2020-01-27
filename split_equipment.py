import pandas as pd


def get_chunks(filename):

	set_of_chunks = pd.read_csv(f'colhedoras/{filename}', sep=',', chunksize=100_000)

	return set_of_chunks

def get_data(chunk):

	data = pd.DataFrame(chunk)

	return data

def main():

	set_of_chunks = get_chunks('colhedoras.csv')

	for id_chunk, chunk in enumerate(set_of_chunks):
		print(f'Processing chunk {id_chunk} ...')
		list_of_equipments = {}
		data               = get_data(chunk)

		print(f'Getting list of equipments ...')
		for id_row, row in data.iterrows():
			
			if row['CD_EQUIPAMENTO'] not in list_of_equipments.keys():
				list_of_equipments[row['CD_EQUIPAMENTO']] = list()
				list_of_equipments[row['CD_EQUIPAMENTO']].append(row)

			else:
				list_of_equipments[row['CD_EQUIPAMENTO']].append(row)

		print(f'Writing files of chunk ...')
		for equipment in list_of_equipments.keys():
			df = pd.DataFrame(list_of_equipments[equipment])
			df.to_csv(f'colhedoras/{equipment}.csv', mode='a', index=False, header =False)


if __name__ == '__main__':
	main()