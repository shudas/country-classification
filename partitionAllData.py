import shutil
import os
import random

## folder tree structure
## ALL_DATA/
    ## AUSTRALIA/
        ## ONE FILE PER USER
    ## CANADA/
        ## ONE FILE PER USER
    ## UK/
        ## ONE FILE PER USER
    ## US/
        ## ONE FILE PER USER

## Perform the partition
def partition_folder(all_dir, country):
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

## First delete existing train/test folder
allFolder = 'ALL_DATA'
UK = 'UK'
US = 'USA'
CAN = 'CANADA'
AUS = 'AUSTRALIA'
trainFolder = 'TRAIN'
testFolder = 'TEST'

# Change this to change the fraction of tweets that get reserved for testing
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
