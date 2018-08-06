
import h5py
import numpy as np
import os, random
from skimage.measure import label
from skimage import morphology
import matplotlib.pyplot as plt


#####extra section  output the prediction situation of each slice


random.seed(7)

patch_size = 14

base_path = 'data/'

results_dir = 'new_result/'
garbage_dir = 'garbage/'



train_path_left = base_path + 'train/left'
train_path_right = base_path + 'train/right'
val_path_left = base_path + 'val/left'
val_path_right = base_path + 'val/right'
test_path_left = base_path + 'test/left'
test_path_right = base_path + 'test/right'


#pred_image = np.load(results_dir + 'predict_2dcnn_3.npy')
pred_image = np.load(garbage_dir + 'predict_713.npy')

#pred_image = np.load(garbage_dir + 'predict_haha.npy')


def perf_measure(y_actual, y_hat):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_hat)):
        if y_actual[i] == y_hat[i] == 1:
            TP += 1
    for i in range(len(y_hat)):
        if y_hat[i] == 1 and y_actual[i] != y_hat[i]:
            FP += 1
    for i in range(len(y_hat)):
        if y_actual[i] == y_hat[i] == 0:
            TN += 1
    for i in range(len(y_hat)):
        if y_hat[i] == 0 and y_actual[i] != y_hat[i]:
            FN += 1
    return (TP, FP, TN, FN)


def reverse(scan):
    scan=scan[:,:,::-1]
    return scan



def post_slice(scan,CartFM,pred_all):
    pred_cor_all = []
    cart_cor_all = []
    pred_last = []

    for z in range(104):
     print(z)
     image = scan[:,:,z]
     cart = CartFM[:, :, z]
     pred = pred_all[z]
     pred_rev = np.zeros(image.size)
     #print(len(pred))

     for i in range(len(pred)):
        thr = 0.55
        pred[i][0] = pred[i][0] / (1 - thr)
        pred[i][1] = pred[i][1] / thr
        pred_rev[i] = np.argmax(pred[i])

     pred_rev = pred_rev.reshape(170, 170)
     label_image = label(pred_rev, connectivity=2)
     pred_rev = morphology.remove_small_objects(label_image, min_size=200, connectivity=2)
     pred_rev = pred_rev.reshape(image.size)
     for i in range(len(pred_rev)):
        if pred_rev[i] > 0:
            pred_rev[i] = 1
     pred_rev = pred_rev.reshape(170, 170)
     pred_last.append(pred_rev)
     pred_cor = np.array(np.where(pred_rev > 0)).T
     pred_cor_all.extend(pred_cor)
     print(len(pred_cor))

     cart_cor = np.array(np.where(cart > 0)).T
     cart_cor_all.extend(cart_cor)
     print(len(cart_cor))


#with h5py.File('data/val/left/101280-001-L-Turbo 3D T1, 1-2004.mat', 'r') as file:
#    print(list(file.keys()))
#    scan = np.array(file['scan'])
#    CartFM = np.array(file['CartTM'])

with h5py.File('data/train/left/060938-002-L-Turbo 3D T1, 1-2004.mat', 'r') as file:
    print(list(file.keys()))
    scan = np.array(file['scan'])
    CartFM = np.array(file['CartTM'])



print(scan.shape)
print(len(pred_image[3]))

a = post_slice(scan,CartFM,pred_image[3])

print(a)
