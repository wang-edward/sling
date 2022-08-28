# multi-class classification with Keras
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

import numpy as np

dataframe = pandas.read_csv("id_data.csv", header=None)
dataset = dataframe.values
X = dataset[:,0:5].astype(float)
Y = dataset[:,5]

encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

print(X)
print(Y)

# define baseline model
	# create model
model = Sequential()
model.add(Dense(15, input_dim=5, activation='relu'))
model.add(Dense(20, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'], run_eagerly=True)

model.fit(X,dummy_y, epochs = 50, batch_size=1 )

model.save('.')

# new instances where we do not know the answer
dataframe2 = pandas.read_csv("random_data.csv", header=None)
dataset2 = dataframe2.values
xNew = dataset2[:,0:5].astype(float)
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
#kfold = KFold(n_splits=10, shuffle=True)
#results = cross_val_score(estimator, X, dummy_y, cv=kfold)
#print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
