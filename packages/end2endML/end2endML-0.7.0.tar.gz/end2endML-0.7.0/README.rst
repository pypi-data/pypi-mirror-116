Installation
============

Prerequisites
-------------

The end2endML package requires the following dependencies:

.. code:: 

   numpy>=1.19
   pandas>=1.1
   scikit-learn>=0.23
   imbalanced-learn>=0.8.0
   pandas-profiling>=2.9.0
   joblib
   xgboost>=1.4 
   optuna>=2.7

Install
-------

It is recommended to use a virtual environment to install the package
and its dependencies. You can use the following command to create a
virtual environment, ``conda create --name your_env_name``. The package
can be installed as ``pip install -U end2endML`` after I upload the
package to PyPI.

I have already tested the packaging process in the test PyPI. Now the
test package can be installed as
``pip install -i https://test.pypi.org/simple/ end2endML``. However, as
the test PyPI is only for testing, it doesn't contain all the required
dependencies. Therefore, the dependencies will not automatically
installed by pip when test PyPI is used. When the package is uploaded to
PyPI, pip will automate install all the specified dependencies. Now you
can manually install all the dependencies by the following command
``pip install -r requirements.txt``

User Guide
==========

A general introduction
----------------------

The end2endML package implemented all the components, data
preprocessing, data splitting, model selection, model fitting and model
evaluation, required for defining pipelines to do do automate data
analysis using some most commonly used machine learning algorithms. Some
of the key components are summarised as follows.

Read and summarise the raw data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using the following script to check the arguments to control the
behaviour of loading data and summarising data.

``import end2endML.utilities as utilities``

``help(utilities.read_data)``

``help(utilities.summarize_data)``

Key points

-  Only csv and sas7bdat format data sets are allowed.

-  The data set is supposed to only contains features X and outcome y.

Data splitting
~~~~~~~~~~~~~~

``help(utilities.split_data)``

key points

-  When test_size == 0, K-Fold CV will be used to evaluate the selected
   models.

-  When test_size > 0, test size will be used to evaluate the selected
   models. In addition, K-Fold CV can also be used.

Data preprocessing
~~~~~~~~~~~~~~~~~~

Using the following script to check the arguments to control the
behaviour of the data preprocessing process.

``from end2endML.preprocessing import data_preprocessing``

``help(data_preprocessing)``

Key points

-  All the samples with missing values at the outcome are removed.

-  All the features with unique values less than a threshould, e.g., 15,
   are taken as categorical variables.

-  The columns contain strings and over 15 unique values are taken as
   text data, and are dropped.

-  Samples and features with more than 50% missing values are dropped.

-  Categorical variables are one-hot coded with missing value as a new
   level and the first column is dropped.

-  Median imputation is used to tackle the missing values in
   quantitative variables.

-  Variables with a single unique value are dropped.

Select and Fit the models
~~~~~~~~~~~~~~~~~~~~~~~~~

Using the following script to check the arguments to control the
behaviour of automate model selection and fitting.

``from end2endML.automate_modeling_evaluation import automate_modeling``

``help(automate_modeling)``

Key points

-  Depends on the data type of outcome y and its unique values, the
   modelling will be classified as the following tasks, regression,
   binary and multiclass classification.

-  The following models, standard linear model (linear), linear model
   with lasso penalty (lasso), linear model with ridge penalty (ridge);
   linear model with ElasticNet penalty (elasticNet), support vector
   machine (svm), neural network (nn), gradient boosting (gb), random
   forest (rf) are installed for all the above three tasks.

-  When imbalances is high, majority category is over 10 times of the
   minority category, ensemble based imbalanced learning models,
   balanced random forest model, Random under-sampling integrated in the
   learning of AdaBoost and Bag of balanced boosted learners, are used
   to model the data.

-  For, lasso, ridge and elasticNet, the model selection is based on the
   model selection procedures provided by sklearn.

-  For svm, nn, gb and rf, Bayesian optimization is used to do the model
   selection. The evaluation is based on either K-Fold CV or the
   performance on the validation set.

Evaluate the selected models using multiple metrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

key points

-  The selected model can be evaluated on test set and (or) through
   K-Fold CV.

-  | For classification problem, these metrics, sensitivity,
     specificity, balanced_accuracy, recall, precision
   | f1_score and AUC, are used.

-  For regression problem, these metrics, :math:`R^2`, mean squared
   error (MSE) and mean absolute error (MAE), are used.

Saved data report, preprocessed data and saved models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The generated data summarization report, preprocessed data sets, saved
models and saved evaluation metrics are in the results folder of the
current working directory.

Automate data analysis
----------------------

Automate data analysis can be done in the following way. The generated
data summarization report, preprocessed data sets, saved models and
saved evaluation metrics are in the results folder of the current
working directory. When such a results folder is not available, the data
analysis procedure will create one by itself.

``from end2endML.automate_analysis import automate_analysis``

``help(automate_analysis)``

``# define path2data and outcome``

``path2data = 'the path to your data set'``

``outcome = 'the outcome variable in the data'``

``automate_analysis(path2data, outcome)``

Command line interface
~~~~~~~~~~~~~~~~~~~~~~

For some data analyst, especially those who works on the remote server
via command line, the command line interface is always preferred. We
also implemented the command line interface. The script can be found in
https://gitlab.com/YipengUva/end2endml/-/blob/master/automate_analysis_pipeline.py.
The usage of the command line interface is show as follows

``python automate_analysis --help``

``python automate_analysis --path2data='your path to data' --outcome='your outcome variable'``

Semi-automate data analysis
---------------------------

Some data analyst would prefer a semi-automate data analysis pipeline,
so they can also more control over the whole process, or they just want
to use part of the process. We use defined a template pipeline in to do
semi-automate data analysis. The pipeline is an almost copy of the
ene2endML.automate_analysis precedure. The script is in
https://gitlab.com/YipengUva/end2endml/-/blob/master/semi-automate_analysis_pepeline.py.

Explore the saved results
-------------------------

All the results are saved in the results folder of the current
directory. Suppose the experiment name, which is a combination of the
data name and the outcome name, is name. Usually, the following results
are saved.

-  name_profile_report.html contains a report to summarise the data set.

-  name.npz contains the design matrix X, the outcome y, the sample
   index sample_index and the variable names feature_names.

-  name_saved_selected_models.joblib saves all the results. Load this
   file into python using joblib.load will result into a dictionary,
   which can be called as results. The key of the results is the
   model_name, the value is the saved model. The saved model is an
   object of a self defined class. print(results['model_name']) to see
   how to get access to the selected hyperparameters, the searching
   range of the hyperparameters, the selected models, the feature
   importance, and the time used to train and select the model.

The script to load and explore the data sets can be shown as follows.

``import joblib``

``path2results = './results/name_saved_selected_models.joblib'``

``results = joblib.load(path2results)``

``print(results.keys())``

``model_name = 'clf_gb'``

``selected_model = results[model_name]``

``print(selected_model)``

TODO
====

-  [STRIKEOUT:Implement feature extraction feature to the models.]

   -  The feature extraction methods only implemented for linear models,
      svm and neural network. For Tree based methods, they are not
      implemented.

   -  The number of components are taken as a hyperparameter for model
      selection.

-  Implement the unite test suite to do automate testing for every
   update.

-  [STRIKEOUT:Currently, if we specify a gradient boosting model for
   imbalanced classification both RUSBOOST and EASYENSYMBLE, which
   differs in how the undersampling is implemented, are selected and
   trained. Need to find a way to let the user to set it.]

-  [STRIKEOUT:If the trained model has already used 10 cores, specify
   the CV procedure to use another 10 cores, in general is Ok. However,
   it can be a problem for easyensemble models when the data set is
   large. Fix it by set the CV procedure n_jobs to be None in
   easyensembler model]

-  [STRIKEOUT:Add the fun to check if the preprocessed data is
   avaliable. If the data is avaliable, there is no need to preprocess
   the data anymore. Myabe this is not a good idea, as sometime we may
   use different parameters to control the behavior to do data
   preprocessing. And the time to re-preprocess time is not much.]

-  [STRIKEOUT:Bug. The data analysis pipline should has the ability to
   remove the inifnte values existed in X and y.]

-  [STRIKEOUT:When cat_threshold set to 2, which means we are not going
   to classify the subjects with numerical data type but with limited
   unique values, then the y will not be transformed to object data
   type, then the automate data analysis procedure will take it as a
   regression task.]

-  [STRIKEOUT:We should re-save the preprocessed data sets every time.
   Currently, if the function detect the preprocessed data has already
   saved, it will not save the preprocessed data anymore. This can lead
   to serious issue when the data preprocessing parameters change. In
   addition, it doesn't take much time, we should save the preprocessed
   data.]

-  [STRIKEOUT:For binary classificatoin and regression problems, the
   saved feature importances should be one dimentional rather than two
   dimensional.]

-  --user, why

-  Keep track of all the preprocessing steps, so we can apply the exat
   same preprocessing steps to the new data.

-  Add Dan and Mengzhe

-  Print out time
