import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier 
from prediction import ml_metrics
from sklearn import svm   
from sklearn.preprocessing import StandardScaler  
from sklearn.cluster import AgglomerativeClustering 
import time


##ADD TRAINING SCRIPTS HERE

featuresFile = open("features_dataFrame.pkl", "rb")
features = pickle.load(featuresFile)
featuresFile.close()

##Remove rows with NaN values
features = features.dropna()

X = features.loc[:, 'Hurst' : 'PFD']
Y = features['Class']
x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size=0.3, random_state=2)
filename = 'train_data.pkl'
pickle.dump(x_train, open(filename, 'wb'))
stdsc = StandardScaler()            
X_train_std = stdsc.fit_transform(x_train)

X_test_std = stdsc.transform(x_test)

#ada boost
begin = time.time()
model = AdaBoostClassifier()
model.fit(x_train, y_train)
print("*"*50)
print("ADA BOOSTING")
print("Training Execution Time : " ,(time.time() - begin), "s")
with open("ada_model.pkl", "wb") as file:
    pickle.dump(model, file)
begin = time.time()
y_pred = model.predict(x_test)
print("Testing Execution Time : " ,(time.time() - begin))
ml_metrics(y_test, y_pred)

#SVM
begin = time.time()
supp_vect_machine = svm.SVC(C=1.0, kernel='sigmoid', degree=3, gamma='scale', coef0=0.0, 
                shrinking=True, probability=False, tol=1e-3,cache_size=200,
                class_weight='balanced', verbose=False, max_iter=-1,
                decision_function_shape='ovr', 
                random_state=None)

supp_vect_machine.fit(X_train_std,y_train)
print("*"*50)
print("SUPPORT VECTOR MACHINE")
print("Training Execution Time : " ,(time.time() - begin))

begin = time.time()
y_pred = supp_vect_machine.predict(X_test_std)

print("Testing Execution Time : " ,(time.time() - begin))
ml_metrics(y_test,y_pred)
filename = 'svm_model_trained_1.pkl'
pickle.dump(supp_vect_machine, open(filename, 'wb'))

# RANDOM FOREST CLASSIFIER
begin = time.time()
model = RandomForestClassifier()
model.fit(x_train, y_train)
print("*"*50)
print("RANDOM FOREST CLASSIFIER")
print("Training Execution Time : " ,(time.time() - begin))
begin = time.time()
y_pred = model.predict(x_test)

print("Testing Execution Time : " ,(time.time() - begin))

ml_metrics(y_test,y_pred)

with open("rf_model.pkl", "wb") as file:
    pickle.dump(model, file)

# LOGISTIC REGERESSION
begin = time.time()
model = LogisticRegression()
model.fit(X_train_std, y_train)
print("*"*50)
print("LOGISTIC REGRESSION")
print("Training Execution Time : " ,(time.time() - begin))

begin = time.time()
y_pred = model.predict(X_test_std)
print("Testing Execution Time : " ,(time.time() - begin))
ml_metrics(y_test,y_pred)

with open("lr_model.pkl", "wb") as file:
    pickle.dump(model, file)

#HIERARCHICAL CLUSTERING
begin = time.time()
model = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
model.fit(X_train_std, y_train)
print("*"*50)
print("HIERARCHICAL CLUSTERING")
print("Training Execution Time : " ,(time.time() - begin))
begin = time.time()
y_pred = model.fit_predict(X_test_std)

print("Testing Execution Time : " ,(time.time() - begin))
ml_metrics(y_test, y_pred)
filename = 'HC_Model.pkl'
pickle.dump(model, open(filename, 'wb'))

#MULTILAYER PERCEPTRON CLASSIFIER
begin = time.time()
model = MLPClassifier(hidden_layer_sizes=(100),activation ='logistic',
                                max_iter = 2000, alpha= 0.0001,solver ='adam',
                                tol = 0.0001,random_state = None,
                                learning_rate = 'constant')
print("*"*50)
print("MULTILAYER PERCEPTRON CLASSIFIER")
begin = time.time()
model.fit(x_train, y_train)
print("Training Execution Time : " ,(time.time() - begin))

filename = 'mlpc_model_trained_1.pkl'
pickle.dump(model, open(filename, 'wb'))
begin = time.time()
y_pred = model.predict(x_test)

print("Testing Execution Time : " ,(time.time() - begin))
ml_metrics(y_test,y_pred)