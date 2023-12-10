from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.metrics import mean_squared_error, r2_score

#model = SGDRegressor() #solution 1
model = LinearRegression() #solution 2

def update_model(x, y):
    #model.partial_fit(x, y) #solution 1
    model.fit(x, y) #solution 2
    return 

def predict_rating(x):
    y_pred = model.predict(x)
    return y_pred

def model_error(y_label, y_pred):
    #error_mse = mean_squared_error(y_label, y_pred)
    error_r2 = r2_score(y_label, y_pred)
    return error_r2
