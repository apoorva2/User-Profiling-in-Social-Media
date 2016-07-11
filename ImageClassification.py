from PIL import Image
import numpy as np
from sklearn.decomposition import RandomizedPCA
import pandas as pd
import matplotlib.pyplot as pl
from sklearn.neighbors import KNeighborsClassifier
import glob


# setup a standard image size; this will distort some images but will get everything into the same shape
STANDARD_SIZE = (200, 140)


def img_to_matrix(img, verbose=False):

    if verbose is True:
        print("changing size from %s to %s" % (str(img.size), str(STANDARD_SIZE)))
    img = img.resize(STANDARD_SIZE)
    img = (list(img.getdata()))
    # img = map(list, img)
    img = np.array(img)
    return img

def flatten_image(img):
    s = img.shape[0] * img.shape[1]
    img_wide = img.reshape(1, s)
    return img_wide[0]

par_dir = "C:\\Users\\apoorva\\Desktop\\WINTER QUARTER\\Machine Learning\\Project\\"
img_dir_Train = par_dir+"FacebookDataTCSS555Project\\TCSS555\\Train\\Image_Debug\\*.jpg"
images = [f for f in glob.glob(img_dir_Train)]
labels = ["Female" if "Female" in f.split('/')[-1] else "Male" for f in images]

count = 0
data = []
for image in images:
    try:
        with Image.open(image) as img:
            img = img_to_matrix(img)
            img = flatten_image(img)
            data.append(img)
            count += 1
            print(str(count)+"."+image)

    except IndexError as e:
        with Image.open(image) as img:
            img = Image.new("RGB", img.size)
            img = img_to_matrix(img)
            img = flatten_image(img)
            data.append(img)


data = np.array(data)
y = np.where(np.array(labels) == "Male", '1', '0')
train_x, train_y = data, y
data = []
print("train data ready")

img_dir_Test = "C:\\Users\\apoorva\\Desktop\\Test\\Profile\\*.jpg"
images = [f for f in glob.glob(img_dir_Test)]
# labels = ["Female" if "Female" in f.split('/')[-1] else "Male" for f in images]



test_data = []
for image in images:
    try:
        with Image.open(image) as img:
            img = img_to_matrix(img)
            img = flatten_image(img)
            test_data.append(img)
            count += 1
            print(str(count)+"."+image)

    except IndexError as e:
        with Image.open(image) as img:
            img = Image.new("RGB", img.size)
            img = img_to_matrix(img)
            img = flatten_image(img)
            test_data.append(img)

test_data = np.array(test_data)

print("test data ready")

# test_y = np.where(np.array(labels) == "Male", '1', '0')
# test_x, test_y = test_data, test_y
test_x = test_data
print("Test_x and Test_y are ready")


pca = RandomizedPCA(n_components=6)
train_x.reshape(-1, 1)
train_x = pca.fit_transform(train_x)
test_x = pca.transform(test_x)

# print(train_x[:5])
knn = KNeighborsClassifier(10)
knn.fit(train_x, train_y)
# print(pd.crosstab(test_y, knn.predict(test_x), rownames=["Actual"], colnames=["Predicted"]))
print("called classify_image")
preds = knn.predict(test_x)
preds = np.where(preds==0, "Male", "Female")
# pred = preds[0]
print ("image_label: ", preds)



