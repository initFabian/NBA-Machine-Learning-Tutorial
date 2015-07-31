# runNBA_Data.py
import time
import pandas as pd
import numpy as np

# Machine Learning algorithms
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures,scale
from sklearn.cross_validation import train_test_split, KFold
from sklearn.learning_curve import learning_curve

# Plot modules
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
pd.options.display.max_columns = 50
pd.set_option('expand_frame_repr', False)

# Custom modules
from nbaImport import readMongo, WANTED_FEATURES, PER_FEATURES

def flatten(objToFlatten):
    return [item for sublist in objToFlatten for item in sublist]

def BuildDataSet():

    # 1
    nbaFrame = readMongo(db='YOUR DATABASE',collection='above50Games',
            query= {}, queryReturn=WANTED_FEATURES, no_id=False,
            mongo_uri='YOUR URI')

    # 2
    statsDF = pd.DataFrame(list(flatten(nbaFrame.Seasons)))
    print(statsDF)


    # 1
    stats = pd.DataFrame(list(statsDF.totals.values))
    stats['FT_M'] = stats['FTA'] - stats['FT']
    stats['FG_M'] = stats['FGA'] - stats['FG']
    stats[PER_FEATURES] = stats[PER_FEATURES].astype(float)

    # 2
    stats['PER'] = pd.DataFrame(list(statsDF.advanced.values))

    # 3
    stats = stats.reindex(np.random.permutation(stats.index))
    X = np.array(stats[PER_FEATURES].values)
    y = (stats["PER"].values.tolist())

    return X,y

def PlotLearningCurve(X_data, y_data,algorithm, s_time):

    print('PlotLearningCurve called')

    # 1
    sizes = np.array([.1,.2,.5,.8,.99])

    train_sizes, train_scores, test_scores = learning_curve(
                                                    algorithm,
                                                    X_data,
                                                    y_data,
                                                    train_sizes=sizes)
    print('after learning_curve')
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

    # 2
    plt.figure(figsize=(15,10)) # Width, Height

    # Training Set
    plt.fill_between(train_sizes, train_mean-train_std,
                    train_mean+train_std, alpha=0.1, color="r")

    # Cross Validation Set
    plt.fill_between(train_sizes, test_mean-test_std,
                    test_mean+test_std, alpha=0.1, color="g")

    # Graph Legend text
    trainLabel = ('%.3f%% Training score' % (train_mean[4]))
    testLabel = ('%.3f%% Cross-validation score' % (test_mean[4]))

    # Plot lines
    plt.plot(train_sizes, train_mean, 'o-', color="r", label=trainLabel)
    plt.plot(train_sizes, test_mean, 'o-', color="g", label=testLabel)

    # Place title, X-axis label, Y-axis label
    plt.suptitle('Linear Regression: NBA PER', fontsize=20)
    plt.xlabel('Training examples')
    plt.ylabel('Accuracy')

    # Set limit on Y-axis, Place graph legend
    plt.ylim((0.5, 1.1))
	plt.xlim((0, 6500))
	plt.legend(loc="best")

    # Print duration of program
    print("--- %s seconds ---" % (time.time() - s_time))
    plt.show()

def Analysis(_deg=1):
    start_time = time.time()

    # 1
    X, y = BuildDataSet()
    linear_regression = LinearRegression()

    # 2
    polynomial_features = PolynomialFeatures(degree=_deg, include_bias=False)

    # 3
    algorithm = Pipeline([("polynomial_features", polynomial_features),
                         ("linear_regression", linear_regression)])
    #========================================================================== */
    print('after Pipeline')

    # 4
    PlotLearningCurve(X, y, algorithm, start_time)

Analysis(3)