# User Profiling based on Facebook Page Likes and Profile Pictures 
*****Implementation Language: Python 
*****Prerequisites and Input Data: 
1. Training Data Folder Structure – 
Training\
Training\Images\<All images here>
Training\Profile\Profile.csv <This file has all userid and labels mapped>
Training\Relation\relation.csv<This file has one-to-many mappings between users
and facebook PageIDs they have liked>
 
2. Test data will have a similar folder structure.
 
3. All images are to be in .jpg format.
 
4. Important Python Packages required:
NLTK packages for Naïve Bayes classifier
Numpy for np arrays in images
PIL for image manipulation.
sklearn.decomposition for Randomized PCA
sklearn.neighbors for KNN classifier.
facebook API to get page information based o PageIDs
 
****Basic flow:  
1.  LikeID classification:
 The code for this implemented in the following files: 

<getPageInfoLikeID.py> This is mainly for data preparation. 
 We are provided with one-to-many mapping of each user-ID and all the facebook
page IDs (of pages) that user has liked. We use the Facebook’s APIs to extract the
required information about the page like page name and category. We use these
features and train the data further using Naïve Bayes classifier.  
<ageLabel.py>This will have the classifiers methods that will train the prepared data
and also predict the test data. 
2. Image: 
<DataPreperation.py> This is used to create image files with gender and age 
information.  
<ImageClassification.py> This is where we train and predict the labels based for
images. 
Following are steps used : 
Prepare the data to map Image and corresponding gender and image and corresponding age
range. 
We loop through each image and for each image:
Standardize the image to a particular size, say 100x100, this means we will have 10000 
pixels for the image.
For each pixel extract the RGB values and store all of them in an nx3 array (where n= no. 
of pixels, 3 is (R, G, B) value)
All these values are stored in a higher dimensional np array which will store the RGB 
values for all the pixels of all images.
In case the image is black & white then we store the intensity of the pixels across R, G, B 
which will be 255. 
Now that we have the np array that has all the RGB values of all pixels of images, this becomes a 
huge dataset to be classified. Hence we use RandomizedPCA to summarize the dataset. 
We bring down the dimensionality of each image (which was 10000x3=3000) to 5.
We run a K- Nearest Neighbor classifier to classify the summarized data with corresponding 
labels. We have used the no. of components=10.
We can now start predicting the output using this classifier. 
 
**** Output: 
 XML files will be generated for each of the data in the output folder with labels in the following
format:  
Command Arguments: tcss555 -i path/to/test/my-test-data -o path/to/output/directory  
There will be one file for each user (named by userID) in the following format:
<userId="{user-id}" 
age_group="18-24|25-34|35-49|50-xx" 
gender="male|female"
extrovert="1 to 5" 
neurotic="1 to 5" 
agreeable="1 to 5" 
conscientious="1 to 5" open="1 to 5" /> 
 
 
 
User Profiling based on Facebook Status Messages: Text
Classification 
*****Implementation Language: Python 
*****Prerequisites and Input Data: 
1. Training Data Folder Structure – 
Training\
Training\Profile\Profile.csv <This file has all userid and labels mapped>
Training\LIWC.csv <This file has all the word counts and ratios of status messages
for users in profile> 
2. Test data will have a similar folder structure.
 
3. Important Python Packages required:
Pandas
Scikit-Learn 
****Basic flow:  
Text Classification:  
- The code for this implemented in the following files: 
<TCSS555.py> this is the code for text classification into Age, gender and
personality traits.  This code will train the data using Random Forest Classifier for 
Age and gender and Linear regression for Personality traits. The classifiers then is
used to predict the age, gender and personality traits for the test data. 

- <GenderClassification.py> This code will take status messages as input and 
predicts Gender by using manually constructed Naïve Bayes Classifier.
 
- <AgeClassification.py> This code will take status messages as input and predicts
Age by using manually constructed Naïve Bayes Classifier.
 
- <Age_Classification.py> This code will take status messages as input and predicts
Age, Gender by using manually constructed Random Forest Classifier.
 
- <Personality_Traits.py> This code will take status messages as input and
predicts personality traits by using Linear Regression. 
 
**** Output: 
 XML files will be generated for each of the data in the output folder with labels in the following
format:  
Command Arguments: tcss555 -i path/to/test/my-test-data -o path/to/output/ 
There will be one file for each user (named by userID) in the following format:
<userId="{user-id}" 
age_group="18-24|25-34|35-49|50-xx" 
gender="male|female"
extrovert="1 to 5" 
neurotic="1 to 5" 
agreeable="1 to 5" 
conscientious="1 to 5" 
open="1 to 5" /> 
 
*****************************************************END*************************************** 
