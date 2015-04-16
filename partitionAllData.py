import shutil
import os
import random

## folder tree structure
## ALL_DATA/
    ## AUSTRALIA/
        ## SHITTON OF TWEETS
    ## CANADA/
        ## SHITTON OF TWEETS
    ## UK/
        ## SHITTON OF TWEETS
    ## US/
        ## SHITTON OF TWEETS

def partition_folder(all_dir, country):
    print len(all_dir)
    print [i for i in range(len(all_dir))]
    num_in_test = int(test_percentage * len(all_dir))
    test_idx = set(random.sample([i for i in range(len(all_dir))], num_in_test))
    src = os.path.join(allFolder, country)
    destTest = os.path.join(testFolder, country)
    destTrain = os.path.join(trainFolder, country)
    if not os.path.exists(destTest):
        os.makedirs(destTest)
    if not os.path.exists(destTrain):
        os.makedirs(destTrain)
    for i in range(len(all_dir)):
        if i in test_idx:
            shutil.copy(os.path.join(src, all_dir[i]), os.path.join(destTest, all_dir[i]))
        else:
            shutil.copy(os.path.join(src, all_dir[i]), os.path.join(destTrain, all_dir[i]))

## first delete existing training/test folder
allFolder = 'ALL_DATA'
UK = 'UK'
US = 'USA'
CAN = 'CANADA'
AUS = 'AUSTRALIA'
trainFolder = 'TRAIN'
testFolder = 'TEST'
test_percentage = 0.2

if os.path.exists(trainFolder):
    shutil.rmtree(trainFolder)
if os.path.exists(testFolder):
    shutil.rmtree(testFolder)

all_us = os.listdir(allFolder + os.sep + US)
all_uk = os.listdir(allFolder + os.sep + UK)
all_can = os.listdir(allFolder + os.sep + CAN)
all_aus = os.listdir(allFolder + os.sep + AUS)
partition_folder(all_us, US)
partition_folder(all_uk, UK)
partition_folder(all_can, CAN)
partition_folder(all_aus, AUS)
