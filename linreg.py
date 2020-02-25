import numpy as np
import pandas as pd
from numpy.linalg import inv
from numpy import matmul
from collections import OrderedDict

from sklearn.linear_model import LinearRegression

class AnalysisDataAndFitLinearRegression:

    def __init__(self):
        self.version = 1

    @staticmethod
    def fit_sklearn(df, target):
        X = df.drop(columns=[target])
        y = df[target]
        reg = LinearRegression(fit_intercept=True).fit(X, y)
        print(f"\n sklearn Betas:\n{reg.coef_}")
        return reg

    @staticmethod
    def fit(df, target):

        # print(AnalysisDataAndFitLinearRegression.fit_sklearn(df,target))

        df = df.assign(Intercept=1)
        inputs = df.drop(columns=[target])
        keys = inputs.columns.insert(0, 'Intercept')

        X = inputs.values
        y = df[target]

        X_t = X.transpose()

        betas = matmul(matmul(inv(matmul(X_t, X)), X_t), y)
        betas_keyed = OrderedDict(zip(keys, betas))
        # print(f"\n Analytical Betas:\n{betas_keyed}")

        return betas_keyed

    @staticmethod
    def tax_stats(df, stats=('mean', 'std', '50%', 'min', 'max')):

        #  mean, standard deviation, median, minimum and maximum
        # two bathrooms and four bedrooms
        filtered = df[(df.Bathroom == 2) & (df.Bedroom == 4)]
        desc = filtered['Tax'].describe()
        return [desc[s] for s in stats]

    @staticmethod
    def predict(coefficients: OrderedDict, house: dict):
        price = 0
        for name, value in house.items():
            price += coefficients[name] * value
        return price

    def analyse_and_fit_lrm(self, path):
        # a path to a dataset is "./data/realest.csv"
        df = pd.read_csv(path).dropna()

        summary_dict = {
            'statistics': self.tax_stats(df),
            'data_frame': df[df.Space > 800],
            'number_of_observations': len(df[df.Lot >= df.Lot.quantile(.8)])
        }

        coefficients = self.fit(df, 'Price')

        house = {
            'Intercept':1,
            'Bedroom': 3,
            'Space': 1500,
            'Room': 8,
            'Lot': 40,
            'Tax': 1000,
            'Bathroom': 2,
            'Garage': 1,
            'Condition': 0
        }

        regression_dict = {
            'model_parameters': coefficients.values(),
            'price_prediction': self.predict(coefficients, house)
        }

        return {
            'summary_dict': summary_dict,
            'regression_dict': regression_dict
        }


model = AnalysisDataAndFitLinearRegression()
result = model.analyse_and_fit_lrm("./data/realest.csv")
print(result['summary_dict']['statistics'])