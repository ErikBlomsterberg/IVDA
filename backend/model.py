from sklearn.linear_model import LinearRegression, SGDRegressor
import numpy as np

#model = LinearRegression() #solution 2
model = SGDRegressor()

def update_model(x, y):
    model.partial_fit(x, y)
    #model.fit(x, y) #solution 2
    return 

def predict_rating(x):
    y_pred = model.predict(x)
    return y_pred