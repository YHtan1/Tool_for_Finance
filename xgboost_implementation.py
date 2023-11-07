import xgboost as xgb
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold


#store data in a format that can be read of xgboost
d_train=xgb.DMatrix(x_train,y_train,enable_categorical=True)
d_test=xgb.DMatrix(x_test,y_test,enable_categorical=True)

#k fold cv to get learning rate]
learning_rate_list=list(np.arange(0,1,0.0001))
param_grid = dict(learning_rate=learning_rate_list)
kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=7)
grid_search = GridSearchCV(model, param_grid, scoring="neg_mean_squared_error", n_jobs=-1, cv=kfold)
#print out best learning rate parameters
grid_result=learning_rate_list[grid_search.best_index]

params = {
    "tree_method": "hist",
#"colsample_bylevel": 0.7
}

#fit model
model=xgb.XGBClassifier(**params,eval_metric="rmse",enable_categorical=True)
model.fit(d_train,y_train,eval_set=[(X_test, y_test), (X_train, y_train)])

#print probability of prediction
# Assuming you have already trained the model and have the test data stored in `d_test`
probabilities = model.predict_proba(d_test)
print(probabilities)