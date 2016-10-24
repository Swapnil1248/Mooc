from random import random
import os

root_dir = '../data/complete/'
train_dir = root_dir + '../train/'
test_dir = root_dir + '../test/'
validation_dir = root_dir + '../validation/'
enrollment_file = 'enrollment_train.csv'
truth_file = 'truth_train.csv'
events_file = 'log_train.csv'
 
split_ratio = [.6, .2, .2]
split_threshold = [split_ratio[0], split_ratio[0] + split_ratio[1], 1.]

train_count = 0
validation_count = 0
test_count = 0

dataSetAssigned = {}


if not os.path.exists(train_dir):
    os.makedirs(train_dir)
if not os.path.exists(test_dir):
    os.makedirs(test_dir)
if not os.path.exists(validation_dir):
    os.makedirs(validation_dir)

with open(root_dir + enrollment_file) as input_file, \
     open(train_dir + enrollment_file, 'w') as train_file, \
     open(validation_dir + enrollment_file, 'w') as validation_file, \
     open(test_dir + enrollment_file, 'w') as test_file:
    header = input_file.next()
    train_file.write(header)
    test_file.write(header)
    validation_file.write(header)
    for line in input_file:
        enrollment_id = line.split(",")[0]
        r = random()
        if (r < split_threshold[0]):
            train_file.write(line)
            train_count += 1
            dataSetAssigned[enrollment_id] = "train"
        elif (r < split_threshold[1]):
            validation_file.write(line)
            validation_count += 1
            dataSetAssigned[enrollment_id] = "validation"
        else:
            test_file.write(line)
            test_count += 1
            dataSetAssigned[enrollment_id] = "test"
    train_file.close()
    validation_file.close()
    test_file.close()
    
    
with open(root_dir + truth_file) as input_file, \
     open(train_dir + truth_file, 'w') as train_file, \
     open(validation_dir + truth_file, 'w') as validation_file, \
     open(test_dir + truth_file, 'w') as test_file:
    for line in input_file:
        enrollment_id = line.split(",")[0]
        if (dataSetAssigned[enrollment_id]  == "train"):
            train_file.write(line)
        elif (dataSetAssigned[enrollment_id]  == "validation"):
            validation_file.write(line)
        else:
            test_file.write(line)
    train_file.close()
    validation_file.close()
    test_file.close()

with open(root_dir + events_file) as input_file, \
     open(train_dir + events_file, 'w') as train_file, \
     open(validation_dir + events_file, 'w') as validation_file, \
     open(test_dir + events_file, 'w') as test_file:
    header = input_file.next()
    train_file.write(header)
    test_file.write(header)
    validation_file.write(header)
    for line in input_file:
        enrollment_id = line.split(",")[0]
        if (dataSetAssigned[enrollment_id]  == "train"):
            train_file.write(line)
        elif (dataSetAssigned[enrollment_id]  == "validation"):
            validation_file.write(line)
        else:
            test_file.write(line)
    train_file.close()
    validation_file.close()
    test_file.close()
    
print('Train: %d, validation: %d, test: %d' % (train_count, validation_count, test_count))
total = 1.0 * (train_count + validation_count + test_count)
print('Train: %.3f, validation: %.3f, test: %.3f' % (train_count / total, validation_count / total, test_count / total))

