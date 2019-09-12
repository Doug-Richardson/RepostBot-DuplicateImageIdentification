#Ah shit here we go again.
#This function takes a directory of images and outputs a directory of normalized images.
import numpy as np
import os
from PIL import Image


Normalize_X = 128
Normalize_Y = 128
input_file_directory = "Memelist_New/"
output_file_directory = "Memelist_Normalized/"

list_of_files = os.listdir(input_file_directory)
print(list_of_files)

for input_file in list_of_files:
	input_file_name =  input_file_directory + input_file
	output_file_name = output_file_directory + input_file
	#\ Doesn't work for filepath, use / instead.
	src = None
	output = None
	try:
		src = Image.open(input_file_name)
	except IOError:
		print("File could not be opened!")
	except:
		print("Something went rather wrong.")
		
	# Check if image is loaded fine
	if src is None:
		print ('Error opening image!')
		exit()
	output = src.resize((Normalize_X,Normalize_Y))
	output.save(output_file_name)
	src.close()
	try:
		os.remove(input_file_name)
	except PermissionError:
		print("File is 'in use', I doubt that but whatever")
print("Done.")
