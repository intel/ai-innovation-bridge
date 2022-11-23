import time
import torch

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
    print(f'time = {time.time()-start_time}')
    return pred_y_class