from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.impute import KNNImputer, SimpleImputer


def create_preprocessor(bin_features, ohe_features, std_features, norm_features):

    ## THAT was the idea but cant make it work even thought documentation says i should use this
    # bins = [60*x for x in [0,  25, 30, 35, 40, 45]]
    # bins.append(np.inf)
    # labels = ['<25', '25-30', '30-35', '35-40', '40-45', '>45']
    # ('bin', FunctionTransformer(pd.cut, kw_args={'bins': bins, 'labels': labels, 'retbins': False}))

    ################################### 
    # bining
    ###################################
    bin_pipe = Pipeline([
        ('bin', KBinsDiscretizer(n_bins=6, encode='ordinal')),
    ])

    ################################### 
    # onehotencoding
    ###################################
    ohe_pipe = Pipeline([
        ('ohe', OneHotEncoder(sparse_output=False)),
    ])

    ################################### 
    # standardizing
    ###################################
    std_pipe = Pipeline([
        ('imp', SimpleImputer(strategy='median', add_indicator=True)),
        ('std', StandardScaler()),
    ])

    ################################### 
    # normalizing
    ###################################

    norm_pipe = Pipeline([
        ('imp', SimpleImputer(strategy='most_frequent', add_indicator=True)),
        ('minmax', MinMaxScaler())
    ])

    # #### imputation, actually not now because this basically means that a game was from china, we need to have 
    # direct nation column to use it

    # also first perform all transformation except these two, then impute, on transformed features and standardize it
    # imput_features = ['monsterkillsownjungle', 'monsterkillsenemyjungle']

    # imput_pipe = Pipeline([
    #     ('imputer', KNNImputer(add_indicator=True)),
    # ])

    ################################### 
    # PREPROCSESSING UNIT
    ###################################
    preprocessor = ColumnTransformer([
        ('bining', bin_pipe, bin_features),
        ('onehotencoding', ohe_pipe, ohe_features),
        ('stdizing', std_pipe, std_features),
        ('normalizing', norm_pipe, norm_features),
        # ('imputing', imput_pipe, imput_features),
    ])

    return preprocessor


import numpy as np
import matplotlib.pyplot as plt

def plot_roc(model, X, y):
    tpr, fpr, gmeans = [], [], []
    thresholds = np.linspace(0, 1, 50)

    for th in thresholds:
        # predict outputfor different thresholds
        y_pred = model.predict_proba(X)
        y_pred = np.where(y_pred >= th, 1, 0)[:, 1]
        # tpr, sum where it is true
        idx_true = np.where(y == 1)[0]
        tpr_val = sum(y_pred[idx_true])/sum(y)
        # fpr, sum where should be false but is true
        idx_false = np.where(y == 0)[0]
        fpr_val = sum(y_pred[idx_false])/sum(y)
        # geometric mean to pick best threshold 
        gmean = tpr_val * (1 - fpr_val)
        tpr.append(tpr_val), fpr.append(fpr_val), gmeans.append(gmean)

    idx = np.argmax(gmeans)
    print(f'Best threshold: {thresholds[idx]}')

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    ax.plot(fpr, tpr)
    ax.set_title('ROC')
    fig.tight_layout()