# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

'''
Module to train and prediction using XGBoost Classifier
'''
# !/usr/bin/env python
# coding: utf-8
# pylint: disable=import-error
import daal4py as d4p
import sys
import numpy as np
import xgboost as xgb
import pandas as pd 
import logging
import warnings
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearnex import patch_sklearn
patch_sklearn()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
warnings.filterwarnings("ignore")


class RoboMaintenance():
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.file = ''
        self.y_train = ''
        self.y_test = ''
        self.X_train_scaled_transformed = ''
        self.X_test_scaled_transformed = ''
        self.d4p_model = ''
        self.accuracy_score = ''
        self.model_path = ''
        self.parameters = ''
        self.robust_scaler = ''
        
    def process_data(self, file: str, test_size: int = .25):
        """_summary_

        Parameters
        ----------
        file : str
            _description_
        test_size : int, optional
            _description_, by default .25
        """

        # Generating our data
        logger.info('Reading the dataset from %s...', file)
        try:
            data = pd.read_pickle(file)
        except FileNotFoundError:
            sys.exit('Dataset file not found')


        X = data.drop('Asset_Label', axis=1)
        y = data.Asset_Label

        X_train, X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size)

        df_num_train = X_train.select_dtypes(['float', 'int', 'int32'])
        df_num_test = X_test.select_dtypes(['float', 'int', 'int32'])
        self.robust_scaler = RobustScaler()
        X_train_scaled = self.robust_scaler.fit_transform(df_num_train)
        X_test_scaled = self.robust_scaler.transform(df_num_test)

        # Making them pandas dataframes
        X_train_scaled_transformed = pd.DataFrame(X_train_scaled,
                                                  index=df_num_train.index,
                                                  columns=df_num_train.columns)
        X_test_scaled_transformed = pd.DataFrame(X_test_scaled,
                                                 index=df_num_test.index,
                                                 columns=df_num_test.columns)

        del X_train_scaled_transformed['Number_Repairs']

        del X_test_scaled_transformed['Number_Repairs']

        # Dropping the unscaled numerical columns
        X_train = X_train.drop(['Age', 'Temperature', 'Last_Maintenance', 'Motor_Current'], axis=1)
        X_test = X_test.drop(['Age', 'Temperature', 'Last_Maintenance', 'Motor_Current'], axis=1)
        
        X_train = X_train.astype(int)
        X_test = X_test.astype(int)

        # Creating train and test data with scaled numerical columns
        X_train_scaled_transformed = pd.concat([X_train_scaled_transformed, X_train], axis=1)
        X_test_scaled_transformed = pd.concat([X_test_scaled_transformed, X_test], axis=1)

        self.X_train_scaled_transformed = X_train_scaled_transformed.astype(
                                        {'Motor_Current': 'float64'})
        self.X_test_scaled_transformed = X_test_scaled_transformed.astype(
                                        {'Motor_Current': 'float64'})
        

    def train(self, ncpu: int = 4):
        """_summary_

        Parameters
        ----------
        ncpu : int, optional
            _description_, by default 4
        """
        
        # Set xgboost parameters
        self.parameters = {
        'max_bin': 256,
        'scale_pos_weight': 2,
        'lambda_l2': 1,
        'alpha': 0.9,
        'max_depth': 8,
        'num_leaves': 2**8,
        'verbosity': 0,
        'objective': 'multi:softmax',
        'learning_rate': 0.3,
        'num_class': 3,
        'nthread': ncpu
        }
        
        xgb_train = xgb.DMatrix(self.X_train_scaled_transformed, label=np.array(self.y_train))
    
        xgb_model = xgb.train(self.parameters, xgb_train, num_boost_round=100)
        self.d4p_model = d4p.get_gbt_model_from_xgboost(xgb_model)
        

    def validate(self):
        """_summary_

        Returns
        -------
        _type_
            _description_
        """
        daal_predict_algo = d4p.gbt_classification_prediction( 
            nClasses=self.parameters["num_class"],
            resultsToEvaluate="computeClassLabels",
            fptype='float')
            
        daal_prediction = daal_predict_algo.compute(self.X_test_scaled_transformed, self.d4p_model)
        
        daal_errors_count  = np.count_nonzero(daal_prediction.prediction[:, 0] - np.ravel(self.y_test))
        self.d4p_acc = abs((daal_errors_count  / daal_prediction.prediction.shape[0]) - 1)
        

        print('=====> XGBoost Daal accuracy score %f', self.d4p_acc)
        print('DONE')
        return self.d4p_acc
    
    def save(self, model_path):
        """_summary_

        Parameters
        ----------
        model_path : _type_
            _description_
        """

        self.model_path = model_path +  self.model_name + '.joblib'
        self.scaler_path = model_path +  self.model_name + '_scaler.joblib'
        
        logger.info("Saving model")
        with open( self.model_path, "wb") as fh:
            joblib.dump(self.d4p_model, fh.name)
        
        logger.info("Saving Scaler")
        with open( self.scaler_path, "wb") as fh:
            joblib.dump(self.robust_scaler, fh.name)