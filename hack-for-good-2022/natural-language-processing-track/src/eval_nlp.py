import pandas as pd
from transformers import DistilBertTokenizerFast
import torch
import time
from optimum.intel.neural_compressor.quantization import IncQuantizedModelForSequenceClassification
from transformers import DistilBertForSequenceClassification


def model_load_int8(local_directory_to_config,device):
    '''
    Function to load int8 model. config.json and pytorch_model.bin must be present in the directory
    '''
    model_int8 = IncQuantizedModelForSequenceClassification.from_pretrained(local_directory_to_config)
    model_int8.to(device)
    return model_int8
    
def model_load_fp32(local_directory_to_config,device):
    '''
    Function to load fp32 model. config.json and pytorch_model.bin must be present in the path
    '''
    model_fp32 = DistilBertForSequenceClassification.from_pretrained(local_directory_to_config) 
    model_fp32.to(device)
    return model_fp32

class newDatasetWithLabels(torch.utils.data.Dataset):
    '''
    A class to convert a dataset into PyTorch format 
    that has both the raw data and the associated target labels. 
    '''
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item
    def __len__(self):
        return len(self.labels)

class newDatasetNoLabels(torch.utils.data.Dataset):
    '''
    A class to convert a dataset into PyTorch format 
    that has only the raw data and no labels.
    '''
    def __init__(self, encodings):
        self.encodings = encodings
    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item
    def __len__(self):
        return len(self.encodings['input_ids'])

def csv_to_torch(csv_path,labels=True):
    '''
    Convert a CSV with column headings "text" 
    (and if labels are present, "label") to a PyTorch format.
    '''
    hdf = pd.read_csv(csv_path)
    # hdf = hdf.head(500) #temp
    if labels:
        hdf["label"] = hdf["humor"].astype(int)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    data_encoded = tokenizer(list(hdf['text']), padding='max_length', truncation=True, max_length=50, return_tensors='pt')  
    if labels:
        torch_data = newDatasetWithLabels(data_encoded,list(hdf['label']))
    else:
        torch_data = newDatasetNoLabels(data_encoded)
    return torch_data

def mainLoader(csv_path,batch_size,labels=True):
    '''
    Making use of the DataLoader from PyTorch with a specific batch size, 
    so we can load in the data by batch for model prediction
    '''
    torch_data = csv_to_torch(csv_path,labels=labels)
    torch_data_loader = torch.utils.data.DataLoader(torch_data,batch_size)
    return torch_data_loader


def load_csv_with_labels(csv_path):
    hdf = pd.read_csv(csv_path)
    hdf["label"] = hdf["humor"].astype(int)
    return hdf
    
def load_csv_no_labels(csv_path):
    hdf = pd.read_csv(csv_path)
    return hdf

def df_to_labels_list(df):
    return list(df['label'])

def nlp_evaluate(model, dataloader, device):
    model.to(device)
    model.eval()
    y_true_list = []
    y_preds_raw = []
    start_time = time.time()
    for idx,data in enumerate(dataloader):
        inputs = data['input_ids'].to(device)
        try:
            labels = data['labels'].to(device)
            y_true_list.append(labels)
        except KeyError:
            labels = None
            y_true = None
        with torch.no_grad():
            preds = model(inputs)
            preds_class = torch.argmax(preds.logits,dim=-1) 
            y_preds_raw.append(preds_class) 
        
    torch.enable_grad()
    infer_time = time.time()-start_time
    print(f'inference_time={infer_time}')
    return y_true_list, y_preds_raw, infer_time

def extract_class_from_preds(y_preds_raw):
    pred_y_class = []
    start_time = time.time()
    for y in tqdm(y_preds_raw):
        pred_y_class.extend(y.tolist())
    # print(f'time = {time.time()-start_time}')
    return pred_y_class

def main(csv_path,precision,local_directory_to_config,device='cpu',labels=True):
    data_loader = mainLoader(csv_path,labels=labels)
    if precision.lower() == 'fp32':
        model = model_load_fp32(local_directory_to_config,device)
    elif precision.lower() == 'int8':
        model = model_load_int8(local_directory_to_config,device)
    else:
        print(f'model tag is not precision==int8 or precision==fp32. model precision = {precision}. Stopping run.)
        break
    y_true_raw, y_preds_raw, infer_time = nlp_evaluate(model, data_loader, device)
    y_true_list = extract_class_from_preds(y_true_raw)
    y_pred_list = extract_class_from_preds(y_preds_raw)
    
    #delete local copy of pytorch_model.bin, and config.json
    
    return y_true_list, y_pred_list, infer_time
    