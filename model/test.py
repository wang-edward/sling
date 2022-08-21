from tensorflow import keras

import pandas
import json
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.datasets import make_blobs
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

model = keras.models.load_model('.')

dataframe2 = pandas.read_csv("random_data.csv", header=None)
dataset2 = dataframe2.values
#xNew = dataset2[:,0:5].astype(float)
xNew = [[0.0, 0.0, 0.0, 0.0, 0.0]]
yNew = model.predict(xNew)

# find largest number in each instance of yNew to get the correct letter
index_of_largest = [0] * len(xNew)
for i in range(len(xNew)):
	max = yNew[i][0]
	index_of_largest[i] = 0
	for j in range(1,len(yNew[i])):
		if yNew[i][j] > max:
			max = yNew[i][j]
			index_of_largest[i] = j

with open("alphabet.json", "r") as read_file:
	alphabet_dict = json.load(read_file)
	# show the inputs and predicted outputs
	for i in range(len(xNew)):
		print("X=%s, Predicted=%s" % (xNew[i], alphabet_dict[str(index_of_largest[i])]))

