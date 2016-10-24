
from FeatureVectorGen import FeaturePrep

from FeatureVectorGen import PrintMetrics

from sklearn.linear_model import LogisticRegression
from sklearn import metrics

from Module import Module


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

print('Start LogisticRegression training')
lambdas = [1.0E-4, 1.0E-3, 1.0E-2, 1.0E-1, 1.0, 1.0E2, 1.0E3]
models = []
for lambda_value in lambdas:
    lr = LogisticRegression(penalty='l2', tol=1.0E-5, C=lambda_value, fit_intercept=True)
    model = lr.fit(train_feature_matrix, train_target_vector)
    scores = lr.predict_proba(validation_feature_matrix)[:,1]
    auc = metrics.roc_auc_score(validation_target_vector, scores)
    models.append((lambda_value, lr, model, auc, 'Logistic regression'))

print("%10s%10s%20s" % ("lambda", "roc_auc", "model"))

x_axis = []
y_axis = []
for x, y, z, w, v in models:
    x_axis.append(x)
    y_axis.append(w)
    print("%10f%10f%20s" % (x, w, v))





best_model = max(models, key=lambda model:model[3])
algo = best_model[1]

coefs = best_model[1].coef_.tolist()[0]
cn = zip(coefs, feature_names)
cn.sort(key=lambda x:abs(x[0]))
for coef, name in cn:
    print(str(coef) + ',' + name)
    
print("Best model: lambda=%f" % best_model[0])



print "\nTest Set Metrics"
PrintMetrics(test_target_vector, algo.predict(test_feature_matrix), algo.predict_proba(test_feature_matrix)[:,1])
print "\nValidation Set Metrics"
PrintMetrics(validation_target_vector, algo.predict(validation_feature_matrix), algo.predict_proba(validation_feature_matrix)[:,1])



