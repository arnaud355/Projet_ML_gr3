import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from yellowbrick.classifier import ClassificationReport
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.cluster import KMeans
import pickle 
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ParameterGrid
import statistics
def plot_classification_report(cl, X_train, y_train,X_test, y_test, classe_labels):
    viz = ClassificationReport(cl, classes=classe_labels, support=True,)
    viz.fit(X_train, y_train)
    viz.score(X_test, y_test)
    g = viz.poof()

def plot_roc_auc(cl, X, y,classe_labels, colors):
    y_roc_auc = label_binarize(y, classes=[i for i in range(len(classe_labels))])
    n_classes = y_roc_auc.shape[1]

    X_train, X_test, y_train, y_test = train_test_split(X, y_roc_auc, test_size=.5, random_state=0)
    classifier = OneVsRestClassifier(cl)
    y_score = classifier.fit(X_train, y_train).decision_function(X_test)

    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    #plt.figure(figsize=(15,10))
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    #colors = ['blue', 'red', 'green']
    for i, color in zip(range(n_classes), colors):
        plt.plot(fpr[i], tpr[i], color=color,
                 label='ROC curve of {0} (area = {1:0.2f})'
                 ''.format(classe_labels[i], roc_auc[i]))
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic for multi-class data')
    plt.legend(loc="lower right")
    plt.show()
   

def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    given a sklearn confusion matrix (cm), make a nice plot

    Arguments
    ---------
    cm:           confusion matrix from sklearn.metrics.confusion_matrix

    target_names: given classification classes such as [0, 1, 2]
                  the class names, for example: ['high', 'medium', 'low']

    title:        the text to display at the top of the matrix

    cmap:         the gradient of the values displayed from matplotlib.pyplot.cm
                  see http://matplotlib.org/examples/color/colormaps_reference.html
                  plt.get_cmap('jet') or plt.cm.Blues

    normalize:    If False, plot the raw numbers
                  If True, plot the proportions

    Usage
    -----
    plot_confusion_matrix(cm           = cm,                  # confusion matrix created by
                                                              # sklearn.metrics.confusion_matrix
                          normalize    = True,                # show proportions
                          target_names = y_labels_vals,       # list of names of the classes
                          title        = best_estimator_name) # title of graph

    Citiation
    ---------
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    #plt.figure(figsize=(15,10))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    #plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()

def grid_search_simple(classificateur,file_name, X, y):
    modeles = {"logreg":[LogisticRegression(),[
                {'penalty': ['l2'],'C':[0.1,0.6,1,2,5,10],
                  'multi_class':['ovr', 'multinomial'],'class_weight':['balanced', None],
                  'solver':['lbfgs','sag','newton-cg'],'max_iter':[1000],"random_state": [0]
                },
                {'penalty': ['l1','l2'],'C':[0.1,0.6,1,2,5,10],
                  'multi_class':['ovr'],'class_weight':['balanced', None],
                  'solver':['liblinear'],'max_iter':[1000],"random_state": [0]
                },]],
              "SVM":[SVC(),[
                {'C': [0.1,0.6,1,2,5,10],'class_weight':['balanced', None],
                 'gamma': ['scale','auto'], 'kernel': ['linear'],
                 'decision_function_shape': ['ovo', 'ovr'],"random_state": [0]
                },
                {'C': [0.1,0.6,1,2,5,10], 'class_weight':['balanced', None],
                 'gamma': ['scale','auto'], 'kernel': ['rbf'],
                 'decision_function_shape': ['ovo', 'ovr'],"random_state": [0]
                },
                {'C': [0.1,0.6,1,2,5,10], 'class_weight':['balanced', None],
                 'gamma': ['scale','auto'], 'kernel': ['poly'], 'degree': [2,3,4,5,6,7],
                 'decision_function_shape': ['ovo', 'ovr'],"random_state": [0]
                },
                {'C': [0.1,0.6,1,2,5,10],'class_weight':['balanced', None],
                 'gamma': ['scale','auto'], 'kernel': ['sigmoid'],
                 'decision_function_shape': ['ovo', 'ovr'],"random_state": [0]
                }]],
              "RanFor":[RandomForestClassifier(),{
                   'n_estimators': [100,150,200],
                   "criterion": ["gini", "entropy"],
                   "max_depth": [8, 10, 12, None],
                   "min_samples_split": [2, 5],
                   "max_features": ["sqrt", "log2", None],
                   "bootstrap": [True, False],
                   "class_weight": ["balanced", "balanced_subsample", None],
                   "random_state": [0]
                   }],
              "ExtTre":[ExtraTreesClassifier(),{
                   'n_estimators': [50,100,150,200],
                   "criterion": ["gini", "entropy"],
                   "max_depth": [8, 10, 12, None],
                   "min_samples_split": [2, 5],
                   "max_features": ["sqrt", "log2", None],
                   "bootstrap": [True, False],
                   "class_weight": ["balanced", "balanced_subsample", None],
                   "random_state": [0]
                  }],
              "graboo":[GradientBoostingClassifier(),{"loss":["deviance"],
                   "learning_rate": [0.1, 0.3, 0.5],
                   "min_samples_split": [0.1, 0.5, 2],
                   "min_samples_leaf": [0.1, 0.5, 1],
                   "max_depth":[3,5,8],
                   "max_features":["log2","sqrt",None],
                   "criterion": ["friedman_mse"],
                   "subsample":[0.5, 0.8, 1.0],
                   "n_estimators":[100,150,200],
                   "random_state": [0]
                  }],
              "xgboost":[xgb.XGBClassifier(),{
                  'objective':['multi:softmax'],
                  'num_class': 4,
                  "max_depth": [3, 5, 8],
                  "subsample": [0.5,0.8,1],
                  "learning_rate": [0.1, 0.3, 0.5],
                  "n_estimators":[100,150,200],
                  "random_state": [0]
                  }]}
    
    
    estimat = modeles[classificateur][0]
    parameters = modeles[classificateur][1]
    clf = GridSearchCV(estimat, param_grid = parameters, return_train_score=True, cv = 5, n_jobs=-1)
    clf.fit(X, y)
    result = pd.DataFrame.from_dict(clf.cv_results_)
    best = [clf.best_estimator_, clf.best_score_, clf.best_params_, clf.scorer_]
    
    hyperparameters_file = "hyperparameters/" + file_name + ".csv"
    weights_file = "weights/" + file_name + ".sav"
    
    result.to_csv(hyperparameters_file, index = False)
    pickle.dump(clf.best_estimator_, open(weights_file, 'wb'))
    
    print(clf.best_estimator_)
    return clf.best_estimator_

def graph_result(fichier, n = 1500, variance = 0.1):
    res = pd.read_csv("hyperparameters/" + fichier)
    result = res[res['mean_test_score'] > 0.65]
    result_variance = result[(result['mean_train_score'] - result['mean_test_score']) < variance * result['mean_test_score']]
    plt.figure(num=None, figsize=(14, 6), dpi=80, facecolor='w', edgecolor='k')
    
    plt.subplot(121)
    plt.scatter(result['rank_test_score'][result['rank_test_score'] < n],
                result['mean_test_score'][result['rank_test_score'] < n],color='red',
                marker = "+", label="Test Score")
    plt.scatter(result['rank_test_score'][result['rank_test_score'] < n],
                result['mean_train_score'][result['rank_test_score'] < n],color='blue',
                marker = "x", label="Train Score")
    plt.ylim(0.64, 1)
    plt.title("Test Score et Train Score \nen fonction du classement au Test Score",
              fontsize = 14, loc = 'center')
    plt.xlabel("Classement au Test Score",fontsize = 12)
    plt.ylabel("Score",fontsize = 12)
    plt.legend(loc = 3)
    
    plt.subplot(122)
    plt.scatter(result_variance['rank_test_score'][result_variance['rank_test_score'] < n],
                result_variance['mean_test_score'][result_variance['rank_test_score'] < n],color='red',
                marker = "+", label="Test Score")
    plt.scatter(result_variance['rank_test_score'][result_variance['rank_test_score'] < n],
                result_variance['mean_train_score'][result_variance['rank_test_score'] < n],color='blue',
                marker = "x", label="Train Score")
    plt.ylim(0.64, 1)
    plt.title("Test Score et Train Score \nen fonction du classement au Test Score",
              fontsize = 14, loc = 'center')
    plt.xlabel("Classement au Test Score",fontsize = 12)
    plt.ylabel("Score",fontsize = 12)
    plt.legend(loc = 3)
    plt.show()

def get_classes(y):
    kmeans = KMeans(n_clusters=4, init='k-means++', max_iter=1000).fit(y.values.reshape(-1, 1))
    y_class_orig = kmeans.labels_
    correspondance = list(pd.DataFrame(kmeans.cluster_centers_, columns=['center']).sort_values('center').index)
    y_dic = {correspondance[i]: i for i in range(len(kmeans.cluster_centers_))}
    y_ord = []
    for i in y_class_orig:
        y_ord.append(y_dic[i])
    y_class = np.array(y_ord)

    centroid = kmeans.cluster_centers_
    centroid.sort(axis=0)
    centre = list(centroid.reshape(1, -1)[0])
    classe = [(centre[i] + centre[i + 1]) / 2 for i in range(len(centre) - 1)]
    classe_labels = []
    dic_min_max_mean = {}
    k = 1000
    for index, item in enumerate(classe):
        b = 0
        e = int(classe[index] / k)
        if index > 0:
            b = int(classe[index - 1] / k)
        classe_labels.append("[{0}K - {1}K]".format(b, e))
        dic_min_max_mean[index] = [min(b, e)*100,statistics.mean([b, e])*k,max(b, e)*k]
    classe_labels.append("[{0}K - {1}]".format(int(classe[len(classe) - 1] / k), "+"))
    dic_min_max_mean[len(classe)] = [int(classe[len(classe) - 1]), statistics.mean([int(classe[len(classe) - 1]), 200000]), 200000]
    dic_classe_labels = {i: classe_labels[i] for i in range(len(classe_labels))}
    #dic_min_max_mean = {i: [] for i,e in  enumerate(classe)}
    return y_class, dic_classe_labels, dic_min_max_mean