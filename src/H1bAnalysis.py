import sys
import os
from io import open as ioopen

#define the hib analysis function to compute the top 10 occupations
#and States of the anaual H1B verified cases and output the results into files
def run_analysis():

	#take the sys arguments as the input and output file path and names
	input_dir=sys.argv[1]
	output_top_10_occupations_file=sys.argv[2]
	output_top_10_states_file=sys.argv[3]
	
	#find the file in input directory and pass to the input_file
	file_list=os.listdir(input_dir)
	input_file=input_dir+file_list[0]

	#create the variables of map data structures holding the key of occupations and working_states
	# and values of counts respectfully
	Certified_Total=0.0
	occupations={}
	working_states={}

	# read the csvfile line by line and parsing each line of data into 
	# fields, then put the SOC(occupation names) and working states fields
	# into occupations and working_states map
	with ioopen(input_file,encoding='utf-8') as csvfile:
		lines=csvfile.readlines()

		field_index=lines[0].split(';')

		for i in field_index:
			if 'STATUS' in i:
				status_index=field_index.index(i)
				print(status_index)
			if 'SOC_NAME' in i:
				SOC_index=field_index.index(i)
				print(SOC_index)
			if 'WORKLOC1_STATE' in i or 'WORKSITE_STATE' in i:
				states_index=field_index.index(i)
				print(states_index)
		rest_lines=lines[1:]		
		for line in rest_lines:
			row=line.split(";")
			status=row[status_index].replace('"','')
			occupation=row[SOC_index].replace('"','')
			state=row[states_index].replace('"','')
			if status=='CERTIFIED':
				Certified_Total+=1
				
				if occupation in occupations and state in working_states:
					occupations[occupation]+=1
					working_states[state]+=1
				elif occupation in occupations and state not in working_states:
					occupations[occupation]+=1
					working_states[state]=1
				elif occupation not in occupations and state in working_states:
					occupations[occupation]=1
					working_states[state]+=1
				else:
					occupations[occupation]=1
					working_states[state]=1
					
	csvfile.close() 

			   
	# sort the occupations and working_states by values(total counts of the key)
	# and store the sorted result as list of tuples
	sorted_Occupations=sorted(sorted(occupations.items(),key=lambda x:x[0]),key=lambda x:x[1],reverse=True)
	sorted_States=sorted(sorted(working_states.items(),key=lambda x:x[0]),key=lambda x:x[1],reverse=True)

	# create the top10 occupations output file and write the top 10 occupations 
	# from the sorted list results to it	
	occupations_file = open(output_top_10_occupations_file,"w")
	header='TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'+'\n'
	occupations_file.write(header)
	for i in sorted_Occupations[0:10]:
		output_str=str(i[0])+';'+str(i[1])+';'+str(round((i[1]/Certified_Total)*100,1))+'%'+'\n'
		occupations_file.write(output_str)
		print(str(i[0])+';'+str(i[1])+';'+str(round((i[1]/Certified_Total)*100,1))+'%')
	occupations_file.close()	

	
	
	# create the top10 states output file and write the top 10 states info
	# from the sorted list restults 
	states_file = open(output_top_10_states_file,"w")
	header='TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'+'\n'
	states_file.write(header)
	for j in sorted_States[0:10]:
		output_state=str(j[0])+';'+str(j[1])+';'+str(round((j[1]/Certified_Total)*100,1))+'%'+'\n'
		states_file.write(output_state)
		print(str(j[0])+';'+str(j[1])+';'+str(round((j[1]/Certified_Total)*100,1))+'%')
	states_file.close()

	
	
# run the analysis function if the file been triggered directly
if __name__ == '__main__':
    run_analysis()
