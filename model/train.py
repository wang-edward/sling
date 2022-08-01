# multi-class classification with Keras
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

import numpy as np

dataframe = pandas.read_csv("finger_data.csv", header=None)
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

model.fit(X,dummy_y, batch_size=1 )

# A few random samples
use_samples = [5, 38, 20, 13, 20]
samples_to_predict = []

# Convert into Numpy array
samples_to_predict = np.array(samples_to_predict)

model.predict(samples_to_predict)

#kfold = KFold(n_splits=10, shuffle=True)
#results = cross_val_score(estimator, X, dummy_y, cv=kfold)
#print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
