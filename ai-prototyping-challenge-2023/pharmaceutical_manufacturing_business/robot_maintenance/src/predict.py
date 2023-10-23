import daal4py as d4p
import joblib
import os
# import pdb
import numpy as np
import pandas as pd

def inference(model, data, num_class: int = 3):
    
    # wrangle scaler name
    filename_without_extension = os.path.splitext(model)[0]
    scaler_path = filename_without_extension + '_scaler.joblib'
    
    # load robust scaler
    with open(scaler_path, "rb") as fh:
        robust_scaler = joblib.load(fh.name)
    
    # load daal model
    with open(model, "rb") as fh:
        daal_model = joblib.load(fh.name)
        
    # process data sample
    Categorical_Variables = pd.get_dummies(
                           data[[
                               'Manufacturer',
                               'Generation',
                               'Lubrication',
                               'Product_Assignment']],
                           drop_first=False)
    data = pd.concat([data, Categorical_Variables], axis=1)
    data.drop(['Manufacturer', 'Generation', 'Lubrication', 'Product_Assignment'], axis=1, inplace=True)

    data = data.astype({'Motor_Current': 'float64', 'Number_Repairs': 'float64'})
    
    
    number_samples = data.select_dtypes(['float', 'int', 'int32'])
    scaled_samples = robust_scaler.transform(number_samples)
    scaled_samples_transformed = pd.DataFrame(scaled_samples,
                                                 index=number_samples.index,
                                                 columns=number_samples.columns)
    del scaled_samples_transformed['Number_Repairs']
    data = data.drop(['Age', 'Temperature', 'Last_Maintenance', 'Motor_Current'], axis=1)
    data = data.astype(int)
    processed_sample = pd.concat([scaled_samples_transformed, data], axis=1)
    processed_sample = processed_sample.astype({'Motor_Current': 'float64'})
    
    
    column_names = ['Age', 'Temperature', 'Last_Maintenance', 'Motor_Current',
                'Number_Repairs', 'Manufacturer_A', 'Manufacturer_B',
                'Manufacturer_C', 'Manufacturer_D', 'Manufacturer_E', 'Manufacturer_F',
                'Manufacturer_G', 'Manufacturer_H', 'Manufacturer_I', 'Manufacturer_J',
                'Generation_Gen1', 'Generation_Gen2', 'Generation_Gen3',
                'Generation_Gen4', 'Lubrication_LTA', 'Lubrication_LTB',
                'Lubrication_LTC', 'Product_Assignment_PillA',
                'Product_Assignment_PillB', 'Product_Assignment_PillC']

    zeroes_dataframe = pd.DataFrame(0, index=np.arange(1), columns=column_names)
    merged_df = pd.merge(zeroes_dataframe, processed_sample, on=processed_sample.columns.tolist(), how='right').fillna(0)

        
    # perform inference
    daal_predict_algo = d4p.gbt_classification_prediction(
            nClasses=num_class,
            resultsToEvaluate="computeClassLabels",
            fptype='float')
            
    daal_prediction = daal_predict_algo.compute(merged_df, daal_model)
    
    for prediction in daal_prediction.prediction[:, 0]:
        if prediction == 0:
            status = 'Equipment Does Not Require Scheduled Maintenance'
            return status
        elif prediction == 1:
            status = 'Equipment Requires Scheduled Maintenance - Plan Accordingly'
            return status
            
    return status