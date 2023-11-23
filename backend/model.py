from sklearn.linear_model import LinearRegression, SGDRegressor

#model = LinearRegression()
model = SGDRegressor()

def update_model(x, y):
    model.partial_fit(x, y)
    return 

def predict_rating(x):
    y_pred = model.predict(x)
    return y_pred