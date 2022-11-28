# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""System module."""
# pylint: disable=E1101,E1102,E0401,R0913,R0914,C0209
import time
import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
from sklearn.metrics import confusion_matrix, accuracy_score, \
    balanced_accuracy_score, f1_score
from torchvision import transforms
from utils.constants import (
    INPUT_IMG_SIZE,
    NEG_CLASS,
)


def data_augmentation(inputs, labels):
    """
    This module is responsible for applying data augumentation
    on existing dataset
    """

    img_p = transforms.ToPILImage()
    img_filp_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE),
             transforms.RandomHorizontalFlip(), transforms.ToTensor()])
    img_crop_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE),
             transforms.CenterCrop(224), transforms.ToTensor()])
    img_rotation_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE),
             transforms.RandomRotation(25), transforms.ToTensor()])
    img_enhance_transform = transforms.Compose(
            [transforms.Resize(INPUT_IMG_SIZE), transforms.ColorJitter(
                brightness=0.3, contrast=0.3,
                saturation=0.3, hue=0.2), transforms.ToTensor()])
    n_inputs = []
    n_labels = []
    for i, _ in enumerate(inputs):
        n_inputs.append(inputs[i])
        n_labels.append(labels[i])
        img_filp = img_filp_transform(img_p(inputs[i]))
        n_inputs.append(img_filp)
        n_labels.append(labels[i])
        img_crop = img_crop_transform(img_p(inputs[i]))
        n_inputs.append(img_crop)
        n_labels.append(labels[i])
        img_rotation = img_rotation_transform(img_p(inputs[i]))
        n_inputs.append(img_rotation)
        n_labels.append(labels[i])
        img_enhance = img_enhance_transform(img_p(inputs[i]))
        n_inputs.append(img_enhance)
        n_labels.append(labels[i])
    return torch.stack(n_inputs, 0), torch.stack(n_labels, 0)


def train(dataloader, model, optimizer, criterion,
          epochs, device, target_accuracy=None, data_aug=0):
    """
    Script to train a model. Returns trained model.
    This module will be responsible for training and updating the weights of
    Deep learning model based on the dataset provided
    """
    model.to(device)
    model.train()
    if data_aug:
        print("Applying DataAugmentation----> Flipping/Rotation/"
              "Enhancing/Cropping and keeping the Regular images as well")

    for epoch in range(1, epochs + 1):
        print(f"Epoch {epoch}/{epochs}:", end=" ")
        running_loss = 0
        running_corrects = 0
        n_samples = 0

        for inputs1, labels1 in dataloader:
            inputs, labels = inputs1, labels1
            if data_aug:
                inputs, labels = data_augmentation(inputs1, labels1)
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            preds_scores = model(inputs)
            preds_class = torch.argmax(preds_scores, dim=-1)
            loss = criterion(preds_scores, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds_class == labels)
            n_samples += inputs.size(0)

        epoch_loss = running_loss / n_samples
        epoch_acc = running_corrects.double() / n_samples
        print("Loss = {:.4f}, Accuracy = {:.4f}".format(epoch_loss, epoch_acc))

        if target_accuracy is not None:
            if epoch_acc > target_accuracy:
                print("Early Stopping")
                break

    return model


def evaluate(model, dataloader, device, class_names="auto", labels=True):
    """
    This module will be responsible for evaluating the trained model and calculate the accuracy
    Script to evaluate a model after training.
    Outputs accuracy and balanced accuracy, draws confusion matrix.
    """
    
    model.to(device)
    model.eval()
    
    if labels:
        y_true = np.empty(shape=(0,))
        y_pred = np.empty(shape=(0,))
    
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            start_time = time.time()
            preds_probs = model(inputs)[0]
            infer_time = time.time()-start_time
            print('infer_time_per_sample=', infer_time)
            preds_class = torch.argmax(preds_probs, dim=-1)
            labels = labels.to("cpu").numpy()
            preds_class = preds_class.detach().to("cpu").numpy()
            y_true = np.concatenate((y_true, labels))
            y_pred = np.concatenate((y_pred, preds_class))
    
        accuracy = f1_score(y_true, y_pred)
        balanced_accuracy = balanced_accuracy_score(y_true, y_pred)
    
        print("f1 Accuracy Score: ", accuracy)
        print("Balanced Accuracy: ", balanced_accuracy)
    
        plot_confusion_matrix(y_true, y_pred, class_names=class_names)
        return y_true, y_pred
    else:
        
        model.to(device)
        model.eval()
        
        y_pred = np.empty(shape=(0,))
        file_list = []
    
        for inputs, fn in dataloader:
            inputs = inputs.to(device)
            preds_probs = model(inputs)[0]
            preds_class = torch.argmax(preds_probs, dim=-1)
            preds_class = preds_class.detach().to("cpu").numpy()
            y_pred = np.concatenate((y_pred, preds_class))
            file_list.append(list(fn))
        
        files = [item for sublist in file_list for item in sublist]
    
        return y_pred, files
        


def plot_confusion_matrix(y_true, y_pred, class_names="auto"):
    """
    Visualization
    """
    confusion = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=[5, 5])
    sns.heatmap(
        confusion,
        annot=True,
        cbar=False,
        xticklabels=class_names,
        yticklabels=class_names,
    )

    plt.ylabel("True labels")
    plt.xlabel("Predicted labels")
    plt.title("Confusion Matrix")
    plt.show()


def get_bbox_from_heatmap(heatmap, thres=0.8):
    """
    Returns bounding box around the defected area:
    Upper left and lower right corner.
    Threshold affects size of the bounding box.
    The higher the threshold, the wider the bounding box.
    """
    binary_map = heatmap > thres

    x_dim = np.max(binary_map, axis=0) * np.arange(0, binary_map.shape[1])
    x_0 = int(x_dim[x_dim > 0].min())
    x_1 = int(x_dim.max())

    y_dim = np.max(binary_map, axis=1) * np.arange(0, binary_map.shape[0])
    y_0 = int(y_dim[y_dim > 0].min())
    y_1 = int(y_dim.max())

    return x_0, y_0, x_1, y_1


def predict_localize(
    model, dataloader, device, thres=0.8, n_samples=9, show_heatmap=False
):
    """
    Runs predictions for the samples in the dataloader.
    Shows image, its true label, predicted label and probability.
    If an anomaly is predicted, draws bbox around defected region and heatmap.
    """
    model.to(device)
    model.eval()

    transform_to_pil = transforms.ToPILImage()

    n_cols = 4
    n_rows = int(np.ceil(n_samples / n_cols))
    plt.figure(figsize=[n_cols * 5, n_rows * 5])

    counter = 0
    for inputs, _ in dataloader:
        inputs = inputs.to(device)
        out = model(inputs)
        _, class_preds = torch.max(out[0], dim=-1)
        feature_maps = out[1].to(device)

        for img_i in range(inputs.size(0)):
            img = transform_to_pil(inputs[img_i])
            class_pred = class_preds[img_i]
            heatmap = feature_maps[img_i][NEG_CLASS].detach().cpu().numpy()

            counter += 1
            plt.subplot(n_rows, n_cols, counter)
            plt.imshow(img)
            plt.axis("off")

            if class_pred == NEG_CLASS:
                x_0, y_0, x_1, y_1 = get_bbox_from_heatmap(heatmap, thres)
                rectangle = Rectangle(
                    (x_0, y_0),
                    x_1 - x_0,
                    y_1 - y_0,
                    edgecolor="red",
                    facecolor="none",
                    lw=3,
                )
                plt.gca().add_patch(rectangle)
                if show_heatmap:
                    plt.imshow(heatmap, cmap="Reds", alpha=0.3)

            if counter == n_samples:
                plt.tight_layout()
                plt.show()
                return
