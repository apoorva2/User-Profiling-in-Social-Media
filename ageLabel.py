#!/usr/bin/python

import csv
import facebook
import requests
import traceback
import sys
import os
import argparse

def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with
    result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return result

def parse_args():
    parser = argparse.ArgumentParser(description="""Script takes full input path to
                         test directory, output directory and training directory""")

    parser.add_argument('-d',
                        "--training_dir",
                        default='',
                        type=str,
                        help='Full path to input trainig directory')


    args = parser.parse_args()
    return args

def run(training_dir):
    faceargs = {'fields' : 'id,name,likes,category', }
    graph = facebook.GraphAPI(get_fb_token(1158759920825300,"20e776e34570246acf2321b5abd1e991"))
    profileFilePath = os.path.join(training_dir, "profile\\profile.csv")
    profileFile = open(profileFilePath,'r')
    ageInputFilePath = os.path.join(training_dir, "ageInfo\\ageInput.csv")
    ageInputFile = open(ageInputFilePath,'wb')
    fieldnames = ['PageID','Page_Name','PageCategory','Likes','userid','ageLabel','age','Gender','open','con','ext','agr','neu']
    fileWriter = csv.DictWriter(ageInputFile,fieldnames)
    fileWriter.writeheader()
    errorFile = open('Error.csv','w')
    profileRow = {}
    profileRow['userid'] = ""
    firstRound = "true"
    pageName = ""
    pageCategory = ""
    count = 0


    with open(training_dir +'\Relation\Relation.csv','r') as relationFile:
        fileReader = csv.DictReader(relationFile)
        for row in fileReader:
            count += 1
            print (row['userid'], count)
            try:
                page = graph.get_object(row['like_id'],**faceargs)
                if row['userid'] != profileRow['userid']:
                    if firstRound == "false":
                        try:
                            # pageName.encode('utf-8')
                            # pageCategory.encode('utf-8')
                            fileWriter.writerow({'PageID':page['id'], 'Page_Name':pageName.encode('utf-8'),'PageCategory':pageCategory.encode('utf-8'), 'Likes':page['likes'], 'userid':profileRow['userid'],'ageLabel':ageLabel, 'age': profileRow['age'], 'Gender':profileRow['gender'], 'open': round(float(profileRow['ope'])/0.25) * 0.25, 'con':round(float(profileRow['con'])/0.25) * 0.25, 'ext': round(float(profileRow['ext'])/0.25) * 0.25, 'agr': round(float(profileRow['agr'])/0.25) * 0.25, 'neu': round(float(profileRow['neu'])/0.25) * 0.25})
                            pageName = ""
                            pageCategory = ""
                        except Exception as e:
                            errorFile.write("error with id {0}, error {1}\n".format(row['userid'],traceback.format_exception(*sys.exc_info())))

                    with open(training_dir +'\Profile\Profile.csv','r') as profileFile:
                        profileReader = csv.DictReader(profileFile)
                        for profileRow in profileReader:
                            if (row['userid'] == profileRow['userid']):
                                if (18 <= float(profileRow['age']) <= 24):
                                    ageLabel = 'A'
                                if (25 <= float(profileRow['age']) <= 34):
                                    ageLabel = 'B'
                                if (35 <= float(profileRow['age']) <= 49):
                                    ageLabel = 'C'
                                if (float(profileRow['age']) >= 50):
                                    ageLabel = 'D'

                                firstRound = "false"
                                pageName = pageName + " " + page['name']
                                pageCategory = pageCategory + " " + page['category']
                                break
                else:
                    pageName = pageName + " " + page['name']
                    pageCategory = pageCategory + " " + page['category']

            except facebook.GraphAPIError as error:
                errorFile.write("error with id {0}, error {1}\n".format(row['userid'],str(error.message)))
            except Exception as e:
                errorFile.write("error with id {0}, error {1}\n".format(row['userid'],traceback.format_exception(*sys.exc_info())))


    profileFile.close()
    ageInputFile.close()
    errorFile.close()

def main(args):
   run(args.training_dir)

if __name__ == "__main__":
    args = parse_args()
    main(args)

