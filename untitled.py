			if row_1['src_ap'] in iata:
				flag_out = True
				ap_out=iata[row_1['src_ap']]
			elif row_1['src_ap'] in icao:
				flag_out = True
				ap_out=iata[row_1['src_ap']]

			if row_1['dest_ap'] in iata:
				flag_in = True
				ap_in=iata[row_1['dest_ap']]
			elif row_1['dest_ap'] in icao:
				flag_in = True
				ap_in=iata[row_1['dest_ap']]

			if flag_in==True and flag_out= True:
				for ap_t in airports:
					if ap_t.country==
