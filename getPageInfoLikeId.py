#!/usr/bin/python
import argparse
import os
from os.path import exists
import traceback
from textblob.classifiers import NaiveBayesClassifier
from textblob import formats
from xml.etree import ElementTree
import json
import sys
import random
import facebook
import requests
from sklearn.cross_validation import train_test_split


class PipeDelimitedFormat(formats.DelimitedFormat):
    delimiter = '|'

formats.register('psv', PipeDelimitedFormat)
errorFile = open('Error.csv','w')


separator="|"
processed_data="processed_data.psv"
processed_age_data = "processed_age_data.psv"

reload(sys)
#sys.setdefaultencoding("utf-8")

import csv
def get_fb_token(app_id, app_secret):
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': app_secret}
    file = requests.post('https://graph.facebook.com/oauth/access_token?', params = payload)
    #print file.text #to test what the FB api responded with
    result = file.text.split("=")[1]
    #print file.text #to test the TOKEN
    return result


def prepare_training_data(training_data_dir):
    f = open(processed_data,'w+')
    profile_file_path = os.path.join(training_data_dir, "profile\\profile.csv")
    print (profile_file_path)
    counter = 0
    with open(profile_file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if counter > 100:
                break
            uuid = row['userid']
            if exists(os.path.join(training_data_dir, "text", uuid+".txt")):
                train_file = os.path.join(training_data_dir, "text", uuid+".txt")
                with open(train_file, "r+") as fo:
                    try:
                        file_content = fo.read().strip()
                        file_content = file_content.replace(r"|"," ")
                        file_content = file_content.replace(r"\n", " ")
                        values = file_content.split()

                        f.write(" ".join(values)+separator+row['gender']+"\n")
                    except UnicodeDecodeError:
                        print("Bad data")
                counter += 1
    f.close()
    csvfile.close()

def prepare_age_training_data(training_data_dir, label, processedFile):
    ageInputFilePath = os.path.join(training_data_dir,"ageInfo\\ageInput.csv")
    if not (exists (ageInputFilePath)):
        os.system("ageLabel " + training_data_dir)# agelabel.py
    f = open(processedFile,'w+')
    counter = 0
    with open(ageInputFilePath) as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            if counter > 20:
                break
            uuid = row['userid']
            try:
                file_content = row['Page_Name'] + " " + row['PageCategory']
                file_content = file_content.replace(r"|"," ")
                file_content = file_content.replace(r"\n", " ")
                values = file_content.split()

                f.write(" ".join(values)+separator+row[label]+"\n")
            except UnicodeDecodeError:
                print("Bad data")
            counter += 1
    f.close()

def getLikeinfo(userid, test_data_dir):
    relationFilePath = os.path.join(test_data_dir,"Relation\\Relation.csv")
    faceargs = {'fields' : 'id,name,likes,category', }
    graph = facebook.GraphAPI(get_fb_token(1158759920825300,"20e776e34570246acf2321b5abd1e991"))
    returnValue = ""
    with open (relationFilePath, 'r') as relationFile:
        fileReader = csv.DictReader(relationFile)
        for row in fileReader:
            if (row['userid'] == userid):
                try:
                    page = graph.get_object(row['like_id'],**faceargs)
                    returnValue = returnValue + " " + page['name'] + " " + page['category']
                except facebook.GraphAPIError as error:
                    errorFile.write("error with id {0}, error {1}\n".format(row['userid'],str(error.message)))
                except Exception as e:
                    errorFile.write("error with id {0}, error {1}\n".format(row['userid'],traceback.format_exception(*sys.exc_info())))

    return returnValue


def predict_and_write(ageClassifier_obj, genClassifier_obj, opeClassifier_obj, conClassifier_obj, extClassifier_obj, agrClassifier_obj, neuClassifier_obj, test_data_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
#Create a csv file to store out data
    outputdatafile = open('OutputData.csv','wb')
    fieldnames = ['UserID','Gender']
    fileWriter = csv.DictWriter(outputdatafile,fieldnames)
    fileWriter.writeheader()
#Create Output XML files
    profile_file_path = os.path.join(test_data_dir, "profile\\profile.csv")
    print (profile_file_path)
    with open(profile_file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            uuid = row['userid']
            try:
                file_content = getLikeinfo(uuid, test_data_dir).strip()
                predictedAge = ageClassifier_obj.classify(file_content)
                predictedGender = genClassifier_obj.classify(file_content)
                predictedOpen = opeClassifier_obj.classify(file_content)
                predictedCon = conClassifier_obj.classify(file_content)
                predictedExt = extClassifier_obj.classify(file_content)
                predictedAgr = agrClassifier_obj.classify(file_content)
                predictedNeu = neuClassifier_obj.classify(file_content)
                # print("Prediction ", prediction )
            except Exception as e:
                predictedAge = 'C'
                predictedGender = "1.0"
                predictedOpen = str(round(random.uniform(3.5, 4.3),1))
                predictedCon = str(round(random.uniform(3.5, 4.3),1))
                predictedExt = str(round(random.uniform(3.5, 4.3),1))
                predictedAgr = str(round(random.uniform(3.5, 4.3),1))
                predictedNeu = str(round(random.uniform(3.5, 4.3),1))

            if (predictedAge == 'A'):
                ageGroup = "18-24"
            if (predictedAge == 'B'):
                ageGroup = "25-34"
            if (predictedAge == 'C'):
                ageGroup = "35-49"
            if (predictedAge == 'D'):
                ageGroup = "50+"
            output_file = os.path.join(output_dir, uuid+".xml")
            with open(output_file, "w") as out_f:
                attrs = {'userId': uuid,
                         'gender' : "female" if predictedGender == "1.0" else "male",
                         'age_group' : ageGroup,
                         'extrovert' : predictedExt,
                         "neurotic" :  predictedNeu,
                         "agreeable" : predictedAgr,
                         "conscientious" : predictedCon,
                         "open" : predictedCon
                         }
                tree = ElementTree.Element('', attrs)
                out_f.write(ElementTree.tostring(tree))
                # fileWriter.writerow({'UserID':uuid, 'Gender':prediction[1]})


def jsonify(fileName):
    csvfile = open(fileName, 'r')
    jsonFileName = fileName + ".json"
    jsonfile = open(jsonFileName, 'w+')
    result = []
    fieldnames = ("text","label")
    reader = csv.DictReader(csvfile, fieldnames, delimiter = '|')
    for row in reader:
        try:
            row['text'] = row['text'].encode("ascii", errors="ignore")
            result.append(row)
            print(row)
        except UnicodeDecodeError:
            print("Bad unicode data in jsonify")

    print(result)
    json.dump(result, jsonfile)
    return jsonFileName


def train_model(json_data_file):
    """
    Given a json file, train the data and return the classifier.
    """

    with open(json_data_file, 'r') as fp:
        cl = NaiveBayesClassifier(fp, format="json")
        return cl


def run(training_dir, test_dir, output_dir):
    # data preperation
    prepare_age_training_data(training_dir, "ageLabel", "ageFile") # age
    json_file_name = jsonify("ageFile")
    ageClassifier = train_model(json_file_name)
    prepare_age_training_data(training_dir, "Gender", "genderFile") # age
    json_file_name = jsonify("genderFile")
    genClassifier = train_model(json_file_name)
    prepare_age_training_data(training_dir, "open", "opeFile") # age
    json_file_name = jsonify("opeFile")
    opeClassifier = train_model(json_file_name)
    prepare_age_training_data(training_dir, "con", "conFile") # age
    json_file_name = jsonify("conFile")
    conClassifier = train_model(json_file_name)
    prepare_age_training_data(training_dir, "ext", "extFile") # age
    json_file_name = jsonify("extFile")
    extClassifier = train_model(json_file_name)
    prepare_age_training_data(training_dir, "agr", "agrFile") # age
    json_file_name = jsonify("agrFile")
    agrClassifier = train_model(json_file_name)
    prepare_age_training_data(training_dir, "neu", "neuFile") # age
    json_file_name = jsonify("neuFile")
    neuClassifier = train_model(json_file_name)
    predict_and_write(ageClassifier, genClassifier, opeClassifier, conClassifier, extClassifier, agrClassifier, neuClassifier, test_dir, output_dir)


def main(args):
   run(args.training_dir, args.test_dir, args.output_dir)

def parse_args():
    parser = argparse.ArgumentParser(description="""Script takes full input path to
                         test directory, output directory and training directory""")

    parser.add_argument('-i',
                        "--test_dir",
                        type=str,
                        required=True,
                        help='Full path to input test directory containing profile and text dir')

    parser.add_argument('-o', "--output_dir",
                        type=str,
                        required=True,
                        help='The path to output directory')


    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    args.training_dir = "data\\training\\"
    # if args.test_dir:
    #     args.test_dir = "Public Test"
    main(args)
