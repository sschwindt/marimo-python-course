import marimo

__generated_with = "0.25.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Import data set
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_wine # example dataset for wine classification
    from sklearn.model_selection import train_test_split # function to split testing and training datasets
    from sklearn.svm import SVC # class Support Vector Machine
    from sklearn.model_selection import validation_curve # function too stract error through validation
    from sklearn.metrics import ConfusionMatrixDisplay # class to plot confusion matrix


    data = load_wine(as_frame=True, # return only data as tuple (parametrs, target)
                     return_X_y=True # return as pandas dataframe
                    )
    df_wine_predictors = data[0]
    df_wine_target = data[1]


    # Visualize 
    print("PREDICTORS (X) \n")
    print(df_wine_predictors.head())
    print("Number of predictors:", df_wine_predictors.shape[1])
    print("Number of samples:", df_wine_predictors.shape[0])
    print("--------------------------------------------------------\n")

    print("TARGET CLASSES (Y)  \n")
    print(df_wine_target.head(),"\n") 
    print("----------------------------------------------------------")
    print("Wine Classes: {} -->> [0: bad wine, 1: goof wine, 2:excellent wine]".format(df_wine_target.unique()))
    return (
        ConfusionMatrixDisplay,
        SVC,
        df_wine_predictors,
        df_wine_target,
        np,
        pd,
        plt,
        train_test_split,
        validation_curve,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check the data
    """)
    return


@app.cell
def _(df_wine_predictors):
    # Basic check for errors in the dataset
    print("Verify the type of data within the columns:\n")
    print(df_wine_predictors.dtypes,"\n")
    df_wine_predictors.columns.to_list()

    print("----------------------------------------")
 
    print("Check for NaN under the columns:\n")
    for column in df_wine_predictors.columns.to_list():
        print(column,":",df_wine_predictors[column].isnull().any())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Split training and testing sets
    """)
    return


@app.cell
def _(df_wine_predictors, df_wine_target, train_test_split):
    X_train, X_test, y_train, y_test = train_test_split(df_wine_predictors,  
                                                        df_wine_target,
                                                        test_size=0.33, # percentage of data that goes into the testing set
                                                        random_state=42 # seed for random selection of data
                                                       )

    # visualize
    print("TRAINING DATASET PREDICTORS")
    print(X_train.head(), "\n")
    print("dataframe size", X_train.shape,"\n")
    print("------------------------------------------")
    print("TRAINING DATASET TARGET")
    print(y_train,"\n")
    print()
    print("------------------------------------------------------------------------------------\n")

    print("TESTING DATASET PREDICTORS")
    print(X_test.head())
    print("dataframe size", X_test.shape,"\n")
    print("------------------------------------------")
    print("TESTING DATASET TARGET")
    print(y_test.head())
    print("Vector size", y_test.shape)
    return X_test, X_train, y_test, y_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## k-fold Cross Validation
    """)
    return


@app.cell
def _(SVC, X_train, np, plt, validation_curve, y_train):
    # interval of possible parameters 
    param_range = np.logspace(-7, -0.01, 20) 

    # Peform 5-fold cross-validation and save training and validation error
    train_scores, test_scores = validation_curve(
        SVC(),
        X_train, 
        y_train,
        param_name="gamma", # parameter to vary
        param_range=param_range,
        scoring="accuracy", 
        cv=5,    # number of folders
    )


    # convert accuracy into error
    train_error = 1-train_scores
    validation_error = 1-test_scores

    # compute 5-fold cross-validation mean and std of error 
    train_error_mean = np.mean(train_error, axis=1)
    train_error_std = np.std(train_error, axis=1)
    validation_error_mean = np.mean(validation_error, axis=1)
    validation_error_std = np.std(validation_error, axis=1)

    # visualize
    plt.title("Validation Curve with SVM")
    plt.xlabel(r"$\gamma$")
    plt.ylabel("Error (1-accuracy)")
    plt.ylim(-0.01, 1.1)
    lw = 2
    plt.semilogx(
        param_range, train_error_mean, label="Training score", color="darkorange", lw=lw
    )
    plt.fill_between(
        param_range,
        train_error_mean - train_error_std,
        train_error_mean + train_error_std,
        alpha=0.2,
        color="darkorange",
        lw=lw,
    )
    plt.semilogx(
        param_range, validation_error_mean, label="Cross-validation score", color="navy", lw=lw
    )
    plt.fill_between(
        param_range,
        validation_error_mean - validation_error_std,
        validation_error_mean + validation_error_std,
        alpha=0.2,
        color="navy",
        lw=lw,
    )
    plt.legend(loc="best")
    plt.show()
    return param_range, validation_error_mean


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose optimal parameter
    """)
    return


@app.cell
def _(np, param_range, pd, validation_error_mean):
    # save optimal gamma
    index_min = min(range(len(validation_error_mean)), key=validation_error_mean.__getitem__)
    validation_error_min = validation_error_mean[index_min]
    gamma_opt = param_range[index_min] # gamma that gives minimun validation error

    # visualize 
    columns = ["Mean validation error","gamma"]
    array = np.array([validation_error_mean, param_range]).transpose()

    print( pd.DataFrame(array,columns=columns), "\n")
    print("Minimun mean validation error:", validation_error_min)
    print("optimal gamma:", gamma_opt)
    return (gamma_opt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Train the optimal hypothesis model
    """)
    return


@app.cell
def _(SVC, X_test, X_train, gamma_opt, y_test, y_train):
    # train optimal model and evaluate accuracy 
    h_opt = SVC(gamma=gamma_opt) # instiate optimal model 
    h_opt.fit(X_train,y_train) # train the model to the entire training set
    print("Error (1-Accuracy) of h_opt on testing data: \n -->>",1- h_opt.score(X_test,y_test))
    return (h_opt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Performance evaluation
    """)
    return


@app.cell
def _(ConfusionMatrixDisplay, X_test, h_opt, plt, y_test):
    #plot confution Matrix
    ConfusionMatrixDisplay.from_estimator(
        h_opt, # trained optimal hypothesis model
        X_test,
        y_test,
        display_labels=["bad wine", "good wine", "excellent wine"]
    )
    plt.show()
    return


if __name__ == "__main__":
    app.run()
