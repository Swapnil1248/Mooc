from sklearn.linear_model import LogisticRegression
from sklearn import metrics, preprocessing
from FeatureVectorGen import FeaturePrep

from FeatureVectorGen import PrintMetrics
from FeatureVectorGen import list_list
from pprint import pprint

from sklearn.linear_model import LogisticRegression
from sklearn import metrics

from Module import Module
from Course import Course
from sklearn.ensemble import RandomForestClassifier

objectsFile = '../data/object/object.csv'
date_file = '../data/object/date.csv'

print "Reading obects from "+ objectsFile

with open(objectsFile) as openfileobject:
    openfileobject.next()
    objects = [Module(line) for line in openfileobject]

object_map = dict([(obj.module_id, obj) for obj in objects])

detached_objects = 0

for obj in objects:
    valid_children = []
    for child in obj.children:
        if (child in object_map):
            child_node = object_map[child]
            child_node.parent = obj
            obj.children_nodes.append(child_node)
            valid_children.append(child)
        else:
            detached_objects += 1
    obj.children = valid_children


module_roots = set([value.module_id for value in object_map.values() if value.parent is None])

print "Finished reading objects"


root_dir = '../data/'

test_target_vector, test_feature_matrix, feature_names = FeaturePrep(root_dir + 'test/', object_map, "Features.csv")
train_target_vector, train_feature_matrix, feature_names = FeaturePrep(root_dir + 'train/', object_map, "Features.csv")
validation_target_vector, validation_feature_matrix, feature_names = FeaturePrep(root_dir + 'validation/', object_map, "Features.csv")

print('Start RF training')

num_trees = [10, 20, 50, 80, 100, 150, 200, 300, 400, 500];
models = []
for lambda_value in num_trees:
     clf = RandomForestClassifier(n_estimators=lambda_value, criterion="entropy",)
     print "trained"
     model = clf.fit(train_feature_matrix, train_target_vector)
     print "fitted"
     scores = clf.predict_proba(validation_feature_matrix)[:,1]
     auc = metrics.roc_auc_score(validation_target_vector, scores)
     models.append((lambda_value, clf, model, auc, 'RF'))

print("%10s%10s%20s" % ("num_trees", "roc_auc", "model"))

for x, y, z, w, v in models:
    print("%10f%10f%20s" % (x, w, v))

best_model = max(models, key=lambda model:model[3])
algo = best_model[1]

print("Best model: lambda=%f" % best_model[0])

print "\nTest Set Metrics"
PrintMetrics(test_target_vector, algo.predict(test_feature_matrix), algo.predict_proba(test_feature_matrix)[:,1])
print "\nValidation Set Metrics"
PrintMetrics(validation_target_vector, algo.predict(validation_feature_matrix), algo.predict_proba(validation_feature_matrix)[:,1])