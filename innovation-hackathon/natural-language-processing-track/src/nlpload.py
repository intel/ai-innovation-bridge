import pandas as pd
from transformers import DistilBertTokenizerFast
import torch


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