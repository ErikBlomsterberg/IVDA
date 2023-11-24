from sklearn.linear_model import LinearRegression, SGDRegressor
import numpy as np

model = SGDRegressor() #solution 1
#model = LinearRegression() #solution 2

def update_model(x, y):
    model.partial_fit(x, y) #solution 1
    #model.fit(x, y) #solution 2
    return 

def predict_rating(x):
    y_pred = model.predict(x)
    return y_pred