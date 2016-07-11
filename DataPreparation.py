import csv
import facebook
import requests
import traceback
import sys
import glob
import shutil


par_dir = "C:\\Users\\apoorva\\Desktop\\WINTER QUARTER\\Machine Learning\\Project\\"
img_dir_Train = par_dir+"FacebookDataTCSS555Project\\TCSS555\\Train\\Image\\*.jpg"
destination_directory = par_dir + "FacebookDataTCSS555Project\\TCSS555\\Train\\Image\\Renamed\\"
count = 0
for fileName in glob.glob(img_dir_Train):
    with open('Profile.csv', 'r') as profileFile:
        profileReader = csv.DictReader(profileFile)
        for profileRow in profileReader:
            if fileName.split('\\')[-1].split('.')[0] == profileRow['userid']:
                value = "Female" if profileRow['gender'] == "1.0" else "Male"
                destination_file = destination_directory + value + '_' + profileRow['age'] + '_' + str(count) + ".jpg"
                shutil.copy(fileName, destination_file)
                count += 1
                break






