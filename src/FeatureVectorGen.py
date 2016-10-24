import numpy as np
from Event import Event
from sklearn import metrics

tp_list = []
fp_list = []

def list_list():
    print tp_list
    print fp_list

def tpRate(conf):
    return conf[1][1]/(conf[1][0] + conf[1][1])

def fpRate(conf):
    return conf[0][1]/(conf[0][0] + conf[0][1])

def PrintMetrics(test_target_vector, test_scores, test_proba):
    ret = ""
    ret += "AUC Score:" + str(metrics.roc_auc_score(test_target_vector, test_proba))
    conf_mat = metrics.confusion_matrix(test_target_vector, test_scores)
    tp_list.append(tpRate(conf_mat))
    fp_list.append(fpRate(conf_mat))
    ret +="\nConfusion matrix: \n"
    ret += str(conf_mat)
    ret += "\nF1 Score (negative):" + str(metrics.f1_score(test_target_vector, test_scores, pos_label=0))
    ret += "\nF1 Score (positive):" + str(metrics.f1_score(test_target_vector, test_scores, pos_label=1))
    print ret

def formatKey(f_arg, *argv):
    ret = f_arg
    for arg in argv:
        ret = ret + "_" + arg
    return ret


def FeaturePrep(dataSet_dir, object_map, featureFile):
    print('Preparing data for %s' % dataSet_dir)
    enroll_file = dataSet_dir + 'enrollment_train.csv'
    log_file = dataSet_dir + 'log_train.csv'
    truth_file = dataSet_dir + 'truth_train.csv'
    training_data_file = dataSet_dir + featureFile

    feature_names = set()
    static_feature_list = ['problem', 'navigate', 'access', 'discussion', 'page_close', 'video', 'wiki']

    for feature in static_feature_list:
        feature_names.add(feature)
        feature_names.add(formatKey('server', feature))
        feature_names.add(formatKey('browser' , feature))

    print(feature_names)

    enrollment_map = {}

    with open(enroll_file) as enrollment_file:
        enrollment_file.next()
        for line in enrollment_file:
            split = line.strip().split(',')
            id = int(split[0])
            enrollment_map[id] = (split[1], split[2])

    label_set = {}
    features_set = {}

    for enrollment_id in enrollment_map.keys():
        features_set[enrollment_id] = {}
        for feature in feature_names:
            features_set[enrollment_id][feature] = 0

    with open(truth_file) as label_file:
        for line in label_file:
            words = line.split(',')
            id = int(words[0])
            assert(id in enrollment_map)
            label_set[id] = int(words[1])


    with open(log_file) as open_log_file:
        open_log_file.next()
        for line in open_log_file:
            event = Event(line)
            event.setCategory(object_map)
            if(event.enrollment_id in enrollment_map):

                if(event.event_type in static_feature_list):
                    features_set[event.enrollment_id][event.event_type] += 1
                    features_set[event.enrollment_id][formatKey(event.source, event.event_type)] += 1

    feature_name_list = list(feature_names)
    header_str = ('%s,%s,%s') % ('enrollment_id', 'label', ','.join(feature_name_list))
    target_vector = np.zeros(len(enrollment_map))
    rowNum = 0
    feature_matrix = np.zeros((len(enrollment_map), len(feature_name_list)))

    with open(training_data_file, 'w') as data_file:
        data_file.write(header_str + '\n')
        for enrollment_id in enrollment_map.keys():
            line = []
            line.append(str(enrollment_id))
            line.append(str(label_set[enrollment_id]))
            target_vector[rowNum] = label_set[enrollment_id]
            columnNum = 0
            for feature in feature_name_list:
                line.append(str(features_set[enrollment_id][feature]))
                feature_matrix[rowNum][columnNum] = features_set[enrollment_id][feature]
                columnNum += 1
            data_file.write(','.join(line) + '\n')
            rowNum = rowNum + 1
    return (target_vector, feature_matrix, feature_name_list)