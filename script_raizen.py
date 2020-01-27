import pandas as pd
import os
import random
import datetime

def get_seconds(string_time):
	seconds = string_time.strip().split(':')[2]

	seconds = seconds.replace('.', '')

	return int(seconds)

def get_minutes(string_time):

	minutes = string_time.strip().split(':')[1]

	return int(minutes)

def get_hour(string_time):

	hour = string_time.strip().split(':')[0]

	return int(hour)

def read_data(id_equipment):

	data = pd.read_csv(f'colhedoras/{id_equipment}', sep=',', chunksize=100_000, names=["VL_ALARME","STATUS","FG_TP_COMUNICACAO","CD_EQUIPAMENTO","VL_LATITUDE","VL_LONGITUDE","DT_HR_LOCAL","DT_HR_SERVIDOR","DIFERENCA"])

	count_off_menorq10 = 0
	count_on_menorq10  = 0

	count_off_maiorq10 = 0
	count_on_maiorq10  = 0

	count_off_menorq10_time =  []
	count_on_menorq10_time  =  []
	count_off_maiorq10_time =  []
	count_on_maiorq10_time  =  []

	for chunk in data:
		df = pd.DataFrame(chunk)

		status    = df['STATUS'].values
		vl_alarme = df['VL_ALARME'].values
		comm      = df['FG_TP_COMUNICACAO'].values
		diferenca = df['DIFERENCA'].values

		for _ in range(len(status)):
			
			fist_num = str(vl_alarme[_])[0]
						
			minutes = get_minutes(diferenca[_])
			seconds = get_seconds(diferenca[_])
			hour    = get_hour(diferenca[_])


			# if fist_num != '8' and fist_num != 'C' and status[_] == 1:
			# 	print 'STATUS', status[_], 'VL_ALARME', vl_alarme[_]#, 'COM', comm[_], 'DIFF', diferenca[_]

			if status[_] == 1 and hour < 1 and minutes < 1 and seconds <= 10 :
				count_on_menorq10 += 1
				count_on_menorq10_time.append(diferenca[_])

			elif status[_] == 0 and hour < 1 and minutes < 1 and seconds <= 10:
				count_off_menorq10 += 1
				count_off_menorq10_time.append(diferenca[_])

			elif status[_] == 1 and minutes > 1:
				count_on_maiorq10 += 1
				count_on_maiorq10_time.append(diferenca[_])

			elif status[_] == 0 and minutes > 1:
				count_off_maiorq10 += 1
				count_off_maiorq10_time.append(diferenca[_])


			# # if len(str(vl_alarme[_])) > 3 and status[_] == 1:
			# if comm[_] == 'C' and status[_] == 0:
			# 	# print comm[_]
				# print('STATUS', status[_], 'VL_ALARME', vl_alarme[_], 'COM', comm[_], 'DIFF', diferenca[_])

	file         = open('log_plot_raizen.txt', 'a')
	id_equipment = id_equipment.split('.')[0]

	file.write(f'{id_equipment} \t {count_on_menorq10} \t {count_off_menorq10} \t {count_on_maiorq10} \t {count_off_maiorq10} \n')
	file.close()


	file  = open('avg_time.txt', 'a')
	file.write(f'{id_equipment}')
	for list_of_times in (count_on_menorq10_time, count_off_menorq10_time, count_on_maiorq10_time, count_off_maiorq10_time):
		avg_time = get_avg_time(list_of_times)
		file.write(f'\t {str(avg_time)}')
	file.write('\n')
	file.close()




def get_avg_time(list_of_times):

	total_time = 0

	for i in list_of_times:
		i = i.replace('.', '')
		(h, m, s)   = i.split(':')
		d           = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
		total_time += d.seconds

	if len(list_of_times) > 0:
		return float(total_time/len(list_of_times))

	else: 
		return 0

list_equipment = os.listdir('colhedoras/')

# for id_equipment in ('101474', '72121', '101469', '101481', '101514'):

# chosen_list  = []
# id_equipment = '101474.csv'
# for _ in range(20):
	
# 	while True:
# 		id_equipment = random.choice(list_equipment)

# 		if id_equipment not in chosen_list:
# 			chosen_list.append(id_equipment)
# 			break

for id_equipment in list_equipment:
		
	if id_equipment.startswith('c'):
		continue
	print(f'Processing equipment {id_equipment} ... ')
	read_data(id_equipment)


