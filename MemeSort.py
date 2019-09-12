import numpy as np
import os
from PIL import Image
import subprocess

def CloseMatch(pair1, pair2):
	Fuzzy = 30
	if (pair1[0] == pair2[0] and pair1[1] == pair2[1] and pair1[2] == pair2[2]):
		return True
	else:
		if (pair1[0] + Fuzzy >= pair2[0] and pair1[0] - Fuzzy <= pair2[0]):
			if (pair1[1] + Fuzzy >= pair2[1] and pair1[1] - Fuzzy <= pair2[1]):
				if (pair1[2] + Fuzzy >= pair2[2] and pair1[2] - Fuzzy <= pair2[2]):
					return True
		return False

#def RangeMatch(image1, image2, x, y, given_range):
#	for newx in range(0,given_range)
#	CloseMatch(rgb_im.getpixel((x,y)),rgb_test.getpixel((x,y)))

input_file = ""
input_file_directory = "Memelist_Normalized/"
output_file_directory = "Memelist_Archives/"
unacceptability = 0.94

list_of_input_files = os.listdir(input_file_directory)

for input_file in list_of_input_files:
	input_file_name = input_file_directory+input_file
	print("Starting " + input_file_name)
	nrm = None
	try:
		nrm = Image.open(input_file_name)
	except IOError:
		print("File could not be opened!")
		exit()
	except:
		print("Something went rather wrong.")
		exit()

	list_of_archived_files = os.listdir(output_file_directory)
	Worst_Offender = ""
	Worst_Match = -1
	cycle = 0
	max_cycle = 30
	for test_file in list_of_archived_files:
		if (cycle == 0):
			print('.', end = '', flush = True)
		cycle += 1
		if (cycle >= max_cycle):
			cycle = 0
			
		test_image = None
		try:
			nrm_test = Image.open(output_file_directory+test_file)
		except IOError:
			print("File could not be opened!")
			exit()
		except:
			print("Something went rather wrong.")
			exit()
		rgb_test = nrm_test.convert('RGB')
		rgb_im = nrm.convert('RGB')
		if (rgb_test.size[0] != rgb_im.size[0] or rgb_test.size[1] != rgb_im.size[1]):
			print("Mismatched normalized sizes!")
			print(output_file_directory+test_file)
			print(input_file_name)
			exit()
		Matched = 0
		Total = 0
		for x in range(0,rgb_im.size[0]):
			for y in range(0,rgb_im.size[1]):
				#print(x, y, "Attempting...")
				if (CloseMatch(rgb_im.getpixel((x,y)),rgb_test.getpixel((x,y)))):
					Matched += 1
				Total += 1
		#print("Matched:"+ str(Matched))
		#print("Total:" + str(Total))
		ratio = Matched / Total
		#print("%Match = " + str(ratio))
		if (Worst_Match < ratio):
			Worst_Match = ratio
			Worst_Offender = test_file
	print("\nFinished analyzing:" + input_file)
	print("Worst Offender = " + Worst_Offender)
	print("Match ratio:" + str(Worst_Match))
	#If it is not above the unacceptability threshold.
	if Worst_Match < unacceptability:
		nrm.save(output_file_directory + input_file)
		nrm.close()
		try:
			os.remove(input_file_name)
		except PermissionError:
			print("File is 'in use', I doubt that but whatever")
	else:
		#THIS IS A REPOST
		print("Repost Detected, please handle.")