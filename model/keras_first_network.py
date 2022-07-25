# first neural network with keras tutorial
from numpy import loadtxt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
# load the dataset
input = loadtxt('data.csv', delimiter=',', usecols=[0,1,2,3,4])
letter = loadtxt('data.csv', dtype=str, delimiter=",",usecols=[5])

# split into input (X) and output (y) variables
X = input[:,0:4]
y = letter[:,0]

# define the keras model
model = Sequential()
model.add(Dense(21, input_shape=(5,), activation='relu'))
model.add(Dense(26, activation='softmax'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
model.fit(X, y, epochs=150, batch_size=10)
# make class predictions with the model
predictions = (model.predict(X) > 0.5).astype(int)
# summarize the first 5 cases
for i in range(5):
	print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))