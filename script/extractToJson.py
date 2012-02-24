#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json

#you can play the game "Find the errors" in this buggy script! (:(){ :|:& };:)
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main(filename='example.txt',write_to_file = True):
    lines = open('example.txt').readlines()

    #extract first informations (login,semester,number of uvs, uvs)
    line = lines[0]
    data = re.findall(r'\w+', line)
    login = data[0]
    semester = data[1]
    number_of_uvs = data[2]
    uvs = data[3:]
    uvs_json = []

    DAYS = ['LUNDI','MARDI','MERCREDI','JEUDI','VENDREDI','SAMEDI']
    TYPES = {'C':'AMPHI','D':'TD','T':'TP'}

    #extract schedule of uvs
    for line in lines[1:]:
	if len(line) > 2: #not empty
	    data = re.findall(r'\w+', line)
	    uv = {'name':data[0]}
	    uv['type'] = TYPES[data[1]]
	    if is_number(data[2]):
		uv['grp'] = data[2]
		uv['day'] = data[3].replace('.','')
	    else:
		uv['day'] = data[2].replace('.','')
	    uv['hors'] = re.findall(r'\d?\d:\d\d', line)
	    i = line.find("S=")
	    uv['place'] = line[i+2:].replace('\n','').replace(' ','')
	    uvs_json += [uv]
    json_arr = {'login':login,'semester':semester,'theoric_number_of_uvs':number_of_uvs,'uvs':uvs_json}
    if write_to_file:
	json_file = open('utc.json','w')
	d = json.dump(json_arr,json_file, indent=4)
	json_file.write(str(d)[:-4])
	json_file.close()
    return json_arr
    
if __name__ == '__main__':
	main()
