import os
import sys

from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

from xgboost import XGBRFRegressor
from sklearn.ensemble import(
    AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    model_trainer_file_path_config = os.path.join('artifacts','model.pkl')

class ModelTrainer :
    def __init__(self):
        self.model_trainer_file_path = ModelTrainerConfig()
    
    def initiate_model_trainer_config (self, train_arr, test_arr):
        try:
            logging.info ('Split data into train and test successfully')
            X_train ,y_train , X_test ,y_test = train_arr[:,:-1], train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1]
            models = {
                "Linear Regression":LinearRegression(),
                "Decision Tree":DecisionTreeRegressor(),
                "RandomForest Regressor":RandomForestRegressor(),
                "XGBoost":XGBRFRegressor(),
                "AdaBoost":AdaBoostRegressor(),
                "GradientBoost":GradientBoostingRegressor()
            }
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "RandomForest Regressor":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "GradientBoost":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBoost":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "AdaBoost":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            model_report:dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models,param=params)
            
            best_model_name = max(model_report,key = lambda x: model_report[x]['r2_test'])
            best_model = model_report[best_model_name]['model']
            best_model_score = model_report[best_model_name]['r2_test']

            if best_model_score < 0.6 : 
                raise CustomException("No founded best model")
            logging.info("Best founded model in training and testing dataset")
            save_object(file_path= self.model_trainer_file_path.model_trainer_file_path_config,obj=best_model)


            pred = best_model.predict(X_test)

            r2_squared = r2_score(y_test,pred)
            return r2_squared
            
        except Exception as e:
            raise CustomException(e,sys)
            


