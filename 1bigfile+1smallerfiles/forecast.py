import numpy as np
import datetime
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    accuracy_score,
    balanced_accuracy_score,
    hamming_loss,
)

# sklearn: Linear Models
from sklearn.linear_model import (
    LinearRegression,
    SGDRegressor,
    Ridge,
    Lasso,
    ElasticNet,
    Lars,
    LassoLars,
    OrthogonalMatchingPursuit,
    BayesianRidge,
    ARDRegression,
    LogisticRegression,
    TweedieRegressor,
    PassiveAggressiveRegressor,
    TheilSenRegressor,
    HuberRegressor,
    QuantileRegressor,
    # RANSACRegressor,
)

# sklearn: Ensemble Models
from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier,
    ExtraTreesRegressor,
    ExtraTreesClassifier,
    BaggingRegressor,
    BaggingClassifier,
    GradientBoostingRegressor,
    GradientBoostingClassifier,
    HistGradientBoostingRegressor,
    HistGradientBoostingClassifier,
    AdaBoostRegressor,
    AdaBoostClassifier,
)

# sklearn: Tree Models
from sklearn.tree import (
    DecisionTreeRegressor,
    DecisionTreeClassifier,
)

# sklearn: Neighbors Models
from sklearn.neighbors import (
    KNeighborsRegressor,
    KNeighborsClassifier,
    RadiusNeighborsRegressor,
    RadiusNeighborsClassifier,
    NearestCentroid,
)

# sklearn: Support-Vector Models
from sklearn.svm import SVR, SVC, NuSVR, NuSVC, LinearSVR, LinearSVC

# sklearn: Neural-Network Models
from sklearn.neural_network import MLPRegressor, MLPClassifier

# sklearn: KernelRidge Models
from sklearn.kernel_ridge import KernelRidge

# sklearn: Isotonic Models
from sklearn.isotonic import IsotonicRegression

# sklearn: Cross-Decomposition Models
from sklearn.cross_decomposition import PLSRegression, PLSCanonical

# sklearn: Naive-Bayes Models
from sklearn.naive_bayes import (
    GaussianNB,
    MultinomialNB,
    ComplementNB,
    BernoulliNB,
    CategoricalNB,
)
from api.models import ConnectionProfile
from qubles.core.quble import Quble
from qubles.core.iterators.quble_iterators import (
    DistinctOrthoIndexIterator,
)
from qubles.io.base.datalib import DataLib
from qubles.io.util.libaddress import LibAddress
from qubles.io.util.multi_build_lib import MultiBuildLib
from qubles.io.base.rootlib import RootLib, ControlContextManager
from qubles.io.base.analyticlib import AnalyticLib
from qubles.io.util.model_utils import generate_random_table_name
from qubles.io.snowflake.core import execute, execute_with_timeout
from qubles.util.logger import init_logger
from qubles.io.snowflake.constants import ML_STATEMENT_TIMEOUT_IN_SECONDS

_logger = init_logger(__name__)


class Forecast(AnalyticLib):
    # Assume each of these linear models has attribute: "coef_", "intercept_"
    LINEAR_REGRESSORS = [
        "LinearRegression",
        "SGDRegressor",
        "Ridge",
        "Lasso",
        "ElasticNet",
        "Lars",
        "LassoLars",
        "OrthogonalMatchingPursuit",
        "BayesianRidge",
        "ARDRegression",
        "LogisticRegression",
        "TweedieRegressor",
        "PassiveAggressiveRegressor",
        "TheilSenRegressor",
        "HuberRegressor",
        "QuantileRegressor",
        # "RANSACRegressor",
    ]
    LINEAR_CLASSIFIERS = []
    NON_LINEAR_REGRESSORS = [
        "RandomForestRegressor",
        "BaggingRegressor",
        "AdaBoostRegressor",
        "DecisionTreeRegressor",
        "SVR",
        "NuSVR",
        "LinearSVR",
        "KNeighborsRegressor",
        "RadiusNeighborsRegressor",
        "MLPRegressor",
        "ExtraTreesRegressor",
        "HistGradientBoostingRegressor",
        "DecisionTreeRegressor",
        "PLSRegression",
        "PLSCanonical",
        "KernelRidge",
        "IsotonicRegression",
    ]
    NON_LINEAR_CLASSIFIERS = [
        "RandomForestClassifier",
        "BaggingClassifier",
        "AdaBoostClassifier",
        "DecisionTreeClassifier",
        "SVC",
        "NuSVC",
        "LinearSVC",
        "KNeighborsClassifier",
        "RadiusNeighborsClassifier",
        "MLPClassifier" "ExtraTreesClassifier",
        "HistGradientBoostingClassifier",
        "DecisionTreeClassifier",
        "NearestCentroid",
        "GaussianNB",
        "MultinomialNB",
        "ComplementNB",
        "BernoulliNB",
        "CategoricalNB",
    ]
    REGRESSORS = LINEAR_REGRESSORS + NON_LINEAR_REGRESSORS
    CLASSIFIERS = LINEAR_CLASSIFIERS + NON_LINEAR_CLASSIFIERS
    LINEAR_MODELS = LINEAR_REGRESSORS + LINEAR_CLASSIFIERS
    NON_LINEAR_MODELS = NON_LINEAR_REGRESSORS + NON_LINEAR_CLASSIFIERS
    ALL_MODELS = REGRESSORS + CLASSIFIERS

    FORECAST_PROPERTIES = (
        "model_mode",
        "output_mode",
        "output_transform",
        "security_keyspace",
        "dates_keyspace",
        "summary_keyspace",
        "feature_keyspace",
        "offset_key",
        "fitness_keyspace",
        "sample_keyspace",
        "feature_transform",
        "horizon",
        "feature_delay",
        "feature_tfill_max",
        "num_stagger",
        "stagger_persist",
        "daterange_mode",
        "horizon_keyspace",
        "delay_keyspace",
        "stagger_keyspace",
        "daterange_keyspace",
    )

    REDEFINE_PROPERTY_LIST = AnalyticLib.REDEFINE_PROPERTY_LIST + FORECAST_PROPERTIES

    description_dict = {
        "PREDICTIONS": "Predictions",
        "PREDICTIONS_XCORR": "Historical Cross-Sectional (Cross-Security) Correlation of Security Alphas",
        "PREDICTIONS_XCORR_SUMMARY": "Summary of Cross-Sectional (Cross-Security) Correlation of Security Alphas",
        "ASSET_FWD_RETURNS": "Security Forward Returns (at Specified Return Horizon)",
        "OUTPUTS": "Normalized/Cleansed Outputs (Dependent Variable)",
        "BASE_OUTPUTS": "Source (Non-Normalized / Non-Cleansed) Outputs",
        "ASSET_RETURNS": "Security Returns [Format:1.0=100%]",
        "ASSET_RETURNS_100": "Security Returns [Format:100.0=100%]",
        "ASSET_NEXT_RETS": "Security Returns over the Next Period [Format:1.0=100%]",
        "ASSET_NEXT_RETS_100": "Security Returns over the Next Period [Format:100.0=100%]",
        "ASSET_TRI": "Security Total Return Index",
        "MODEL": "Forecasting Model",
        "DATE_RANGES": "Date Ranges for Conditional Historical Analysis (Historical Booleans)",
        "FEATURES": "Normalized / Transformed / Screened Factors: Serves as Independent Variables for Forward Return Forecast",
        "BASE_FEATURES": "Source (Non-Normalized / Non-Cleansed) Security Features (Factors)",
        "TRAINING_FITNESS": "Training Fitness Metrics (RSQ, NUM_OBS, ...)",
        "TRAINING_DETAIL": "Training Details (COEFFS, STD_ERRS, TSTATS, P_VALUES, IC)",
        "TRAINING_PANEL": "Training Panel Data (Cleansed Outputs + Features)",
        "APPLIED_FITNESS": "Applied Fitness Metrics (RSQ, NUM_OBS, ...)",
        "SCREEN": "Pre-Screen Applied to Security Factors",
    }

    # ======================================= NLP MODEL CONFIGURATIONS =====================================

    model_constructor = {}  # <-- Will be assigned per model below
    model_constructor_name = {}  # <-- Will be assigned per model below
    model_fit_fn_attr_name = {}  # <-- Will be assigned per model below
    model_predict_fn_attr_name = {}  # <-- Will be assigned per model below
    model_constructor_arg_defaults = {}  # <-- Will be assigned per model below
    model_required_non_cnstr_attribs = {}  # <-- Will be assigned per model below
    model_optional_non_cnstr_attribs = {}  # <-- Will be assigned per model below

    # List of any model constructor args that expect int list
    # (to trap for string property asignments that will need conversion to int list)
    constructor_args_that_expect_int_list = ["hidden_layer_sizes"]

    # ================================= RandomForestRegressor MODEL CONFIGURATION =====================================

    # ================================= LinearRegression MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # LinearRegression: Ordinary least squares Linear Regression
    # LinearRegression Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  fit_intercept: bool (default=True)
    #     Whether to calculate the intercept for this model.
    #     If set to False, no intercept will be used in calculations
    #     (i.e. data is expected to be centered).
    #
    #  normalize: bool (default=False)
    #     This parameter is ignored when fit_intercept is set to False.
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0 and will be removed in 1.2.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  n_jobs: int (default=None)
    #     The number of jobs to use for the computation.
    #     This will only provide speedup in case of sufficiently large problems,
    #     that is if firstly n_targets > 1 and secondly X is sparse
    #     or if positive is set to True.
    #     None means 1 unless in a joblib.parallel_backend context.
    #     -1 means using all processors. See Glossary for more details.
    #
    #  positive: bool (default=False)
    #     When set to True, forces the coefficients to be positive.
    #     This option is only supported for dense arrays.
    # --------------------------------------------------
    model_constructor["LinearRegression"] = LinearRegression
    model_constructor_name["LinearRegression"] = "LinearRegression"
    model_fit_fn_attr_name["LinearRegression"] = "fit"
    model_predict_fn_attr_name["LinearRegression"] = "predict"
    model_constructor_arg_defaults["LinearRegression"] = {
        "fit_intercept": True,
        # "normalize": False, # Deprecated since version 1.0
        "copy_X": True,
        "n_jobs": None,
        "positive": False,
    }
    model_required_non_cnstr_attribs["LinearRegression"] = [
        "coef_",
        "intercept_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["LinearRegression"] = [
        "rank_",  # New in version 1.0
        "singular_",
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= SGDRegressor MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # SGDRegressor: Linear model fitted by minimizing a regularized empirical loss with SGD
    # SGDRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  loss: str (default="squared_error")
    #     The loss function to be used.
    #     The possible values are 'squared_error', 'huber',
    #     'epsilon_insensitive', or 'squared_epsilon_insensitive'
    #
    #     The 'squared_error' refers to the ordinary least squares fit.
    #
    #     'huber' modifies 'squared_error' to focus less on getting outliers correct
    #     by switching from squared to linear loss past a distance of epsilon.
    #
    #     'epsilon_insensitive' ignores errors less than epsilon and is linear past that;
    #     this is the loss function used in SVR.
    #
    #     'squared_epsilon_insensitive' is the same but becomes
    #     squared loss past a tolerance of epsilon.
    #
    #     More details about the losses formulas can be found in the User Guide.
    #
    #     Deprecated since version 1.0: The loss 'squared_loss' was deprecated in v1.0
    #     and will be removed in version 1.2.
    #     Use loss='squared_error' which is equivalent.
    #
    #  penalty: str {'l2', 'l1', 'elasticnet'} (default='l2')
    #     The penalty (aka regularization term) to be used.
    #     Defaults to 'l2' which is the standard regularizer for linear SVM models.
    #
    #     'l1' and 'elasticnet' might bring sparsity to the model
    #     (feature selection) not achievable with 'l2'.
    #
    #  alpha: float (default=0.0001)
    #     Constant that multiplies the regularization term.
    #     The higher the value, the stronger the regularization.
    #     Also used to compute the learning rate
    #     when set to learning_rate is set to 'optimal'.
    #
    #  l1_ratio: float (default=0.15)
    #     The Elastic Net mixing parameter, with 0 <= l1_ratio <= 1.
    #     l1_ratio=0 corresponds to L2 penalty, l1_ratio=1 to L1.
    #     Only used if penalty is 'elasticnet'.
    #
    #  fit_intercept: bool (default=True)
    #     Whether the intercept should be estimated or not.
    #     If False, the data is assumed to be already centered.
    #
    #  max_iter: int (default=1000)
    #     The maximum number of passes over the training data (aka epochs).
    #     It only impacts the behavior in the fit method,
    #     and not the partial_fit method.
    #     New in version 0.19.
    #
    #  tol: float (default=1e-3)
    #     The stopping criterion
    #     If it is not None, training will stop when (loss > best_loss - tol)
    #     for n_iter_no_change consecutive epochs.
    #     Convergence is checked against the training loss
    #     or the validation loss depending on the early_stopping parameter.
    #     New in version 0.19.
    #
    #  shuffle: bool (default=True)
    #     Whether or not the training data should be shuffled after each epoch.
    #
    #  verbose: int (default=0)
    #     The verbosity level.
    #
    #  epsilon: float (default=0.1)
    #     Epsilon in the epsilon-insensitive loss functions;
    #     only if loss is 'huber', 'epsilon_insensitive', or 'squared_epsilon_insensitive'.
    #     For 'huber', determines the threshold at which it becomes less important
    #     to get the prediction exactly right.
    #
    #     For epsilon-insensitive, any differences between the current prediction
    #     and the correct label are ignored if they are less than this threshold.
    #
    #  random_state: int, RandomState instance (default=None)
    #     Used for shuffling the data, when shuffle is set to True.
    #     Pass an int for reproducible output across multiple function calls.
    #     See Glossary.
    #
    #  learning_rate: str (default='invscaling')
    #     The learning rate schedule:
    #
    #        'constant': eta = eta0
    #        'optimal': eta = 1.0 / (alpha * (t + t0))
    #           where t0 is chosen by a heuristic proposed by Leon Bottou.
    #        'invscaling': eta = eta0 / pow(t, power_t)
    #        'adaptive': eta = eta0, as long as the training keeps decreasing.
    #           Each time n_iter_no_change consecutive epochs fail to decrease
    #           the training loss by tol or fail to increase validation score
    #           by tol if early_stopping is True, the current learning rate
    #           is divided by 5.
    #
    #      New in version 0.20: Added 'adaptive' option
    #
    #  eta0: float (default=0.01)
    #     The initial learning rate for the
    #     'constant', 'invscaling' or 'adaptive' schedules.
    #     The default value is 0.01.
    #
    #  power_t: float (default=0.25)
    #     The exponent for inverse scaling learning rate.
    #
    #  early_stopping: bool (default=False)
    #     Whether to use early stopping to terminate training
    #     when validation score is not improving.
    #
    #     If set to True, it will automatically set aside a fraction
    #     of training data as validation and terminate training when
    #     validation score returned by the score method is not improving by
    #     at least tol for n_iter_no_change consecutive epochs.
    #
    #     New in version 0.20: Added 'early_stopping' option
    #
    #  validation_fraction: float (default=0.1)
    #     The proportion of training data to set aside as validation set for early stopping.
    #     Must be between 0 and 1.
    #     Only used if early_stopping is True.
    #     New in version 0.20: Added 'validation_fraction' option
    #
    #  n_iter_no_change: int (default=5)
    #     Number of iterations with no improvement to wait before stopping fitting.
    #     Convergence is checked against the training loss
    #     or the validation loss depending on the early_stopping parameter.
    #     New in version 0.20: Added 'n_iter_no_change' option
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call to fit
    #     as initialization, otherwise, just erase the previous solution.
    #     See the Glossary.
    #
    #     Repeatedly calling fit or partial_fit when warm_start is True
    #     can result in a different solution than when calling fit a single time
    #     because of the way the data is shuffled.
    #
    #     If a dynamic learning rate is used, the learning rate is adapted
    #     depending on the number of samples already seen.
    #
    #     Calling fit resets this counter, while partial_fit
    #     will result in increasing the existing counter.
    #
    #  average: bool or int (default=False)
    #     When set to True, computes the averaged SGD weights across
    #     all updates and stores the result in the coef_ attribute.
    #
    #     If set to an int greater than 1, averaging will begin once
    #     the total number of samples seen reaches average.
    #
    #     So average=10 will begin averaging after seeing 10 samples.
    # --------------------------------------------------
    model_constructor["SGDRegressor"] = SGDRegressor
    model_constructor_name["SGDRegressor"] = "SGDRegressor"
    model_fit_fn_attr_name["SGDRegressor"] = "fit"
    model_predict_fn_attr_name["SGDRegressor"] = "predict"
    model_constructor_arg_defaults["SGDRegressor"] = {
        "loss": "squared_error",
        "penalty": "l2",
        "alpha": 0.0001,
        "l1_ratio": 0.15,
        "fit_intercept": True,
        "max_iter": 1000,
        "tol": 1e-3,
        "shuffle": True,
        "verbose": 0,
        "epsilon": 0.1,
        "random_state": None,
        "learning_rate": "invscaling",
        "eta0": 0.01,
        "power_t": 0.25,
        "early_stopping": False,
        "validation_fraction": 0.1,
        "n_iter_no_change": 5,
        "warm_start": False,
        "average": False,
    }
    model_required_non_cnstr_attribs["SGDRegressor"] = [
        "coef_",
        "intercept_",
        "n_iter_",
        "t_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["SGDRegressor"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= Ridge MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # Ridge: Linear least squares with l2 regularization
    # Ridge Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  alpha: {float, ndarray of shape (n_targets,)} (default=1.0)
    #     Constant that multiplies the L2 term, controlling regularization strength.
    #     alpha must be a non-negative float i.e. in [0, inf).
    #
    #     When alpha = 0, the objective is equivalent to ordinary least squares,
    #     solved by the LinearRegression object.
    #
    #     For numerical reasons, using alpha = 0 with the Ridge object is not advised.
    #     Instead, you should use the LinearRegression object.
    #
    #     If an array is passed, penalties are assumed to be specific to the targets.
    #     Hence they must correspond in number.
    #
    #  fit_intercept: bool (default=True)
    #     Whether to fit the intercept for this model.
    #     If set to false, no intercept will be used in calculations
    #     (i.e. X and y are expected to be centered).
    #
    #  normalize: bool (default=False)
    #     This parameter is ignored when fit_intercept is set to False.
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0 and will be removed in 1.2.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  max_iter: int (default=None)
    #     Maximum number of iterations for conjugate gradient solver.
    #
    #     For 'sparse_cg' and 'lsqr' solvers, the default value
    #     is determined by scipy.sparse.linalg.
    #
    #     For 'sag' solver, the default value is 1000.
    #
    #     For 'lbfgs' solver, the default value is 15000.
    #
    #  tol: float (default=1e-3)
    #     Precision of the solution.
    #
    #  solver: {'auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga', 'lbfgs'} (default='auto')
    #     Solver to use in the computational routines:
    #
    #     'auto' chooses the solver automatically based on the type of data.
    #     'svd' uses a Singular Value Decomposition of X to compute the Ridge coefficients. It is the most stable solver, in particular more stable for singular matrices than 'cholesky' at the cost of being slower.
    #     'cholesky' uses the standard scipy.linalg.solve function to obtain a closed-form solution.
    #     'sparse_cg' uses the conjugate gradient solver as found in scipy.sparse.linalg.cg. As an iterative algorithm, this solver is more appropriate than 'cholesky' for large-scale data (possibility to set tol and max_iter).
    #     'lsqr' uses the dedicated regularized least-squares routine scipy.sparse.linalg.lsqr. It is the fastest and uses an iterative procedure.
    #     'sag' uses a Stochastic Average Gradient descent, and 'saga' uses its improved, unbiased version named SAGA. Both methods also use an iterative procedure, and are often faster than other solvers when both n_samples and n_features are large. Note that 'sag' and 'saga' fast convergence is only guaranteed on features with approximately the same scale. You can preprocess the data with a scaler from sklearn.preprocessing.
    #     'lbfgs' uses L-BFGS-B algorithm implemented in scipy.optimize.minimize. It can be used only when positive is True.
    #
    #     All solvers except 'svd' support both dense and sparse data.
    #     However, only 'lsqr', 'sag', 'sparse_cg', and 'lbfgs'
    #     support sparse input when fit_intercept is True.
    #
    #     New in version 0.17: Stochastic Average Gradient descent solver.
    #     New in version 0.19: SAGA solver.
    #
    #  positive: bool (default=False)
    #     When set to True, forces the coefficients to be positive.
    #     Only 'lbfgs' solver is supported in this case.
    #
    #  random_state: int, RandomState instance (default=None)
    #     Used when solver == 'sag' or 'saga' to shuffle the data.
    #     See Glossary for details.
    #     New in version 0.17: random_state to support Stochastic Average Gradient.
    #
    # --------------------------------------------------
    model_constructor["Ridge"] = Ridge
    model_constructor_name["Ridge"] = "Ridge"
    model_fit_fn_attr_name["Ridge"] = "fit"
    model_predict_fn_attr_name["Ridge"] = "predict"
    model_constructor_arg_defaults["Ridge"] = {
        "alpha": 1.0,
        "fit_intercept": True,
        # "normalize": False, # Deprecated since version 1.0
        "copy_X": True,
        "max_iter": None,
        "tol": 1e-3,
        "solver": "auto",
        "positive": False,
        "random_state": None,
    }
    model_required_non_cnstr_attribs["Ridge"] = [
        "coef_",
        "intercept_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["Ridge"] = [
        "n_iter_",
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= Lasso MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # Lasso: Linear Model trained with L1 prior as regularizer (aka the Lasso)
    # Lasso Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  alpha: float (default=1.0)
    #     Constant that multiplies the L1 term,
    #     controlling regularization strength.
    #     alpha must be a non-negative float i.e. in [0, inf).
    #
    #     When alpha = 0, the objective is equivalent to ordinary least squares,
    #     solved by the LinearRegression object. For numerical reasons,
    #     using alpha = 0 with the Lasso object is not advised.
    #
    #     Instead, you should use the LinearRegression object.
    #
    #  fit_intercept: bool (default=True)
    #     Whether to calculate the intercept for this model.
    #     If set to False, no intercept will be used in calculations
    #    (i.e. data is expected to be centered).
    #
    #  normalize: bool (default=False)
    #     This parameter is ignored when fit_intercept is set to False.
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0 and will be removed in 1.2.
    #
    #  precompute: bool or array-like of shape (n_features, n_features) (default=False)
    #     Whether to use a precomputed Gram matrix to speed up calculations.
    #     The Gram matrix can also be passed as argument.
    #     For sparse input this option is always False to preserve sparsity.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  max_iter: int (default=1000)
    #     The maximum number of iterations.
    #
    #  tol: float (default=1e-4)
    #     The tolerance for the optimization: if the updates are smaller than tol,
    #     the optimization code checks the dual gap for optimality
    #     and continues until it is smaller than tol, see Notes below.
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call to fit
    #     as initialization, otherwise, just erase the previous solution.
    #     See the Glossary.
    #
    #  positive: bool (default=False)
    #     When set to True, forces the coefficients to be positive.
    #
    #  random_state: int, RandomState instance (default=None)
    #     The seed of the pseudo random number generator
    #     that selects a random feature to update.
    #     Used when selection == 'random'.
    #     Pass an int for reproducible output across multiple function calls.
    #     See Glossary.
    #
    #  selection: {'cyclic', 'random'}, default='cyclic'
    #     If set to 'random', a random coefficient is updated every iteration
    #     rather than looping over features sequentially by default.
    #
    #     This (setting to 'random') often leads to significantly
    #     faster convergence especially when tol is higher than 1e-4.
    # --------------------------------------------------
    model_constructor["Lasso"] = Lasso
    model_constructor_name["Lasso"] = "Lasso"
    model_fit_fn_attr_name["Lasso"] = "fit"
    model_predict_fn_attr_name["Lasso"] = "predict"
    model_constructor_arg_defaults["Lasso"] = {
        "alpha": 1.0,
        "fit_intercept": True,
        # "normalize": False, # Deprecated since version 1.0
        "precompute": False,
        "copy_X": True,
        "max_iter": 1000,
        "tol": 1e-4,
        "warm_start": False,
        "positive": False,
        "random_state": None,
        "selection": "cyclic",
    }
    model_required_non_cnstr_attribs["Lasso"] = [
        "coef_",
        "dual_gap_",
        "sparse_coef_",
        "intercept_",
        "n_iter_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["Lasso"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= ElasticNet MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # ElasticNet: Linear regression with combined L1 and L2 priors as regularizer
    # ElasticNet Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  alpha: float (default=1.0)
    #     Constant that multiplies the penalty terms.
    #     Defaults to 1.0. See the notes for the exact
    #     mathematical meaning of this parameter.
    #
    #     alpha = 0 is equivalent to an ordinary least square,
    #     solved by the LinearRegression object.
    #
    #     For numerical reasons, using alpha = 0 with the Lasso object
    #     is not advised. Given this, you should use the LinearRegression object.
    #
    #  l1_ratio: float (default=0.5)
    #
    #     The ElasticNet mixing parameter, with 0 <= l1_ratio <= 1.
    #     For l1_ratio = 0 the penalty is an L2 penalty.
    #     For l1_ratio = 1 it is an L1 penalty.
    #     For 0 < l1_ratio < 1, the penalty is a combination of L1 and L2.
    #
    #  fit_intercept: bool (default=True)
    #     Whether the intercept should be estimated or not.
    #     If False, the data is assumed to be already centered.
    #
    #  normalize: bool (default=False)
    #     This parameter is ignored when fit_intercept is set to False.
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0 and will be removed in 1.2.
    #
    #  precompute: bool or array-like of shape (n_features, n_features) (default=False)
    #     Whether to use a precomputed Gram matrix to speed up calculations.
    #     The Gram matrix can also be passed as argument.
    #     For sparse input this option is always False to preserve sparsity.
    #
    #  max_iter: int (default=1000)
    #     The maximum number of iterations.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  tol: float (default=1e-4)
    #     The tolerance for the optimization:
    #        if the updates are smaller than tol, the optimization code
    #        checks the dual gap for optimality and continues until
    #        it is smaller than tol, see Notes below.
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call to fit
    #     as initialization, otherwise, just erase the previous solution.
    #     See the Glossary.
    #
    #  positive: bool (default=False)
    #     When set to True, forces the coefficients to be positive.
    #
    #  random_state: int, RandomState instance (default=None)
    #     The seed of the pseudo random number generator
    #     that selects a random feature to update.
    #     Used when selection == 'random'.
    #     Pass an int for reproducible output across multiple function calls.
    #     See Glossary.
    #
    #  selection: {'cyclic', 'random'}, default='cyclic'
    #     If set to 'random', a random coefficient is updated every iteration
    #     rather than looping over features sequentially by default.
    #     This (setting to 'random') often leads to significantly faster
    #     convergence especially when tol is higher than 1e-4.
    #
    # --------------------------------------------------
    model_constructor["ElasticNet"] = ElasticNet
    model_constructor_name["ElasticNet"] = "ElasticNet"
    model_fit_fn_attr_name["ElasticNet"] = "fit"
    model_predict_fn_attr_name["ElasticNet"] = "predict"
    model_constructor_arg_defaults["ElasticNet"] = {
        "alpha": 1.0,
        "l1_ratio": 0.5,
        "fit_intercept": True,
        # "normalize": False, # Deprecated since version 1.0
        "precompute": False,
        "max_iter": 1000,
        "copy_X": True,
        "tol": 1e-4,
        "warm_start": False,
        "positive": False,
        "random_state": None,
        "selection": "cyclic",
    }
    model_required_non_cnstr_attribs["ElasticNet"] = [
        "coef_",
        "sparse_coef_",
        "intercept_",
        "n_iter_",
        "dual_gap_",
        "n_features_in",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["ElasticNet"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= Lars MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # Lars: Least Angle Regression model a.k.a. LAR
    # Lars Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  fit_intercept: bool (default=True)
    #     Whether to calculate the intercept for this model.
    #     If set to false, no intercept will be used in calculations
    #     (i.e. data is expected to be centered).
    #
    #  verbose: bool or int (default=False)
    #     Sets the verbosity amount.
    #
    #  normalize: bool (default=True)
    #     This parameter is ignored when fit_intercept is set to False.
    #
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0. It will default to False in 1.2 and be removed in 1.4.
    #
    #  precompute: bool, 'auto' or array-like (default='auto')
    #     Whether to use a precomputed Gram matrix to speed up calculations.
    #     If set to 'auto' let us decide.
    #     The Gram matrix can also be passed as argument.
    #
    #  n_nonzero_coefs: int (default=500)
    #     Target number of non-zero coefficients.
    #     Use np.inf for no limit.
    #
    #  eps: float (default=np.finfo(float).eps)
    #     The machine-precision regularization in the computation
    #     of the Cholesky diagonal factors.
    #     Increase this for very ill-conditioned systems.
    #     Unlike the tol parameter in some iterative optimization-based
    #     algorithms, this parameter does not control the tolerance
    #     of the optimization.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  fit_path: bool (default=True)
    #     If True the full path is stored in the coef_path_ attribute.
    #     If you compute the solution for a large problem or many targets,
    #     setting fit_path to False will lead to a speedup,
    #     especially with a small alpha.
    #
    #  jitter: float (default=None)
    #     Upper bound on a uniform noise parameter to be added to the y values,
    #     to satisfy the model's assumption of one-at-a-time computations.
    #     Might help with stability.
    #     New in version 0.23.
    #
    #  random_state: int, RandomState instance or None (default=None)
    #     Determines random number generation for jittering.
    #     Pass an int for reproducible output across multiple function calls.
    #     See Glossary. Ignored if jitter is None.
    #     New in version 0.23.
    #
    # --------------------------------------------------
    model_constructor["Lars"] = Lars
    model_constructor_name["Lars"] = "Lars"
    model_fit_fn_attr_name["Lars"] = "fit"
    model_predict_fn_attr_name["Lars"] = "predict"
    model_constructor_arg_defaults["Lars"] = {
        "fit_intercept": True,
        "verbose": False,
        # "normalize": False, # Deprecated since version 1.0
        "precompute": "auto",
        "n_nonzero_coefs": 500,
        "eps": np.finfo(float).eps,
        "copy_X": True,
        "fit_path": True,
        "jitter": None,
        "random_state": None,
    }
    model_required_non_cnstr_attribs["Lars"] = [
        "alphas_",
        "active_",
        "coef_path_",
        "coef_",
        "intercept_",
        "n_iter_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["Lars"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= LassoLars MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # LassoLars: Lasso model fit with Least Angle Regression a.k.a. Lars
    # LassoLars Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  alpha: float (default=1.0)
    #     Constant that multiplies the penalty term.
    #     Defaults to 1.0. alpha = 0 is equivalent to an ordinary least square,
    #     solved by LinearRegression.
    #
    #     For numerical reasons, using alpha = 0 with the LassoLars object
    #     is not advised and you should prefer the LinearRegression object.
    #
    #  fit_intercept: bool (default=True)
    #     Whether to calculate the intercept for this model.
    #     If set to false, no intercept will be used in calculations
    #     (i.e. data is expected to be centered).
    #
    #  verbose: bool or int (default=False)
    #     Sets the verbosity amount.
    #
    #  normalize: bool (default=True)
    #     This parameter is ignored when fit_intercept is set to False.
    #
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0. It will default to False in 1.2 and be removed in 1.4.
    #
    #  precompute: bool, 'auto' or array-like (default='auto')
    #     Whether to use a precomputed Gram matrix to speed up calculations.
    #     If set to 'auto' let us decide.
    #     The Gram matrix can also be passed as argument.
    #
    #  max_iter: int (default=500)
    #     Maximum number of iterations to perform.
    #
    #  eps: float (default=np.finfo(float).eps)
    #     The machine-precision regularization in the computation
    #     of the Cholesky diagonal factors.
    #
    #     Increase this for very ill-conditioned systems.
    #
    #     Unlike the tol parameter in some iterative optimization-based
    #     algorithms, this parameter does not control
    #     the tolerance of the optimization.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  fit_path: bool (default=True)
    #     If True the full path is stored in the coef_path_ attribute.
    #     If you compute the solution for a large problem or many targets,
    #     setting fit_path to False will lead to a speedup,
    #     especially with a small alpha.
    #
    #  positive: bool (default=False)
    #     Restrict coefficients to be >= 0.
    #
    #     Be aware that you might want to remove fit_intercept
    #     which is set True by default.
    #
    #     Under the positive restriction the model coefficients
    #     will not converge to the ordinary-least-squares solution
    #     for small values of alpha.
    #
    #     Only coefficients up to the smallest alpha value
    #     (alphas_[alphas_ > 0.].min() when fit_path=True)
    #     reached by the stepwise Lars-Lasso algorithm are typically in congruence with the solution of the coordinate descent Lasso estimator.
    #
    #  jitter: float (default=None)
    #     Upper bound on a uniform noise parameter to be added to the y values,
    #     to satisfy the model's assumption of one-at-a-time computations.
    #     Might help with stability.
    #     New in version 0.23.
    #
    #  random_state: int, RandomState instance or None (default=None)
    #     Determines random number generation for jittering.
    #     Pass an int for reproducible output across multiple function calls.
    #     See Glossary. Ignored if jitter is None.
    #     New in version 0.23.
    #
    # --------------------------------------------------
    model_constructor["LassoLars"] = LassoLars
    model_constructor_name["LassoLars"] = "LassoLars"
    model_fit_fn_attr_name["LassoLars"] = "fit"
    model_predict_fn_attr_name["LassoLars"] = "predict"
    model_constructor_arg_defaults["LassoLars"] = {
        "alpha": 1.0,
        "fit_intercept": True,
        "verbose": False,
        # "normalize": False, # Deprecated since version 1.0
        "precompute": "auto",
        "max_iter": 500,
        "eps": np.finfo(float).eps,
        "copy_X": True,
        "fit_path": True,
        "positive": False,
        "jitter": None,
        "random_state": None,
    }
    model_required_non_cnstr_attribs["LassoLars"] = [
        "alphas_",
        "active_",
        "coef_path_",
        "coef_",
        "intercept_",
        "n_iter_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["LassoLars"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ======================== OrthogonalMatchingPursuit MODEL CONFIGURATION ============================
    # --------------------------------------------------
    # OrthogonalMatchingPursuit: Orthogonal Matching Pursuit model (OMP)
    # OrthogonalMatchingPursuit Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  n_nonzero_coefs: int (default=None)
    #     Desired number of non-zero entries in the solution.
    #     If None (by default) this value is set to 10% of n_features.
    #
    #  tol: float (default=None)
    #     Maximum norm of the residual.
    #     If not None, overrides n_nonzero_coefs.
    #
    #  fit_intercept: bool (default=True)
    #     Whether to calculate the intercept for this model.
    #     If set to false, no intercept will be used in calculations
    #    (i.e. data is expected to be centered).
    #
    #  normalize: bool (default=True)
    #     This parameter is ignored when fit_intercept is set to False.
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0. It will default to False in 1.2 and be removed in 1.4.
    #
    #  precompute: 'auto' or bool (default='auto')
    #     Whether to use a precomputed Gram and Xy matrix to speed up calculations.
    #     Improves performance when n_targets or n_samples is very large.
    #     Note that if you already have such matrices,
    #     you can pass them directly to the fit method.
    #
    # --------------------------------------------------
    model_constructor["OrthogonalMatchingPursuit"] = OrthogonalMatchingPursuit
    model_constructor_name["OrthogonalMatchingPursuit"] = "OrthogonalMatchingPursuit"
    model_fit_fn_attr_name["OrthogonalMatchingPursuit"] = "fit"
    model_predict_fn_attr_name["OrthogonalMatchingPursuit"] = "predict"
    model_constructor_arg_defaults["OrthogonalMatchingPursuit"] = {
        "n_nonzero_coefs": None,
        "tol": None,
        "fit_intercept": True,
        # "normalize": True, # Deprecated since version 1.0
        "precompute": "auto",
    }
    model_required_non_cnstr_attribs["OrthogonalMatchingPursuit"] = [
        "coef_",
        "intercept_",
        "n_iter_",
        "n_nonzero_coefs_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["OrthogonalMatchingPursuit"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= BayesianRidge MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # BayesianRidge: Bayesian ridge regression
    # BayesianRidge Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  n_iter: int (default=300)
    #     Maximum number of iterations.
    #     Should be greater than or equal to 1.
    #
    #  tol: float (default=1e-3)
    #     Stop the algorithm if w has converged.
    #
    #  alpha_1: float (default=1e-6)
    #     Hyper-parameter : shape parameter for the Gamma distribution
    #     prior over the alpha parameter.
    #
    #  alpha_2: float (default=1e-6)
    #     Hyper-parameter : inverse scale parameter (rate parameter)
    #     for the Gamma distribution prior over the alpha parameter.
    #
    #  lambda_1: float (default=1e-6)
    #     Hyper-parameter : shape parameter for the Gamma distribution
    #     prior over the lambda parameter.
    #
    #  lambda_2: float (default=1e-6)
    #     Hyper-parameter : inverse scale parameter (rate parameter)
    #     for the Gamma distribution prior over the lambda parameter.
    #
    #  alpha_init: float (default=None)
    #     Initial value for alpha (precision of the noise).
    #     If not set, alpha_init is 1/Var(y).
    #     New in version 0.22.
    #
    #  lambda_init: float (default=None)
    #     Initial value for lambda (precision of the weights).
    #     If not set, lambda_init is 1.
    #     New in version 0.22.
    #
    #  compute_score: bool (default=False)
    #     If True, compute the log marginal likelihood
    #     at each iteration of the optimization.
    #
    #  fit_intercept: bool (default=True)
    #     Whether to calculate the intercept for this model.
    #     The intercept is not treated as a probabilistic parameter
    #     and thus has no associated variance. If set to False,
    #     no intercept will be used in calculations
    #     (i.e. data is expected to be centered).
    #
    #  normalize: bool (default=False)
    #     This parameter is ignored when fit_intercept is set to False.
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0 and will be removed in 1.2.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  verbose: bool (default=False)
    #     Verbose mode when fitting the model.
    #
    # --------------------------------------------------
    model_constructor["BayesianRidge"] = BayesianRidge
    model_constructor_name["BayesianRidge"] = "BayesianRidge"
    model_fit_fn_attr_name["BayesianRidge"] = "fit"
    model_predict_fn_attr_name["BayesianRidge"] = "predict"
    model_constructor_arg_defaults["BayesianRidge"] = {
        "n_iter": 300,
        "tol": 1e-3,
        "alpha_1": 1e-6,
        "alpha_2": 1e-6,
        "lambda_1": 1e-6,
        "lambda_2": 1e-6,
        "alpha_init": None,
        "lambda_init": None,
        "compute_score": False,
        "fit_intercept": True,
        # "normalize": False, # Deprecated since version 1.0
        "copy_X": True,
        "verbose": False,
    }
    model_required_non_cnstr_attribs["BayesianRidge"] = [
        "coef_",
        "intercept_",
        "alpha_",
        "lambda",
        "sigma_",
        "n_iter_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["BayesianRidge"] = [
        "scores_",
        "X_offset_",  # applicable only if normalize=True
        "X_scale_",  # applicable only if normalize=True
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= ARDRegression MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # ARDRegression: Bayesian ARD regression
    # ARDRegression Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  n_iter: int (default=300)
    #     Maximum number of iterations.
    #
    #  tol: float (default=1e-3)
    #     Stop the algorithm if w has converged.
    #
    #  alpha_1: float (default=1e-6)
    #     Hyper-parameter : shape parameter for the Gamma distribution
    #     prior over the alpha parameter.
    #
    #  alpha_2: float (default=1e-6)
    #     Hyper-parameter : inverse scale parameter (rate parameter)
    #     for the Gamma distribution prior over the alpha parameter.
    #
    #  lambda_1: float (default=1e-6)
    #     Hyper-parameter : shape parameter for the Gamma distribution
    #     prior over the lambda parameter.
    #
    #  lambda_2: float (default=1e-6)
    #     Hyper-parameter : inverse scale parameter (rate parameter)
    #     for the Gamma distribution prior over the lambda parameter.
    #
    #  compute_score: bool (default=False)
    #     If True, compute the objective function at each step of the model.
    #
    #  threshold_lambda: float (default=10 000)
    #     Threshold for removing (pruning) weights
    #     with high precision from the computation.
    #
    #  fit_intercept: bool (default=True)
    #     Whether to calculate the intercept for this model.
    #     The intercept is not treated as a probabilistic parameter
    #     and thus has no associated variance. If set to False,
    #     no intercept will be used in calculations
    #     (i.e. data is expected to be centered).
    #
    #  normalize: bool (default=False)
    #     This parameter is ignored when fit_intercept is set to False.
    #     If True, the regressors X will be normalized before regression
    #     by subtracting the mean and dividing by the l2-norm.
    #
    #     If you wish to standardize, please use StandardScaler
    #     before calling fit on an estimator with normalize=False.
    #
    #     Deprecated since version 1.0: normalize was deprecated
    #     in version 1.0 and will be removed in 1.2.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  verbose: bool (default=False)
    #     Verbose mode when fitting the model.
    #
    # --------------------------------------------------
    model_constructor["ARDRegression"] = ARDRegression
    model_constructor_name["ARDRegression"] = "ARDRegression"
    model_fit_fn_attr_name["ARDRegression"] = "fit"
    model_predict_fn_attr_name["ARDRegression"] = "predict"
    model_constructor_arg_defaults["ARDRegression"] = {
        "n_iter": 300,
        "tol": 1e-3,
        "alpha_1": 1e-6,
        "alpha_2": 1e-6,
        "lambda_1": 1e-6,
        "lambda_2": 1e-6,
        "compute_score": False,
        "threshold_lambda": 10000,
        "fit_intercept": True,
        # "normalize": False, # Deprecated since version 1.0
        "copy_X": True,
        "verbose": False,
    }
    model_required_non_cnstr_attribs["ARDRegression"] = [
        "coef_",
        "alpha_",
        "lambda",
        "sigma_",
        "intercept_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["ARDRegression"] = [
        "scores_",
        "X_offset_",  # applicable only if normalize=True
        "X_scale_",  # applicable only if normalize=True
        "feature_names_in_",
    ]
    # Exclusions: None

    # ============================= LogisticRegression MODEL CONFIGURATION =================================
    # --------------------------------------------------
    # LogisticRegression: Logistic Regression (aka logit, MaxEnt) classifier
    # LogisticRegression Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  penalty: {'l1', 'l2', 'elasticnet', 'none'} (default='l2')
    #     Specify the norm of the penalty:
    #
    #     'none': no penalty is added;
    #
    #     'l2': add a L2 penalty term and it is the default choice;
    #
    #     'l1': add a L1 penalty term;
    #
    #     'elasticnet': both L1 and L2 penalty terms are added.
    #
    #     Warning Some penalties may not work with some solvers.
    #     See the parameter solver below, to know the compatibility between the penalty and solver.
    #     New in version 0.19: l1 penalty with SAGA solver (allowing 'multinomial' + L1)
    #
    #  dual: bool (default=False)
    #     Dual or primal formulation.
    #     Dual formulation is only implemented for l2 penalty with liblinear solver.
    #     Prefer dual=False when n_samples > n_features.
    #
    #  tol: float (default=1e-4)
    #     Tolerance for stopping criteria.
    #
    #  C: float (default=1.0)
    #     Inverse of regularization strength; must be a positive float.
    #     Like in support vector machines, smaller values specify stronger regularization.
    #
    #  fit_intercept: bool (default=True)
    #     Specifies if a constant (a.k.a. bias or intercept)
    #     should be added to the decision function.
    #
    #  intercept_scaling: float (default=1)
    #     Useful only when the solver 'liblinear' is used
    #     and self.fit_intercept is set to True.
    #
    #     In this case, x becomes [x, self.intercept_scaling],
    #     i.e. a "synthetic" feature with constant value equal to
    #     intercept_scaling is appended to the instance vector.
    #
    #     The intercept becomes intercept_scaling * synthetic_feature_weight.
    #
    #     Note! the synthetic feature weight is subject to
    #     l1/l2 regularization as all other features.
    #     To lessen the effect of regularization on synthetic feature weight
    #     (and therefore on the intercept) intercept_scaling has to be increased.
    #
    #  class_weight: dict or 'balanced' (default=None)
    #     Weights associated with classes in the form {class_label: weight}.
    #     If not given, all classes are supposed to have weight one.
    #
    #     The "balanced" mode uses the values of y to automatically
    #     adjust weights inversely proportional to class frequencies in
    #     the input data as n_samples / (n_classes * np.bincount(y)).
    #
    #     Note that these weights will be multiplied with sample_weight
    #     (passed through the fit method) if sample_weight is specified.
    #
    #     New in version 0.17: class_weight='balanced'
    #
    #  random_state: int, RandomState instance (default=None)
    #     Used when solver == 'sag', 'saga' or 'liblinear' to shuffle the data.
    #     See Glossary for details.
    #
    #  solver: {'newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'} (default='lbfgs')
    #     Algorithm to use in the optimization problem.
    #     Default is 'lbfgs'.
    #
    #     To choose a solver, you might want to consider the following aspects:
    #
    #        For small datasets, 'liblinear' is a good choice,
    #        whereas 'sag' and 'saga' are faster for large ones;
    #
    #        For multiclass problems, only 'newton-cg', 'sag', 'saga' and 'lbfgs'
    #        handle multinomial loss;
    #
    #        'liblinear' is limited to one-versus-rest schemes.
    #
    #     Warning The choice of the algorithm depends on the penalty chosen:
    #     Supported penalties by solver:
    #        'newton-cg' - ['l2', 'none']
    #        'lbfgs' - ['l2', 'none']
    #        'liblinear' - ['l1', 'l2']
    #        'sag' - ['l2', 'none']
    #        'saga' - ['elasticnet', 'l1', 'l2', 'none']
    #     Note 'sag' and 'saga' fast convergence is only guaranteed on features with approximately the same scale. You can preprocess the data with a scaler from sklearn.preprocessing.
    #
    #     See also Refer to the User Guide for more information regarding LogisticRegression
    #     and more specifically the Table summarizing solver/penalty supports.
    #
    #     New in version 0.17: Stochastic Average Gradient descent solver.
    #     New in version 0.19: SAGA solver.
    #     Changed in version 0.22: The default solver changed from 'liblinear' to 'lbfgs' in 0.22.
    #
    #  max_iter: int (default=100)
    #     Maximum number of iterations taken for the solvers to converge.
    #
    #  multi_class: {'auto', 'ovr', 'multinomial'} (default='auto')
    #     If the option chosen is 'ovr', then a binary problem is fit for each label.
    #     For 'multinomial' the loss minimised is the multinomial loss fit
    #     across the entire probability distribution, even when the data is binary.
    #
    #     'multinomial' is unavailable when solver='liblinear'.
    #     'auto' selects 'ovr' if the data is binary, or if solver='liblinear',
    #     and otherwise selects 'multinomial'.
    #
    #     New in version 0.18: Stochastic Average Gradient descent solver for 'multinomial' case.
    #     Changed in version 0.22: Default changed from 'ovr' to 'auto' in 0.22.
    #
    #  verbose: int (default=0)
    #     For the liblinear and lbfgs solvers set verbose
    #     to any positive number for verbosity.
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call
    #     to fit as initialization, otherwise, just erase the previous solution.
    #     Useless for liblinear solver. See the Glossary.
    #     New in version 0.17: warm_start to support lbfgs, newton-cg, sag, saga solvers.
    #
    #  n_jobs: int (default=None)
    #     Number of CPU cores used when parallelizing over classes if multi_class='ovr'.
    #     This parameter is ignored when the solver is set to 'liblinear'
    #     regardless of whether 'multi_class' is specified or not.
    #
    #     None means 1 unless in a joblib.parallel_backend context.
    #     -1 means using all processors. See Glossary for more details.
    #
    #  l1_ratio: float (default=None)
    #     The Elastic-Net mixing parameter, with 0 <= l1_ratio <= 1.
    #
    #     Only used if penalty='elasticnet'.
    #
    #     Setting l1_ratio=0 is equivalent to using penalty='l2',
    #     while setting l1_ratio=1 is equivalent to using penalty='l1'.
    #
    #     For 0 < l1_ratio <1, the penalty is a combination of L1 and L2
    #
    # --------------------------------------------------
    model_constructor["LogisticRegression"] = LogisticRegression
    model_constructor_name["LogisticRegression"] = "LogisticRegression"
    model_fit_fn_attr_name["LogisticRegression"] = "fit"
    model_predict_fn_attr_name["LogisticRegression"] = "predict"
    model_constructor_arg_defaults["LogisticRegression"] = {
        "penalty": "l2",
        "dual": False,
        "tol": 1e-4,
        "C": 1.0,
        "fit_intercept": True,
        "intercept_scaling": 1,
        "class_weight": None,
        "random_state": None,
        "solver": "lbfgs",
        "max_iter": 100,
        "multi_class": "auto",
        "verbose": 0,
        "warm_start": False,
        "n_jobs": None,
        "l1_ratio": None,
    }
    model_required_non_cnstr_attribs["LogisticRegression"] = [
        "classes_",
        "coef_",
        "intercept_",
        "n_features_in_",
        "n_iter_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["LogisticRegression"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ============================== TweedieRegressor MODEL CONFIGURATION ==================================
    # --------------------------------------------------
    # TweedieRegressor: Generalized Linear Model with a Tweedie distribution
    # TweedieRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  power: float (default=0)
    #     The power determines the underlying target distribution
    #     according to the following table:
    #
    #        Power  Distribution
    #        -----  ------------
    #          0    Normal
    #          1    Poisson
    #          2    Power Distribution
    #        (1,2)  Cpmpound Poisson Distribution
    #          2    Gamma
    #          3    Inverse Gaussian
    #
    #     For 0 < power < 1, no distribution exists.
    #
    #  alpha: float (default=1)
    #     Constant that multiplies the penalty term
    #     and thus determines the regularization strength.
    #     alpha = 0 is equivalent to unpenalized GLMs.
    #     In this case, the design matrix X must have full column rank (no collinearities).
    #     Values must be in the range [0.0, inf).
    #
    #  fit_intercept: bool (default=True)
    #     Specifies if a constant (a.k.a. bias or intercept)
    #     should be added to the linear predictor (X @ coef + intercept).
    #
    #  link: {'auto', 'identity', 'log'} (default='auto')
    #     The link function of the GLM, i.e. mapping from
    #     linear predictor X @ coeff + intercept to prediction y_pred.
    #
    #     Option 'auto' sets the link depending on
    #     the chosen power parameter as follows:
    #
    #        'identity' for power <= 0, e.g. for the Normal distribution
    #
    #        'log' for power > 0, e.g. for Poisson, Gamma
    #         and Inverse Gaussian distributions
    #
    #  max_iter: int (default=100)
    #     The maximal number of iterations for the solver.
    #     Values must be in the range [1, inf).
    #
    #  tol: float (default=1e-4)
    #     Stopping criterion.
    #     For the lbfgs solver, the iteration will stop when
    #     max{|g_j|, j = 1, ..., d} <= tol where g_j is the j-th component
    #     of the gradient (derivative) of the objective function.
    #
    #     Values must be in the range (0.0, inf).
    #
    #  warm_start: bool (default=False)
    #     If set to True, reuse the solution of the previous call
    #     to fit as initialization for coef_ and intercept_ .
    #
    #  verbose: int (default=0)
    #     For the lbfgs solver set verbose to any positive number for verbosity.
    #     Values must be in the range [0, inf).
    #
    # --------------------------------------------------
    model_constructor["TweedieRegressor"] = TweedieRegressor
    model_constructor_name["TweedieRegressor"] = "TweedieRegressor"
    model_fit_fn_attr_name["TweedieRegressor"] = "fit"
    model_predict_fn_attr_name["TweedieRegressor"] = "predict"
    model_constructor_arg_defaults["TweedieRegressor"] = {
        "power": 0,
        "alpha": 1.0,
        "fit_intercept": True,
        "link": "auto",
        "max_iter": 100,
        "tol": 1e-4,
        "warm_start": False,
        "verbose": 0,
    }
    model_required_non_cnstr_attribs["TweedieRegressor"] = [
        "coef_",
        "intercept_",
        "n_iter_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["TweedieRegressor"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ========================= PassiveAggressiveRegressor MODEL CONFIGURATION =============================
    # --------------------------------------------------
    # PassiveAggressiveRegressor: Passive Aggressive Regressor
    # PassiveAggressiveRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  C: float (default=1.0)
    #     Maximum step size (regularization).
    #     Defaults to 1.0.
    #
    #  fit_intercept: bool (default=True)
    #     Whether the intercept should be estimated or not.
    #     If False, the data is assumed to be already centered.
    #     Defaults to True.
    #
    #  max_iter: int (default=1000)
    #     The maximum number of passes over the training data (aka epochs).
    #     It only impacts the behavior in the fit method,
    #     and not the partial_fit method.
    #     New in version 0.19.
    #
    #  tol: float or None (default=1e-3)
    #     The stopping criterion.
    #     If it is not None, the iterations will stop
    #     when (loss > previous_loss - tol).
    #     New in version 0.19.
    #
    #  early_stopping: bool (default=False)
    #     Whether to use early stopping to terminate training
    #     when validation. score is not improving.
    #
    #     If set to True, it will automatically set aside a fraction
    #     of training data as validation and terminate training
    #     when validation score is not improving by at least
    #     tol for n_iter_no_change consecutive epochs.
    #
    #     New in version 0.20.
    #
    #  validation_fraction: float (default=0.1)
    #     The proportion of training data to set aside
    #     as validation set for early stopping.
    #
    #     Must be between 0 and 1.
    #
    #     Only used if early_stopping is True.
    #
    #     New in version 0.20.
    #
    #  n_iter_no_change: int (default=5)
    #     Number of iterations with no improvement to wait
    #     before early stopping.
    #     New in version 0.20.
    #
    #  shuffle: bool (default=True)
    #     Whether or not the training data should be shuffled after each epoch.
    #
    #  verbose: int (default=0)
    #     The verbosity level.
    #
    #  loss: str (default="epsilon_insensitive")
    #     The loss function to be used: epsilon_insensitive:
    #     equivalent to PA-I in the reference paper.
    #
    #     squared_epsilon_insensitive: equivalent to PA-II in the reference paper.
    #
    #  epsilon: float (default=0.1)
    #     If the difference between the current prediction
    #     and the correct label is below this threshold,
    #     the model is not updated.
    #
    #  random_state: int, RandomState instance (default=None)
    #     Used to shuffle the training data, when shuffle is set to True.
    #     Pass an int for reproducible output across multiple function calls.
    #     See Glossary.
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call to fit
    #     as initialization, otherwise, just erase the previous solution.
    #     See the Glossary.
    #
    #     Repeatedly calling fit or partial_fit when warm_start is True
    #     can result in a different solution than when calling fit
    #     a single time because of the way the data is shuffled.
    #
    #  average: bool or int (default=False)
    #     When set to True, computes the averaged SGD weights
    #     and stores the result in the coef_ attribute.
    #
    #     If set to an int greater than 1, averaging will begin
    #     once the total number of samples seen reaches average.
    #
    #     So average=10 will begin averaging after seeing 10 samples.
    #
    #     New in version 0.19: parameter average to use weights averaging in SGD.
    #
    # --------------------------------------------------
    model_constructor["PassiveAggressiveRegressor"] = PassiveAggressiveRegressor
    model_constructor_name["PassiveAggressiveRegressor"] = "PassiveAggressiveRegressor"
    model_fit_fn_attr_name["PassiveAggressiveRegressor"] = "fit"
    model_predict_fn_attr_name["PassiveAggressiveRegressor"] = "predict"
    model_constructor_arg_defaults["PassiveAggressiveRegressor"] = {
        "C": 1.0,
        "fit_intercept": True,
        "max_iter": 1000,
        "tol": 1e-3,
        "early_stopping": False,
        "validation_fraction": 0.1,
        "n_iter_no_change": 5,
        "shuffle": True,
        "verbose": 0,
        "loss": "epsilon_insensitive",
        "epsilon": 0.1,
        "random_state": None,
        "warm_start": False,
        "average": False,
    }
    model_required_non_cnstr_attribs["PassiveAggressiveRegressor"] = [
        "coef_",
        "intercept_",
        "n_features_in_",
        "n_iter_",
        "t_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["PassiveAggressiveRegressor"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ============================= TheilSenRegressor MODEL CONFIGURATION =================================
    # --------------------------------------------------
    # TheilSenRegressor: Theil-Sen Estimator: robust multivariate regression model.
    # TheilSenRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  fit_intercept: bool (default=True)
    #     Whether to calculate the intercept for this model.
    #     If set to false, no intercept will be used in calculations.
    #
    #  copy_X: bool (default=True)
    #     If True, X will be copied; else, it may be overwritten.
    #
    #  max_subpopulation: int (default=1e4)
    #     Instead of computing with a set of cardinality 'n choose k',
    #     where n is the number of samples and k is the number of subsamples
    #     (at least number of features), consider only a stochastic subpopulation
    #     of a given maximal size if 'n choose k' is larger than max_subpopulation.
    #
    #     For other than small problem sizes this parameter will determine
    #     memory usage and runtime if n_subsamples is not changed.
    #
    #     Note that the data type should be int
    #     but floats such as 1e4 can be accepted too.
    #
    #  n_subsamples: int (default=None)
    #     Number of samples to calculate the parameters.
    #     This is at least the number of features (plus 1 if fit_intercept=True)
    #     and the number of samples as a maximum.
    #
    #     A lower number leads to a higher breakdown point and a low efficiency
    #     while a high number leads to a low breakdown point and a high efficiency.
    #
    #     If None, take the minimum number of subsamples leading to maximal robustness.
    #     If n_subsamples is set to n_samples, Theil-Sen is identical to least squares.
    #
    #  max_iter: int (default=300)
    #     Maximum number of iterations for the calculation of spatial median.
    #
    #  tol: float (default=1e-3)
    #     Tolerance when calculating spatial median.
    #
    #  random_state: int, RandomState instance or None (default=None)
    #     A random number generator instance to define
    #    the state of the random permutations generator.
    #
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    #  n_jobs: int (default=None)
    #    Number of CPUs to use during the cross validation.
    #    None means 1 unless in a joblib.parallel_backend context.
    #    -1 means using all processors.
    #    See Glossary for more details.
    #
    #  verbose: bool (default=False)
    #     Verbose mode when fitting the model.
    #
    # --------------------------------------------------
    model_constructor["TheilSenRegressor"] = TheilSenRegressor
    model_constructor_name["TheilSenRegressor"] = "TheilSenRegressor"
    model_fit_fn_attr_name["TheilSenRegressor"] = "fit"
    model_predict_fn_attr_name["TheilSenRegressor"] = "predict"
    model_constructor_arg_defaults["TheilSenRegressor"] = {
        "fit_intercept": True,
        "copy_X": True,
        "max_subpopulation": 1e4,
        "n_subsamples": None,
        "max_iter": 300,
        "tol": 1e-3,
        "random_state": None,
        "n_jobs": None,
        "verbose": False,
    }
    model_required_non_cnstr_attribs["TheilSenRegressor"] = [
        "coef_",
        "intercept_",
        "breakdown_",
        "n_iter_",
        "n_subpopulation_",
        "n_features_in_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["TheilSenRegressor"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # =============================== HuberRegressor MODEL CONFIGURATION ===================================
    # --------------------------------------------------
    # HuberRegressor: L2-regularized linear regression model that is robust to outlier
    # HuberRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  epsilon: float, greater than 1.0 (default=1.35)
    #     The parameter epsilon controls the number of samples
    #     that should be classified as outliers.
    #
    #     The smaller the epsilon, the more robust it is to outliers.
    #
    #  max_iter: int (default=100)
    #     Maximum number of iterations that
    #    scipy.optimize.minimize(method="L-BFGS-B") should run for.
    #
    #  alpha: float (default=0.0001)
    #     Strength of the squared L2 regularization.
    #     Note that the penalty is equal to alpha * ||w||^2.
    #     Must be in the range [0, inf).
    #
    #  warm_start: bool (default=False)
    #     This is useful if the stored attributes
    #     of a previously used model has to be reused.
    #
    #     If set to False, then the coefficients will be rewritten
    #     for every call to fit.
    #     See the Glossary.
    #
    #  fit_intercept: bool (default=True)
    #     Whether or not to fit the intercept.
    #
    #     This can be set to False if the data
    #     is already centered around the origin.
    #
    #  tol: float (default=1e-05)
    #     The iteration will stop when max{|proj g_i | i = 1, ..., n} <= tol
    #     where pg_i is the i-th component of the projected gradient.
    #
    # --------------------------------------------------
    model_constructor["HuberRegressor"] = HuberRegressor
    model_constructor_name["HuberRegressor"] = "HuberRegressor"
    model_fit_fn_attr_name["HuberRegressor"] = "fit"
    model_predict_fn_attr_name["HuberRegressor"] = "predict"
    model_constructor_arg_defaults["HuberRegressor"] = {
        "epsilon": 1.35,
        "max_iter": 100,
        "alpha": 0.0001,
        "warm_start": False,
        "fit_intercept": True,
        "tol": 1e-5,
    }
    model_required_non_cnstr_attribs["HuberRegressor"] = [
        "coef_",
        "intercept_",
        "scale_",
        "n_features_in_",
        "n_iter_",
        "outliers_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["HuberRegressor"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= QuantileRegressor MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # QuantileRegressor: Linear regression model that predicts conditional quantiles
    # QuantileRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  quantile: float (default=0.5)
    #     The quantile that the model tries to predict.
    #     It must be strictly between 0 and 1.
    #     If 0.5 (default), the model predicts the 50% quantile, i.e. the median.
    #
    #  alpha: float (default=1.0)
    #     Regularization constant that multiplies the L1 penalty term.
    #
    #  fit_intercept: bool (default=True)
    #     Whether or not to fit the intercept.
    #
    #  solver: {'highs-ds', 'highs-ipm', 'highs', 'interior-point', 'revised simplex'} (default='interior-point')
    #     Method used by scipy.optimize.linprog to solve the linear programming formulation.
    #
    #     Note that the highs methods are recommended for usage
    #     with scipy>=1.6.0 because they are the fastest ones.
    #
    #     Solvers "highs-ds", "highs-ipm" and "highs" support
    #     sparse input data and, in fact, always convert to sparse csc.
    #
    #  solver_options: dict (default=None)
    #     Additional parameters passed to scipy.optimize.linprog as options.
    #
    #     If None and if solver='interior-point', then {"lstsq": True}
    #     is passed to scipy.optimize.linprog for the sake of stability.
    #
    # --------------------------------------------------
    model_constructor["QuantileRegressor"] = QuantileRegressor
    model_constructor_name["QuantileRegressor"] = "QuantileRegressor"
    model_fit_fn_attr_name["QuantileRegressor"] = "fit"
    model_predict_fn_attr_name["QuantileRegressor"] = "predict"
    model_constructor_arg_defaults["QuantileRegressor"] = {
        "quantile": 0.5,
        "alpha": 1.0,
        "fit_intercept": True,
        "solver": "interior-point",
    }
    model_required_non_cnstr_attribs["QuantileRegressor"] = [
        "coef_",
        "intercept_",
        "n_features_in_",
        "n_iter_",
    ]
    # Exclusions: None

    model_optional_non_cnstr_attribs["QuantileRegressor"] = [
        "feature_names_in_",
    ]
    # Exclusions: None

    # ================================= RandomForestRegressor MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # RandomForestRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  n_estimators: int (default=100)
    #     The number of trees in the forest.
    #
    #  criterion : str {"squared_error", "absolute_error", "poisson"}, (default="squared_error")
    #     The function to measure the quality of a split.
    #     Supported criteria are "squared_error" for the mean squared error,
    #     which is equal to variance reduction as feature selection criterion,
    #     "absolute_error" for the mean absolute error, and "poisson"
    #     which uses reduction in Poisson deviance to find splits.
    #     Training using "absolute_error" is significantly slower
    #     than when using "squared_error".
    #
    #     New in version 0.18: Mean Absolute Error (MAE) criterion.
    #     New in version 1.0: Poisson criterion.
    #     Deprecated since version 1.0: Criterion "mse" was deprecated in v1.0
    #         and will be removed in version 1.2.
    #         Use criterion="squared_error" which is equivalent.
    #     Deprecated since version 1.0: Criterion "mae" was deprecated in v1.0
    #         and will be removed in version 1.2
    #         Use criterion="absolute_error" which is equivalent.
    #
    #  max_depth: int or None (default=None)
    #     The maximum depth of the tree.
    #     If None, then nodes are expanded until all leaves are pure
    #     or until all leaves contain less than min_samples_split samples.
    #
    #  min_samples_split: int or float (default=2)
    #     The minimum number of samples required to split an internal node:
    #        If int, then consider min_samples_split as the minimum number.
    #        If float, then min_samples_split is a fraction
    #           and ceil(min_samples_split * n_samples)
    #           are the minimum number of samples for each split.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_samples_leaf: int or float (default=1)
    #     The minimum number of samples required to be at a leaf node.
    #     A split point at any depth will only be considered if it leaves
    #     at least min_samples_leaf training samples in each of the left and right branches.
    #     This may have the effect of smoothing the model, especially in regression.
    #        If int, then consider min_samples_leaf as the minimum number.
    #        If float, then min_samples_leaf is a fraction
    #           and ceil(min_samples_leaf * n_samples)
    #           are the minimum number of samples for each node.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_weight_fraction_leaf: float (default=0.0)
    #     The minimum weighted fraction of the sum total of weights
    #     (of all the input samples) required to be at a leaf node.
    #     Samples have equal weight when sample_weight is not provided.
    #
    #  max_features: int, float, str {"sqrt","log2"}, None (default=1.0)
    #     The number of features to consider when looking for the best split:
    #        If int, then consider max_features features at each split.
    #        If float, then max_features is a fraction and
    #           int(max_features * n_features) features are considered at each split.
    #        If "auto", then max_features=n_features. [DEPRECATED since version 1.1]
    #        If "sqrt", then max_features=sqrt(n_features).
    #        If "log2", then max_features=log2(n_features).
    #        If None, then max_features=n_features.
    #     NOTE: The default of 1.0 is equivalent to bagged trees
    #        and more randomness can be achieved by setting smaller values, e.g. 0.3.
    #     Changed in version 1.1: The default of max_features changed from "auto" to 1.0.
    #     Deprecated since version 1.1: The "auto" option was deprecated in 1.1 and will be removed in 1.3.
    #     NOTE: the search for a split does not stop until at least one valid partition
    #        of the node samples is found, even if it requires to effectively inspect
    #        more than max_features features.
    #
    #  max_leaf_nodes: int or None (default=None)
    #     Grow trees with max_leaf_nodes in best-first fashion.
    #     Best nodes are defined as relative reduction in impurity.
    #     If None then unlimited number of leaf nodes.
    #
    #  min_impurity_decrease: float (default=0.0)
    #     A node will be split if this split induces a decrease
    #     of the impurity greater than or equal to this value.
    #     The weighted impurity decrease equation is the following:
    #        N_t / N * (impurity - N_t_R / N_t * right_impurity - N_t_L / N_t * left_impurity)
    #     where:
    #        N is the total number of samples
    #        N_t is the number of samples at the current node
    #        N_t_L is the number of samples in the left child
    #        N_t_R is the number of samples in the right child.
    #        N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed
    #
    #     New in version 0.19.
    #
    #  bootstrap: bool (default=True)
    #     Whether bootstrap samples are used when building trees.
    #     If False, the whole dataset is used to build each tree.
    #
    #  oob_score: bool (default=False)
    #     Whether to use out-of-bag samples to estimate the generalization score.
    #     Only available if bootstrap=True.
    #
    #  n_jobs: int or None (default=None)
    #     The number of jobs to run in parallel.
    #     fit, predict, decision_path and apply are all parallelized over the trees.
    #     None means 1 unless in a joblib.parallel_backend context.
    #     -1 means using all processors.
    #     See Glossary for more details.
    #
    #  random_state: int, RandomState instance, or None (default=None)
    #     Controls both the randomness of the bootstrapping of the samples
    #     used when building trees (if bootstrap=True)
    #     and the sampling of the features to consider
    #     when looking for the best split at each node
    #     (if max_features < n_features).
    #     See Glossary for more details.
    #
    #     If None (default):
    #        Use the global random state instance from numpy.random.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #     If int:
    #        Use a new random number generator seeded by the given integer.
    #        Using an int will produce the same results across different calls.
    #        However, it may be worthwhile checking that your results
    #        are stable across a number of different distinct random seeds.
    #        Popular integer random seeds are 0 and 42.
    #        Integer values must be in the range [0, 2**32 - 1].
    #
    #     If RandomState instance:
    #        Use the provided random state, only affecting other users
    #        of that same random state instance.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #  verbose: int (default=0)
    #     Controls the verbosity when fitting and predicting.
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call
    #     to fit and add more estimators to the ensemble,
    #     otherwise, just fit a whole new forest.
    #     See the Glossary.
    #
    #  ccp_alpha: (non-negative) float (default=0.0)
    #     Complexity parameter used for Minimal Cost-Complexity Pruning.
    #     The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
    #     By default, no pruning is performed.
    #     See Minimal Cost-Complexity Pruning for details.
    #     New in version 0.22.
    #
    #  max_samples: int or float (default=None)
    #     If bootstrap is True, the number of samples to draw
    #     from X to train each base estimator.
    #        If None (default), then draw X.shape[0] samples.
    #        If int, then draw max_samples samples.
    #        If float, then draw max_samples * X.shape[0] samples.
    #           Thus, max_samples should be in the interval (0.0, 1.0]
    #     New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["RandomForestRegressor"] = RandomForestRegressor
    model_constructor_name["RandomForestRegressor"] = "RandomForestRegressor"
    model_fit_fn_attr_name["RandomForestRegressor"] = "fit"
    model_predict_fn_attr_name["RandomForestRegressor"] = "predict"
    model_constructor_arg_defaults["RandomForestRegressor"] = {
        "n_estimators": 100,
        "criterion": "squared_error",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        # "max_features": 1.0,
        "max_features": None,  # <-- None is equivalent to 1.0, but using for consistency with discrete options
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.0,  #'min_impurity_split' : 1e-7,  #<-- Deprecated AFTER v0.19, will be removed >= v0.25 [Use min_impurity_decrease arg instead]
        "bootstrap": True,
        "oob_score": False,
        "n_jobs": None,
        "random_state": None,
        "verbose": 0,
        "warm_start": False,
        "ccp_alpha": 0.0,  # New in version 0.22
        "max_samples": None,  # New in version 0.22
    }
    model_required_non_cnstr_attribs["RandomForestRegressor"] = [
        "estimators_",
        "n_features_in_",
    ]
    # Exclusions:
    # 'base_estimator_' is an internal structure that should be reproduced at instantiation (?)
    # 'feature_importances_' is actually a class property (formulation), not an assignable/persistable attribute
    # 'oob_prediction_' # <-- Perhaps does not need to be persisted in model as relates to training data.(?) NOTE: 'feature_importances_' cannot be set before fit is called...perhaps it is (only_ created by fit call??
    model_optional_non_cnstr_attribs["RandomForestRegressor"] = [
        "feature_names_in_",  # New in version 1.0
        "n_outputs_",
        "oob_score_",
    ]
    # Exclusions:
    # "_n_samples", # <-- Perhaps does not need to be persisted in model as relates to training data.(?) NOTE: 'feature_importances_' cannot be set before fit is called...perhaps it is (only_ created by fit call??

    # ================================= RandomForestClassifier MODEL CONFIGURATION =====================================

    # --------------------------------------------------
    # RandomForestClassifier Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  n_estimators: int (default=100)
    #     The number of trees in the forest.
    #     Changed in version 0.22:
    #        The default value of n_estimators
    #        changed from 10 to 100 in 0.22.
    #
    #  criterion: str {"gini", "entropy", "log_loss"}, (default="gini")
    #     The function to measure the quality of a split.
    #      Supported criteria are:
    #        "gini" for the Gini impurity
    #        "log_loss" and "entropy" both for the Shannon information gain,
    #           see Mathematical formulation.
    #        NOTE: This parameter is tree-specific.
    #
    #  max_depth: (int or None) None*
    #     The maximum depth of the tree.
    #     If None, then nodes are expanded until all leaves are pure
    #     or until all leaves contain less than min_samples_split samples.
    #
    #  min_samples_split: int or float (default=2)
    #     The minimum number of samples required to split an internal node:
    #        If int, then consider min_samples_split as the minimum number.
    #        If float, then min_samples_split is a fraction
    #           and ceil(min_samples_split * n_samples)
    #           are the minimum number of samples for each split.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_samples_leaf: int or float (default=1)
    #     The minimum number of samples required to be at a leaf node.
    #     A split point at any depth will only be considered if it leaves
    #     at least min_samples_leaf training samples in each of the left and right branches.
    #     This may have the effect of smoothing the model, especially in regression.
    #        If int, then consider min_samples_leaf as the minimum number.
    #        If float, then min_samples_leaf is a fraction
    #           and ceil(min_samples_leaf * n_samples)
    #           are the minimum number of samples for each node.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_weight_fraction_leaf: float (default=0.0)
    #     The minimum weighted fraction of the sum total of weights
    #     (of all the input samples) required to be at a leaf node.
    #     Samples have equal weight when sample_weight is not provided.
    #
    #  max_features: int, float, str {"sqrt", "log2"}, None (default="sqrt")
    #     The number of features to consider when looking for the best split:
    #        If int, then consider max_features features at each split.
    #        If float, then max_features is a fraction and
    #           int(max_features * n_features) features are considered at each split.
    #        If "auto", then max_features=n_features. [DEPRECATED since version 1.1]
    #        If "sqrt", then max_features=sqrt(n_features).
    #        If "log2", then max_features=log2(n_features).
    #        If None, then max_features=n_features.
    #     Changed in version 1.1: The default of max_features changed from "auto" to 1.0.
    #     Deprecated since version 1.1: The "auto" option was deprecated in 1.1 and will be removed in 1.3.
    #     NOTE: the search for a split does not stop until at least one valid partition
    #        of the node samples is found, even if it requires to effectively inspect
    #        more than max_features features.
    #
    #  max_leaf_nodes: int or None (default=None)
    #     Grow trees with max_leaf_nodes in best-first fashion.
    #     Best nodes are defined as relative reduction in impurity.
    #     If None then unlimited number of leaf nodes.
    #
    #  min_impurity_decrease: float (default=0.0)
    #     A node will be split if this split induces a decrease
    #     of the impurity greater than or equal to this value.
    #     The weighted impurity decrease equation is the following:
    #        N_t / N * (impurity - N_t_R / N_t * right_impurity - N_t_L / N_t * left_impurity)
    #     where:
    #        N is the total number of samples
    #        N_t is the number of samples at the current node
    #        N_t_L is the number of samples in the left child
    #        N_t_R is the number of samples in the right child.
    #        N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed
    #
    #     New in version 0.19.
    #
    #  bootstrap: bool (default=True)
    #     Whether bootstrap samples are used when building trees.
    #     If False, the whole dataset is used to build each tree.
    #
    #  oob_score: bool (default=False)
    #     Whether to use out-of-bag samples to estimate the generalization score.
    #     Only available if bootstrap=True.
    #
    #  n_jobs: int or None (default=None)
    #     The number of jobs to run in parallel.
    #     fit, predict, decision_path and apply are all parallelized over the trees.
    #     None means 1 unless in a joblib.parallel_backend context.
    #     -1 means using all processors.
    #     See Glossary for more details.
    #
    #  random_state: int, RandomState instance, None (default=None)
    #     Controls both the randomness of the bootstrapping of the samples
    #     used when building trees (if bootstrap=True)
    #     and the sampling of the features to consider
    #     when looking for the best split at each node
    #     (if max_features < n_features).
    #     See Glossary for more details.
    #
    #     If None (default):
    #        Use the global random state instance from numpy.random.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #     If int:
    #        Use a new random number generator seeded by the given integer.
    #        Using an int will produce the same results across different calls.
    #        However, it may be worthwhile checking that your results
    #        are stable across a number of different distinct random seeds.
    #        Popular integer random seeds are 0 and 42.
    #        Integer values must be in the range [0, 2**32 - 1].
    #
    #     If RandomState instance:
    #        Use the provided random state, only affecting other users
    #        of that same random state instance.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #  verbose: int (default=0)
    #     Controls the verbosity when fitting and predicting.
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call
    #     to fit and add more estimators to the ensemble,
    #     otherwise, just fit a whole new forest.
    #     See the Glossary.
    #
    #  class_weight: str {"balanced", "balanced_subsample"}, dict or list of dicts, (default=None)
    #     Weights associated with classes in the form {class_label: weight}.
    #     If not given, all classes are supposed to have weight one.
    #     For multi-output problems, a list of dicts can be provided
    #        in the same order as the columns of y.
    #
    #     Note that for multioutput (including multilabel) weights should be defined
    #     for each class of every column in its own dict.
    #     For example, for four-class multilabel classification weights should be
    #        [{0: 1, 1: 1}, {0: 1, 1: 5}, {0: 1, 1: 1}, {0: 1, 1: 1}]
    #        instead of [{1:1}, {2:5}, {3:1}, {4:1}].
    #
    #     The "balanced" mode uses the values of y to automatically adjust
    #     weights inversely proportional to class frequencies
    #     in the input data as n_samples / (n_classes * np.bincount(y))
    #
    #     The "balanced_subsample" mode is the same as "balanced" except that
    #     weights are computed based on the bootstrap sample for every tree grown.
    #
    #     For multi-output, the weights of each column of y will be multiplied.
    #
    #     Note that these weights will be multiplied with sample_weight
    #     (passed through the fit method) if sample_weight is specified.
    #
    #  ccp_alpha: (non-negative) float (default=0.0)
    #     Complexity parameter used for Minimal Cost-Complexity Pruning.
    #     The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
    #     By default, no pruning is performed.
    #     See Minimal Cost-Complexity Pruning for details.
    #     New in version 0.22.
    #
    #  max_samples: int or float (default=None)
    #     If bootstrap is True, the number of samples to draw
    #     from X to train each base estimator.
    #        If None (default), then draw X.shape[0] samples.
    #        If int, then draw max_samples samples.
    #        If float, then draw max_samples * X.shape[0] samples.
    #           Thus, max_samples should be in the interval (0.0, 1.0]
    #     New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["RandomForestClassifier"] = RandomForestClassifier
    model_constructor_name["RandomForestClassifier"] = "RandomForestClassifier"
    model_fit_fn_attr_name["RandomForestClassifier"] = "fit"
    model_predict_fn_attr_name["RandomForestClassifier"] = "predict"
    model_constructor_arg_defaults["RandomForestClassifier"] = {
        "n_estimators": 100,
        "criterion": "gini",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        "max_features": "sqrt",
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.0,  #'min_impurity_split' : 1e-7,  #<-- Deprecated AFTER v0.19, will be removed >= v0.25 [Use min_impurity_decrease arg instead]
        "bootstrap": True,
        "oob_score": False,
        "n_jobs": None,
        "random_state": None,
        "verbose": 0,
        "warm_start": False,
        "class_weight": None,
        "ccp_alpha": 0.0,  # New in version 0.22
        "max_samples": None,  # New in version 0.22
    }
    model_required_non_cnstr_attribs["RandomForestClassifier"] = [
        "estimators_",
        "classes_",
        "n_classes_",
        "n_features_in_",
    ]
    # Exclusions:
    # 'base_estimator_' is an internal structure that should be reproduced at instantiation (?)
    # 'feature_importances_' # Not present for RandomForestClassifier (?)
    model_optional_non_cnstr_attribs["RandomForestClassifier"] = [
        "feature_names_in_",  # New in version 1.0
        "n_outputs_",
        "oob_score_",
        #'oob_decision_function_' # <-- NOTE: oob_decision_function_ relates to training data...Perhaps do not need to be persisted in model as relates to training data.(?)
        #'oob_prediction_' # # Not present for RandomForestClassifier (?)
    ]
    # Exclusions:
    # "_n_samples", # Not present for RandomForestClassifier (?)

    # ================================= ExtraTreesRegressor MODEL CONFIGURATION =====================================

    # --------------------------------------------------
    # ExtraTreesRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  n_estimators: int (default=100)
    #     The number of trees in the forest.
    #     Changed in version 0.22: The default value of n_estimators changed from 10 to 100 in 0.22.
    #
    #  criterion : str {"squared_error", "absolute_error"}, (default="squared_error")
    #     The function to measure the quality of a split.
    #     Supported criteria are "squared_error" for the mean squared error,
    #     which is equal to variance reduction as feature selection criterion,
    #     and "absolute_error" for the mean absolute error.
    #     Training using "absolute_error" is significantly slower
    #     than when using "squared_error".
    #
    #     New in version 0.18: Mean Absolute Error (MAE) criterion.
    #     New in version 1.0: Poisson criterion.
    #     Deprecated since version 1.0: Criterion "mse" was deprecated in v1.0
    #         and will be removed in version 1.2.
    #         Use criterion="squared_error" which is equivalent.
    #     Deprecated since version 1.0: Criterion "mae" was deprecated in v1.0
    #         and will be removed in version 1.2.
    #         Use criterion="absolute_error" which is equivalent.
    #
    #  max_depth: int or None (default=None)
    #     The maximum depth of the tree.
    #     If None, then nodes are expanded until all leaves are pure
    #     or until all leaves contain less than min_samples_split samples.
    #
    #  min_samples_split: int or float (default=2)
    #     The minimum number of samples required to split an internal node:
    #        If int, then consider min_samples_split as the minimum number.
    #        If float, then min_samples_split is a fraction
    #           and ceil(min_samples_split * n_samples)
    #           are the minimum number of samples for each split.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_samples_leaf: int or float (default=1)
    #     The minimum number of samples required to be at a leaf node.
    #     A split point at any depth will only be considered if it leaves
    #     at least min_samples_leaf training samples in each of the left and right branches.
    #     This may have the effect of smoothing the model, especially in regression.
    #        If int, then consider min_samples_leaf as the minimum number.
    #        If float, then min_samples_leaf is a fraction
    #           and ceil(min_samples_leaf * n_samples)
    #           are the minimum number of samples for each node.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_weight_fraction_leaf: float (default=0.0)
    #     The minimum weighted fraction of the sum total of weights
    #     (of all the input samples) required to be at a leaf node.
    #     Samples have equal weight when sample_weight is not provided.
    #
    #  max_features: int, float, str {"sqrt","log2"} or None (default=1.0)
    #     The number of features to consider when looking for the best split:
    #        If int, then consider max_features features at each split.
    #        If float, then max_features is a fraction and
    #           int(max_features * n_features) features are considered at each split.
    #        If "auto", then max_features=n_features. [DEPRECATED since version 1.1]
    #        If "sqrt", then max_features=sqrt(n_features).
    #        If "log2", then max_features=log2(n_features).
    #        If None or 1.0, then max_features=n_features.
    #     NOTE: The default of 1.0 is equivalent to bagged trees
    #        and more randomness can be achieved by setting smaller values, e.g. 0.3.
    #     Changed in version 1.1: The default of max_features changed from "auto" to 1.0.
    #     Deprecated since version 1.1: The "auto" option was deprecated in 1.1 and will be removed in 1.3.
    #     NOTE: the search for a split does not stop until at least one valid partition
    #        of the node samples is found, even if it requires to effectively inspect
    #        more than max_features features.
    #
    #  max_leaf_nodes: int or None (default=None)
    #     Grow trees with max_leaf_nodes in best-first fashion.
    #     Best nodes are defined as relative reduction in impurity.
    #     If None then unlimited number of leaf nodes.
    #
    #  min_impurity_decrease: float (default=0.0)
    #     A node will be split if this split induces a decrease
    #     of the impurity greater than or equal to this value.
    #     The weighted impurity decrease equation is the following:
    #        N_t / N * (impurity - N_t_R / N_t * right_impurity - N_t_L / N_t * left_impurity)
    #     where:
    #        N is the total number of samples
    #        N_t is the number of samples at the current node
    #        N_t_L is the number of samples in the left child
    #        N_t_R is the number of samples in the right child.
    #        N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed
    #
    #     New in version 0.19.
    #
    #  bootstrap: bool (default=False)
    #     Whether bootstrap samples are used when building trees.
    #     If False, the whole dataset is used to build each tree.
    #
    #  oob_score: bool (default=False)
    #     Whether to use out-of-bag samples to estimate the generalization score.
    #     Only available if bootstrap=True.
    #
    #  n_jobs: int or  None (default=None)
    #     The number of jobs to run in parallel.
    #     fit, predict, decision_path and apply are all parallelized over the trees.
    #     None means 1 unless in a joblib.parallel_backend context.
    #     -1 means using all processors.
    #     See Glossary for more details.
    #
    #  random_state: (int, RandomState instance, None) (default=None)
    #     Controls 3 sources of randomness:
    #        the bootstrapping of the samples used when building trees (if bootstrap=True)
    #        the sampling of the features to consider when looking for the best split at each node (if max_features < n_features)
    #        the draw of the splits for each of the max_features
    #
    #     See Glossary for more details.
    #
    #  verbose: int (default=0)
    #     Controls the verbosity when fitting and predicting.
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call
    #     to fit and add more estimators to the ensemble,
    #     otherwise, just fit a whole new forest.
    #     See the Glossary.
    #
    #  ccp_alpha: non-negative float (default=0.0)
    #     Complexity parameter used for Minimal Cost-Complexity Pruning.
    #     The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
    #     By default, no pruning is performed.
    #     See Minimal Cost-Complexity Pruning for details.
    #     New in version 0.22.
    #
    #  max_samples: int or float (default=None)
    #     If bootstrap is True, the number of samples to draw
    #     from X to train each base estimator.
    #        If None (default), then draw X.shape[0] samples.
    #        If int, then draw max_samples samples.
    #        If float, then draw max_samples * X.shape[0] samples.
    #           Thus, max_samples should be in the interval (0.0, 1.0]
    #     New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["ExtraTreesRegressor"] = ExtraTreesRegressor
    model_constructor_name["ExtraTreesRegressor"] = "ExtraTreesRegressor"
    model_fit_fn_attr_name["ExtraTreesRegressor"] = "fit"
    model_predict_fn_attr_name["ExtraTreesRegressor"] = "predict"
    model_constructor_arg_defaults["ExtraTreesRegressor"] = {
        "n_estimators": 100,
        "criterion": "squared_error",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        # "max_features": 1.0,
        "max_features": None,  # <-- Choosing this option per front-end menu options
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.0,  #'min_impurity_split' : 1e-7,  #<-- Deprecated AFTER v0.19, will be removed >= v0.25 [Use min_impurity_decrease arg instead]
        "bootstrap": False,
        "oob_score": False,
        "n_jobs": None,
        "random_state": None,
        "verbose": 0,
        "warm_start": False,
        "ccp_alpha": 0.0,  # New in version 0.22
        "max_samples": None,  # New in version 0.22
    }
    model_required_non_cnstr_attribs["ExtraTreesRegressor"] = [
        "estimators_",
        "n_features_in_",  # New in version 0.24.
    ]
    # Exclusions:
    # 'base_estimator_' is an internal structure that should be reproduced at instantiation (?)
    # 'feature_importances_' is actually a class property (formulation), not an assignable/persistable attribute
    model_optional_non_cnstr_attribs["ExtraTreesRegressor"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
        "n_outputs_",
        "oob_score_",
        # "oob_prediction_", # <-- Perhaps does not need to be persisted in model as relates to training data.(?) NOTE: 'feature_importances_' cannot be set before fit is called...perhaps it is (only_ created by fit call??
    ]
    # Exclusions:
    # "_n_samples", # <-- Perhaps does not need to be persisted in model as relates to training data.(?) NOTE: 'feature_importances_' cannot be set before fit is called...perhaps it is (only_ created by fit call??

    # ================================= ExtraTreesClassifier MODEL CONFIGURATION =====================================

    # --------------------------------------------------
    # ExtraTreesClassifier Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  n_estimators: int (default=100)
    #     The number of trees in the forest.
    #     Changed in version 0.22: The default value of n_estimators changed from 10 to 100 in 0.22.
    #
    #  criterion : str {"gini", "entropy", "log_loss"}, (default="gini")
    #     The function to measure the quality of a split.
    #     Supported criteria are "gini" for the Gini impurity
    #     and "log_loss" and "entropy" both for the Shannon information gain,
    #     see Mathematical formulation.
    #     NOTE: This parameter is tree-specific.
    #
    #  max_depth: int or None (default=None)
    #     The maximum depth of the tree.
    #     If None, then nodes are expanded until all leaves are pure
    #     or until all leaves contain less than min_samples_split samples.
    #
    #  min_samples_split: int or float (default=2)
    #     The minimum number of samples required to split an internal node:
    #        If int, then consider min_samples_split as the minimum number.
    #        If float, then min_samples_split is a fraction
    #           and ceil(min_samples_split * n_samples)
    #           are the minimum number of samples for each split.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_samples_leaf: int or float (default=1)
    #     The minimum number of samples required to be at a leaf node.
    #     A split point at any depth will only be considered if it leaves
    #     at least min_samples_leaf training samples in each of the left and right branches.
    #     This may have the effect of smoothing the model, especially in regression.
    #        If int, then consider min_samples_leaf as the minimum number.
    #        If float, then min_samples_leaf is a fraction
    #           and ceil(min_samples_leaf * n_samples)
    #           are the minimum number of samples for each node.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_weight_fraction_leaf: float (default=0.0)
    #     The minimum weighted fraction of the sum total of weights
    #     (of all the input samples) required to be at a leaf node.
    #     Samples have equal weight when sample_weight is not provided.
    #
    #  max_features: int, float, str {"sqrt","log2"} or None (default="sqrt")
    #     The number of features to consider when looking for the best split:
    #        If int, then consider max_features features at each split.
    #        If float, then max_features is a fraction and
    #           int(max_features * n_features) features are considered at each split.
    #        If "auto", then max_features=n_features. [DEPRECATED since version 1.1]
    #        If "sqrt", then max_features=sqrt(n_features).
    #        If "log2", then max_features=log2(n_features).
    #        If None or 1.0, then max_features=n_features.
    #     NOTE: The default of 1.0 is equivalent to bagged trees
    #        and more randomness can be achieved by setting smaller values, e.g. 0.3.
    #     Changed in version 1.1: The default of max_features changed from "auto" to 1.0.
    #     Deprecated since version 1.1: The "auto" option was deprecated in 1.1 and will be removed in 1.3.
    #     NOTE: the search for a split does not stop until at least one valid partition
    #        of the node samples is found, even if it requires to effectively inspect
    #        more than max_features features.
    #
    #  max_leaf_nodes: int or None (default=None)
    #     Grow trees with max_leaf_nodes in best-first fashion.
    #     Best nodes are defined as relative reduction in impurity.
    #     If None then unlimited number of leaf nodes.
    #
    #  min_impurity_decrease: float (default=0.0)
    #     A node will be split if this split induces a decrease
    #     of the impurity greater than or equal to this value.
    #     The weighted impurity decrease equation is the following:
    #        N_t / N * (impurity - N_t_R / N_t * right_impurity - N_t_L / N_t * left_impurity)
    #     where:
    #        N is the total number of samples
    #        N_t is the number of samples at the current node
    #        N_t_L is the number of samples in the left child
    #        N_t_R is the number of samples in the right child.
    #        N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed
    #
    #     New in version 0.19.
    #
    #  bootstrap: bool (default=False)
    #     Whether bootstrap samples are used when building trees.
    #     If False, the whole dataset is used to build each tree.
    #
    #  oob_score: bool (default=False)
    #     Whether to use out-of-bag samples to estimate the generalization score.
    #     Only available if bootstrap=True.
    #
    #  n_jobs: int or  None (default=None)
    #     The number of jobs to run in parallel.
    #     fit, predict, decision_path and apply are all parallelized over the trees.
    #     None means 1 unless in a joblib.parallel_backend context.
    #     -1 means using all processors.
    #     See Glossary for more details.
    #
    #  random_state: (int, RandomState instance, None) (default=None)
    #     Controls 3 sources of randomness:
    #        the bootstrapping of the samples used when building trees (if bootstrap=True)
    #        the sampling of the features to consider when looking for the best split at each node (if max_features < n_features)
    #        the draw of the splits for each of the max_features
    #
    #     See Glossary for more details.
    #
    #  verbose: int (default=0)
    #     Controls the verbosity when fitting and predicting.
    #
    #  warm_start: bool (default=False)
    #     When set to True, reuse the solution of the previous call
    #     to fit and add more estimators to the ensemble,
    #     otherwise, just fit a whole new forest.
    #     See the Glossary.
    #
    #  class_weight str {"balanced", "balanced_subsample"}, dict or list of dicts, default=None
    #     Weights associated with classes in the form {class_label: weight}.
    #     If not given, all classes are supposed to have weight one.
    #     For multi-output problems, a list of dicts can be provided
    #        in the same order as the columns of y.
    #
    #     Note that for multioutput (including multilabel) weights should be defined
    #     for each class of every column in its own dict.
    #     For example, for four-class multilabel classification weights should be [{0: 1, 1: 1}, {0: 1, 1: 5}, {0: 1, 1: 1}, {0: 1, 1: 1}] instead of [{1:1}, {2:5}, {3:1}, {4:1}].
    #
    #     The "balanced" mode uses the values of y to automatically adjust
    #     weights inversely proportional to class frequencies
    #     in the input data as n_samples / (n_classes * np.bincount(y))
    #
    #     The "balanced_subsample" mode is the same as "balanced" except that
    #     weights are computed based on the bootstrap sample for every tree grown.
    #
    #     For multi-output, the weights of each column of y will be multiplied.
    #
    #     Note that these weights will be multiplied with sample_weight
    #     (passed through the fit method) if sample_weight is specified.
    #
    #  ccp_alpha: non-negative float (default=0.0)
    #     Complexity parameter used for Minimal Cost-Complexity Pruning.
    #     The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
    #     By default, no pruning is performed.
    #     See Minimal Cost-Complexity Pruning for details.
    #     New in version 0.22.
    #
    #  max_samples: int or float (default=None)
    #     If bootstrap is True, the number of samples to draw
    #     from X to train each base estimator.
    #        If None (default), then draw X.shape[0] samples.
    #        If int, then draw max_samples samples.
    #        If float, then draw max_samples * X.shape[0] samples.
    #           Thus, max_samples should be in the interval (0.0, 1.0]
    #     New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["ExtraTreesClassifier"] = ExtraTreesClassifier
    model_constructor_name["ExtraTreesClassifier"] = "ExtraTreesClassifier"
    model_fit_fn_attr_name["ExtraTreesClassifier"] = "fit"
    model_predict_fn_attr_name["ExtraTreesClassifier"] = "predict"
    model_constructor_arg_defaults["ExtraTreesClassifier"] = {
        "n_estimators": 100,
        "criterion": "gini",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        "max_features": "sqrt",
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.0,  #'min_impurity_split' : 1e-7,  #<-- Deprecated AFTER v0.19, will be removed >= v0.25 [Use min_impurity_decrease arg instead]
        "bootstrap": False,
        "oob_score": False,
        "n_jobs": None,
        "random_state": None,
        "verbose": 0,
        "warm_start": False,
        "class_weight": None,
        "ccp_alpha": 0.0,  # New in version 0.22
        "max_samples": None,  # New in version 0.22
    }
    model_required_non_cnstr_attribs["ExtraTreesClassifier"] = [
        "estimators_",
        "classes_",
        "n_classes_",
        "n_features_in_",  # New in version 0.24.
    ]
    # Exclusions:
    # 'base_estimator_' is an internal structure that should be reproduced at instantiation (?)
    # 'feature_importances_' is actually a class property (formulation), not an assignable/persistable attribute
    model_optional_non_cnstr_attribs["ExtraTreesClassifier"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
        "n_outputs_",
        "oob_score_",
        #'oob_decision_function_' # <-- NOTE: oob_decision_function_ relates to training data...Perhaps do not need to be persisted in model as relates to training data.(?)
        # "oob_prediction_", # <-- Perhaps does not need to be persisted in model as relates to training data.(?) NOTE: 'feature_importances_' cannot be set before fit is called...perhaps it is (only_ created by fit call??
    ]
    # Exclusions:
    # "_n_samples", # <-- Perhaps does not need to be persisted in model as relates to training data.(?) NOTE: 'feature_importances_' cannot be set before fit is called...perhaps it is (only_ created by fit call??

    # ================================= BaggingRegressor MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # BaggingRegressor Estimation Parameters
    # NOTE: Apparently, BaggingRegressor DOES NOT SUPPORT multiple outputs
    # All arguments are optional.
    # --------------------------------------------------
    # base_estimator : object or None (default=None)
    #    The base estimator to fit on random subsets of the dataset.
    #    If None, then the base estimator is a DecisionTreeRegressor.
    #
    # n_estimators : int (default=10)
    #    The number of base estimators in the ensemble.
    #
    # max_samples : int or float (default=1.0)
    #    The number of samples to draw from X to train each base estimator
    #    (with replacement by default, see bootstrap for more details).
    #
    #    If int, then draw max_samples samples.
    #    If float, then draw max_samples * X.shape[0] samples.
    #
    # max_features : int or float (default=1.0)
    #    The number of features to draw from X to train each base
    #    (without replacement by default, see bootstrap_features for more details).
    #
    #    If int, then draw max_features features.
    #    If float, then draw max(1, int(max_features * n_features_in_)) features.
    #
    # bootstrap : bool (default=True)
    #    Whether samples are drawn with replacement.
    #    If False, sampling without replacement is performed.
    #
    # bootstrap_features : bool (default=False)
    #    Whether features are drawn with replacement.
    #
    # oob_score : bool (default=False)
    #    Whether to use out-of-bag samples to estimate the generalization error.
    #    Only available if bootstrap=True.
    #
    # warm_start : bool (default=False)
    #    When set to True, reuse the solution of the previous call
    #    to fit and add more estimators to the ensemble,
    #    otherwise, just fit a whole new ensemble.
    #    See the Glossary.
    #
    # n_jobs : int or None (default=None)
    #    The number of jobs to run in parallel for both fit and predict.
    #    None means 1 unless in a joblib.parallel_backend context.
    #    -1 means using all processors.
    #    See Glossary for more details.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Controls the random resampling of the original dataset
    #    (sample wise and feature wise).
    #    If the base estimator accepts a random_state attribute,
    #    a different seed is generated for each instance in the ensemble.
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    # verbose : int (default=0)
    #    Controls the verbosity when fitting and predicting.
    #
    # --------------------------------------------------
    model_constructor["BaggingRegressor"] = BaggingRegressor
    model_constructor_name["BaggingRegressor"] = "BaggingRegressor"
    model_fit_fn_attr_name["BaggingRegressor"] = "fit"
    model_predict_fn_attr_name["BaggingRegressor"] = "predict"
    model_constructor_arg_defaults["BaggingRegressor"] = {
        "base_estimator": None,
        "n_estimators": 10,
        "max_samples": 1.0,
        "max_features": 1.0,
        "bootstrap": True,
        "bootstrap_features": False,
        "oob_score": False,
        "warm_start": False,
        "n_jobs": None,
        "random_state": None,
        "verbose": 0,
    }
    # NOTE: Apparently, BaggingRegressor DOES NOT SUPPORT multiple outputs
    model_required_non_cnstr_attribs["BaggingRegressor"] = [
        "n_features_in_",  # New in version 0.24.
        "estimators_",
        "estimators_features_",
    ]  # 'estimators_samples_', 'oob_prediction_' # <-- NOTE: estimators_samples_ & oob_prediction_ relates to training data...Perhaps do not need to be persisted in model as relates to training data.(?)
    model_optional_non_cnstr_attribs["BaggingRegressor"] = [
        "feature_names_in_",  # New in version 1.0.
        "_n_samples",
        "oob_score_",
        "_estimator_type",
    ]  # <-- Do we need to include this???

    # ================================= BaggingClassifier MODEL CONFIGURATION =====================================
    # --------------------------------------------------
    # BaggingClassifier Estimation Parameters
    # NOTE: Apparently, BaggingClassifier DOES NOT SUPPORT multiple outputs
    # All arguments are optional.
    # --------------------------------------------------
    # base_estimator : object or None (default=None)
    #    The base estimator to fit on random subsets of the dataset.
    #    If None, then the base estimator is a DecisionTreeClassifier.
    #
    # n_estimators : int (default=10)
    #    The number of base estimators in the ensemble.
    #
    # max_samples : int or float (default=1.0)
    #    The number of samples to draw from X to train each base estimator
    #    (with replacement by default, see bootstrap for more details).
    #
    #    If int, then draw max_samples samples.
    #    If float, then draw max_samples * X.shape[0] samples.
    #
    # max_features : int or float (default=1.0)
    #    The number of features to draw from X to train each base
    #    (without replacement by default, see bootstrap_features for more details).
    #
    #    If int, then draw max_features features.
    #    If float, then draw max(1, int(max_features * n_features_in_)) features.
    #
    # bootstrap : bool (default=True)
    #    Whether samples are drawn with replacement.
    #    If False, sampling without replacement is performed.
    #
    # bootstrap_features : bool (default=False)
    #    Whether features are drawn with replacement.
    #
    # oob_score : bool (default=False)
    #    Whether to use out-of-bag samples to estimate the generalization error.
    #    Only available if bootstrap=True.
    #
    # warm_start : bool (default=False)
    #    When set to True, reuse the solution of the previous call
    #    to fit and add more estimators to the ensemble,
    #    otherwise, just fit a whole new ensemble.
    #    See the Glossary.
    #    New in version 0.17: warm_start constructor parameter.
    #
    # n_jobs : int or None (default=None)
    #    The number of jobs to run in parallel for both fit and predict.
    #    None means 1 unless in a joblib.parallel_backend context.
    #    -1 means using all processors.
    #    See Glossary for more details.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Controls the random resampling of the original dataset
    #    (sample wise and feature wise).
    #    If the base estimator accepts a random_state attribute,
    #    a different seed is generated for each instance in the ensemble.
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    # verbose : int (default=0)
    #    Controls the verbosity when fitting and predicting.
    #
    # --------------------------------------------------
    model_constructor["BaggingClassifier"] = BaggingClassifier
    model_constructor_name["BaggingClassifier"] = "BaggingClassifier"
    model_fit_fn_attr_name["BaggingClassifier"] = "fit"
    model_predict_fn_attr_name["BaggingClassifier"] = "predict"
    model_constructor_arg_defaults["BaggingClassifier"] = {
        "base_estimator": None,
        "n_estimators": 10,
        "max_samples": 1.0,
        "max_features": 1.0,
        "bootstrap": True,
        "bootstrap_features": False,
        "oob_score": False,
        "warm_start": False,
        "n_jobs": None,
        "random_state": None,
        "verbose": 0,
    }
    # NOTE: Apparently, BaggingClassifier DOES NOT SUPPORT multiple outputs
    model_required_non_cnstr_attribs["BaggingClassifier"] = [
        "n_features_in_",  # New in version 0.24.
        "estimators_",
        "estimators_features_",
        "classes_",
        "n_classes_",
    ]  # 'estimators_samples_', 'oob_decision_function_' # <-- NOTE: estimators_samples_ & oob_decision_function_ relates to training data...Perhaps do not need to be persisted in model as relates to training data.(?)
    model_optional_non_cnstr_attribs["BaggingClassifier"] = [
        "feature_names_in_",  # New in version 1.0.
        "_n_samples",
        "oob_score_",
        "_estimator_type",
    ]  # <-- Do we need to include this???

    # ============================================ GradientBoostingRegressor =========================================

    # Comments/documentation as of Sept 2022 with scikit-learn v1.12
    # --------------------------------------------------
    # GradientBoostingRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    # loss : str {"squared_error", "absolute_error", "huber", "quantile"} (default="squared_error")
    #    Loss function to be optimized.
    #       "squared_error" refers to the squared error for regression.
    #       "absolute_error" refers to the absolute error of regression
    #          and is a robust loss function.
    #       "huber" is a combination of the two.
    #       "quantile" allows quantile regression
    #          (use alpha to specify the quantile).
    #
    #    Deprecated since version 1.0: The loss "ls" was deprecated in v1.0
    #       and will be removed in version 1.2.
    #       Use loss="squared_error" which is equivalent.
    #
    #    Deprecated since version 1.0: The loss "lad" was deprecated in v1.0
    #       and will be removed in version 1.2.
    #       Use loss="absolute_error" which is equivalent.
    #
    # learning_rate : float (default=0.1)
    #    Learning rate shrinks the contribution of each tree by learning_rate.
    #    There is a trade-off between learning_rate and n_estimators.
    #    Values must be in the range (0.0, inf).
    #
    # n_estimators : int (default=100)
    #    The number of boosting stages to perform.
    #    Gradient boosting is fairly robust to over-fitting
    #    so a large number usually results in better performance.
    #    Values must be in the range [1, inf).
    #
    # subsample : float (default=1.0)
    #    The fraction of samples to be used for fitting the individual base learners.
    #    If smaller than 1.0 this results in Stochastic Gradient Boosting.
    #    subsample interacts with the parameter n_estimators.
    #    Choosing subsample < 1.0 leads to a reduction of variance
    #       and an increase in bias.
    #    Values must be in the range (0.0, 1.0].
    #
    # criterion : string {"friedman_mse", "squared_error"} (default="friedman_mse")
    #    The function to measure the quality of a split.
    #    Supported criteria are:
    #       "friedman_mse" for the mean squared error with improvement score by Friedman
    #       "squared_error" for mean squared error.
    #    The default value of "friedman_mse" is generally the best
    #       as it can provide a better approximation in some cases.
    #    New in version 0.18.
    #    Deprecated since version 1.0: Criterion "mse" was deprecated in v1.0
    #       and will be removed in version 1.2.
    #       Use criterion='squared_error' which is equivalent.
    #
    # min_samples_split : int, float (default=2)
    #    The minimum number of samples required to split an internal node:
    #
    #    If int, values must be in the range [2, inf)
    #    If float, values must be in the range (0.0, 1.0]
    #       and min_samples_split will be ceil(min_samples_split * n_samples).
    #    Changed in version 0.18: Added float values for fractions.
    #
    # min_samples_leaf : int, float (default=1)
    #    The minimum number of samples required to be at a leaf node.
    #    A split point at any depth will only be considered if it leaves
    #    at least min_samples_leaf training samples in each of the left and right branches.
    #    This may have the effect of smoothing the model, especially in regression.
    #
    #    If int, values must be in the range [1, inf).
    #    If float, values must be in the range (0.0, 1.0] and
    #       min_samples_leaf will be ceil(min_samples_leaf * n_samples).
    #
    # min_weight_fraction_leaf : float (default=0.0)
    #    The minimum weighted fraction of the sum total of weights
    #    (of all the input samples) required to be at a leaf node.
    #    Samples have equal weight when sample_weight is not provided.
    #    Values must be in the range [0.0, 0.5].
    #
    # max_depth : int (default=3)
    #    maximum depth of the individual regression estimators.
    #    The maximum depth limits the number of nodes in the tree.
    #    Tune this parameter for best performance;
    #    the best value depends on the interaction of the input variables.
    #    Values must be in the range [1, inf).
    #
    # min_impurity_decrease : float (default=0.0)
    #    A node will be split if this split induces a decrease
    #    of the impurity greater than or equal to this value.
    #    Values must be in the range [0.0, inf).
    #
    #    The weighted impurity decrease equation is the following:
    #
    #    N_t / N * (impurity - N_t_R / N_t * right_impurity - N_t_L / N_t * left_impurity)
    #       where: N is the total number of samples
    #              N_t is the number of samples at the current node
    #              N_t_L is the number of samples in the left child
    #          and N_t_R is the number of samples in the right child.
    #
    #    N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed.
    #    New in version 0.19.
    #
    # init : estimator or "zero" (default=None)
    #    An estimator object that is used to compute the initial predictions.
    #    init has to provide fit and predict.
    #    If "zero", the initial raw predictions are set to zero.
    #    By default a DummyEstimator is used, predicting either
    #       the average target value (for loss="squared_error"),
    #       or a quantile for the other losses.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Controls the random seed given to each Tree estimator at each boosting iteration.
    #    In addition, it controls the random permutation of the features at each split (see Notes for more details).
    #    It also controls the random splitting of the training data
    #    to obtain a validation set if n_iter_no_change is not None.
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    #    If None (default):
    #       Use the global random state instance from numpy.random.
    #      Calling the function multiple times will reuse the same instance,
    #      and will produce different results.
    #
    #    If int:
    #       Use a new random number generator seeded by the given integer.
    #       Using an int will produce the same results across different calls.
    #       However, it may be worthwhile checking that your results are stable
    #       across a number of different distinct random seeds.
    #       Popular integer random seeds are 0 and 42.
    #       Integer values must be in the range [0, 2**32 - 1].
    #
    #    If RandomState instance:
    #       Use the provided random state, only affecting other users
    #       of that same random state instance.
    #       Calling the function multiple times will reuse the same instance,
    #       and will produce different results.
    #
    # max_features : int, float, string {"auto", "sqrt", "log2"} or None (default=None)
    #    The number of features to consider when looking for the best split:
    #
    #    If int, values must be in the range [1, inf).
    #    If float, values must be in the range (0.0, 1.0]
    #      and the features considered at each split
    #      will be max(1, int(max_features * n_features_in_)).
    #    If "auto", then max_features=n_features.
    #    If "sqrt", then max_features=sqrt(n_features).
    #    If "log2", then max_features=log2(n_features).
    #    If None, then max_features=n_features.
    #    Choosing max_features < n_features leads to a reduction
    #    of variance and an increase in bias.
    #
    #    NOTE: the search for a split does not stop until
    #    at least one valid partition of the node samples is found,
    #    even if it requires to effectively inspect more than max_features features.
    #
    # alpha : float (default=0.9)
    #    The alpha-quantile of the huber loss function and the quantile loss function.
    #    Only if loss="huber" or loss="quantile".
    #    Values must be in the range (0.0, 1.0).
    #
    # verbose : int (default=0)
    #    Enable verbose output.
    #    If 1 then it prints progress and performance once in a while
    #    (the more trees the lower the frequency).
    #    If greater than 1 then it prints progress and performance for every tree.
    #    Values must be in the range [0, inf).
    #
    # max_leaf_nodes : int or None (default=None)
    #    Grow trees with max_leaf_nodes in best-first fashion.
    #    Best nodes are defined as relative reduction in impurity.
    #    Values must be in the range [2, inf).
    #    If None then unlimited number of leaf nodes.
    #
    # warm_start : bool (default=False)
    #    When set to True, reuse the solution of the previous call
    #    to fit and add more estimators to the ensemble,
    #    otherwise, just erase the previous solution.
    #    See the Glossary.
    #
    # validation_fraction : float (default=0.1)
    #    The proportion of training data to set aside as validation set for early stopping.
    #    Values must be in the range (0.0, 1.0).
    #    Only used if n_iter_no_change is set to an integer.
    #    New in version 0.20.
    #
    # n_iter_no_change : int (default=None)
    #
    #    n_iter_no_change is used to decide if early stopping will be used
    #    to terminate training when validation score is not improving.
    #
    #    By default it is set to None to disable early stopping.
    #
    #    If set to a number, it will set aside validation_fraction
    #    size of the training data as validation and terminate training
    #    when validation score is not improving in all of the previous
    #    n_iter_no_change numbers of iterations.
    #
    #    Values must be in the range [1, inf)
    #
    #    New in version 0.20.
    #
    # tol : float (default=1e-4)
    #    Tolerance for the early stopping.
    #    When the loss is not improving by at least tol for
    #    n_iter_no_change iterations (if set to a number), the training stops.
    #    Values must be in the range (0.0, inf).
    #    New in version 0.20.
    #
    #  ccp_alpha: non-negative float (default=0.0*)
    #     Complexity parameter used for Minimal Cost-Complexity Pruning.
    #     The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
    #     By default, no pruning is performed.
    #     Values must be in the range [0.0, inf).
    #     See Minimal Cost-Complexity Pruning for details.
    #     New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["GradientBoostingRegressor"] = GradientBoostingRegressor
    model_constructor_name["GradientBoostingRegressor"] = "GradientBoostingRegressor"
    model_fit_fn_attr_name["GradientBoostingRegressor"] = "fit"
    model_predict_fn_attr_name["GradientBoostingRegressor"] = "predict"
    model_constructor_arg_defaults["GradientBoostingRegressor"] = {
        "loss": "squared_error",
        "learning_rate": 0.1,
        "n_estimators": 100,
        "subsample": 1.0,
        "criterion": "friedman_mse",
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        "max_depth": 3,
        "min_impurity_decrease": 0.0,  #'min_impurity_split' : 1e-7, \  #<-- Deprecated AFTER v0.19, will be removed >= v0.25 [Use min_impurity_decrease arg instead]
        "init": None,
        "random_state": None,
        "max_features": None,
        "alpha": 0.9,
        "verbose": 0,
        "max_leaf_nodes": None,
        "warm_start": False,
        "validation_fraction": 0.1,
        "n_iter_no_change": None,
        "tol": 1e-4,
        "ccp_alpha": 0.0,
    }
    model_required_non_cnstr_attribs["GradientBoostingRegressor"] = [
        "train_score_",
        "init_",
        "estimators_",
        "n_estimators_",
        "n_features_in_",
        "max_features_",
    ]
    # NOTE: "n_features_in_" attribute seems to be required by predict() method, but not mentioned in docs for GradientBoostingRegressor. Also, 'oob_improvement_' relates to training data...Perhaps do not need to be persisted in model as relates to training data.(?)
    # NOTE: "loss_" DEPRECATED: Attribute "loss_" was deprecated in version 1.1 and will be removed in 1.3.
    model_optional_non_cnstr_attribs["GradientBoostingRegressor"] = [
        "oob_improvement_",
        "feature_names_in_",  # New in version 0.24.
    ]
    # NOTE: "feature_importances_" is actually a class property (formulation), not an assignable/persistable attribute

    # ============================================ GradientBoostingClassifier =========================================

    # --------------------------------------------------
    # GradientBoostingClassifier Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    # loss : str {"log_loss", "deviance", "exponential"} (default="log_loss")
    #    The loss function to be optimized.
    #       "log_loss" refers to binomial and multinomial deviance, the same as used in logistic regression.
    #       It is a good choice for classification with probabilistic outputs.
    #       For loss "exponential", gradient boosting recovers the GradientBoostingClassifier algorithm.
    #
    #    Deprecated since version 1.1: The loss "deviance" was deprecated in v1.1
    #       and will be removed in version 1.3.
    #       Use loss="log_loss" which is equivalent.
    #
    # learning_rate : float (default=0.1)
    #    Learning rate shrinks the contribution of each tree by learning_rate.
    #    There is a trade-off between learning_rate and n_estimators.
    #    Values must be in the range (0.0, inf).
    #
    # n_estimators : int (default=100)
    #    The number of boosting stages to perform.
    #    Gradient boosting is fairly robust to over-fitting
    #    so a large number usually results in better performance.
    #    Values must be in the range [1, inf).
    #
    # subsample : float (default=1.0)
    #    The fraction of samples to be used for fitting the individual base learners.
    #    If smaller than 1.0 this results in Stochastic Gradient Boosting.
    #    subsample interacts with the parameter n_estimators.
    #    Choosing subsample < 1.0 leads to a reduction of variance
    #       and an increase in bias.
    #    Values must be in the range (0.0, 1.0].
    #
    # criterion : str {"friedman_mse", "squared_error"} (default="friedman_mse")
    #    The function to measure the quality of a split.
    #    Supported criteria are:
    #       "friedman_mse" for the mean squared error with improvement score by Friedman
    #       "squared_error" for mean squared error.
    #    The default value of "friedman_mse" is generally the best
    #       as it can provide a better approximation in some cases.
    #    New in version 0.18.
    #    Deprecated since version 1.0: Criterion "mse" was deprecated in v1.0
    #       and will be removed in version 1.2.
    #       Use criterion='squared_error' which is equivalent.
    #
    # min_samples_split : int, float (default=2)
    #    The minimum number of samples required to split an internal node:
    #
    #    If int, values must be in the range [2, inf)
    #    If float, values must be in the range (0.0, 1.0]
    #       and min_samples_split will be ceil(min_samples_split * n_samples).
    #    Changed in version 0.18: Added float values for fractions.
    #
    # min_samples_leaf : int, float (default=1)
    #    The minimum number of samples required to be at a leaf node.
    #    A split point at any depth will only be considered if it leaves
    #    at least min_samples_leaf training samples in each of the left and right branches.
    #    This may have the effect of smoothing the model, especially in regression.
    #
    #    If int, values must be in the range [1, inf).
    #    If float, values must be in the range (0.0, 1.0] and
    #       min_samples_leaf will be ceil(min_samples_leaf * n_samples).
    #
    # min_weight_fraction_leaf : float (default=0.0)
    #    The minimum weighted fraction of the sum total of weights
    #    (of all the input samples) required to be at a leaf node.
    #    Samples have equal weight when sample_weight is not provided.
    #    Values must be in the range [0.0, 0.5].
    #
    # max_depth : int (default=3)
    #    maximum depth of the individual regression estimators.
    #    The maximum depth limits the number of nodes in the tree.
    #    Tune this parameter for best performance;
    #    the best value depends on the interaction of the input variables.
    #    Values must be in the range [1, inf).
    #
    # min_impurity_decrease : float (default=0.0)
    #    A node will be split if this split induces a decrease
    #    of the impurity greater than or equal to this value.
    #    Values must be in the range [0.0, inf).
    #
    #    The weighted impurity decrease equation is the following:
    #
    #    N_t / N * (impurity - N_t_R / N_t * right_impurity - N_t_L / N_t * left_impurity)
    #       where: N is the total number of samples
    #              N_t is the number of samples at the current node
    #              N_t_L is the number of samples in the left child
    #          and N_t_R is the number of samples in the right child.
    #
    #    N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed.
    #    New in version 0.19.
    #
    # init : estimator or "zero" (default=None)
    #    An estimator object that is used to compute the initial predictions.
    #    init has to provide fit and predict.
    #    If "zero", the initial raw predictions are set to zero.
    #    By default, a DummyEstimator predicting the classes priors is used.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Controls the random seed given to each Tree estimator at each boosting iteration.
    #    In addition, it controls the random permutation of the features at each split (see Notes for more details).
    #    It also controls the random splitting of the training data
    #    to obtain a validation set if n_iter_no_change is not None.
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    #    If None (default):
    #       Use the global random state instance from numpy.random.
    #      Calling the function multiple times will reuse the same instance,
    #      and will produce different results.
    #
    #    If int:
    #       Use a new random number generator seeded by the given integer.
    #       Using an int will produce the same results across different calls.
    #       However, it may be worthwhile checking that your results are stable
    #       across a number of different distinct random seeds.
    #       Popular integer random seeds are 0 and 42.
    #       Integer values must be in the range [0, 2**32 - 1].
    #
    #    If RandomState instance:
    #       Use the provided random state, only affecting other users
    #       of that same random state instance.
    #       Calling the function multiple times will reuse the same instance,
    #       and will produce different results.
    #
    # max_features : int, float, string {"auto", "sqrt", "log2"} or None (default=None)
    #    The number of features to consider when looking for the best split:
    #
    #    If int, values must be in the range [1, inf).
    #    If float, values must be in the range (0.0, 1.0]
    #      and the features considered at each split
    #      will be max(1, int(max_features * n_features_in_)).
    #    If "auto", then max_features=n_features.
    #    If "sqrt", then max_features=sqrt(n_features).
    #    If "log2", then max_features=log2(n_features).
    #    If None, then max_features=n_features.
    #    Choosing max_features < n_features leads to a reduction
    #    of variance and an increase in bias.
    #
    #    NOTE: the search for a split does not stop until
    #    at least one valid partition of the node samples is found,
    #    even if it requires to effectively inspect more than max_features features.
    #
    # verbose : int (default=0)
    #    Enable verbose output.
    #    If 1 then it prints progress and performance once in a while
    #    (the more trees the lower the frequency).
    #    If greater than 1 then it prints progress and performance for every tree.
    #    Values must be in the range [0, inf).
    #
    # max_leaf_nodes : int or None (default=None)
    #    Grow trees with max_leaf_nodes in best-first fashion.
    #    Best nodes are defined as relative reduction in impurity.
    #    Values must be in the range [2, inf).
    #    If None then unlimited number of leaf nodes.
    #
    # warm_start : bool (default=False)
    #    When set to True, reuse the solution of the previous call
    #    to fit and add more estimators to the ensemble,
    #    otherwise, just erase the previous solution.
    #    See the Glossary.
    #
    # validation_fraction : float (default=0.1)
    #    The proportion of training data to set aside as validation set for early stopping.
    #    Values must be in the range (0.0, 1.0).
    #    Only used if n_iter_no_change is set to an integer.
    #    New in version 0.20.
    #
    # n_iter_no_change : int (default=None)
    #
    #    n_iter_no_change is used to decide if early stopping will be used
    #    to terminate training when validation score is not improving.
    #
    #    By default it is set to None to disable early stopping.
    #
    #    If set to a number, it will set aside validation_fraction
    #    size of the training data as validation and terminate training
    #    when validation score is not improving in all of the previous
    #    n_iter_no_change numbers of iterations.
    #
    #    Values must be in the range [1, inf)
    #
    #    New in version 0.20.
    #
    # tol : float (default=1e-4)
    #    Tolerance for the early stopping.
    #    When the loss is not improving by at least tol for
    #    n_iter_no_change iterations (if set to a number), the training stops.
    #    Values must be in the range (0.0, inf).
    #    New in version 0.20.
    #
    #  ccp_alpha: non-negative float (default=0.0)
    #     Complexity parameter used for Minimal Cost-Complexity Pruning.
    #     The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
    #     By default, no pruning is performed.
    #     Values must be in the range [0.0, inf).
    #     See Minimal Cost-Complexity Pruning for details.
    #     New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["GradientBoostingClassifier"] = GradientBoostingClassifier
    model_constructor_name["GradientBoostingClassifier"] = "GradientBoostingClassifier"
    model_fit_fn_attr_name["GradientBoostingClassifier"] = "fit"
    model_predict_fn_attr_name["GradientBoostingClassifier"] = "predict"
    model_constructor_arg_defaults["GradientBoostingClassifier"] = {
        "loss": "log_loss",
        "learning_rate": 0.1,
        "n_estimators": 100,
        "subsample": 1.0,
        "criterion": "friedman_mse",
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        "max_depth": 3,
        "min_impurity_decrease": 0.0,  #'min_impurity_split' : 1e-7, \  #<-- Deprecated AFTER v0.19, will be removed >= v0.25 [Use min_impurity_decrease arg instead]
        "init": None,
        "random_state": None,
        "max_features": None,
        "verbose": 0,
        "max_leaf_nodes": None,
        "warm_start": False,
        "validation_fraction": 0.1,
        "n_iter_no_change": None,
        "tol": 1e-4,
        "ccp_alpha": 0.0,
    }
    model_required_non_cnstr_attribs["GradientBoostingClassifier"] = [
        "n_estimators_",
        "train_score_",
        "init_",
        "estimators_",
        "classes_",
        "n_features_in_",  # New in version 0.24.
        "n_classes_",
        "max_features_",
    ]
    # NOTE: "n_features_in_" attribute seems to be required by predict() method, but not mentioned in docs for GradientBoostingClassifier. Also, 'oob_improvement_' relates to training data...Perhaps do not need to be persisted in model as relates to training data.(?)
    # NOTE: "loss_" DEPRECATED: Attribute "loss_" was deprecated in version 1.1 and will be removed in 1.3.
    model_optional_non_cnstr_attribs["GradientBoostingClassifier"] = [
        "oob_improvement_",
        "feature_names_in_",  # New in version 0.24.
    ]
    # NOTE: "feature_importances_" is actually a class property (formulation), not an assignable/persistable attribute

    # ============================================ HistGradientBoostingRegressor =========================================

    # --------------------------------------------------
    # HistGradientBoostingRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    # loss : str {"squared_error", "absolute_error", "poisson", "quantile"} (default="squared_error")
    #    The loss function to use in the boosting process.
    #
    #    Note that the "squared error" and "poisson" losses actually
    #    implement "half least squares loss" and "half poisson deviance"
    #    to simplify the computation of the gradient.
    #
    #    Furthermore, "poisson" loss internally uses a log-link
    #    and requires y >= 0. "quantile" uses the pinball loss.
    #
    #    Changed in version 0.23: Added option "poisson".
    #
    #    Changed in version 1.1: Added option "quantile".
    #
    #    Deprecated since version 1.0:
    #       The loss "least_squares" was deprecated in v1.0
    #       and will be removed in version 1.2.
    #       Use loss="squared_error" which is equivalent.
    #
    #    Deprecated since version 1.0:
    #       The loss "least_absolute_deviation" was deprecated in v1.0
    #       and will be removed in version 1.2.
    #       Use loss="absolute_error" which is equivalent.
    #
    # quantile : float (default=None)
    #    If loss is "quantile", this parameter specifies which
    #    quantile to be estimated and must be between 0 and 1.
    #
    # learning_rate : float (default=0.1)
    #    The learning rate, also known as shrinkage.
    #    This is used as a multiplicative factor for the leaves values.
    #    Use 1 for no shrinkage.
    #
    # max_iter : int (default=100)
    #    The maximum number of iterations of the boosting process,
    #    i.e. the maximum number of trees.
    #
    # max_leaf_nodes : int or None (default=31)
    #    The maximum number of leaves for each tree.
    #    Must be strictly greater than 1.
    #    If None, there is no maximum limit.
    #
    # max_depth : int or None (default=None)
    #    The maximum depth of each tree.
    #    The depth of a tree is the number of edges
    #    to go from the root to the deepest leaf.
    #    Depth isn't constrained by default.
    #
    # min_samples_leaf : int (default=20)
    #    The minimum number of samples per leaf.
    #    For small datasets with less than a few hundred samples,
    #    it is recommended to lower this value
    #    since only very shallow trees would be built.
    #
    # l2_regularization : float (default=0)
    #    The L2 regularization parameter.
    #    Use 0 for no regularization (default).
    #
    # max_bins : int (default=255)
    #    The maximum number of bins to use for non-missing values.
    #    Before training, each feature of the input array X
    #    is binned into integer-valued bins, which allows for
    #    a much faster training stage.
    #
    #    Features with a small number of unique
    #    values may use less than max_bins bins.
    #    In addition to the max_bins bins, one more bin
    #    is always reserved for missing values.
    #
    #    Must be no larger than 255.
    #
    # categorical_features : array-like of {bool, int} of shape (n_features)
    #                        or shape (n_categorical_features,), (default=None)
    #    Indicates the categorical features.
    #       None : no feature will be considered categorical.
    #       boolean array-like : boolean mask indicating categorical features.
    #       integer array-like : integer indices indicating categorical features.
    #
    #    For each categorical feature, there must be at most max_bins unique categories,
    #    and each categorical value must be in [0, max_bins -1].
    #
    #    Read more in the User Guide.
    #    New in version 0.24.
    #
    # monotonic_cst: array-like of int of shape (n_features), (default=None)
    #    Indicates the monotonic constraint to enforce on each feature.
    #
    #    -1, 1 and 0 respectively correspond to a
    #    negative constraint, positive constraint and no constraint.
    #
    #    Read more in the User Guide.
    #    New in version 0.23.
    #
    # warm_start : bool, (default=False)
    #    When set to True, reuse the solution of the previous call
    #    to fit and add more estimators to the ensemble.
    #    For results to be valid, the estimator
    #    should be re-trained on the same data only.
    #    See the Glossary.
    #
    # early_stopping : "auto" or bool (default="auto")
    #    If "auto", early stopping is enabled if the sample size is larger than 10000.
    #    If True, early stopping is enabled, otherwise early stopping is disabled.
    #
    #    New in version 0.23.
    #
    # scoring : str or callable or None (default="loss")
    #    Scoring parameter to use for early stopping.
    #    It can be a single string
    #    (see The scoring parameter: defining model evaluation rules)
    #    or a callable (see Defining your scoring strategy from metric functions).
    #
    #    If None, the estimator's default scorer is used.
    #    If scoring="loss", early stopping is checked w.r.t the loss value.
    #
    #    Only used if early stopping is performed.
    #
    # validation_fraction : int or float (default=0.1)
    #    Proportion (or absolute size) of training data
    #    to set aside as validation data for early stopping.
    #
    #    If None, early stopping is done on the training data.
    #
    #    Only used if early stopping is performed.
    #
    # n_iter_no_change : int (default=10)
    #    Used to determine when to "early stop".
    #    The fitting process is stopped when none of the last
    #    n_iter_no_change scores are better than
    #    the n_iter_no_change - 1 -th-to-last one,
    #    up to some tolerance.
    #
    #    Only used if early stopping is performed.
    #
    # tol : float (default=1e-7)
    #    The absolute tolerance to use when comparing scores during early stopping.
    #
    #    The higher the tolerance, the more likely we are to early stop:
    #       higher tolerance means that it will be harder for subsequent iterations
    #       to be considered an improvement upon the reference score.
    #
    # verbose : int, (default=0)
    #    The verbosity level.
    #    If not zero, print some information about the fitting process.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Pseudo-random number generator to control the subsampling in the binning process,
    #    and the train/validation data split if early stopping is enabled.
    #
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    # --------------------------------------------------
    model_constructor["HistGradientBoostingRegressor"] = HistGradientBoostingRegressor
    model_constructor_name["HistGradientBoostingRegressor"] = (
        "HistGradientBoostingRegressor"
    )
    model_fit_fn_attr_name["HistGradientBoostingRegressor"] = "fit"
    model_predict_fn_attr_name["HistGradientBoostingRegressor"] = "predict"
    model_constructor_arg_defaults["HistGradientBoostingRegressor"] = {
        "loss": "squared_error",
        "quantile": None,
        "learning_rate": 0.1,
        "max_iter": 100,
        "max_leaf_nodes": 31,
        "max_depth": None,
        "min_samples_leaf": 20,
        "l2_regularization": 0,
        "max_bins": 255,
        "categorical_features": None,
        "monotonic_cst": None,
        "warm_start": False,
        "early_stopping": "auto",
        "scoring": "loss",
        "validation_fraction": 0.1,
        "n_iter_no_change": 10,
        "tol": 1e-7,
        "verbose": 0,
        "random_state": None,
    }
    model_required_non_cnstr_attribs["HistGradientBoostingRegressor"] = [
        "do_early_stopping_",
        "n_iter_",
        "n_trees_per_iteration_",
        "train_score_",
        "validation_score_",
        "is_categorical_",
        "n_features_in_",  # New in version 0.24.
    ]
    # NOTE: "n_features_in_" attribute seems to be required by predict() method, but not mentioned in docs for HistGradientBoostingRegressor. Also, 'oob_improvement_' relates to training data...Perhaps do not need to be persisted in model as relates to training data.(?)
    model_optional_non_cnstr_attribs["HistGradientBoostingRegressor"] = [
        "feature_names_in_",  # New in version 1.0.
    ]

    # ============================================ HistGradientBoostingClassifier =========================================

    # --------------------------------------------------
    # HistGradientBoostingClassifier Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    # loss : str {"log_loss", "auto", "binary_crossentropy"} (default="log_loss")
    #    The loss function to use in the boosting process.
    #
    #    For binary classification problems, "log_loss" is also known as
    #    logistic loss, binomial deviance or binary crossentropy.
    #    Internally, the model fits one tree per boosting iteration
    #    and uses the logistic sigmoid function (expit) as inverse link function
    #    to compute the predicted positive class probability.
    #
    #    For multiclass classification problems, "log_loss" is also known as
    #    multinomial deviance or categorical crossentropy.
    #    Internally, the model fits one tree per boosting iteration
    #    and per class and uses the softmax function as inverse link function
    #    to compute the predicted probabilities of the classes.
    #
    #    Deprecated since version 1.1: The loss arguments "auto",
    #    "binary_crossentropy" and "categorical_crossentropy" were deprecated in v1.1
    #    and will be removed in version 1.3.
    #    Use loss="log_loss" which is equivalent.
    #
    # learning_rate : float (default=0.1)
    #    The learning rate, also known as shrinkage.
    #    This is used as a multiplicative factor for the leaves values.
    #    Use 1 for no shrinkage.
    #
    # max_iter : int (default=100)
    #    The maximum number of iterations of the boosting process,
    #    i.e. the maximum number of trees for binary classification.
    #    For multiclass classification, n_classes trees per iteration are built.
    #
    # max_leaf_nodes : int or None (default=31)
    #    The maximum number of leaves for each tree.
    #    Must be strictly greater than 1.
    #    If None, there is no maximum limit.
    #
    # max_depth : int or None (default=None)
    #    The maximum depth of each tree.
    #    The depth of a tree is the number of edges
    #    to go from the root to the deepest leaf.
    #    Depth isn't constrained by default.
    #
    # min_samples_leaf : int (default=20)
    #    The minimum number of samples per leaf.
    #    For small datasets with less than a few hundred samples,
    #    it is recommended to lower this value
    #    since only very shallow trees would be built.
    #
    # l2_regularization : float (default=0)
    #    The L2 regularization parameter.
    #    Use 0 for no regularization.
    #
    # max_bins : int (default=255)
    #    The maximum number of bins to use for non-missing values.
    #    Before training, each feature of the input array X
    #    is binned into integer-valued bins, which allows for
    #    a much faster training stage.
    #
    #    Features with a small number of unique
    #    values may use less than max_bins bins.
    #    In addition to the max_bins bins, one more bin
    #    is always reserved for missing values.
    #
    #    Must be no larger than 255.
    #
    # categorical_features : array-like of {bool, int} of shape (n_features)
    #                        or shape (n_categorical_features,), (default=None)
    #    Indicates the categorical features.
    #       None : no feature will be considered categorical.
    #       boolean array-like : boolean mask indicating categorical features.
    #       integer array-like : integer indices indicating categorical features.
    #
    #    For each categorical feature, there must be at most max_bins unique categories,
    #    and each categorical value must be in [0, max_bins -1].
    #
    #    Read more in the User Guide.
    #    New in version 0.24.
    #
    # monotonic_cst: array-like of int of shape (n_features), (default=None)
    #    Indicates the monotonic constraint to enforce on each feature.
    #
    #    -1, 1 and 0 respectively correspond to a
    #    negative constraint, positive constraint and no constraint.
    #
    #    Read more in the User Guide.
    #    New in version 0.23.
    #
    # warm_start : bool, (default=False)
    #    When set to True, reuse the solution of the previous call
    #    to fit and add more estimators to the ensemble.
    #    For results to be valid, the estimator
    #    should be re-trained on the same data only.
    #    See the Glossary.
    #
    # early_stopping : "auto" or bool (default="auto")
    #    If "auto", early stopping is enabled if the sample size is larger than 10000.
    #    If True, early stopping is enabled, otherwise early stopping is disabled.
    #
    #    New in version 0.23.
    #
    # scoring : str or callable or None (default="loss")
    #    Scoring parameter to use for early stopping.
    #    It can be a single string
    #    (see The scoring parameter: defining model evaluation rules)
    #    or a callable (see Defining your scoring strategy from metric functions).
    #
    #    If None, the estimator's default scorer is used.
    #    If scoring="loss", early stopping is checked w.r.t the loss value.
    #
    #    Only used if early stopping is performed.
    #
    # validation_fraction : int or float (default=0.1)
    #    Proportion (or absolute size) of training data
    #    to set aside as validation data for early stopping.
    #
    #    If None, early stopping is done on the training data.
    #
    #    Only used if early stopping is performed.
    #
    # n_iter_no_change : int (default=10)
    #    Used to determine when to "early stop".
    #    The fitting process is stopped when none of the last
    #    n_iter_no_change scores are better than
    #    the n_iter_no_change - 1 -th-to-last one,
    #    up to some tolerance.
    #
    #    Only used if early stopping is performed.
    #
    # tol : float (default=1e-7)
    #    The absolute tolerance to use when comparing scores.
    #
    #    The higher the tolerance, the more likely we are to early stop:
    #       higher tolerance means that it will be harder for subsequent iterations
    #       to be considered an improvement upon the reference score.
    #
    # verbose : int, (default=0)
    #    The verbosity level.
    #    If not zero, print some information about the fitting process.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Pseudo-random number generator to control the subsampling in the binning process,
    #    and the train/validation data split if early stopping is enabled.
    #
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    # --------------------------------------------------
    model_constructor["HistGradientBoostingClassifier"] = HistGradientBoostingClassifier
    model_constructor_name["HistGradientBoostingClassifier"] = (
        "HistGradientBoostingClassifier"
    )
    model_fit_fn_attr_name["HistGradientBoostingClassifier"] = "fit"
    model_predict_fn_attr_name["HistGradientBoostingClassifier"] = "predict"
    model_constructor_arg_defaults["HistGradientBoostingClassifier"] = {
        "loss": "log_loss",
        "learning_rate": 0.1,
        "max_iter": 100,
        "max_leaf_nodes": 31,
        "max_depth": None,
        "min_samples_leaf": 20,
        "l2_regularization": 0,
        "max_bins": 255,
        "categorical_features": None,
        "monotonic_cst": None,
        "warm_start": False,
        "early_stopping": "auto",
        "scoring": "loss",
        "validation_fraction": 0.1,
        "n_iter_no_change": 10,
        "tol": 1e-7,
        "verbose": 0,
        "random_state": None,
    }
    model_required_non_cnstr_attribs["HistGradientBoostingClassifier"] = [
        "classes_",
        "do_early_stopping_",
        "n_iter_",
        "n_trees_per_iteration_",
        "train_score_",
        "validation_score_",
        "is_categorical_",
        "n_features_in_",  # New in version 0.24.
    ]
    # NOTE: "n_features_in_" attribute seems to be required by predict() method, but not mentioned in docs for HistGradientBoostingClassifier. Also, 'oob_improvement_' relates to training data...Perhaps do not need to be persisted in model as relates to training data.(?)
    model_optional_non_cnstr_attribs["HistGradientBoostingClassifier"] = [
        "feature_names_in_",  # New in version 1.0.
    ]

    # ============================================ AdaBoostRegressor =========================================

    # --------------------------------------------------
    # AdaBoostRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  base_estimator : object (default=None)
    #    The base estimator from which the boosted ensemble is built.
    #
    #    If None, then the base estimator is DecisionTreeRegressor
    #    is initialized with max_depth=3.
    #
    # n_estimators : int (default=50)
    #    The maximum number of estimators at which boosting is terminated.
    #    In case of perfect fit, the learning procedure is stopped early.
    #    Values must be in the range [1, inf).
    #
    # learning_rate : float (default=1.0)
    #    Weight applied to each regressor at each boosting iteration.
    #    A higher learning rate increases the contribution of each regressor.
    #    There is a trade-off between learning_rate and n_estimators parameters.
    #    Values must be in the range (0.0, inf).
    #
    # loss : {"linear", "square", "exponential"} (default="linear")
    #    The loss function to use when updating the weights after each boosting iteration.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Controls the random seed given at each base_estimator at each boosting iteration.
    #    Thus, it is only used when base_estimator exposes a random_state.
    #    In addition, it controls the bootstrap of the weights used to train
    #    the base_estimator at each boosting iteration. Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    #    If None (default):
    #        Use the global random state instance from numpy.random.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #    If int:
    #       Use a new random number generator seeded by the given integer.
    #       Using an int will produce the same results across different calls.
    #       However, it may be worthwhile checking that your results are stable
    #       across a number of different distinct random seeds.
    #       Popular integer random seeds are 0 and 42.
    #       Integer values must be in the range [0, 2**32 - 1].
    #
    #    If RandomState instance:
    #       Use the provided random state, only affecting other users
    #       of that same random state instance.
    #       Calling the function multiple times will reuse the same instance,
    #       and will produce different results.
    #
    # --------------------------------------------------
    model_constructor["AdaBoostRegressor"] = AdaBoostRegressor
    model_constructor_name["AdaBoostRegressor"] = "AdaBoostRegressor"
    model_fit_fn_attr_name["AdaBoostRegressor"] = "fit"
    model_predict_fn_attr_name["AdaBoostRegressor"] = "predict"
    model_constructor_arg_defaults["AdaBoostRegressor"] = {
        "base_estimator": None,
        "n_estimators": 50,
        "learning_rate": 1.0,
        "loss": "linear",
        "random_state": None,
    }
    model_required_non_cnstr_attribs["AdaBoostRegressor"] = [
        "estimators_",
        "estimator_weights_",
        "estimator_errors_",
        "feature_importances_",
        "n_features_in_",  # New in version 0.24.
    ]  # <-- 'n_features', 'n_outputs' attributes do not seem to appear (not applicable) within AdaBoost Models
    # Exclusions:
    # 'base_estimator_' is an internal structure that should be reproduced at instantiation (?)
    model_optional_non_cnstr_attribs["AdaBoostRegressor"] = [
        "feature_names_in_",  # New in version 1.0.
    ]
    # <-- NOTE: '_n_samples', 'max_n_classes' attributes do not seem to appear. Also, 'feature_importances_' is actually a class property (formulation), not an assignable/persistable attribute

    # ============================================ AdaBoostClassifier =========================================

    # --------------------------------------------------
    # AdaBoostClassifier Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  base_estimator : object (default=None)
    #    The base estimator from which the boosted ensemble is built.
    #
    #    Support for sample weighting is required, as well as proper classes_ and n_classes_ attributes.
    #    If None, then the base estimator is DecisionTreeClassifier initialized with max_depth=1.
    #
    # n_estimators : int (default=50)
    #    The maximum number of estimators at which boosting is terminated.
    #    In case of perfect fit, the learning procedure is stopped early.
    #    Values must be in the range [1, inf).
    #
    # learning_rate : float (default=1.0)
    #    Weight applied to each regressor at each boosting iteration.
    #    A higher learning rate increases the contribution of each classifier.
    #    There is a trade-off between the learning_rate and n_estimators parameters.
    #    Values must be in the range (0.0, inf).
    #
    # algorithm : {"SAMME", "SAMME.R"} (default="SAMME.R")
    #    If "SAMME.R" then use the SAMME.R real boosting algorithm.
    #    base_estimator must support calculation of class probabilities.
    #
    #    If "SAMME" then use the SAMME discrete boosting algorithm.
    #
    #    The SAMME.R algorithm typically converges faster than SAMME,
    #    achieving a lower test error with fewer boosting iterations.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Controls the random seed given at each base_estimator at each boosting iteration.
    #    Thus, it is only used when base_estimator exposes a random_state.
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    #    If None (default):
    #        Use the global random state instance from numpy.random.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #    If int:
    #       Use a new random number generator seeded by the given integer.
    #       Using an int will produce the same results across different calls.
    #       However, it may be worthwhile checking that your results are stable
    #       across a number of different distinct random seeds.
    #       Popular integer random seeds are 0 and 42.
    #       Integer values must be in the range [0, 2**32 - 1].
    #
    #    If RandomState instance:
    #       Use the provided random state, only affecting other users
    #       of that same random state instance.
    #       Calling the function multiple times will reuse the same instance,
    #       and will produce different results.
    #
    # --------------------------------------------------
    model_constructor["AdaBoostClassifier"] = AdaBoostClassifier
    model_constructor_name["AdaBoostClassifier"] = "AdaBoostClassifier"
    model_fit_fn_attr_name["AdaBoostClassifier"] = "fit"
    model_predict_fn_attr_name["AdaBoostClassifier"] = "predict"
    model_constructor_arg_defaults["AdaBoostClassifier"] = {
        "base_estimator": None,
        "n_estimators": 50,
        "learning_rate": 1.0,
        "algorithm": "SAMME.R",
        "random_state": None,
    }
    model_required_non_cnstr_attribs["AdaBoostClassifier"] = [
        "estimators_",
        "classes_",
        "n_classes_",
        "estimator_weights_",
        "estimator_errors_",
        "feature_importances_",
        "n_features_in_",  # New in version 0.24.
    ]  # <-- 'n_features', 'n_outputs' attributes do not seem to appear (not applicable) within AdaBoost Models
    # Exclusions:
    # 'base_estimator_' is an internal structure that should be reproduced at instantiation (?)
    model_optional_non_cnstr_attribs["AdaBoostClassifier"] = [
        "feature_names_in_",  # New in version 1.0.
    ]
    # <-- NOTE: '_n_samples', 'max_n_classes' attributes do not seem to appear. Also, 'feature_importances_' is actually a class property (formulation), not an assignable/persistable attribute

    # ================================= DecisionTreeRegressor MODEL CONFIGURATION =====================================

    # --------------------------------------------------
    # DecisionTreeRegressor Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  criterion: str {"squared_error", "absolute_error", "poisson"}, (default="squared_error")
    #     The function to measure the quality of a split.
    #     Supported criteria are "squared_error" for the mean squared error,
    #     which is equal to variance reduction as feature selection criterion
    #     and minimizes the L2 loss using the mean of each terminal node, "friedman_mse",
    #     which uses mean squared error with Friedman's improvement score
    #     for potential splits, "absolute_error" for the mean absolute error,
    #     which minimizes the L1 loss using the median of each terminal node,
    #     and "poisson" which uses reduction in Poisson deviance to find splits.
    #
    #     New in version 0.18: Mean Absolute Error (MAE) criterion.
    #     New in version 0.24: Poisson deviance criterion.
    #
    #     Deprecated since version 1.0: Criterion "mse" was deprecated in v1.0
    #        and will be removed in version 1.2.
    #        Use criterion="squared_error" which is equivalent.
    #     Deprecated since version 1.0: Criterion "mae" was deprecated in v1.0
    #
    #        and will be removed in version 1.2.
    #        Use criterion="absolute_error" which is equivalent.
    #
    #  splitter: str {"best", "random"}, (default="best")
    #     The strategy used to choose the split at each node.
    #     Supported strategies are "best" to choose the best split
    #     and "random" to choose the best random split.
    #
    #  max_depth: int or None (default=None)
    #     The maximum depth of the tree.
    #     If None, then nodes are expanded until all leaves are pure
    #     or until all leaves contain less than min_samples_split samples.
    #
    #  min_samples_split: int or float (default=2)
    #     The minimum number of samples required to split an internal node:
    #        If int, then consider min_samples_split as the minimum number.
    #        If float, then min_samples_split is a fraction
    #           and ceil(min_samples_split * n_samples)
    #           are the minimum number of samples for each split.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_samples_leaf: int or float (default=1)
    #     The minimum number of samples required to be at a leaf node.
    #     A split point at any depth will only be considered if it leaves
    #     at least min_samples_leaf training samples in each of the left and right branches.
    #     This may have the effect of smoothing the model, especially in regression.
    #        If int, then consider min_samples_leaf as the minimum number.
    #        If float, then min_samples_leaf is a fraction
    #           and ceil(min_samples_leaf * n_samples)
    #           are the minimum number of samples for each node.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_weight_fraction_leaf: float (default=0.0)
    #     The minimum weighted fraction of the sum total of weights
    #     (of all the input samples) required to be at a leaf node.
    #     Samples have equal weight when sample_weight is not provided.
    #
    #  max_features: int, float, str {"sqrt","log2"}, None (default=None)
    #     The number of features to consider when looking for the best split:
    #        If int, then consider max_features features at each split.
    #        If float, then max_features is a fraction and
    #           int(max_features * n_features) features are considered at each split.
    #        If "auto", then max_features=n_features. [DEPRECATED since version 1.1]
    #        If "sqrt", then max_features=sqrt(n_features).
    #        If "log2", then max_features=log2(n_features).
    #        If None, then max_features=n_features.
    #     Deprecated since version 1.1: The "auto" option was deprecated in 1.1 and will be removed in 1.3.
    #     NOTE: the search for a split does not stop until at least one valid partition
    #        of the node samples is found, even if it requires to effectively inspect
    #        more than max_features features.
    #
    #  random_state: int, RandomState instance, None (default=None)
    #     Controls the randomness of the estimator.
    #     The features are always randomly permuted at each split,
    #     even if splitter is set to "best".
    #
    #     When max_features < n_features, the algorithm will select max_features
    #     at random at each split before finding the best split among them.
    #     But the best found split may vary across different runs,
    #     even if max_features=n_features.
    #
    #     That is the case, if the improvement of the criterion is identical for several splits
    #     and one split has to be selected at random.
    #     To obtain a deterministic behaviour during fitting,
    #     random_state has to be fixed to an integer.
    #
    #     See Glossary for details.
    #
    #     If None (default):
    #        Use the global random state instance from numpy.random.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #     If int:
    #        Use a new random number generator seeded by the given integer.
    #        Using an int will produce the same results across different calls.
    #        However, it may be worthwhile checking that your results
    #        are stable across a number of different distinct random seeds.
    #        Popular integer random seeds are 0 and 42.
    #        Integer values must be in the range [0, 2**32 - 1].
    #
    #     If RandomState instance:
    #        Use the provided random state, only affecting other users
    #        of that same random state instance.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #  max_leaf_nodes: int or None (default=None)
    #     Grow a tree with max_leaf_nodes in best-first fashion.
    #     Best nodes are defined as relative reduction in impurity.
    #     If None then unlimited number of leaf nodes.
    #
    #  min_impurity_decrease: float (default=0.0)
    #     A node will be split if this split induces a decrease
    #     of the impurity greater than or equal to this value.
    #     The weighted impurity decrease equation is the following:
    #        N_t / N * (impurity - N_t_R / N_t * right_impurity - N_t_L / N_t * left_impurity)
    #     where:
    #        N is the total number of samples
    #        N_t is the number of samples at the current node
    #        N_t_L is the number of samples in the left child
    #        N_t_R is the number of samples in the right child.
    #        N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed
    #
    #     New in version 0.19.
    #
    #  ccp_alpha: (non-negative) float (default=0.0)
    #     Complexity parameter used for Minimal Cost-Complexity Pruning.
    #     The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
    #     By default, no pruning is performed.
    #     See Minimal Cost-Complexity Pruning for details.
    #     New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["DecisionTreeRegressor"] = DecisionTreeRegressor
    model_constructor_name["DecisionTreeRegressor"] = "DecisionTreeRegressor"
    model_fit_fn_attr_name["DecisionTreeRegressor"] = "fit"
    model_predict_fn_attr_name["DecisionTreeRegressor"] = "predict"
    model_constructor_arg_defaults["DecisionTreeRegressor"] = {
        "criterion": "squared_error",
        "splitter": "best",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        "max_features": 1.0,
        "random_state": None,
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.0,  #'min_impurity_split' : 1e-7,  #<-- Deprecated AFTER v0.19, will be removed >= v0.25 [Use min_impurity_decrease arg instead]
        "ccp_alpha": 0.0,  # New in version 0.22
    }
    model_required_non_cnstr_attribs["DecisionTreeRegressor"] = [
        "max_features_",
        "n_features_in_",
        "tree_",
    ]
    # Exclusions:
    # 'feature_importances_' is actually a class property (formulation), not an assignable/persistable attribute
    model_optional_non_cnstr_attribs["DecisionTreeRegressor"] = [
        "feature_names_in_",  # New in version 1.0
        "n_outputs_",
    ]

    # ================================= DecisionTreeClassifier MODEL CONFIGURATION =====================================

    # --------------------------------------------------
    # DecisionTreeClassifier Estimation Parameters
    # All arguments are optional.
    # --------------------------------------------------
    #  criterion: str {"gini", "entropy", "log_loss"}, (default="gini")
    #     The function to measure the quality of a split.
    #     Supported criteria are "gini" for the Gini impurity
    #     and "log_loss" and "entropy" both for the Shannon information gain,
    #     see Mathematical formulation.
    #
    #  splitter: str {"best", "random"}, (default="best")
    #     The strategy used to choose the split at each node.
    #     Supported strategies are "best" to choose the best split
    #     and "random" to choose the best random split.
    #
    #  max_depth: int or None (default=None)
    #     The maximum depth of the tree.
    #     If None, then nodes are expanded until all leaves are pure
    #     or until all leaves contain less than min_samples_split samples.
    #
    #  min_samples_split: int or float (default=2)
    #     The minimum number of samples required to split an internal node:
    #        If int, then consider min_samples_split as the minimum number.
    #        If float, then min_samples_split is a fraction
    #           and ceil(min_samples_split * n_samples)
    #           are the minimum number of samples for each split.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_samples_leaf: int or float (default=1)
    #     The minimum number of samples required to be at a leaf node.
    #     A split point at any depth will only be considered if it leaves
    #     at least min_samples_leaf training samples in each of the left and right branches.
    #     This may have the effect of smoothing the model, especially in regression.
    #        If int, then consider min_samples_leaf as the minimum number.
    #        If float, then min_samples_leaf is a fraction
    #           and ceil(min_samples_leaf * n_samples)
    #           are the minimum number of samples for each node.
    #     Changed in version 0.18: Added float values for fractions.
    #
    #  min_weight_fraction_leaf: float (default=0.0)
    #     The minimum weighted fraction of the sum total of weights
    #     (of all the input samples) required to be at a leaf node.
    #     Samples have equal weight when sample_weight is not provided.
    #
    #  max_features: int, float, string {"sqrt","log2"}, None (default=None)
    #     The number of features to consider when looking for the best split:
    #        If int, then consider max_features features at each split.
    #        If float, then max_features is a fraction and
    #           int(max_features * n_features) features are considered at each split.
    #        If "auto", then max_features=n_features. [DEPRECATED since version 1.1]
    #        If "sqrt", then max_features=sqrt(n_features).
    #        If "log2", then max_features=log2(n_features).
    #        If None, then max_features=n_features.
    #     Deprecated since version 1.1: The "auto" option was deprecated in 1.1 and will be removed in 1.3.
    #     NOTE: the search for a split does not stop until at least one valid partition
    #        of the node samples is found, even if it requires to effectively inspect
    #        more than max_features features.
    #
    #  random_state: int, RandomState instance, None (default=None)
    #     Controls the randomness of the estimator.
    #     The features are always randomly permuted at each split,
    #     even if splitter is set to "best".
    #
    #     When max_features < n_features, the algorithm will select max_features
    #     at random at each split before finding the best split among them.
    #     But the best found split may vary across different runs,
    #     even if max_features=n_features.
    #
    #     That is the case, if the improvement of the criterion is identical for several splits
    #     and one split has to be selected at random.
    #     To obtain a deterministic behaviour during fitting,
    #     random_state has to be fixed to an integer.
    #
    #     See Glossary for details.
    #
    #     If None (default):
    #        Use the global random state instance from numpy.random.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #     If int:
    #        Use a new random number generator seeded by the given integer.
    #        Using an int will produce the same results across different calls.
    #        However, it may be worthwhile checking that your results
    #        are stable across a number of different distinct random seeds.
    #        Popular integer random seeds are 0 and 42.
    #        Integer values must be in the range [0, 2**32 - 1].
    #
    #     If RandomState instance:
    #        Use the provided random state, only affecting other users
    #        of that same random state instance.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #  max_leaf_nodes: int or None (default=None)
    #     Grow a tree with max_leaf_nodes in best-first fashion.
    #     Best nodes are defined as relative reduction in impurity.
    #     If None then unlimited number of leaf nodes.
    #
    #  min_impurity_decrease: float (default=0.0)
    #     A node will be split if this split induces a decrease
    #     of the impurity greater than or equal to this value.
    #     The weighted impurity decrease equation is the following:
    #        N_t / N * (impurity - N_t_R / N_t * right_impurity - N_t_L / N_t * left_impurity)
    #     where:
    #        N is the total number of samples
    #        N_t is the number of samples at the current node
    #        N_t_L is the number of samples in the left child
    #        N_t_R is the number of samples in the right child.
    #        N, N_t, N_t_R and N_t_L all refer to the weighted sum, if sample_weight is passed
    #
    #     New in version 0.19.
    #
    #  class_weight : dict, list of dict or "balanced", (default=None)
    #     Weights associated with classes in the form {class_label: weight}.
    #     If None, all classes are supposed to have weight one.
    #     For multi-output problems, a list of dicts can be provided
    #     in the same order as the columns of y.
    #
    #     Note that for multioutput (including multilabel) weights
    #     should be defined for each class of every column in its own dict.
    #     For example, for four-class multilabel classification weights
    #     should be [{0: 1, 1: 1}, {0: 1, 1: 5}, {0: 1, 1: 1}, {0: 1, 1: 1}]
    #     instead of [{1:1}, {2:5}, {3:1}, {4:1}].
    #
    #     The "balanced" mode uses the values of y to automatically adjust weights
    #     inversely proportional to class frequencies in the input data
    #     as n_samples / (n_classes * np.bincount(y))
    #
    #     For multi-output, the weights of each column of y will be multiplied.
    #
    #     Note that these weights will be multiplied with sample_weight
    #     (passed through the fit method) if sample_weight is specified.
    #
    #  ccp_alpha: (non-negative) float (default=0.0)
    #     Complexity parameter used for Minimal Cost-Complexity Pruning.
    #     The subtree with the largest cost complexity that is smaller than ccp_alpha will be chosen.
    #     By default, no pruning is performed.
    #     See Minimal Cost-Complexity Pruning for details.
    #     New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["DecisionTreeClassifier"] = DecisionTreeClassifier
    model_constructor_name["DecisionTreeClassifier"] = "DecisionTreeClassifier"
    model_fit_fn_attr_name["DecisionTreeClassifier"] = "fit"
    model_predict_fn_attr_name["DecisionTreeClassifier"] = "predict"
    model_constructor_arg_defaults["DecisionTreeClassifier"] = {
        "criterion": "gini",
        "splitter": "best",
        "max_depth": None,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "min_weight_fraction_leaf": 0.0,
        "max_features": 1.0,
        "random_state": None,
        "max_leaf_nodes": None,
        "min_impurity_decrease": 0.0,  #'min_impurity_split' : 1e-7,  #<-- Deprecated AFTER v0.19, will be removed >= v0.25 [Use min_impurity_decrease arg instead]
        "class_weight": None,
        "ccp_alpha": 0.0,  # New in version 0.22
    }
    model_required_non_cnstr_attribs["DecisionTreeClassifier"] = [
        "classes_",
        "max_features_",
        "n_classes_",
        "n_features_in_",
        "tree_",
    ]
    # Exclusions:
    # 'feature_importances_' is actually a class property (formulation), not an assignable/persistable attribute
    model_optional_non_cnstr_attribs["DecisionTreeClassifier"] = [
        "feature_names_in_",  # New in version 1.0
        "n_outputs_",
    ]

    # ============================================ 'KNeighborsRegressor', 'RadiusNeighborsRegressor' =========================================

    # --------------------------------------------------
    # KNeighborsRegressor / RadiusNeighborsRegressor Estimation Parameters
    # --------------------------------------------------
    #  n_neighbors : int (default=5) [KNeighborsRegressor ONLY] [NOT RadiusNeighborsRegressor]
    #     Number of neighbors to use by default for kneighbors queries.
    #
    #  radius : float (default=1.0) [RadiusNeighborsRegressor ONLY] [NOT KNeighborsRegressor]
    #     Range of parameter space to use by default for radius_neighbors queries.
    #
    #  weights : str {"uniform", "distance"} or callable (default="uniform")
    #     Weight function used in prediction.
    #     Possible values:
    #        "uniform" : uniform weights. All points in each neighborhood are weighted equally.
    #        "distance" : weight points by the inverse of their distance.
    #                     In this case, closer neighbors of a query point will
    #                     have a greater influence than neighbors which are further away.
    #        [callable] : a user-defined function which accepts an array of distances,
    #                     and returns an array of the same shape containing the weights.
    #     Uniform weights are used by default.
    #
    #  algorithm : str {"auto", "ball_tree", "kd_tree", "brute"} (default="auto")
    #     Algorithm used to compute the nearest neighbors:
    #        "ball_tree" will use BallTree
    #        "kd_tree" will use KDTree
    #        "brute" will use a brute-force search.
    #        "auto" will attempt to decide the most appropriate algorithm
    #           based on the values passed to fit method.
    #     NOTE: fitting on sparse input will override the setting of this parameter, using brute force.
    #
    #  leaf_size : int (default=30)
    #     Leaf size passed to BallTree or KDTree.
    #     This can affect the speed of the construction and query,
    #     as well as the memory required to store the tree.
    #     The optimal value depends on the nature of the problem.
    #
    #  p : integer (default=2)
    #     Power parameter for the Minkowski metric from sklearn.metrics.pairwise.pairwise_distances.
    #     When p = 1, this is equivalent to using manhattan_distance (l1),
    #     and euclidean_distance (l2) for p = 2.
    #     For arbitrary p, minkowski_distance (l_p) is used.
    #
    #  metric : str {"minkowski","precomputed", ...} or callable (default="minkowski")
    #     Metric to use for distance computation.
    #     Default is "minkowski", which results in the standard Euclidean distance when p = 2.
    #     See the documentation of scipy.spatial.distance
    #     and the metrics listed in distance_metrics for valid metric values.
    #
    #     If metric is "precomputed", X is assumed to be a distance matrix and must be square during fit.
    #     X may be a sparse graph, in which case only "nonzero" elements may be considered neighbors.
    #
    #     If metric is a callable function, it takes two arrays representing 1D vectors
    #     as inputs and must return one value indicating the distance between those vectors.
    #     This works for Scipy's metrics, but is less efficient than passing the metric name as a string.
    #
    #  metric_params : dict (default=None)
    #    Additional keyword arguments for the metric function.
    #
    #  n_jobs : int or None (default=None)
    #    The number of parallel jobs to run for neighbors search.
    #    None means 1 unless in a joblib.parallel_backend context.
    #    -1 means using all processors.
    #    See Glossary for more details.
    # --------------------------------------------------
    # NOTE: NearestNeighbors appears to be a base class for
    #       KNeighborsRegressor, RadiusNeighborsRegressor, KNeighborsClassifier, RadiusNeighborsClassifier
    #   ==> As such, we DO NOT implement NearestNeighbors class here

    # K_NEIGHBORS:
    model_constructor["KNeighborsRegressor"] = KNeighborsRegressor
    model_constructor_name["KNeighborsRegressor"] = "KNeighborsRegressor"
    model_fit_fn_attr_name["KNeighborsRegressor"] = "fit"
    model_predict_fn_attr_name["KNeighborsRegressor"] = "predict"
    model_constructor_arg_defaults["KNeighborsRegressor"] = {
        "n_neighbors": 5,
        "weights": "uniform",
        "algorithm": "auto",
        "leaf_size": 30,
        "p": 2,
        "metric": "minkowski",
        "metric_params": None,
        "n_jobs": None,
    }
    model_required_non_cnstr_attribs["KNeighborsRegressor"] = [
        "effective_metric_",
        "n_features_in_",
    ]  # <-- 'outputs_2d_' attributes only seems to apply to KNeighborsClassifier (not KNeighborsRegressor). Also, 'classes_' attribute does not seem to apply
    # Exclusions:
    # "_fit_X", "_fit_method", "_tree", "_y"
    model_optional_non_cnstr_attribs["KNeighborsRegressor"] = [
        "effective_metric_params_",
        "feature_names_in_" "n_samples_fit_",  # New in version 0.24.
    ]

    # RADIUS_NEIGHBORS:
    model_constructor["RadiusNeighborsRegressor"] = RadiusNeighborsRegressor
    model_constructor_name["RadiusNeighborsRegressor"] = "RadiusNeighborsRegressor"
    model_fit_fn_attr_name["RadiusNeighborsRegressor"] = "fit"
    model_predict_fn_attr_name["RadiusNeighborsRegressor"] = "predict"
    model_constructor_arg_defaults["RadiusNeighborsRegressor"] = {
        "radius": 1.0,
        "weights": "uniform",
        "algorithm": "auto",
        "leaf_size": 30,
        "p": 2,
        "metric": "minkowski",
        "metric_params": None,
        "n_jobs": None,
    }
    model_required_non_cnstr_attribs["RadiusNeighborsRegressor"] = [
        "effective_metric_",
        "n_features_in_",
    ]  # <-- 'outputs_2d_' attributes only seems to apply to KNeighborsClassifier (not KNeighborsRegressor). Also, 'classes_' attribute does not seem to apply
    # Exclusions:
    # "_fit_X", "_fit_method", "_tree", "_y"
    model_optional_non_cnstr_attribs["RadiusNeighborsRegressor"] = [
        "effective_metric_params_",
        "feature_names_in_" "n_samples_fit_",  # New in version 0.24.
    ]

    # ============================================ 'KNeighborsClassifier', 'RadiusNeighborsClassifier' =========================================

    # --------------------------------------------------
    # KNeighborsClassifier / RadiusNeighborsClassifier Estimation Parameters
    # --------------------------------------------------
    #  n_neighbors : int (default=5) [KNeighborsClassifier ONLY] [NOT RadiusNeighborsClassifier]
    #     Number of neighbors to use by default for kneighbors queries.
    #
    #  radius : float (default=1.0) [RadiusNeighborsClassifier ONLY] [NOT KNeighborsClassifier]
    #     Range of parameter space to use by default for radius_neighbors queries.
    #
    #  weights : str {"uniform", "distance"} or callable (default="uniform")
    #     Weight function used in prediction.
    #     Possible values:
    #        "uniform" : uniform weights. All points in each neighborhood are weighted equally.
    #        "distance" : weight points by the inverse of their distance.
    #                     In this case, closer neighbors of a query point will
    #                     have a greater influence than neighbors which are further away.
    #        [callable] : a user-defined function which accepts an array of distances,
    #                     and returns an array of the same shape containing the weights.
    #     Uniform weights are used by default.
    #
    #  algorithm : str {"auto", "ball_tree", "kd_tree", "brute"} (default="auto")
    #     Algorithm used to compute the nearest neighbors:
    #        "ball_tree" will use BallTree
    #        "kd_tree" will use KDTree
    #        "brute" will use a brute-force search.
    #        "auto" will attempt to decide the most appropriate algorithm
    #           based on the values passed to fit method.
    #     NOTE: fitting on sparse input will override the setting of this parameter, using brute force.
    #
    #  leaf_size : int (default=30)
    #     Leaf size passed to BallTree or KDTree.
    #     This can affect the speed of the construction and query,
    #     as well as the memory required to store the tree.
    #     The optimal value depends on the nature of the problem.
    #
    #  p : integer (default=2)
    #     Power parameter for the Minkowski metric from sklearn.metrics.pairwise.pairwise_distances.
    #     When p = 1, this is equivalent to using manhattan_distance (l1),
    #     and euclidean_distance (l2) for p = 2.
    #     For arbitrary p, minkowski_distance (l_p) is used.
    #
    #  metric : str {"minkowski","precomputed",...} or callable (default="minkowski")
    #
    #     Metric to use for distance computation.
    #     Default is "minkowski", which results in the standard Euclidean distance when p = 2.
    #     See the documentation of scipy.spatial.distance
    #     and the metrics listed in distance_metrics for valid metric values.
    #
    #     If metric is "precomputed", X is assumed to be a distance matrix and must be square during fit.
    #     X may be a sparse graph, in which case only "nonzero" elements may be considered neighbors.
    #
    #     If metric is a callable function, it takes two arrays representing 1D vectors
    #     as inputs and must return one value indicating the distance between those vectors.
    #     This works for Scipy's metrics, but is less efficient than passing the metric name as a string.
    #
    #     Valid metrics (see sklearn/metrics/pairwise.py):
    #        "minkowski", "euclidean", "l2", "l1", "manhattan", "cityblock",
    #        ,"chebyshev", "correlation", "cosine", "haversine"
    #        "seuclidean","sqeuclidean", "wminkowski", "nan_euclidean"
    #        int values only:
    #           "braycurtis", "canberra", "hamming",
    #        boolean values only:
    #           "dice", "jaccard", "kulsinski", "mahalanobis", "matching", "rogerstanimoto",
    #           "russellrao", "sokalmichener", "sokalsneath", "yule"
    #
    #  outlier_labels: {manual label, "most_frequent"}, (default=None) [RadiusNeighborsClassifier ONLY]
    #     Label for outlier samples (samples with no neighbors in given radius).
    #        manual label: str or int label (should be the same type as y) or list of manual labels if multi-output is used.
    #        "most_frequent" : assign the most frequent label of y to outliers.
    #        None : when any outlier is detected, ValueError will be raised.
    #
    #  metric_params : dict (default=None)
    #    Additional keyword arguments for the metric function.
    #
    #  n_jobs : int or None (default=None)
    #    The number of parallel jobs to run for neighbors search.
    #    None means 1 unless in a joblib.parallel_backend context.
    #    -1 means using all processors.
    #    See Glossary for more details.
    # --------------------------------------------------
    # NOTE: NearestNeighbors appears to be a base class for
    #       KNeighborsRegressor, RadiusNeighborsRegressor, KNeighborsClassifier, RadiusNeighborsClassifier
    #   ==> As such, we DO NOT implement NearestNeighbors class here

    # KNeighborsClassifier:
    model_constructor["KNeighborsClassifier"] = KNeighborsClassifier
    model_constructor_name["KNeighborsClassifier"] = "KNeighborsClassifier"
    model_fit_fn_attr_name["KNeighborsClassifier"] = "fit"
    model_predict_fn_attr_name["KNeighborsClassifier"] = "predict"
    model_constructor_arg_defaults["KNeighborsClassifier"] = {
        "n_neighbors": 5,
        "weights": "uniform",
        "algorithm": "auto",
        "leaf_size": 30,
        "p": 2,
        "metric": "minkowski",
        # "outlier_label": None, # DOES NOT APPLY TO KNeighborsClassifier
        "metric_params": None,
        "n_jobs": None,
    }
    model_required_non_cnstr_attribs["KNeighborsClassifier"] = [
        "classes_",
        "effective_metric_",
        "n_features_in_",  # New in version 0.24.
        # "outlier_label_", # DOES NOT APPLY TO KNeighborsClassifier
        "outputs_2d_",
    ]  # <-- "outputs_2d_" attributes only seems to apply to KNeighborsClassifier (not KNeighborsRegressor). Also, 'classes_' attribute does not seem to apply
    # Exclusions:
    # "_fit_X", "_fit_method", "_tree", "_y"
    model_optional_non_cnstr_attribs["KNeighborsClassifier"] = [
        "effective_metric_params_",
        "feature_names_in_",  # New in version 1.0.
        "n_samples_fit_",  # optional since contingent on a fit being performed
    ]

    # RadiusNeighborsClassifier:
    model_constructor["RadiusNeighborsClassifier"] = RadiusNeighborsClassifier
    model_fit_fn_attr_name["RadiusNeighborsClassifier"] = "fit"
    model_predict_fn_attr_name["RadiusNeighborsClassifier"] = "predict"
    model_constructor_arg_defaults["RadiusNeighborsClassifier"] = {
        "radius": 1.0,
        "weights": "uniform",
        "algorithm": "auto",
        "leaf_size": 30,
        "p": 2,
        "metric": "minkowski",
        "outlier_label": None,
        "metric_params": None,
        "n_jobs": None,
    }
    model_required_non_cnstr_attribs["RadiusNeighborsClassifier"] = [
        "classes_",
        "effective_metric_",
        "n_features_in_",  # New in version 0.24.
        "outlier_label_",
        "outputs_2d_",
    ]  # <-- 'outputs_2d_' attributes only seems to apply to KNeighborsClassifier (not KNeighborsClassifier). Also, 'classes_' attribute does not seem to apply
    # Exclusions:
    # "_fit_X", "_fit_method", "_tree", "_y"
    model_optional_non_cnstr_attribs["RadiusNeighborsClassifier"] = [
        "effective_metric_params_",
        "feature_names_in_"  # New in version 1.0.
        "n_samples_fit_",  # optional since contingent on a fit being performed
    ]

    # ============================================ 'NearestCentroid' (Classifier) =========================================

    # --------------------------------------------------
    # NearestCentroid (Classifier) Estimation Parameters
    # --------------------------------------------------
    #  metric : str  or callable (default="euclidean")
    #     Metric to use for distance computation.
    #     Default is "minkowski", which results in the standard Euclidean distance when p = 2.
    #     See the documentation of scipy.spatial.distance
    #     and the metrics listed in distance_metrics for valid metric values.
    #     Note that "wminkowski", "seuclidean" and "mahalanobis" are not supported.
    #
    #     The centroids for the samples corresponding to each class is the point
    #     from which the sum of the distances (according to the metric)
    #     of all samples that belong to that particular class are minimized.
    #     If the "manhattan" metric is provided, this centroid is the median
    #     and for all other metrics, the centroid is now set to be the mean.
    #
    #     Changed in version 0.19: metric="precomputed" was deprecated and now raises an error
    #
    #     Valid metrics for NearestCentroid (see sklearn/metrics/pairwise.py):
    #     ["euclidean", "l2", "l1", "manhattan", "cityblock", "braycurtis",
    #      "canberra", "chebyshev", "correlation", "cosine", "dice", "hamming", "jaccard",
    #      "kulsinski", "mahalanobis", "matching", "minkowski", "rogerstanimoto",
    #      "russellrao", "sokalmichener", "sokalsneath",
    #      "sqeuclidean", "yule", "nan_euclidean", "haversine"]
    #
    #      Invalid metrics for NearestCentroid:
    #         "wminkowski", "seuclidean", "precomputed"
    #
    #  shrink_threshold : float, None (default=None)
    #    Threshold for shrinking centroids to remove features.
    #
    # --------------------------------------------------
    model_constructor["NearestCentroid"] = NearestCentroid
    model_constructor_name["NearestCentroid"] = "NearestCentroid"
    model_fit_fn_attr_name["NearestCentroid"] = "fit"
    model_predict_fn_attr_name["NearestCentroid"] = "predict"
    model_constructor_arg_defaults["NearestCentroid"] = {
        "metric": "euclidean",
        "shrink_threshold": None,
    }
    model_required_non_cnstr_attribs["NearestCentroid"] = [
        "centroids_",
        "classes_",
        "n_features_in_",  # New in version 0.24.
    ]
    model_optional_non_cnstr_attribs["NearestCentroid"] = [
        "feature_names_in_",  # New in version 1.0.
    ]

    # ============================================ SVR (SupportVectorRegressor) =========================================
    # --------------------------------------------------
    # SVR Estimation Parameters
    #
    # kernel : str {"linear", "poly", "rbf", "sigmoid", "precomputed"} or callable (default="rbf")
    #    Specifies the kernel type to be used in the algorithm.
    #    If none is given, "rbf" will be used.
    #    If a callable is given it is used to precompute the kernel matrix.
    #
    # degree : int (default=3)
    #    Degree of the polynomial kernel function ("poly").
    #    Ignored by all other kernels.
    #
    # gamma : str {"scale", "auto"} or float (default="scale")
    #    Kernel coefficient for "rbf", "poly" and "sigmoid".
    #    if gamma="scale" (default) is passed then it uses 1 / (n_features * X.var()) as value of gamma,
    #    if "auto", uses 1 / n_features.
    #
    #    Changed in version 0.22: The default value of gamma changed from "auto" to "scale".
    #
    # coef0 : float (default=0.0)
    #    Independent term in kernel function.
    #    It is only significant in "poly" and "sigmoid".
    #
    # tol : float (default=1e-3)
    #    Tolerance for stopping criterion.
    #
    # C : float (default=1.0)
    #    Regularization parameter.
    #    The strength of the regularization is inversely proportional to C.
    #    Must be strictly positive.
    #    The penalty is a squared l2 penalty.
    #
    # epsilon : float (default=0.1)
    #    Epsilon in the epsilon-SVR model.
    #    It specifies the epsilon-tube within which no penalty is associated in the
    #    training loss function with points predicted within a distance epsilon from the actual value.
    #
    # shrinking : bool (default=True)
    #    Whether to use the shrinking heuristic.
    #    See the User Guide.
    #
    # cache_size : float (default=200)
    #    Specify the size of the kernel cache (in MB).
    #
    # verbose : bool (default=False)
    #    Enable verbose output.
    #    Note that this setting takes advantage of a per-process
    #    runtime setting in libsvm that,
    #    if enabled, may not work properly in a multithreaded context.
    #
    # max_iter : int (default=-1)
    #    Hard limit on iterations within solver, or -1 for no limit.
    # --------------------------------------------------
    model_constructor["SVR"] = SVR
    model_constructor_name["SVR"] = "SVR"
    model_fit_fn_attr_name["SVR"] = "fit"
    model_predict_fn_attr_name["SVR"] = "predict"
    model_constructor_arg_defaults["SVR"] = {
        "kernel": "rbf",
        "degree": 3,
        "gamma": "scale",
        "coef0": 0.0,
        "tol": 1e-3,
        "C": 1.0,
        "epsilon": 0.1,
        "shrinking": True,
        "cache_size": 200,
        "verbose": False,
        "max_iter": -1,
    }
    model_required_non_cnstr_attribs["SVR"] = [
        "class_weight_",
        "dual_coef_",
        "fit_status_",
        "intercept_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
        "n_iter_",  # New in version 1.0. Optional as is contingent on fit being performed (?)
        "n_support_",  # Is this optional (?)
        # "probA_", # post-fit attributes or defunct (?) SVC only not SVR?
        # "probB_", # post-fit attributes or defunct (?) SVC only not SVR?
        "shape_fit_",
        "support_",
        "support_vectors_",
        # "_sparse", NOTE: '_sparse' and 'shape_fit_' are needed by method: BaseLibSVM._validate_for_predict().
        # Old comment... '_dual_coef_', '_intercept_', 'probA_', 'probB_', 'degree', 'coef0', '_gamma', 'cache_size' are needed by BaseLibSVM.predict() method.
        # "shape_fit_", # post-fit attributes or defunct (?)
        # "degree", # post-fit attributes or defunct (?)
        # "coef0", # post-fit attributes or defunct (?)
        # "_gamma", # post-fit attributes or defunct (?)
        # "cache_size", # post-fit attributes or defunct (?)
    ]
    model_optional_non_cnstr_attribs["SVR"] = [
        # "coef_" is actually a class property (formulation), not an assignable/persistable attribute.
        # "coef_", # Only applicable when kernel="linear"
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
        # "n_SV", # post-fit attributes or defunct (?)
        # "_n_samples", # post-fit attributes or defunct (?)
    ]  # <-- Do we need to include this???

    # ============================================ SVC (SupportVectorClassifier) =========================================
    # --------------------------------------------------
    # SVC (Support Vector Classifier) Estimation Parameters
    #
    # C : float (default=1.0)
    #    Regularization parameter.
    #    The strength of the regularization is inversely proportional to C.
    #    Must be strictly positive.
    #    The penalty is a squared l2 penalty.
    #
    # kernel : str {"linear", "poly", "rbf", "sigmoid", "precomputed"} or callable (default="rbf")
    #    Specifies the kernel type to be used in the algorithm.
    #    If none is given, "rbf" will be used.
    #    If a callable is given it is used to pre-compute the kernel matrix from data matrices;
    #    that matrix should be an array of shape (n_samples, n_samples).
    #
    # degree : int (default=3)
    #    Degree of the polynomial kernel function ("poly").
    #    Ignored by all other kernels.
    #
    # gamma : str {"scale", "auto"} or float (default="scale")
    #    Kernel coefficient for "rbf", "poly" and "sigmoid".
    #    if gamma="scale" (default) is passed then it uses 1 / (n_features * X.var()) as value of gamma,
    #    if "auto", uses 1 / n_features.
    #
    #    Changed in version 0.22: The default value of gamma changed from "auto" to "scale".
    #
    # coef0 : float (default=0.0)
    #    Independent term in kernel function.
    #    It is only significant in "poly" and "sigmoid".
    #
    # shrinking : bool (default=True)
    #    Whether to use the shrinking heuristic.
    #    See the User Guide.
    #
    # probability : bool (default=False)
    #    Whether to enable probability estimates.
    #    This must be enabled prior to calling fit, will slow down
    #    that method as it internally uses 5-fold cross-validation,
    #    and predict_proba may be inconsistent with predict.
    #    Read more in the User Guide.
    #
    # tol : float (default=1e-3)
    #    Tolerance for stopping criterion.
    #
    # cache_size : float (default=200)
    #    Specify the size of the kernel cache (in MB).
    #
    # class_weight : dict or "balanced" (default=None)
    #    Set the parameter C of class i to class_weight[i]*C for SVC.
    #    If not given, all classes are supposed to have weight one.
    #    The "balanced" mode uses the values of y to automatically
    #    adjust weights inversely proportional to class frequencies
    #    in the input data as n_samples / (n_classes * np.bincount(y)).
    #
    # verbose : bool (default=False)
    #    Enable verbose output.
    #    Note that this setting takes advantage of a per-process
    #    runtime setting in libsvm that,
    #    if enabled, may not work properly in a multithreaded context.
    #
    # max_iter : int (default=-1)
    #    Hard limit on iterations within solver, or -1 for no limit.
    #
    # decision_function_shape : str {"ovo", "ovr"}, (default="ovr")
    #    Whether to return a one-vs-rest ("ovr") decision function
    #    of shape (n_samples, n_classes) as all other classifiers,
    #    or the original one-vs-one ("ovo") decision function of libsvm
    #    which has shape (n_samples, n_classes * (n_classes - 1) / 2).
    #
    #    However, note that internally, one-vs-one ("ovo") is always used
    #    as a multi-class strategy to train models;
    #    an ovr matrix is only constructed from the ovo matrix.
    #
    #    The parameter is ignored for binary classification.
    #
    #    Changed in version 0.19: decision_function_shape is "ovr" by default.
    #    New in version 0.17: decision_function_shape="ovr" is recommended.
    #    Changed in version 0.17: Deprecated decision_function_shape="ovo" and None.
    #
    # break_ties : bool (default=False)
    #    If true, decision_function_shape="ovr", and number of classes > 2,
    #    predict will break ties according to the confidence values of decision_function;
    #    otherwise the first class among the tied classes is returned.
    #    Please note that breaking ties comes at a relatively high
    #    computational cost compared to a simple predict.
    #
    #    New in version 0.22.
    #
    # random_state: int, RandomState instance, None (default=None)
    #     Controls the pseudo random number generation
    #     for shuffling the data for probability estimates.
    #     Ignored when probability is False.
    #     Pass an int for reproducible output across multiple function calls.
    #     See Glossary.
    #
    #     If None (default):
    #        Use the global random state instance from numpy.random.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #     If int:
    #        Use a new random number generator seeded by the given integer.
    #        Using an int will produce the same results across different calls.
    #        However, it may be worthwhile checking that your results
    #        are stable across a number of different distinct random seeds.
    #        Popular integer random seeds are 0 and 42.
    #        Integer values must be in the range [0, 2**32 - 1].
    #
    #     If RandomState instance:
    #        Use the provided random state, only affecting other users
    #        of that same random state instance.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    # --------------------------------------------------
    model_constructor["SVC"] = SVC
    model_constructor_name["SVC"] = "SVC"
    model_fit_fn_attr_name["SVC"] = "fit"
    model_predict_fn_attr_name["SVC"] = "predict"
    model_constructor_arg_defaults["SVC"] = {
        "C": 1.0,
        "kernel": "rbf",
        "degree": 3,
        "gamma": "scale",
        "coef0": 0.0,
        "shrinking": True,
        "probability": False,
        "tol": 1e-3,
        "cache_size": 200,
        "class_weight": None,
        "verbose": False,
        "max_iter": -1,
        "decision_function_shape": "ovr",
        "break_ties": False,
        "random_state": None,
    }
    model_required_non_cnstr_attribs["SVC"] = [
        "class_weight_",
        "classes_",
        "dual_coef_",
        "fit_status_",
        "intercept_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
        "n_iter_",  # New in version 1.0. Optional as is contingent on fit being performed (?)
        "support_",
        "support_vectors_",
        "n_support_",  # Is this optional (?)
        "probA_",
        "probB_",
        "shape_fit_",
        # "_sparse", NOTE: '_sparse' and 'shape_fit_' are needed by method: BaseLibSVM._validate_for_predict().
        # Old comment... '_dual_coef_', '_intercept_', 'probA_', 'probB_', 'degree', 'coef0', '_gamma', 'cache_size' are needed by BaseLibSVM.predict() method.
        # "shape_fit_", # post-fit attributes or defunct (?)
        # "degree", # post-fit attributes or defunct (?)
        # "coef0", # post-fit attributes or defunct (?)
        # "_gamma", # post-fit attributes or defunct (?)
        # "cache_size", # post-fit attributes or defunct (?)
    ]
    model_optional_non_cnstr_attribs["SVC"] = [
        # "coef_" is actually a class property (formulation), not an assignable/persistable attribute.
        # "coef_", # Only applicable when kernel="linear"
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
        # "n_SV", # post-fit attributes or defunct (?)
        # "_n_samples", # post-fit attributes or defunct (?)
    ]  # <-- Do we need to include this???

    # ============================================ NuSVR (NuSupportVectorRegressor) =========================================
    # --------------------------------------------------
    # NuSVR Estimation Parameters
    #
    # nu : float (default=0.5)
    #    An upper bound on the fraction of training errors
    #    and a lower bound of the fraction of support vectors.
    #    Should be in the interval (0, 1].
    #    By default 0.5 will be taken.
    #
    # C : float (default=1.0)
    #    Penalty parameter C of the error term.
    #
    # kernel : str {"linear", "poly", "rbf", "sigmoid", "precomputed"} or callable, (default="rbf")
    #    Specifies the kernel type to be used in the algorithm.
    #    It must be one of "linear", "poly", "rbf", "sigmoid", "precomputed" or a callable.
    #    If none is given, "rbf" will be used.
    #    If a callable is given it is used to precompute the kernel matrix.
    #
    # degree : int (default=3)
    #    Degree of the polynomial kernel function ("poly").
    #    Ignored by all other kernels.
    #
    # gamma : str {"scale", "auto"} or float (default="scale")
    #    Kernel coefficient for "rbf", "poly" and "sigmoid".
    #    if gamma="scale" (default) is passed then it uses 1 / (n_features * X.var()) as value of gamma,
    #    if "auto", uses 1 / n_features.
    #
    #    Changed in version 0.22: The default value of gamma changed from "auto" to "scale".
    #
    # coef0 : float (default=0.0)
    #    Independent term in kernel function.
    #    It is only significant in "poly" and "sigmoid".
    #
    # shrinking : bool (default=True)
    #    Whether to use the shrinking heuristic.
    #    See the User Guide.
    #
    # tol : float (default=1e-3)
    #    Tolerance for stopping criterion.
    #
    # cache_size : float (default=200)
    #    Specify the size of the kernel cache (in MB).
    #
    # verbose : bool, default: False
    #    Enable verbose output.
    #    Note that this setting takes advantage of a per-process runtime setting
    #    in libsvm that, if enabled, may not work properly in a multithreaded context.
    #
    # max_iter : int (default=-1)
    #    Hard limit on iterations within solver, or -1 for no limit.
    #
    # --------------------------------------------------
    model_constructor["NuSVR"] = NuSVR
    model_constructor_name["NuSVR"] = "NuSVR"
    model_fit_fn_attr_name["NuSVR"] = "fit"
    model_predict_fn_attr_name["NuSVR"] = "predict"
    model_constructor_arg_defaults["NuSVR"] = {
        "nu": 0.5,
        "C": 1.0,
        "kernel": "rbf",
        "degree": 3,
        "gamma": "scale",
        "coef0": 0.0,
        "shrinking": True,
        "tol": 1e-3,
        "cache_size": 200,
        "verbose": False,
        "max_iter": -1,
    }
    model_required_non_cnstr_attribs["NuSVR"] = [
        "class_weight_",
        "dual_coef_",
        "fit_status_",
        "intercept_",
        "n_features_in_",  # New in version 0.24.
        "n_iter_",  # New in version 1.1.
        "n_support_",  # Is this optional (?)
        "shape_fit_",
        "support_",
        "support_vectors_",
        # "probA_",
        # "probB_",
        # NOTE: "_sparse" and "shape_fit_" are needed by method: BaseLibSVM._validate_for_predict().
        # "_sparse",
        # "shape_fit_"
        # Old comment..."dual_coef_", "intercept_", "probA_", "probB_", "degree", "coef0", "_gamma", "cache_size" are needed by BaseLibSVM.predict() method.
        # "degree",
        # "coef0",
        # "_gamma",
        # "cache_size",
    ]
    model_optional_non_cnstr_attribs["NuSVR"] = [
        # "coef_" is actually a class property (formulation), not an assignable/persistable attribute.
        # "coef_", # Only applicable when kernel="linear"
        "features_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
        # "n_SV", # post-fit attributes or defunct (?)
        # "_n_samples", # post-fit attributes or defunct (?)
    ]  # <-- Do we need to include this???

    # ============================================ NuSVC (NuSupportVectorClassifier) =========================================
    # --------------------------------------------------
    # NuSVC Estimation Parameters
    #
    # nu : float (default=0.5)
    #    An upper bound on the fraction of training errors
    #    and a lower bound of the fraction of support vectors.
    #    Should be in the interval (0, 1].
    #
    # kernel : str {"linear", "poly", "rbf", "sigmoid", "precomputed"} or callable, (default="rbf")
    #    Specifies the kernel type to be used in the algorithm.
    #    It must be one of "linear", "poly", "rbf", "sigmoid", "precomputed" or a callable.
    #    If none is given, "rbf" will be used.
    #    If a callable is given it is used to precompute the kernel matrix.
    #
    # degree : int (default=3)
    #    Degree of the polynomial kernel function ("poly").
    #    Ignored by all other kernels.
    #
    # gamma : str {"scale", "auto"} or float (default="scale")
    #    Kernel coefficient for "rbf", "poly" and "sigmoid".
    #    if gamma="scale" (default) is passed then it uses 1 / (n_features * X.var()) as value of gamma,
    #    if "auto", uses 1 / n_features.
    #
    #    Changed in version 0.22: The default value of gamma changed from "auto" to "scale".
    #
    # coef0 : float (default=0.0)
    #    Independent term in kernel function.
    #    It is only significant in "poly" and "sigmoid".
    #
    # shrinking : bool (default=True)
    #    Whether to use the shrinking heuristic.
    #    See the User Guide.
    #
    # probability : bool (default=False)
    #    Whether to enable probability estimates.
    #    This must be enabled prior to calling fit, will slow down
    #    that method as it internally uses 5-fold cross-validation,
    #    and predict_proba may be inconsistent with predict.
    #    Read more in the User Guide.
    #
    # tol : float (default=1e-3)
    #    Tolerance for stopping criterion.
    #
    # cache_size : float (default=200)
    #    Specify the size of the kernel cache (in MB).
    #
    # class_weight : dict or "balanced" (default=None)
    #    Set the parameter C of class i to class_weight[i]*C for SVC.
    #    If not given, all classes are supposed to have weight one.
    #    The "balanced" mode uses the values of y to automatically
    #    adjust weights inversely proportional to class frequencies
    #    in the input data as n_samples / (n_classes * np.bincount(y)).
    #
    # verbose : bool (default=False)
    #    Enable verbose output.
    #    Note that this setting takes advantage of a per-process runtime setting
    #    in libsvm that, if enabled, may not work properly in a multithreaded context.
    #
    # max_iter : int (default=-1)
    #    Hard limit on iterations within solver, or -1 for no limit.
    #
    # decision_function_shape : str {"ovo", "ovr"}, (default="ovr")
    #   Whether to return a one-vs-rest ("ovr") decision function of shape
    #   (n_samples, n_classes) as all other classifiers,
    #   or the original one-vs-one ("ovo") decision function of libsvm
    #   which has shape (n_samples, n_classes * (n_classes - 1) / 2).
    #
    #   However, one-vs-one ("ovo") is always used as multi-class strategy.
    #   The parameter is ignored for binary classification.
    #
    #    Changed in version 0.19: decision_function_shape is "ovr" by default.
    #    New in version 0.17: decision_function_shape="ovr" is recommended.
    #    Changed in version 0.17: Deprecated decision_function_shape="ovo" and None.
    #
    # break_ties : bool (default=False)
    #    If true, decision_function_shape="ovr", and number of classes > 2,
    #    predict will break ties according to the confidence values of decision_function;
    #    otherwise the first class among the tied classes is returned.
    #    Please note that breaking ties comes at a relatively high
    #    computational cost compared to a simple predict.
    #
    #    New in version 0.22.
    #
    # random_state: int, RandomState instance, None (default=None)
    #     Controls the pseudo random number generation
    #     for shuffling the data for probability estimates.
    #     Ignored when probability is False.
    #     Pass an int for reproducible output across multiple function calls.
    #     See Glossary.
    #
    #     If None (default):
    #        Use the global random state instance from numpy.random.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    #     If int:
    #        Use a new random number generator seeded by the given integer.
    #        Using an int will produce the same results across different calls.
    #        However, it may be worthwhile checking that your results
    #        are stable across a number of different distinct random seeds.
    #        Popular integer random seeds are 0 and 42.
    #        Integer values must be in the range [0, 2**32 - 1].
    #
    #     If RandomState instance:
    #        Use the provided random state, only affecting other users
    #        of that same random state instance.
    #        Calling the function multiple times will reuse the same instance,
    #        and will produce different results.
    #
    # --------------------------------------------------
    model_constructor["NU_SVC"] = NuSVC
    model_constructor_name["NuSVC"] = "NuSVC"
    model_fit_fn_attr_name["NU_SVC"] = "fit"
    model_predict_fn_attr_name["NU_SVC"] = "predict"
    model_constructor_arg_defaults["NU_SVC"] = {
        "nu": 0.5,
        "kernel": "rbf",
        "degree": 3,
        "gamma": "scale",
        "coef0": 0.0,
        "shrinking": True,
        "probability": False,
        "tol": 1e-3,
        "cache_size": 200,
        "class_weight": None,
        "verbose": False,
        "max_iter": -1,
        "decision_function_shape": "ovr",
        "break_ties": False,
        "random_state": None,
    }
    model_required_non_cnstr_attribs["NU_SVC"] = [
        "class_weight_",
        "classes_",
        "dual_coef_",
        "fit_status_",
        "intercept_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
        "n_iter_",  # New in version 1.0. Optional as is contingent on fit being performed (?)
        "support_",
        "support_vectors_",
        "n_support_",  # Is this optional (?)
        "probA_",
        "probB_",
        "shape_fit_",
        # "_sparse", NOTE: '_sparse' and 'shape_fit_' are needed by method: BaseLibSVM._validate_for_predict().
        # Old comment... '_dual_coef_', '_intercept_', 'probA_', 'probB_', 'degree', 'coef0', '_gamma', 'cache_size' are needed by BaseLibSVM.predict() method.
        # "shape_fit_", # post-fit attributes or defunct (?)
        # "degree", # post-fit attributes or defunct (?)
        # "coef0", # post-fit attributes or defunct (?)
        # "_gamma", # post-fit attributes or defunct (?)
        # "cache_size", # post-fit attributes or defunct (?)
    ]
    model_optional_non_cnstr_attribs["NU_SVC"] = [
        # "coef_" is actually a class property (formulation), not an assignable/persistable attribute.
        # "coef_", # Only applicable when kernel="linear"
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
        # "n_SV", # post-fit attributes or defunct (?)
        # "_n_samples", # post-fit attributes or defunct (?)
    ]  # <-- Do we need to include this???

    # ============================================ LinearSVR (LinearSupportVectorRegressor) =========================================
    # --------------------------------------------------
    # LinearSVR Estimation Parameters
    #
    # epsilon : float (default=0.0)
    #    Epsilon parameter in the epsilon-insensitive loss function.
    #    Note that the value of this parameter depends on the scale of the target variable y.
    #    If unsure, set epsilon=0.
    #
    # tol : float (default=1e-4)
    #    Tolerance for stopping criteria.
    #
    # C : float (default=1.0)
    #    Regularization parameter.
    #    The strength of the regularization is inversely proportional to C.
    #    Must be strictly positive.
    #
    # loss : str {"epsilon_insensitive", "squared_epsilon_insensitive"} (default="epsilon_insensitive")
    #    Specifies the loss function.
    #    The epsilon-insensitive loss (standard SVR) is the L1 loss,
    #    while the squared epsilon-insensitive loss
    #    ("squared_epsilon_insensitive") is the L2 loss.
    #
    # fit_intercept : bool (default=True)
    #    Whether to calculate the intercept for this model.
    #    If set to false, no intercept will be used in calculations
    #    (i.e. data is expected to be already centered).
    #
    # intercept_scaling : float (default=1.0)
    #    When self.fit_intercept is True,
    #    instance vector x becomes [x, self.intercept_scaling],
    #    i.e. a "synthetic" feature with constant value equals
    #    to intercept_scaling is appended to the instance vector.
    #
    #    The intercept becomes intercept_scaling * synthetic feature weight
    #    NOTE: the synthetic feature weight is subject to l1/l2 regularization as all other features.
    #    To lessen the effect of regularization on synthetic feature weight
    #    (and therefore on the intercept) intercept_scaling has to be increased.
    #
    # dual : bool (default=True)
    #    Select the algorithm to either solve
    #    the dual or primal optimization problem.
    #    Prefer dual=False when n_samples > n_features.
    #
    # verbose : int (default=0)
    #    Enable verbose output.
    #    Note that this setting takes advantage of a per-process
    #    runtime setting in liblinear that, if enabled,
    #    may not work properly in a multithreaded context.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Controls the pseudo random number generation for shuffling the data.
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    # max_iter : int (default=1000)
    #    The maximum number of iterations to be run.
    # --------------------------------------------------
    model_constructor["LinearSVR"] = LinearSVR
    model_constructor_name["LinearSVR"] = "LinearSVR"
    model_fit_fn_attr_name["LinearSVR"] = "fit"
    model_predict_fn_attr_name["LinearSVR"] = "predict"
    model_constructor_arg_defaults["LinearSVR"] = {
        "epsilon": 0.0,
        "tol": 1e-4,
        "C": 1.0,
        "loss": "epsilon_insensitive",
        "fit_intercept": True,
        "intercept_scaling": 1.0,
        "dual": True,
        "verbose": 0,
        "random_state": None,
        "max_iter": 1000,
    }
    model_required_non_cnstr_attribs["LinearSVR"] = [
        "coef_",
        "intercept_",
        "n_features_in_",  # New in version 0.24.
        "n_iter_",
    ]
    model_optional_non_cnstr_attribs["LinearSVR"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
        # "n_classes", # post-fit attributes or defunct (?)
        # "_n_samples", # post-fit attributes or defunct (?)
    ]  # <-- Do we need to include this???

    # ============================================ LinearSVC (LinearSupportVectorClassifier) =========================================
    # --------------------------------------------------
    # LinearSVC Estimation Parameters
    #
    # penalty : str {"l1", "l2"} (default="l2")
    #    Specifies the norm used in the penalization.
    #    The "l2" penalty is the standard used in SVC.
    #    The "l1" leads to coef_ vectors that are sparse.
    #
    # loss : str {"hinge", "squared_hinge"} (default="squared_hinge")
    #    Specifies the loss function. "hinge" is the standard SVM loss
    #    (used e.g. by the SVC class) while "squared_hinge" is the square of the hinge loss.
    #    The combination of penalty="l1" and loss="hinge" is not supported.
    #
    # dual : bool (default=True)
    #    Select the algorithm to either solve the dual or primal optimization problem.
    #    Prefer dual=False when n_samples > n_features.
    #
    # tol : float (default=1e-4)
    #    Tolerance for stopping criteria.
    #
    # C : float (default=1.0)
    #    Regularization parameter.
    #    The strength of the regularization is inversely proportional to C.
    #    Must be strictly positive.
    #
    # multi_class : str {"ovr", "crammer_singer"} (default="ovr")
    #    Determines the multi-class strategy if y contains more than two classes.
    #    "ovr" trains n_classes one-vs-rest classifiers,
    #    while "crammer_singer" optimizes a joint objective over all classes.
    #
    #    While crammer_singer is interesting from a theoretical perspective
    #    as it is consistent, it is seldom used in practice as it rarely
    #    leads to better accuracy and is more expensive to compute.
    #
    #    If "crammer_singer" is chosen, the options loss, penalty and dual will be ignored.
    #
    # fit_intercept : bool (default=True)
    #    Whether to calculate the intercept for this model.
    #    If set to false, no intercept will be used in calculations
    #    (i.e. data is expected to be already centered).
    #
    # intercept_scaling : float (default=1.0)
    #    When self.fit_intercept is True,
    #    instance vector x becomes [x, self.intercept_scaling],
    #    i.e. a "synthetic" feature with constant value equals
    #    to intercept_scaling is appended to the instance vector.
    #
    #    The intercept becomes intercept_scaling * synthetic feature weight
    #    NOTE: the synthetic feature weight is subject to l1/l2 regularization as all other features.
    #    To lessen the effect of regularization on synthetic feature weight
    #    (and therefore on the intercept) intercept_scaling has to be increased.
    #
    # class_weight : dict or "balanced" (default=None)
    #    Set the parameter C of class i to class_weight[i]*C for SVC.
    #    If not given, all classes are supposed to have weight one.
    #    The "balanced" mode uses the values of y to automatically
    #    adjust weights inversely proportional to class frequencies
    #    in the input data as n_samples / (n_classes * np.bincount(y)).
    #
    # verbose : int (default=0)
    #    Enable verbose output.
    #    Note that this setting takes advantage of a per-process
    #    runtime setting in liblinear that, if enabled,
    #    may not work properly in a multithreaded context.
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Controls the pseudo random number generation for shuffling
    #    the data for the dual coordinate descent (if dual=True).
    #
    #    When dual=False the underlying implementation of LinearSVC
    #    is not random and random_state has no effect on the results.
    #
    #    Pass an int for reproducible output across multiple function calls.
    #    See Glossary.
    #
    # max_iter : int (default=1000)
    #    The maximum number of iterations to be run.
    # --------------------------------------------------
    model_constructor["LinearSVC"] = LinearSVC
    model_constructor_name["LinearSVC"] = "LinearSVC"
    model_fit_fn_attr_name["LinearSVC"] = "fit"
    model_predict_fn_attr_name["LinearSVC"] = "predict"
    model_constructor_arg_defaults["LinearSVC"] = {
        "penalty": "l2",
        "loss": "squared_hinge",
        "dual": True,
        "tol": 1e-4,
        "C": 1.0,
        "multi_class": "ovr",
        "fit_intercept": True,
        "intercept_scaling": 1.0,
        "class_weight": None,
        "verbose": 0,
        "random_state": None,
        "max_iter": 1000,
    }
    model_required_non_cnstr_attribs["LinearSVC"] = [
        "coef_",
        "intercept_",
        "classes_",
        "n_features_in_",  # New in version 0.24.
        "n_iter_",
    ]
    model_optional_non_cnstr_attribs["LinearSVC"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
        # "n_classes", # post-fit attributes or defunct (?)
        # "_n_samples", # post-fit attributes or defunct (?)
    ]  # <-- Do we need to include this???

    # ============================================ MLPRegressor =========================================
    # --------------------------------------------------
    # MLP (MultiLayerPerceptron) Estimation Parameters
    #
    #
    # hidden_layer_sizes : tuple, length = n_layers - 2, (default=(100,))
    #    The ith element represents the number of neurons in the ith hidden layer.
    #
    # activation : {"identity", "logistic", "tanh", "relu"} (default="relu")
    #    Activation function for the hidden layer.
    #
    #       "identity", no-op activation, useful to implement linear bottleneck, returns f(x) = x
    #       "logistic", the logistic sigmoid function, returns f(x) = 1 / (1 + exp(-x)).
    #       "tanh", the hyperbolic tan function, returns f(x) = tanh(x).
    #       "relu", the rectified linear unit function, returns f(x) = max(0, x)
    #
    # solver : str {"lbfgs", "sgd", "adam"} (default="adam")
    #    The solver for weight optimization.
    #
    #       "lbfgs" is an optimizer in the family of quasi-Newton methods.
    #       "sgd" refers to stochastic gradient descent.
    #       "adam" refers to a stochastic gradient-based optimizer
    #          proposed by Kingma, Diederik, and Jimmy Ba
    #
    #    NOTE: The default solver "adam" works pretty well on relatively
    #          large datasets (with thousands of training samples or more)
    #          in terms of both training time and validation score.
    #
    #    For small datasets, however, "lbfgs" can converge faster and perform better.
    #
    # alpha : float (default 0.0001)
    #    Strength of the L2 regularization term.
    #    The L2 regularization term is divided by the sample size when added to the loss.
    #
    # batch_size : int (default "auto")
    #    Size of minibatches for stochastic optimizers.
    #    If the solver is "lbfgs", the classifier will not use minibatch.
    #    When set to "auto", batch_size=min(200, n_samples)
    #
    # learning_rate : str {"constant", "invscaling", "adaptive"} (default="constant")
    #    Learning rate schedule for weight updates.
    #
    #       "constant" is a constant learning rate given by "learning_rate_init".
    #       "invscaling" gradually decreases the learning rate learning_rate_
    #          at each time step 't' using an inverse scaling exponent of "power_t".
    #          effective_learning_rate = learning_rate_init / pow(t, power_t)
    #       "adaptive" keeps the learning rate constant to 'learning_rate_init'
    #          as long as training loss keeps decreasing.
    #          Each time two consecutive epochs fail to decrease training loss by at least tol,
    #          or fail to increase validation score by at least tol
    #          if "early_stopping" is on, the current learning rate is divided by 5.
    #
    #    Only used when solver="sgd".
    #
    # learning_rate_init : double (default=0.001)
    #    The initial learning rate used.
    #    It controls the step-size in updating the weights.
    #    Only used when solver="sgd" or "adam".
    #
    # power_t : double (default=0.5)
    #    The exponent for inverse scaling learning rate.
    #    It is used in updating effective learning rate
    #    when the learning_rate is set to "invscaling".
    #    Only used when solver="sgd".
    #
    # max_iter : int (default=200)
    #    Maximum number of iterations.
    #    The solver iterates until convergence (determined by "tol") or this number of iterations.
    #    For stochastic solvers ("sgd", "adam"), note that this determines
    #    the number of epochs (how many times each data point will be used),
    #    not the number of gradient steps.
    #
    # shuffle : bool (default=True)
    #    Whether to shuffle samples in each iteration.
    #    Only used when solver="sgd" or "adam".
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Determines random number generation for weights and bias initialization,
    #    train-test split if early stopping is used,
    #    and batch sampling when solver="sgd" or "adam".
    #
    #    Pass an int for reproducible results across multiple function calls.
    #
    #    See Glossary.
    #
    # tol : float (default=1e-4)
    #    Tolerance for the optimization.
    #    When the loss or score is not improving by at least tol
    #    for n_iter_no_change consecutive iterations,
    #    unless learning_rate is set to "adaptive",
    #    convergence is considered to be reached and training stops.
    #
    # verbose : bool (default=False)
    #    Whether to print progress messages to stdout.
    #
    # warm_start : bool (default=False)
    #    When set to True, reuse the solution of the previous call
    #    to fit as initialization, otherwise, just erase the previous solution.
    #    See the Glossary.
    #
    # momentum : float (default=0.9)
    #    Momentum for gradient descent update.
    #    Should be between 0 and 1.
    #    Only used when solver="sgd".
    #
    # nesterovs_momentum : bool (default=True)
    #    Whether to use Nesterov's momentum.
    #    Only used when solver="sgd" and momentum > 0.
    #
    # early_stopping : bool (default=False)
    #    Whether to use early stopping to terminate training
    #    when validation score is not improving.
    #
    #    If set to true, it will automatically set aside 10% of training data
    #    as validation and terminate training when validation score
    #    is not improving by at least tol for n_iter_no_change consecutive epochs.
    #
    #    Only effective when solver="sgd" or "adam"
    #
    # validation_fraction : float (default=0.1)
    #    The proportion of training data to set aside
    #    as validation set for early stopping.
    #    Must be between 0 and 1.
    #    Only used if early_stopping is True.
    #
    # beta_1 : float (default=0.9)
    #    Exponential decay rate for estimates of first moment vector in adam,
    #    should be in [0, 1).
    #    Only used when solver="adam"
    #
    # beta_2 : float (default=0.999)
    #    Exponential decay rate for estimates of second moment vector in adam,
    #    should be in [0, 1).
    #    Only used when solver="adam"
    #
    # epsilon : float (default=1e-8)
    #    Value for numerical stability in adam.
    #    Only used when solver="adam"
    #
    # n_iter_no_change : int (default=10)
    #    Maximum number of epochs to not meet tol improvement.
    #    Only effective when solver="sgd" or "adam"
    #    New in version 0.20.
    #
    # max_fun : int (default=15000)
    #    Only used when solver="lbfgs".
    #    Maximum number of function calls.
    #    The solver iterates until convergence (determined by "tol"),
    #    number of iterations reaches max_iter, or this number of function calls.
    #    Note that number of function calls will be greater than or equal to
    #    the number of iterations for the MLPRegressor.
    #    New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["MLPRegressor"] = MLPRegressor
    model_constructor_name["MLPRegressor"] = "MLPRegressor"
    model_fit_fn_attr_name["MLPRegressor"] = "fit"
    model_predict_fn_attr_name["MLPRegressor"] = "predict"
    model_constructor_arg_defaults["MLPRegressor"] = {
        "hidden_layer_sizes": (100,),
        "activation": "relu",
        "solver": "adam",
        "alpha": 0.0001,
        "batch_size": "auto",
        "learning_rate": "constant",
        "learning_rate_init": 0.001,
        "power_t": 0.5,
        "max_iter": 200,
        "shuffle": True,
        "random_state": None,
        "tol": 1e-4,
        "verbose": False,
        "warm_start": False,
        "momentum": 0.9,
        "nesterovs_momentum": True,
        "early_stopping": False,
        "validation_fraction": 0.1,
        "beta_1": 0.9,
        "beta_2": 0.999,
        "epsilon": 1e-8,
        "n_iter_no_change": 10,
        "max_fun": 15000,
    }
    model_required_non_cnstr_attribs["MLPRegressor"] = [
        "loss_",
        "loss_curve_",
        "coefs_",
        "intercepts_",
        "n_features_in_",  # New in version 0.24.
        "n_iter_",
        "n_layers_",
        "n_outputs_",
        "out_activation_",
    ]
    model_optional_non_cnstr_attribs["MLPRegressor"] = [
        "best_loss_",  # post-training attrribute (?)
        "t_",  # post-training attrribute (?)
        "feature_names_in_",  # Defined only when X has feature names that are all strings. New in version 1.0.
        # "_n_samples",
    ]  # <-- Do we need to include these???

    # ============================================ MLPClassifier =========================================
    # --------------------------------------------------
    # MLP Classifier (MultiLayerPerceptron) Classifier Estimation Parameters
    #
    #
    # hidden_layer_sizes : tuple, length = n_layers - 2, (default=(100,))
    #    The ith element represents the number of neurons in the ith hidden layer.
    #
    # activation : {"identity", "logistic", "tanh", "relu"} (default="relu")
    #    Activation function for the hidden layer.
    #
    #       "identity", no-op activation, useful to implement linear bottleneck, returns f(x) = x
    #       "logistic", the logistic sigmoid function, returns f(x) = 1 / (1 + exp(-x)).
    #       "tanh", the hyperbolic tan function, returns f(x) = tanh(x).
    #       "relu", the rectified linear unit function, returns f(x) = max(0, x)
    #
    # solver : str {"lbfgs", "sgd", "adam"} (default="adam")
    #    The solver for weight optimization.
    #
    #       "lbfgs" is an optimizer in the family of quasi-Newton methods.
    #       "sgd" refers to stochastic gradient descent.
    #       "adam" refers to a stochastic gradient-based optimizer
    #          proposed by Kingma, Diederik, and Jimmy Ba
    #
    #    NOTE: The default solver "adam" works pretty well on relatively
    #          large datasets (with thousands of training samples or more)
    #          in terms of both training time and validation score.
    #
    #    For small datasets, however, "lbfgs" can converge faster and perform better.
    #
    # alpha : float (default=0.0001)
    #    Strength of the L2 regularization term.
    #    The L2 regularization term is divided by the sample size when added to the loss.
    #
    # batch_size : int (default="auto")
    #    Size of minibatches for stochastic optimizers.
    #    If the solver is "lbfgs", the classifier will not use minibatch.
    #    When set to "auto", batch_size=min(200, n_samples)
    #
    # learning_rate : str {"constant", "invscaling", "adaptive"} (default="constant")
    #    Learning rate schedule for weight updates.
    #
    #       "constant" is a constant learning rate given by "learning_rate_init".
    #       "invscaling" gradually decreases the learning rate learning_rate_
    #          at each time step 't' using an inverse scaling exponent of "power_t".
    #          effective_learning_rate = learning_rate_init / pow(t, power_t)
    #       "adaptive" keeps the learning rate constant to 'learning_rate_init'
    #          as long as training loss keeps decreasing.
    #          Each time two consecutive epochs fail to decrease training loss by at least tol,
    #          or fail to increase validation score by at least tol
    #          if "early_stopping" is on, the current learning rate is divided by 5.
    #
    #    Only used when solver="sgd".
    #
    # learning_rate_init : double (default=0.001)
    #    The initial learning rate used.
    #    It controls the step-size in updating the weights.
    #    Only used when solver="sgd" or "adam".
    #
    # power_t : double (default=0.5)
    #    The exponent for inverse scaling learning rate.
    #    It is used in updating effective learning rate
    #    when the learning_rate is set to "invscaling".
    #    Only used when solver="sgd".
    #
    # max_iter : int (default=200)
    #    Maximum number of iterations.
    #    The solver iterates until convergence (determined by "tol") or this number of iterations.
    #    For stochastic solvers ("sgd", "adam"), note that this determines
    #    the number of epochs (how many times each data point will be used),
    #    not the number of gradient steps.
    #
    # shuffle : bool (default=True)
    #    Whether to shuffle samples in each iteration.
    #    Only used when solver="sgd" or "adam".
    #
    # random_state : int, RandomState instance or None (default=None)
    #    Determines random number generation for weights and bias initialization,
    #    train-test split if early stopping is used,
    #    and batch sampling when solver="sgd" or "adam".
    #
    #    Pass an int for reproducible results across multiple function calls.
    #
    #    See Glossary.
    #
    # tol : float (default=1e-4)
    #    Tolerance for the optimization.
    #    When the loss or score is not improving by at least tol
    #    for n_iter_no_change consecutive iterations,
    #    unless learning_rate is set to "adaptive",
    #    convergence is considered to be reached and training stops.
    #
    # verbose : bool (default=False)
    #    Whether to print progress messages to stdout.
    #
    # warm_start : bool (default=False)
    #    When set to True, reuse the solution of the previous call
    #    to fit as initialization, otherwise, just erase the previous solution.
    #    See the Glossary.
    #
    # momentum : float (default=0.9)
    #    Momentum for gradient descent update.
    #    Should be between 0 and 1.
    #    Only used when solver="sgd".
    #
    # nesterovs_momentum : bool (default=True)
    #    Whether to use Nesterov's momentum.
    #    Only used when solver="sgd" and momentum > 0.
    #
    # early_stopping : bool (default=False)
    #    Whether to use early stopping to terminate training
    #    when validation score is not improving.
    #
    #    If set to true, it will automatically set aside 10% of training data
    #    as validation and terminate training when validation score
    #    is not improving by at least tol for n_iter_no_change consecutive epochs.
    #
    #    The split is stratified, except in a multilabel setting.
    #    If early stopping is False, then the training stops when
    #    the training loss does not improve by more than tol
    #    for n_iter_no_change consecutive passes over the training set.
    #
    #    Only effective when solver="sgd" or "adam"
    #
    # validation_fraction : float (default=0.1)
    #    The proportion of training data to set aside
    #    as validation set for early stopping.
    #    Must be between 0 and 1.
    #    Only used if early_stopping is True.
    #
    # beta_1 : float (default=0.9)
    #    Exponential decay rate for estimates of first moment vector in adam,
    #    should be in [0, 1).
    #    Only used when solver="adam"
    #
    # beta_2 : float (default=0.999)
    #    Exponential decay rate for estimates of second moment vector in adam,
    #    should be in [0, 1).
    #    Only used when solver="adam"
    #
    # epsilon : float (default=1e-8)
    #    Value for numerical stability in adam.
    #    Only used when solver="adam"
    #
    # n_iter_no_change : int (default=10)
    #    Maximum number of epochs to not meet tol improvement.
    #    Only effective when solver="sgd" or "adam"
    #    New in version 0.20.
    #
    # max_fun : int (default=15000)
    #    Only used when solver="lbfgs".
    #    Maximum number of function calls.
    #    The solver iterates until convergence (determined by "tol"),
    #    number of iterations reaches max_iter, or this number of function calls.
    #    Note that number of function calls will be greater than or equal to
    #    the number of iterations for the MLPClassifier.
    #    New in version 0.22.
    #
    # --------------------------------------------------
    model_constructor["MLPClassifier"] = MLPClassifier
    model_constructor_name["MLPClassifier"] = "MLPClassifier"
    model_fit_fn_attr_name["MLPClassifier"] = "fit"
    model_predict_fn_attr_name["MLPClassifier"] = "predict"
    model_constructor_arg_defaults["MLPClassifier"] = {
        "hidden_layer_sizes": (100,),
        "activation": "relu",
        "solver": "adam",
        "alpha": 0.0001,
        "batch_size": "auto",
        "learning_rate": "constant",
        "learning_rate_init": 0.001,
        "power_t": 0.5,
        "max_iter": 200,
        "shuffle": True,
        "random_state": None,
        "tol": 1e-4,
        "verbose": False,
        "warm_start": False,
        "momentum": 0.9,
        "nesterovs_momentum": True,
        "early_stopping": False,
        "validation_fraction": 0.1,
        "beta_1": 0.9,
        "beta_2": 0.999,
        "epsilon": 1e-8,
        "n_iter_no_change": 10,
        "max_fun": 15000,
    }
    model_required_non_cnstr_attribs["MLPClassifier"] = [
        "classes_",
        "loss_",
        "loss_curve_",
        "coefs_",
        "intercepts_",
        "n_features_in_",  # New in version 0.24.
        "n_iter_",
        "n_layers_",
        "n_outputs_",
        "out_activation_",
    ]
    model_optional_non_cnstr_attribs["MLPClassifier"] = [
        "best_loss_",  # post-training attrribute (?)
        "t_",  # post-training attrribute (?)
        "feature_names_in_",  # Defined only when X has feature names that are all strings. New in version 1.0.
        # "_n_samples",
    ]  # <-- Do we need to include these???

    # ============================================ PLSRegression =========================================
    # --------------------------------------------------
    # PLSRegression Estimation Parameters
    #
    # n_components : int (default=2)
    #    Number of components to keep.
    #    Should be in [1, min(n_samples, n_features, n_targets)].
    #
    # scale : bool (default=True)
    #    Whether to scale X and Y.
    #
    # max_iter: int (default=500)
    #    The maximum number of iterations
    #    of the power method when algorithm="nipals".
    #    Ignored otherwise.
    #
    # tol : float (default=1e-6)
    #    The tolerance used as convergence criteria in the power method:
    #    the algorithm stops whenever the squared norm of u_i - u_{i-1}
    #    is less than tol, where u corresponds to the left singular vector.
    #
    # copy : bool (default=True)
    #    Whether to copy X and Y in fit before applying centering, and potentially scaling.
    #    If False, these operations will be done inplace, modifying both arrays.
    #
    # --------------------------------------------------
    model_constructor["PLSRegression"] = PLSRegression
    model_constructor_name["PLSRegression"] = "PLSRegression"
    model_fit_fn_attr_name["PLSRegression"] = "fit"
    model_predict_fn_attr_name["PLSRegression"] = "predict"
    model_constructor_arg_defaults["PLSRegression"] = {
        "n_components": 2,
        "scale": True,
        "max_iter": 500,
        "tol": 1e-6,
        "copy": True,
    }
    model_required_non_cnstr_attribs["PLSRegression"] = [
        "x_weights_",
        "y_weights_",
        "x_loadings_",
        "y_loadings_",
        "x_scores_",
        "y_scores_",
        "x_rotations_",
        "y_rotations_",
        # Consider..."coef_" is actually a class property (formulation), not an assignable/persistable attribute.
        "coef_",
        "intercept_",  # New in version 1.1.
        "n_iter_",
        "n_features_in_",
    ]
    model_optional_non_cnstr_attribs["PLSRegression"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
    ]  # <-- Do we need to include this???

    # ============================================ PLSCanonical =========================================
    # --------------------------------------------------
    # PLSCanonical Estimation Parameters
    #
    # n_components : int (default=2)
    #    Number of components to keep.
    #    Should be in [1, min(n_samples, n_features, n_targets)].
    #
    # scale : bool (default=True)
    #    Whether to scale X and Y.
    #
    # algorithm : str {"nipals", "svd"} (default="nipals")
    #    The algorithm used to estimate the first singular vectors
    #    of the cross-covariance matrix.
    #    "nipals" uses the power method while "svd" will compute the whole SVD.
    #
    # max_iter: int (default=500)
    #    The maximum number of iterations
    #    of the power method when algorithm="nipals".
    #    Ignored otherwise.
    #
    # tol : float (default=1e-6)
    #    The tolerance used as convergence criteria in the power method:
    #    the algorithm stops whenever the squared norm of u_i - u_{i-1}
    #    is less than tol, where u corresponds to the left singular vector.
    #
    # copy : bool (default=True)
    #    Whether to copy X and Y in fit before applying centering, and potentially scaling.
    #    If False, these operations will be done inplace, modifying both arrays.
    #
    # --------------------------------------------------
    model_constructor["PLSCanonical"] = PLSCanonical
    model_constructor_name["PLSCanonical"] = "PLSCanonical"
    model_fit_fn_attr_name["PLSCanonical"] = "fit"
    model_predict_fn_attr_name["PLSCanonical"] = "predict"
    model_constructor_arg_defaults["PLSCanonical"] = {
        "n_components": 2,
        "scale": True,
        "algorithm": "nipals",
        "max_iter": 500,
        "tol": 1e-6,
        "copy": True,
    }
    model_required_non_cnstr_attribs["PLSCanonical"] = [
        "x_weights_",
        "y_weights_",
        "x_loadings_",
        "y_loadings_",
        "x_scores_",
        "y_scores_",
        "x_rotations_",
        "y_rotations_",
        # Consider..."coef_" is actually a class property (formulation), not an assignable/persistable attribute.
        "coef_",
        "intercept_",  # New in version 1.1.
        "n_iter_",
        "n_features_in_",
    ]
    model_optional_non_cnstr_attribs["PLSCanonical"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
    ]  # <-- Do we need to include this???

    # ============================================ KernelRidge(Regressor) =========================================
    # --------------------------------------------------
    # KernelRidge(Regressor) Estimation Parameters
    #
    # alpha: float or array-like of shape (n_targets,) (default=1.0)
    #    Regularization strength; must be a positive float.
    #    Regularization improves the conditioning of the problem
    #    and reduces the variance of the estimates.
    #    Larger values specify stronger regularization.
    #    Alpha corresponds to 1 / (2C) in other linear models
    #    such as LogisticRegression or LinearSVC.
    #    If an array is passed, penalties are assumed to be specific to the targets.
    #    Hence they must correspond in number.
    #    See Ridge regression and classification for formula.
    #
    # kernel : str {"linear", "poly", "rbf", "sigmoid",
    #    "polynomial", "laplacian", "cosine",
    #     "additive_chi2", "chi2", "precomputed"} or callable (default="linear")
    #    Kernel mapping used internally.
    #    This parameter is directly passed to pairwise_kernel.
    #    If kernel is a string, it must be one of the metrics in
    #    pairwise.PAIRWISE_KERNEL_FUNCTIONS or "precomputed".
    #
    #    If kernel is "precomputed", X is assumed to be a kernel matrix.
    #    Alternatively, if kernel is a callable function, it is called on
    #    each pair of instances (rows) and the resulting value recorded.
    #
    #    The callable should take two rows from X as input and return
    #    the corresponding kernel value as a single number.
    #    This means that callables from sklearn.metrics.pairwise are not allowed,
    #    as they operate on matrices, not single samples.
    #    Use the string identifying the kernel instead.
    #
    # gamma : float (default=None)
    #    Gamma parameter for the RBF, laplacian, polynomial,
    #    exponential chi2 and sigmoid kernels.
    #    Interpretation of the default value is left to the kernel;
    #    see the documentation for sklearn.metrics.pairwise.
    #    Ignored by other kernels.
    #
    # degree : int (default=3)
    #    Degree of the polynomial kernel.
    #    Ignored by other kernels.
    #
    # coef0 : float (default=1.0)
    #    Zero coefficient for polynomial and sigmoid kernels.
    #    Ignored by other kernels.
    #
    # kernel_params : mapping of str to any (default=None)
    #    Additional parameters (keyword arguments)
    #    for kernel function passed as callable object.
    #
    # --------------------------------------------------
    model_constructor["KernelRidge"] = KernelRidge
    model_constructor_name["KernelRidge"] = "KernelRidge"
    model_fit_fn_attr_name["KernelRidge"] = "fit"
    model_predict_fn_attr_name["KernelRidge"] = "predict"
    model_constructor_arg_defaults["KernelRidge"] = {
        "alpha": 1.0,
        "kernel": "linear",
        "gamma": None,
        "degree": 3,
        "coef0": 1.0,
        "kernel_params": None,
    }
    model_required_non_cnstr_attribs["KernelRidge"] = [
        "dual_coef_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
    ]
    model_optional_non_cnstr_attribs["KernelRidge"] = [
        # "coef_" is actually a class property (formulation), not an assignable/persistable attribute.
        # "coef_", # Only applicable when kernel="linear"
        "X_fit_",
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
    ]  # <-- Do we need to include this???

    # ============================================ IsotonicRegression =========================================
    # --------------------------------------------------
    # IsotonicRegression Estimation Parameters
    #
    # y_min: float (default=None)
    #    Lower bound on the lowest predicted value (the minimum value may still be higher).
    #    If not set, defaults to -inf.
    #
    # y_max: float (default=None)
    #    Upper bound on the highest predicted value (the maximum may still be lower).
    #    If not set, defaults to +inf.
    #
    # increasing: bool or "auto" (default=True)
    #    Determines whether the predictions should be constrained to
    #    increase or decrease with X. "auto" will decide based on
    #    the Spearman correlation estimate's sign.
    #
    # out_of_bounds: str {"nan", "clip", "raise"}, (default="nan")
    #    Handles how X values outside of the training domain are handled during prediction.
    #       "nan", predictions will be NaN.
    #       "clip", predictions will be set to the value corresponding to the nearest train interval endpoint.
    #       "raise", a ValueError is raised.
    #
    # --------------------------------------------------
    model_constructor["IsotonicRegression"] = IsotonicRegression
    model_constructor_name["IsotonicRegression"] = "IsotonicRegression"
    model_fit_fn_attr_name["IsotonicRegression"] = "fit"
    model_predict_fn_attr_name["IsotonicRegression"] = "predict"
    model_constructor_arg_defaults["IsotonicRegression"] = {
        "y_min": None,
        "y_max": None,
        "increasing": True,
        "out_of_bounds": "nan",
    }
    model_required_non_cnstr_attribs["IsotonicRegression"] = [
        "X_min_",
        "X_max_",
        "X_thresholds_",  # New in version 0.24.
        "y_thresholds_",  # New in version 0.24.
        # "f_", # <-- Will be reconstituted?
        "increasing_",
    ]
    model_optional_non_cnstr_attribs["IsotonicRegression"] = (
        []
    )  # <-- Do we need to include this???

    # ============================================ GaussianNB (Classifier) =========================================
    # --------------------------------------------------
    # GaussianNB(Classifier) Estimation Parameters
    #
    # priors : array-like of shape (n_classes,) (default=None)
    #    Prior probabilities of the classes.
    #    If specified, the priors are not adjusted according to the data.
    #
    # var_smoothing : float (default=1e-9)
    #    Portion of the largest variance of all features that is added
    #    to variances for calculation stability.
    #
    #    New in version 0.20.
    #
    # --------------------------------------------------
    model_constructor["GaussianNB"] = GaussianNB
    model_constructor_name["GaussianNB"] = "GaussianNB"
    model_fit_fn_attr_name["GaussianNB"] = "fit"
    model_predict_fn_attr_name["GaussianNB"] = "predict"
    model_constructor_arg_defaults["GaussianNB"] = {
        "priors": None,
        "var_smoothing": 1e-9,
    }
    model_required_non_cnstr_attribs["GaussianNB"] = [
        "class_count_",
        "class_prior_",
        "classes_",
        "epsilon_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
        "var_",  # New in version 1.0.
        "theta_",
    ]
    model_optional_non_cnstr_attribs["GaussianNB"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
    ]  # <-- Do we need to include this???

    # ============================================ MultinomialNB (Classifier) =========================================
    # --------------------------------------------------
    # MultinomialNB(Classifier) Estimation Parameters
    #
    # alpha : float (default=1.0)
    #    Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).
    #
    # fit_prior : bool (default=True)
    #    Whether to learn class prior probabilities or not.
    #    If false, a uniform prior will be used.
    #
    # class_prior : array-like of shape (n_classes,), (default=None)
    #    Prior probabilities of the classes.
    #    If specified, the priors are not adjusted according to the data.
    #
    # --------------------------------------------------
    model_constructor["MultinomialNB"] = MultinomialNB
    model_constructor_name["MultinomialNB"] = "MultinomialNB"
    model_fit_fn_attr_name["MultinomialNB"] = "fit"
    model_predict_fn_attr_name["MultinomialNB"] = "predict"
    model_constructor_arg_defaults["MultinomialNB"] = {
        "alpha": 1.0,
        "fit_prior": True,
        "class_prior": None,
    }
    model_required_non_cnstr_attribs["MultinomialNB"] = [
        "class_count_",
        "class_log_prior_",
        "classes_",
        "feature_count_",
        "feature_log_prob_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
    ]
    model_optional_non_cnstr_attribs["MultinomialNB"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
    ]  # <-- Do we need to include this???

    # ============================================ ComplementNB (Classifier) =========================================
    # --------------------------------------------------
    # ComplementNB(Classifier) Estimation Parameters
    #
    # alpha : float (default=1.0)
    #    Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).
    #
    # fit_prior : bool (default=True)
    #    Only used in edge case with a single class in the training set.
    #
    # class_prior : array-like of shape (n_classes,), (default=None)
    #    Prior probabilities of the classes. Not used.
    #
    # norm : bool (default=False)
    #    Whether or not a second normalization of the weights is performed.
    #    The default behavior mirrors the implementations found in Mahout and Weka,
    #    which do not follow the full algorithm described in Table 9 of the paper.
    #
    # --------------------------------------------------
    model_constructor["ComplementNB"] = ComplementNB
    model_constructor_name["ComplementNB"] = "ComplementNB"
    model_fit_fn_attr_name["ComplementNB"] = "fit"
    model_predict_fn_attr_name["ComplementNB"] = "predict"
    model_constructor_arg_defaults["ComplementNB"] = {
        "alpha": 1.0,
        "fit_prior": True,
        "class_prior": None,
        "norm": False,
    }
    model_required_non_cnstr_attribs["ComplementNB"] = [
        "class_count_",
        "class_log_prior_",
        "classes_",
        "feature_all_",
        "feature_count_",
        "feature_log_prob_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
    ]
    model_optional_non_cnstr_attribs["ComplementNB"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
    ]  # <-- Do we need to include this???

    # ============================================ BernoulliNB (Classifier) =========================================
    # --------------------------------------------------
    # BernoulliNB(Classifier) Estimation Parameters
    #
    # alpha : float (default=1.0)
    #    Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).
    #
    # binarize : float or None (default=0.0)
    #    Threshold for binarizing (mapping to booleans) of sample features.
    #    If None, input is presumed to already consist of binary vectors.
    #
    # fit_prior : bool (default=True)
    #    Whether to learn class prior probabilities or not.
    #    If false, a uniform prior will be used.
    #
    # class_prior : array-like of shape (n_classes,), (default=None)
    #    Prior probabilities of the classes.
    #    If specified, the priors are not adjusted according to the data
    #
    # --------------------------------------------------
    model_constructor["BernoulliNB"] = BernoulliNB
    model_constructor_name["BernoulliNB"] = "BernoulliNB"
    model_fit_fn_attr_name["BernoulliNB"] = "fit"
    model_predict_fn_attr_name["BernoulliNB"] = "predict"
    model_constructor_arg_defaults["BernoulliNB"] = {
        "alpha": 1.0,
        "binarize": 0.0,
        "fit_prior": True,
        "class_prior": None,
    }
    model_required_non_cnstr_attribs["BernoulliNB"] = [
        "class_count_",
        "class_log_prior_",
        "classes_",
        "feature_count_",
        "feature_log_prob_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
    ]
    model_optional_non_cnstr_attribs["BernoulliNB"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
    ]  # <-- Do we need to include this???

    # ============================================ CategoricalNB (Classifier) =========================================
    # --------------------------------------------------
    # CategoricalNB(Classifier) Estimation Parameters
    #
    # alpha : float (default=1.0)
    #    Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).
    #
    # fit_prior : bool (default=True)
    #    Whether to learn class prior probabilities or not.
    #    If false, a uniform prior will be used.
    #
    # class_prior : array-like of shape (n_classes,), (default=None)
    #    Prior probabilities of the classes.
    #    If specified, the priors are not adjusted according to the data.
    #
    # min_categories : int or array-like of shape (n_features,) (default=None)
    #    Minimum number of categories per feature.
    #       integer: Sets the minimum number of categories per feature to n_categories for each features.
    #       array-like: shape (n_features,) where n_categories[i] holds the minimum number of categories for the ith column of the input.
    #       None (default): Determines the number of categories automatically from the training data.
    #
    #    New in version 0.24.
    # --------------------------------------------------
    model_constructor["CategoricalNB"] = CategoricalNB
    model_constructor_name["CategoricalNB"] = "CategoricalNB"
    model_fit_fn_attr_name["CategoricalNB"] = "fit"
    model_predict_fn_attr_name["CategoricalNB"] = "predict"
    model_constructor_arg_defaults["CategoricalNB"] = {
        "alpha": 1.0,
        "fit_prior": True,
        "class_prior": None,
        "min_categories": None,
    }
    model_required_non_cnstr_attribs["CategoricalNB"] = [
        "category_count_",
        "class_count_",
        "class_log_prior_",
        "classes_",
        "feature_log_prob_",
        "n_features_in_",  # New in version 0.24. Optional as is contingent on fit being performed
        "n_categories_",  # New in version 0.24.
    ]
    model_optional_non_cnstr_attribs["CategoricalNB"] = [
        "feature_names_in_",  # New in version 1.0. Defined only when X has feature names that are all strings.
    ]  # <-- Do we need to include this???

    # ==================================== Forecast constructor ===================================

    def __init__(
        self,
        fields=None,
        default_properties=None,
        fldspec_properties=None,
        address=None,
        time_stamp="now",
        feature_mode=None,
        model_mode="LinearRegression",
        summary_mode="ARITH_TSTAT",
        output_mode="RETURNS",
        output_transform=None,
        security_keyspace="<SECMSTR>",
        dates_keyspace="Dates",
        summary_keyspace="Stats",
        feature_keyspace=None,
        offset_key="OFFSET",
        fitness_keyspace="FITNESS",
        sample_keyspace="<security_keyspace>",
        feature_transform=None,
        horizon=1,
        feature_delay=None,
        feature_tfill_max=None,
        num_stagger=None,
        stagger_persist=False,
        daterange_mode=None,
        horizon_keyspace="Hzn",
        delay_keyspace="Delay",
        stagger_keyspace="Stagger",
        daterange_keyspace="Date Ranges",
        auto_register=False,
        auto_redefine=True,
        store_mode="virtual",
        fieldspace="Forecast_Fields",
        reconfigure_flag=True,
        **kwargs,
    ):
        """Contructs a Forecast object...

        Relevant Fields:
        ================
        FEATURES (independent variables)
        BASE_FEATURES
        SCREEN
        ASSET_FWD_RETURNS or OUTPUTS (dependent variables)

        ASSET_TRI
        ASSET_PRICES
        ASSET_RETURNS
        ASSET_RETURNS_100
        ASSET_NEXT_RETS
        ASSET_NEXT_RETS_100

        PREDICTIONS (predicted output / forecasted forward return)
        TRAINING_FITNESS (fit between the ASSET_FWD_RETURNS/OUTPUTS/deps and PREDICTIONS/indeps)

        MODEL (for ML models, this will be a nebuluous binary file/result)
        IC
        STD_ERRS
        TSTATS
        PANEL

        APPLIED_FITNESS

        TRAINING_FITNESS_SUMMARY
        COEFF_SUMMARY
        IC_SUMMARY
        STD_ERR_SUMMARY
        TSTAT_SUMMARY

        PREDICTIONS_XCORR
        PREDICTIONS_XCORR_SUMMARY


        File I/O (Default) Properties
        ==============================
        path
        filename
        objname
        file_type

        Strategy Settings: (Default) Properties
        ========================================
        feature_mode: Address for Feature inputs
            None: BASE_FEATURES to be provided as source (programmatically/manually assigned later)
            <string>: FACTOR/SCREEN data inherited from data environment,
                    prefixes may be follow by <LibAddress>
                    ==> Example:  'BASE_FEATURES:<LibAddress>,SCREEN:<LibAddress>'
            <dictionary>: BASE_FEATURES/SCREEN data inherited from data environment
                    dict keys: 'BASE_FEATURES' or 'SCREEN', dict values:<LibAddress>
                    ==> Example:  {'BASE_FEATURES':<LibAddress>, 'SCREEN':<LibAddress>}
            <Quble>: FACTOR data assigned as provided accordingly


        model_mode: parameter controlling the model creation (derivation)

            None: (Pre-specified) MODEL must be provided as source (no regression performed)
                               [NOTE: MODEL field data must be susbsequently, manually assigned later]
            'SRC' or 'MODEL': (Pre-specified) MODEL provided as source data (no regression performed)
                               [NOTE: For inheritance from data environment, prefix may be follow by ":" + <LibAddress>]
            'OLS': MODEL DERIVED USING OLS REGRESSION
            'OLS_PINV': MODEL DERIVED USING OLS REGRESSION (MOORE-PENROSE PSEUDO-INVERSE METHOD)
            'OLS_QR': MODEL DERIVED USING OLS REGRESSION (QR FACTORIZATION METHOD)
            'OLS_SVD': MODEL DERIVED USING OLS REGRESSION (SINGLULAR VALUE DECOMPOSITION METHOD)
            'OLS_MLE': MODEL DERIVED USING OLS REGRESSION (MAXIMUM LIKELIHOOD METHOD)
            'RandomForestRegressor': MODEL DERIVED USING RandomForestRegressor (via scikit-lean aka sklearn)
            'BaggingRegressor': MODEL DERIVED USING BaggingRegressor (via scikit-lean aka sklearn)
            'GradientBoostingRegressor': MODEL DERIVED USING GradientBoostingRegressor (via scikit-lean aka sklearn)
            'AdaBoostRegressor': MODEL DERIVED USING AdaBoostRegressor (via scikit-lean aka sklearn)
            'KNeighborsRegressor': MODEL DERIVED USING KNeighborsRegressor (via scikit-lean aka sklearn)
            'RadiusNeighborsRegressor': MODEL DERIVED USING RadiusNeighborsRegressor (via scikit-lean aka sklearn)
            'SVR': MODEL DERIVED USING SVR (SUPPORT-VECTOR REGRESSOR) (via scikit-lean aka sklearn)
            'NuSVR': MODEL DERIVED USING NuSVR (NU-SUPPORT-VECTOR REGRESSOR) (via scikit-lean aka sklearn)
            'LinearSVR': MODEL DERIVED USING LinearSVR (LINEAR-SUPPORT-VECTOR REGRESSOR) (via scikit-lean aka sklearn)
            'MLPRegressor': MODEL DERIVED USING MLPRegressor (MULTI-LAYER PERCEPTRON / NEURAL NETWORK REGRESSOR (via scikit-lean aka sklearn)

        sample_keyspace = (comma-delimited) sample keyspace(s) for the regression samples...

            May reflect the actual keyspace name(s) and/or usage of the following short-cuts:
                '<security_keyspace>' or '<securities>' or '<SECURITIES>': inherits value of the security_keyspace property of the Model
                '<security_keyspace>' or '<a>' or '<A>': inherits value of the security_keyspace property of the Model
                '<dates_keyspace>' or '<d>' or '<D>': inherits value of the dates_keyspace property of the Model
                integer > 0: indicates a rolling regression to be performed over the dates keyspace

            Examples:

                '<security_keyspace>' or '<securities>' or '<SECURITIES>': Regression samples span across the security_keyspace
                '<security_keyspace>' or '<a>' or '<A>': Regression samples span across the security_keyspace
                                                      [In this case, the resultant coefficients (model) will be asset-independent]

                '<dates_keyspace>' or '<d>' or '<D>': Samples span across the dates_keyspace
                                                      [In this case, each asset will possess it's own model (coeffcients)
                                                      but will be date-independent (incorporates all historical information)]

                '<SECMSTR>,<d>': Samples span both the security_keyspace and dates_keyspace
                           ["pooled" regression...asset-independent and date-independent]

                '6': Samples are defined over both the trailing 6 periods in the dates_keyspace (i.e., a "trailing" regression; asset-independent)
                     [In this case, each asset will possess it's own model (coeffcients) but NOT date-indepenedent]

                '<a>,3': Samples span both the security_keyspace and the trailing 3 periods of the dates_keyspace (i.e., a "trailing, pooled" regression; asset-independent)
                         [In this case, the resultant coefficients (model) will be asset-independent but NOT date-independent]

        summary_mode = parameter controlling the mode of the summary stats calcs
                        Any combination of following in any order with any delimiters: 'GEO', 'ARITH', 'TSTAT', 'CORR'

        output_mode: Asset Return Mode: None, 'RETS','RETURNS','ASSET_RETURNS', 'PRICES','ASSET_PRICES','AP', 'TRI','ASSET_TRI', 'RETURNS_100','ASSET_RETURNS_100', 'NEXT_RETS','ASSET_NEXT_RETS', 'NEXT_RETS_100','ASSET_NEXT_RETS_100', 'FWD_HZN, 'COINCIDENT'
                                      [NOTE: For inheritance from data environment, prefix may be follow by ":" + <LibAddress>]

        output_transform: A string representing the desired asset returns format to applied before analysis
                valid formats: None, 'Z', 'ZI', 'ZW', 'PR', 'UR', 'BR', 'DM' (where DM represents De-Meaned Data)
                            'Z:GICS<2/4/6/8>', 'PR:GICS<2/4/6/8>', 'UR:GICS<2/4/6/8>', 'DM:GICS<2/4/6/8>'

        security_keyspace: keyspace name to be used to for asset identifiers
        dates_keyspace: keyspace name to be used to for dates
        summary_keyspace: keyspace name to be used to store coefficients summary stats
        feature_keyspace: model feature keyspace (when applicable)
        offset_key: key to use for offset coeffs/ics/etc (for no-offset regressions: offset_key=None)
        fitness_keyspace: keyspace to store/identify (OLS) fitness information

        Backtest Settings: (Default) Properties
        ========================================
        feature_transform: A string representing the desired factor format to be applied before analysis
                valid formats: None, 'Z', 'ZI', 'ZW', 'PR', 'UR', 'BR', 'DM' (where DM represents De-Meaned Data)
                            'Z:GICS<2/4/6/8>', 'PR:GICS<2/4/6/8>', 'UR:GICS<2/4/6/8>', 'DM:GICS<2/4/6/8>'

        horizon (default=1): None or scalar integer or a string (representing a single integer or a comma-delimited list of multiple integers)

        feature_delay: (default=None) None or scalar integer or a string (representing a single integer or a comma-delimited list of multiple integers)
                      IMPORTANT!!!: IF ASSET_RETS ARE NOT CAST AS FORWARD RETURNS
                      ============  (e.g., IF THEY REPRESENT RETURNS ON THE DATE (INTERVAL) SPECIFIED,
                                    THEN A MINIMUM feature_delay >= 1 IS APPROPRIATE / REQUIRED

        offset_key: Key to store offset information in feature_keyspace (when applicable)
        feature_tfill_max: None or scalar integer (# periods to fill missing factor data)
        num_stagger: None or scalar integer
        stagger_persist: Flag to control whether to persist (or average away) stagger cycles
        daterange_mode: A scalar, list or tuple of strings as follows: 'All','Months','Years','MoY','SoY','DoW','DoM','WoM','<YYYY>','<MMM-YYYY'>'

        horizon_keyspace: keyspace name to be used to for rebal freq dimension
        delay_keyspace: keyspace name to be used to for rebal freq dimension
        stagger_keyspace: keyspace name to be used to for stagger cycle pcts
        daterange_keyspace: keyspace name to be used to store date ranges

        Other Settings:
        ===============
        reconfigure_flag: True/False
                True (default): Appropriate when creating a new Portfolio from scratch
                False: Applies when loading/building a previously configured/persisted Portfolio with constructor args source from a file
        (i.e., constructor args already reflect a valid configuration).
        """
        if default_properties is None:
            default_properties = {}

        # Augment default_properties arg w/kwargs
        # -------------------------------------------
        for default_property_name, default_property_value in list(kwargs.items()):
            if default_property_name not in default_properties:
                default_properties[default_property_name] = default_property_value

        # Augment default_properties arg w/hardcoded defaults
        # ------------------------------------------------------
        if "feature_mode" not in default_properties:
            default_properties["feature_mode"] = feature_mode
        if "model_mode" not in default_properties:
            default_properties["model_mode"] = model_mode
        if "summary_mode" not in default_properties:
            default_properties["summary_mode"] = summary_mode

        if "output_mode" not in default_properties:
            default_properties["output_mode"] = output_mode
        if "output_transform" not in default_properties:
            default_properties["output_transform"] = output_transform

        if "security_keyspace" not in default_properties:
            default_properties["security_keyspace"] = security_keyspace
        if "dates_keyspace" not in default_properties:
            default_properties["dates_keyspace"] = dates_keyspace
        if "summary_keyspace" not in default_properties:
            default_properties["summary_keyspace"] = summary_keyspace
        if "feature_keyspace" not in default_properties:
            default_properties["feature_keyspace"] = feature_keyspace
        if "offset_key" not in default_properties:
            default_properties["offset_key"] = offset_key
        if "fitness_keyspace" not in default_properties:
            default_properties["fitness_keyspace"] = fitness_keyspace
        if "sample_keyspace" not in default_properties:
            default_properties["sample_keyspace"] = sample_keyspace

        if "feature_transform" not in default_properties:
            default_properties["feature_transform"] = feature_transform
        if "horizon" not in default_properties:
            default_properties["horizon"] = horizon
        if "feature_delay" not in default_properties:
            default_properties["feature_delay"] = feature_delay
        if "feature_tfill_max" not in default_properties:
            default_properties["feature_tfill_max"] = feature_tfill_max
        if "num_stagger" not in default_properties:
            default_properties["num_stagger"] = num_stagger
        if "stagger_persist" not in default_properties:
            default_properties["stagger_persist"] = stagger_persist
        if "daterange_mode" not in default_properties:
            default_properties["daterange_mode"] = daterange_mode

        if "horizon_keyspace" not in default_properties:
            default_properties["horizon_keyspace"] = horizon_keyspace
        if "delay_keyspace" not in default_properties:
            default_properties["delay_keyspace"] = delay_keyspace
        if "stagger_keyspace" not in default_properties:
            default_properties["stagger_keyspace"] = stagger_keyspace
        if "daterange_keyspace" not in default_properties:
            default_properties["daterange_keyspace"] = daterange_keyspace

        if "auto_register" not in default_properties:
            default_properties["auto_register"] = auto_register
        if "auto_redefine" not in default_properties:
            default_properties["auto_redefine"] = auto_redefine
        if "store_mode" not in default_properties:
            default_properties["store_mode"] = store_mode
        if "fieldspace" not in default_properties:
            default_properties["fieldspace"] = fieldspace
        if "field_type" not in default_properties:
            default_properties["field_type"] = "Quble"

        super(Forecast, self).__init__(
            fields=fields,
            default_properties=default_properties,
            fldspec_properties=fldspec_properties,
            address=address,
            time_stamp=time_stamp,
            **kwargs,
        )

        if reconfigure_flag:
            self.reconfigure(
                default_properties=default_properties,
                fldspec_properties=fldspec_properties,
            )

    def reconfigure(self, default_properties=None, fldspec_properties=None):
        """Configure fields and builders.

        Reconfigures the fields & builders (and field definition time)
        according to the relevant property settings.

        """
        # Apply new default_properties
        # ----------------------------------
        if default_properties is not None:
            self.properties._add_default_properties(default_properties)

        # First,Popuate a builders dictionary...
        # Here, dictionarty keys will be all applicable fields
        # For source fields, dictionary values will be None
        # For derived fields, dictionary values will be the name of appropriate builder method
        builders = {}
        access_graces = []

        # Procure model_mode
        # -------------------
        model_mode = self.get_property("model_mode")

        # ------------------------------------------------
        # Access "feature_mode" property as a dictionary
        # Acceptable Keys and associate value function
        #   key="BASE_FEATURES": <LibAddress>
        #   key="SCREEN": <LibAddress>
        # ------------------------------------------------
        feature_submodes = self.get_property(
            "feature_mode",
            grace=True,
            try_json_loads=True,
        )
        if isinstance(feature_submodes, str):
            feature_submodes = self._parse_complex_property(
                feature_submodes, delimiter=",", sub_delimiter=":"
            )

        # Make sure the feature_submodes was coerced to a dictionary
        if not isinstance(feature_submodes, dict):
            raise Exception(
                f"Not coerced to dict....feature_submodes:{feature_submodes}"
            )

        # Here temporal_training_mode = None, True, False or <integer> (>0)
        temporal_training_mode = self.temporal_training_mode()

        # Evaluate model_mode
        # ------------------------
        builders["PREDICTIONS_XCORR"] = "_PREDICTIONS_XCORR"
        builders["PREDICTIONS_XCORR_SUMMARY"] = "_PREDICTIONS_XCORR_SUMMARY"

        # builders["FEATURES"] = "_FEATURES"
        builders["FEATURES"] = "_TRAINING_PANEL"

        # Assign builder for 'FEATURES' field
        # ------------------------------------
        features_provided = False  # <-- Initailization
        for feature_submode, feature_subassignment in feature_submodes.items():
            if feature_submode in ("BASE_FEATURES", "SCREEN"):
                if feature_submode == "BASE_FEATURES":
                    features_provided = True

                # BASE_FEATURES/SCREEN ARE AN INPUT FIELD (AND ARE NEVER DERIVED)
                builders[feature_submode] = None
                if feature_subassignment is None:
                    pass
                elif isinstance(feature_subassignment, str) or isinstance(
                    feature_subassignment, LibAddress
                ):
                    self.config_libaddress_field(
                        fieldkey=feature_submode, address=feature_subassignment
                    )
            else:
                raise Exception(
                    "Invalid feature_submode: {0}...only 'BASE_FEATURES' or 'SCREEN' apply".format(
                        feature_submode
                    )
                )

        if not features_provided:
            raise Exception("BASE_FEATURES Must be provided")

        # Assign builder for DATE_RANGES
        # ----------------------------------
        builders["DATE_RANGES"] = "_DATE_RANGES"
        access_graces.append("DATE_RANGES")

        # ------------------------------------------------
        # Access "model_mode" property as a (single-key) dictionary
        # Acceptable Keys and associate value function
        #   key="SRC": <LibAddress>
        #   key="MODEL": <LibAddress>
        #   key="OLS"/"OLS_PINV"/"OLS_QR"/"OLS_SVD"/"OLS_MLE": None
        #   key="RandomForestRegressor"/"BaggingRegressor"/
        #       "GradientBoostingRegressor"/"AdaBoostRegressor"/
        #       "KNeighborsRegressor"/"RadiusNeighborsRegressor"/
        #       "SVR"/"NuSVR"/"LinearSVR"/"MLPRegressor": None
        # ------------------------------------------------

        # Assign builders for regression fields
        # -----------------------------------------
        regression_required = True  # <-- Initialization
        if model_mode is None:
            # No regression, MODEL to be provided (?)
            # builders["PREDICTIONS"] = "_PREDICTIONS" # <-- No "PREDICTIONS" field here (?)
            builders["MODEL"] = None
            regression_required = False

        elif (model_mode[0:3].upper() == "SRC") or (model_mode[0:5].upper() == "MODEL"):
            regression_required = False
            # See if a 'SRC' prefix was followed by ':' + <model_address>
            # [if so, assign libaddress field accordingly]
            # -------------------------------------------------------
            # NOTE: Split at first colon only (may be more after)
            model_mode_colon_locn = model_mode.find(":")
            if model_mode_colon_locn > 0:
                model_address = model_mode[(model_mode_colon_locn + 1) :].strip()
            else:
                model_address = None

            builders["PREDICTIONS"] = "_PREDICTIONS"
            builders["MODEL"] = None  # <-- To be sourced

            if (model_address is not None) and len(model_address) > 0:
                self.config_libaddress_field(fieldkey="MODEL", address=model_address)

        # -------------------------
        # LINEAR REGRESSOR MODELS
        # -------------------------
        elif model_mode in ("OLS", "OLS_PINV", "OLS_QR", "OLS_SVD", "OLS_MLE"):
            builders["PREDICTIONS"] = "_PREDICTIONS"
            builders["TRAINING_PANEL"] = "_TRAINING_PANEL"
            builders["TRAINING_FITNESS"] = "_REGR_OLS"
            builders["TRAINING_DETAIL"] = "_REGR_OLS"
            builders["MODEL"] = "_REGR_OLS"

            if temporal_training_mode == True:
                # IMPORTANT: DO NOT WANT TO INCLUDE CASES OF
                # POSITIVE INTEGER: temporal_training_mode > 1
                pass
            else:
                builders["TRAINING_FITNESS_SUMMARY"] = "_TRAINING_FITNESS_SUMMARY"
                builders["COEFF_SUMMARY"] = "_COEFF_SUMMARY"
                builders["TRAINING_DETAIL_SUMMARY"] = "_TRAINING_DETAIL_SUMMARY"

        # ----------------
        # GENERAL MODELS
        # ----------------
        elif model_mode in self.ALL_MODELS:
            builders["PREDICTIONS"] = "_PREDICTIONS"
            builders["TRAINING_PANEL"] = "_TRAINING_PANEL"
            builders["TRAINING_FITNESS"] = "_TRAIN_NLP"
            builders["MODEL"] = "_TRAIN_NLP"
            if model_mode in self.LINEAR_REGRESSORS:
                builders["COEFFS"] = "_TRAIN_NLP"
                builders["TRAINING_DETAIL"] = "_TRAIN_NLP"

            # IMPORTANT: DO NOT WANT TO INCLUDE CASES OF
            # POSITIVE INTEGER: temporal_training_mode > 1
            if temporal_training_mode == True:
                pass
            else:
                builders["TRAINING_FITNESS_SUMMARY"] = "_TRAINING_FITNESS_SUMMARY"
                if (
                    "TRAINING_DETAIL" in builders
                    and builders["TRAINING_DETAIL"] is not None
                ):
                    builders["TRAINING_DETAIL_SUMMARY"] = "_TRAINING_DETAIL_SUMMARY"

        else:
            print(f"In reconfigure: passed-through with model_mode:{model_mode}")

        # ==============================
        # Procure & Parse: output_mode
        # ==============================
        output_mode = self.get_property("output_mode", grace=True)
        horizon = self.get_property("horizon", grace=True)
        (output_src_type, output_src_address) = self._parse_output_mode(output_mode)

        # ========================
        # Apply: output_src_type
        # ========================
        if output_src_type in ("PRICES", "ASSET_PRICES", "AP"):
            base_output_name = "ASSET_PRICES"
            output_name = "ASSET_FWD_RETS"
            builders["ASSET_RETURNS"] = "_ARET_PRICE"
        elif output_src_type in ("TRI", "ASSET_TRI"):
            base_output_name = "ASSET_TRI"
            output_name = "ASSET_FWD_RETS"
            builders["ASSET_RETURNS"] = "_ARET_TRI"
        elif output_src_type in ("RETURNS_100", "ASSET_RETURNS_100"):
            base_output_name = "ASSET_RETURNS_100"
            output_name = "ASSET_FWD_RETS"
            builders["ASSET_RETURNS"] = "_ARET_RETS_100"
        elif output_src_type in ("NEXT_RETS", "ASSET_NEXT_RETS"):
            base_output_name = "ASSET_NEXT_RETS"
            output_name = "ASSET_FWD_RETS"
            builders["ASSET_RETURNS"] = "_ARET_NEXT_RETS"
        elif output_src_type in ("NEXT_RETS_100", "ASSET_NEXT_RETS_100"):
            base_output_name = "ASSET_NEXT_RETS_100"
            output_name = "ASSET_FWD_RETS"
            builders["ASSET_RETURNS"] = "_ARET_NEXT_RETS_100"
        elif output_src_type in ("RETS", "RETURNS", "ASSET_RETURNS"):
            base_output_name = "ASSET_RETURNS"
            output_name = "ASSET_FWD_RETS"
        elif output_src_type == "FWD_HZN":
            base_output_name = "BASE_OUTPUTS"
            output_name = "OUTPUTS"
        elif output_src_type == "COINCIDENT":
            base_output_name = "BASE_OUTPUTS"
            output_name = "OUTPUTS"
            if horizon:
                _logger.debug(
                    f"Warning:Re-setting horizon from {horizon} -> 0 since output_src_type={output_src_type}"
                )
                self.set_property("horizon", 0)
        elif output_src_type is not None:
            raise Exception(
                f"Invalid output_src_type:{output_src_type}...Expected: RETS/RETURNS/ASSET_RETURNS/PRICES/ASSET_PRICES/AP/TRI/ASSET_TRI/None"
            )

        # CONFIGURE base_output_name
        if output_src_address is not None and base_output_name is not None:
            builders[base_output_name] = None
            self.config_libaddress_field(
                fieldkey=base_output_name, address=output_src_address
            )

        # ================================================================
        # If regression required, then Process, Parse & Apply output_mode
        # and register and configure associated fields accordingly
        # ================================================================
        if output_src_type is not None:
            builders[output_name] = "_TRAINING_PANEL"
            builders["APPLIED_FITNESS"] = "_APPLIED_FITNESS"
        elif regression_required:
            raise Exception("Non-trivial output_src_type required for regression")

        # ==================================================================================
        # CONFIGURE/REGISTER FIELDS BASED ON builders DICTIONARY/CONFIGURATION FROM ABOVE
        # ==================================================================================

        # First, remove any non-applicable old fields
        # ---------------------------------------------
        for fieldkey in self.fields():
            if fieldkey not in builders:
                # unregister_field() should implicitly remove any fldspec_properties for this field
                self.unregister_field(fieldkey)

        # Next, add new fields if necessary
        # Set/remove builder & description property accordingly
        # -------------------------------------------------------
        for fieldkey, builder in builders.items():
            if fieldkey not in self.fields():
                self.register_field(fieldkey)

            if builder is None:
                self.remove_property("builder", fieldkey)
            else:
                self.set_property("builder", builder, fieldkey)

            # Add documentation property:
            # -----------------------------
            if fieldkey in self.description_dict:
                self.set_property(
                    "description", self.description_dict[fieldkey], fieldkey
                )

        # Apply new fldspec_properties
        # ----------------------------------
        if fldspec_properties is not None:
            self.properties._add_fldspec_properties(fldspec_properties)

        # Alter access_grace & access_mode accordingly
        # -------------------------------------------------
        for fieldkey in builders:
            file_type = self.get_property("file_type", fieldkey, grace=True)
            # Assign access_mode accordingly
            if self.is_derived_field(fieldkey, build_access_check=False):
                if file_type is not None:
                    self.set_property("access_mode", "read_build", fieldkey)
                else:
                    self.set_property("access_mode", "build", fieldkey)
            elif file_type is not None:
                self.set_property("access_mode", "read", fieldkey)
            else:
                self.set_property("access_mode", None, fieldkey)

            # Add access_grace where applicable
            if fieldkey in access_graces:
                self.set_property("access_grace", "read", fieldkey)
            elif self.has_property(
                "access_grace",
                fieldkey,
                default_check=False,
                fldspec_check=True,
                native_check=True,
            ):
                self.remove_property("access_grace", fieldkey)

        return  # <-- end of reconfigure method

    def _parse_output_mode(self, output_mode):
        if output_mode is None:
            output_src_type = None
            output_src_address = None
        elif not isinstance(output_mode, str):
            raise Exception(f"Invalid output_mode:{output_mode}...string expected")
        else:
            # Split at first colon only (may be more after)
            output_mode_colon_locn = output_mode.find(":")
            if output_mode_colon_locn < 0:
                output_src_type = output_mode.strip()
                output_src_address = None
            elif len(output_mode) > (output_mode_colon_locn + 1):
                output_src_type = output_mode[0:output_mode_colon_locn].strip()
                output_src_address = output_mode[(output_mode_colon_locn + 1) :].strip()
            else:
                output_src_type = output_mode[0:output_mode_colon_locn].strip()
                output_src_address = None

        return (output_src_type, output_src_address)

    def config_libaddress_field(
        self, fieldkey, address, domain="root_lib", access_mode="read"
    ):
        """
        Configures a single field to be read from a specific address of a library domain
        """
        if fieldkey not in self.fields():
            self.register_field(fieldkey)

        self.set_property("file_type", "LIBADDRESS", fieldkey)
        self.set_property("underlying_filename", address, fieldkey)
        self.set_property("path", domain, fieldkey)
        self.set_property("access_mode", access_mode, fieldkey)


    def check_freq_mode(self, field):
        freq = self.get_property("freq", grace=True)
        if freq == 'User Profile':
            freq = RootLib().get_control("freq")
        freq_mode = self.get_property("freq_mode", grace=True)
        if isinstance(field,Quble):
            ftk = field.first_time_keyspace(grace=True)
            if ftk:
                freq1 = field.get_space_info(space=ftk, info_type='freq')
                if freq1 is not None and freq is not None and freq1 != freq and freq_mode == 'impose':
                    field = field.asfreq(freq=freq)
        return field

    # ===================================================== BUILDER METHODS =====================================================
    
    def set_build_context(self, field):
        """
        Sets 'build context' for the Forecast class
        """
        # Do not impose this Forecast's build context on linked MODEL

        if (
            field == "MODEL"
            and self.get_property(
                "file_type", field, grace=True, suppress_recording=True
            )
            == "LIBADDRESS"
        ):
            RootLib().unfreeze_all_properties()
            return

        start_date, end_date = self._date_range(grace=True)
        date_primer = self.get_property("date_primer", grace=True)
        fx = self.get_property("fx", grace=True)
        freq = self.get_property("freq", grace=True)
        if freq == 'User Profile':
            freq = RootLib().get_control("freq")

        RootLib().set_control(
            "start_date", start_date, freeze=True, freeze_resolution="ignore"
        )

        RootLib().set_control(
            "end_date", end_date, freeze=True, freeze_resolution="ignore"
        )

        if date_primer is not None:
            RootLib().set_control(
                "date_primer", date_primer, freeze=True, freeze_resolution="ignore"
            )

        if fx:
            RootLib().set_control("fx", fx, freeze=True, freeze_resolution="ignore")
        if freq:
            RootLib().set_control("freq", freq, freeze=True, freeze_resolution="ignore")

        if "SCREEN" in self.fields() and self.address:
            screen_address = self.address.append_subpath("SCREEN")
            univ_address = screen_address.translate().globalize()
            RootLib().set_control(
                "univ", "|".join(univ_address), freeze=True, freeze_resolution="ignore"
            )

    def _DATE_RANGES(self):
        """
        See ~AnalyticLib._date_ranges method
        """
        return self._date_ranges(base_field="FEATURES")  # "PREDICTIONS"

    @RootLib.temp_frame()
    def _FEATURES(self):
        """
        Builds mulivariate 'FEATURES' Quble
        given the 'BASE_FEATURES' and 'SCREEN'

        feature_keyspace: keyspace holds feature keys within "FEATURES" (for pivoting)
            ...if None, then valuespaces will be used

        CONSTRUCTION STEPS
        ------------------
            - library fields() to multi-variate Quble
            - pivot (optional: feature_keyspace to creating multivariate features)
            - sub-variate (optional from list of specific valuespaces)
            - shift (to beginning-of-period form if needed)
            - time-filling (optional w/tfill_end_mode="NO_FUTURE" or "IN_PROGRESS")
            - apply delays BEFORE JOINING ASSET_FWD_RETS/OUTPUTS & APPLYING SCREEN (when applicable)
            - project screen (intersection or left if subseuqnet filling will be applied)
                [DECIDED TO PROJECT THE SCREEN AFTER FILLING, DELAYS]
            - cross-security filling (optional)
            - cross-security unfilling (optional)
            - cross-security transform (if applicable)
            - truncate (optional)
            - compress(summarize="any") (optional)
            - apply date limits (may choose to do this later/outside)
        """
        from qubles.io.base.screen import Screen

        features = self["BASE_FEATURES"]
        if features is None:
            raise Exception("BASE_FEATURES not available")

        # Convert Screen or Report to Qubles
        # ------------------------------------
        # Convert DataLib -> Quble
        if isinstance(features, Screen):
            # Handle Screen case ahead of general DataLib case
            features = features.apply_screen()
        elif isinstance(features, DataLib):
            # NOTE: unpivot=False may (intentionally) yield a multi-variate Quble
            features = features.to_quble(unpivot=False)

        # Validate Quble
        # -----------------
        if not isinstance(features, Quble):
            raise Exception("BASE_FEATURES is not a Quble")
        elif features.is_undefined:
            return Quble.undefined_instance()
        elif features.is_nonvariate:
            # Could look to convert to a bool variate Quble?
            raise Exception("BASE_FEATURES is a non-variate Quble")

        # Apply a pivot to the specified feature_keyspace (if applicable)
        feature_keyspace = self.get_property("feature_keyspace", grace=True)
        
        if feature_keyspace is None or len(feature_keyspace) == 0:
            pass
        elif feature_keyspace not in features.keyspaces:
            raise Exception(
                f"feature_keyspace:{feature_keyspace} absent from features.keyspaces:{features.keyspaces}"
            )
        else:
            features = features.pivot(
                pivot_keyspace=feature_keyspace,
                valuespace="<valuespace>",
            )

        # Apply feature_valuespaces (if applicable)
        feature_valuespaces = self.get_property("feature_valuespaces", grace=True)
        
        if feature_valuespaces is not None and (isinstance(feature_valuespaces, list) and len(feature_valuespaces)>0):
            if isinstance(feature_valuespaces, str):
                feature_valuespaces = feature_valuespaces.split(",")

            if isinstance(feature_valuespaces, (list, tuple)):
                feature_valuespaces = [fs.strip() for fs in feature_valuespaces]

            feature_valuespaces = features.sub_variate(
                feature_valuespaces, allow_shallow_copy=True
            )
            if not isinstance(feature_valuespaces, Quble):
                raise Exception(
                    f"type(feature_valuespaces):{type(feature_valuespaces)} after features.sub_variate() call"
                )
            elif feature_valuespaces.is_undefined:
                return Quble.undefined_instance()
            elif feature_valuespaces.is_nonvariate:
                raise Exception(
                    f"feature_valuespaces is non-variate after features.sub_variate() call"
                )
            features = feature_valuespaces

        # Establish dates_keyspace (when present)
        dates_keyspace = features.first_time_keyspace(grace=True)

        # Access fill/unfill properties
        # ------------------------------
        feature_aggr_fill_method = self.get_property(
            "feature_aggr_fill_method", grace=True
        )
        # feature_aggr_fill_group = self.get_property("feature_aggr_fill_group", grace=True)
        feature_aggr_fill_pct_required = self.get_property(
            "feature_aggr_fill_pct_required", grace=True
        )
        feature_aggr_fill_num_required = self.get_property(
            "feature_aggr_fill_num_required", grace=True
        )
        feature_aggr_fill_max = self.get_property("feature_aggr_fill_max", grace=True)
        feature_aggr_fill_pct_required_glb = self.get_property(
            "feature_aggr_fill_pct_required_glb", grace=True
        )
        feature_aggr_fill_num_required_glb = self.get_property(
            "feature_aggr_fill_num_required_glb", grace=True
        )
        feature_aggr_fill_max_glb = self.get_property(
            "feature_aggr_fill_max_glb", grace=True
        )

        feature_unfill_group = self.get_property("feature_unfill_group", grace=True)
        feature_unfill_pct_max = self.get_property("feature_unfill_pct_max", grace=True)
        feature_unfill_max = self.get_property("feature_unfill_max", grace=True)

        # -------------------------------------------
        # NOTE: Apply temporal filling and delays
        #       BEFORE applying SCREEN (or view)
        # -------------------------------------------
        feature_tfill_max = self.get_property("feature_tfill_max", grace=True)
        feature_tfill_end_mode = self.get_property(
            "feature_tfill_end_mode", grace=True, default_property_value="no_future"
        )

        if dates_keyspace is not None:
            if feature_tfill_max is not None:
                features = features.fill1d(
                    keyspace=dates_keyspace,
                    valuespace="<valuespaces>",
                    tfill_method="pad",
                    tfill_max=feature_tfill_max,
                    tfill_end_mode=feature_tfill_end_mode,
                )

        # Incorporate feature_delay (if applicable)
        # ----------------------------------------
        feature_delay = self.get_property("feature_delay", grace=True)
        delay_keyspace = self.get_property(
            "delay_keyspace", grace=True, default_property_value="Delay"
        )

        if dates_keyspace is not None:
            # Convert feature_delay into an int list
            if feature_delay is None:
                pass
            elif isinstance(feature_delay, str):
                # Convert delay string into an int list
                feature_delay = [
                    int(delay_str) for delay_str in feature_delay.split(",")
                ]
            elif isinstance(feature_delay, (list, tuple)):
                pass
            else:
                feature_delay = [feature_delay]

            if feature_delay is not None:
                features = features.multi_shift1d(
                    shifts=feature_delay,
                    keyspace=dates_keyspace,
                    shift_keyspace=delay_keyspace,
                    tfill_end_mode="no_extension",
                )

        # Apply SCREEN (if applicable)
        # -------------------------------
        if "SCREEN" in self.fields():
            screen = self["SCREEN"]
            if screen is None:
                raise Exception("SCREEN not available")
            elif isinstance(screen, Screen):
                screen = screen.apply_screen()
            elif isinstance(screen, DataLib):  # <-- includes Screen objects
                # TODO: How to properly handle DataLib with multiple fields
                # In which case, screen.to_quble() may yield a multi-variate Quble
                screen = screen.to_quble()

            # Make sure screen is now a defined Quble
            if not isinstance(screen, Quble):
                raise Exception("SCREEN is not a Quble")
            elif screen.is_undefined:
                pass
            else:
                if screen.is_variate:
                    screen = screen.variate_to_index()
                features = features.project(screen)

        # Apply view (if applicable)
        # ----------------------------
        view = RootLib().get_control("view")
        if view is not None:
            features = features.apply_view(view, allow_shallow_copy=True)

        # Apply (cross-security) aggr_fill (if applicable)
        # NOTE: Perform aggr_fill AFTER applying SCREEN
        # ------------------------------------------------
        security_keyspace = features.security_keyspace(grace=False)

        if feature_aggr_fill_method is None:
            pass
        elif security_keyspace is None:
            pass
        else:
            features = features.aggr_fill1d(
                keyspace=security_keyspace,
                aggr_method=feature_aggr_fill_method,
                pct_required=feature_aggr_fill_pct_required,
                num_required=feature_aggr_fill_num_required,
                fill_max=feature_aggr_fill_max,
                pct_required_glb=feature_aggr_fill_pct_required_glb,
                num_required_glb=feature_aggr_fill_num_required_glb,
                fill_max_glb=feature_aggr_fill_max_glb,
                view=None,
            )

        # Apply (cross-security) unfill (if applicable)
        # NOTE: Perform unfill AFTER applying aggr_fill
        # ------------------------------------------------
        if security_keyspace is None:
            pass
        elif ((feature_unfill_max is None) or (feature_unfill_max == 0)) and (
            (feature_unfill_pct_max is None) or (feature_unfill_pct_max == 0)
        ):
            # No unfilling here
            pass
        else:
            if feature_unfill_group is None:
                keymap = features.locate_keymap(feature_unfill_group, grace=False)
            else:
                keymap = None

            # Intra-group unfill
            features = features.sub_unfill1d(
                keymap=feature_unfill_group,
                keyspace=security_keyspace,
                unfill_pct_max=feature_unfill_pct_max,
                unfill_max=feature_unfill_max,
                view=None,
            )

        # Transform factor (if applicable)
        # ----------------------------------
        feature_transform = self.get_property("feature_transform", grace=True)
        if feature_transform is not None and security_keyspace is not None:
            if not features.is_numeric(
                space="<valuespaces>", grace=False, summarize="all"
            ):
                raise Exception(
                    f"Numeric valuespaces required for appliaction of feature_transform:{feature_transform}"
                )
            features = features.transform1d(
                feature_transform, keyspace=security_keyspace, view=None
            )

        # Truncate
        # -----------
        feature_truncate_min = self.get_property("feature_truncate_min", grace=True)
        feature_truncate_max = self.get_property("feature_truncate_max", grace=True)
        feature_truncate_outliers_to_missing = self.get_property(
            "feature_truncate_outliers_to_missing",
            grace=True,
            default_property_value=False,
        )
        if feature_truncate_min is not None or feature_truncate_max is not None:
            features = features.truncate(
                min_value=feature_truncate_min,
                max_value=feature_truncate_max,
                outliers_to_missing=feature_truncate_outliers_to_missing,
                compress=False,
            )

        # Compress
        # -----------
        feature_compress = self.get_property(
            "feature_compress", grace=True, default_property_value="all"
        )
        if feature_compress:
            if isinstance(feature_compress, bool):
                # Keep only those rows where all values are not-null
                feature_compress_summarize = "all"
            elif isinstance(feature_compress, str):
                feature_compress_summarize = feature_compress
            else:
                raise Exception(
                    f"Invalid feature_compress:{feature_compress}...bool or string expected"
                )

            features.compress(
                treat_false_as_null=False,
                drop=False,
                auto_squeeze=False,
                summarize=feature_compress_summarize,
                inplace=True,
            )

        return features

    def temporal_training_mode(self):
        sample_keyspace_raw = self.get_property("sample_keyspace", grace=True)

        # Validate the sample_keyspace_raw arg...
        # -------------------------------------------
        if sample_keyspace_raw is None:
            return False
        elif isinstance(sample_keyspace_raw, int):
            if sample_keyspace_raw > 1:
                return sample_keyspace_raw
            else:
                raise Exception(
                    "Invalid sample_keyspace property: {0}...Imbedded numbers must be integer > 1".format(
                        sample_keyspace_raw
                    )
                )
        elif not isinstance(sample_keyspace_raw, str):
            raise Exception(
                "Invalid sample_keyspace property: {0}...string or integer (or None) expected".format(
                    sample_keyspace_raw
                )
            )

        # Split the (comma-delimited) sample_keyspace_raw (string) into parts...
        # --------------------------------------------------------------------------
        sample_keyspace_strlist = sample_keyspace_raw.split(",")

        tr_mode = False  # <-- Initialization (will possibly change later)

        # Parse the list of strings...
        # ---------------------------------
        dates_keyspace = self.get_property("dates_keyspace", grace=True)
        for sample_keyspace1 in sample_keyspace_strlist:
            if sample_keyspace1 in (
                "<security_keyspace>",
                "<a>",
                "<A>",
                "<ASSETS>",
                "<assets>",
                "<security_keyspace>",
                "<SECURITIES>",
                "<securities>",
            ):
                pass

            elif sample_keyspace1 in (
                "<dates_keyspace>",
                "<d>",
                "<D>",
                "<DATES>",
                "<dates>",
            ):
                tr_mode = True
                return tr_mode

            elif sample_keyspace1 == dates_keyspace:
                tr_mode = True
                return tr_mode

            elif sample_keyspace1.isdigit():
                tr_mode = int(sample_keyspace1)
                if tr_mode <= 1:
                    raise Exception(
                        "Invalid sample_keyspace property: {0}...Imbedded numbers must be integer > 1".format(
                            sample_keyspace_raw
                        )
                    )
                return tr_mode

        return tr_mode

    def process_panel_keyspaces(self, panel):
        """
        Processes the panel Quble and returns a four-element tuple as follows:

            [0]: security_keyspace
            [1]: date_keyspace (if present)
            [2]: sample_keyspaces (may or may not include dates_keyspace if not None)
            [3]: temporal_training_mode

        Parses the sample_keyspace property (comma-delimted string with possible template usage)
        Into a tuple result reflecting effective/translated information:

            (security_keyspace, dates_keyspace, sample_keyspaces, temporal_training_mode)

        Here, the third element (sample_keyspaces) will ne a list of strings
        (the latter indicating multiple sample dimensions)

        The fourth element (temporal_training_mode) will be one of the following: False, True, or <integer> (> 0):

           For temporal_training_mode=False: non-temporal regression...No involvement of date_keyspace in the sample keyspace(s)
           For temporal_training_mode=True/1: temporal regression...The dates_keyspace is one of the sample keyspace(s)
           For temporal_training_mode=<integer> > 1: A rolling temporal-regression is performed using a subsets within the dates_keyspace
        """
        # Validate panel
        # ----------------
        if not isinstance(panel, Quble):
            raise Exception("Invalid panel...Quble expected")

        security_keyspace = panel.security_keyspace(grace=False)
        dates_keyspace = panel.first_time_keyspace(grace=True)

        # Validate the sample_keyspace_raw arg...
        # -------------------------------------------
        sample_keyspace_raw = self.get_property("sample_keyspace", grace=True)

        if sample_keyspace_raw is None:
            return (security_keyspace, None, None, False)
        elif isinstance(sample_keyspace_raw, int):
            if sample_keyspace_raw > 1:
                return (None, dates_keyspace, None, sample_keyspace_raw)
            else:
                raise Exception(
                    "Invalid sample_keyspace property: {0}...Imbedded numbers must be integer > 1".format(
                        sample_keyspace_raw
                    )
                )
        elif not isinstance(sample_keyspace_raw, str):
            raise Exception(
                "Invalid sample_keyspace property: {0}...string or integer (or None) expected".format(
                    sample_keyspace_raw
                )
            )

        # Split the (comma-delimited) sample_keyspace_raw (string) into parts...
        # --------------------------------------------------------------------------
        sample_keyspace_strlist = sample_keyspace_raw.split(",")
        sample_keyspaces = []

        temporal_training_mode = False  # <-- Initialization

        # Parse the list of strings...
        # -------------------------------
        for sample_ks in sample_keyspace_strlist:
            if sample_ks in (
                "<security_keyspace>",
                "<assets>",
                "<a>",
                "<ASSETS>",
                "<A>",
                "<security_keyspace>",
                "<securities>",
                "<SECURITIES>",
                "<SECMSTR>",
            ):
                sample_keyspaces.append(security_keyspace)
            elif sample_ks == security_keyspace:
                sample_keyspaces.append(security_keyspace)
                temporal_training_mode = True
            elif sample_ks in ("<dates_keyspace>", "<d>", "<D>", "<DATES>", "<dates>"):
                if dates_keyspace is not None:
                    sample_keyspaces.append(dates_keyspace)
                    temporal_training_mode = True
            elif sample_ks == dates_keyspace:
                if dates_keyspace is not None:
                    sample_keyspaces.append(dates_keyspace)
                    temporal_training_mode = True
            elif sample_ks.isdigit():
                if dates_keyspace is None:
                    raise Exception(
                        "Cannot request moving regression when no dates present"
                    )

                try:
                    temporal_training_mode = int(sample_ks)
                    if temporal_training_mode > 1:
                        # IMPORTANT!!! FOR ROLLING REGRESSIONS, dates_keyspace MUST APPEAR FIRST!!!!
                        # PLACE dates_keyspace IN POLE POSITION
                        sample_keyspaces2 = [dates_keyspace]
                        # APPEND ANY PREVIOUS sample keyspaces
                        for sample_keyspace_tmp in sample_keyspaces:
                            sample_keyspaces2.append(sample_keyspace_tmp)
                        sample_keyspaces = sample_keyspaces2
                    else:
                        raise Exception(
                            "Invalid sample_keyspace property: {0}...Imbedded numbers must be integer > 1".format(
                                sample_keyspace_raw
                            )
                        )
                except ValueError:
                    raise Exception(
                        "Invalid sample_keyspace property: {0}...Imbedded numbers must be integer > 1".format(
                            sample_keyspace_raw
                        )
                    )

            elif sample_ks not in panel.keyspaces:
                raise Exception(
                    f"sample_ks:{sample_ks} absent from panel.keyspaces:{panel.keyspaces}"
                )
            else:
                sample_keyspaces.append(sample_ks)

        # Validate sample_keyspaces
        # ---------------------------
        if len(sample_keyspaces) == 0:
            raise Exception("No sample keyspaces identified")
        else:
            for sample_ks in sample_keyspaces:
                if sample_ks not in panel.keyspaces:
                    raise Exception(
                        f"sample_ks:{sample_ks} absent from panel.keyspaces:{panel.keyspaces}"
                    )

        # Return the requisite tuple...
        # ------------------------------
        return (
            security_keyspace,
            dates_keyspace,
            sample_keyspaces,
            temporal_training_mode,
        )

    @RootLib.temp_frame()
    def _ARET_PRICE(self):
        ap = self["ASSET_PRICES"]
        if ap is None:
            return None
        elif not isinstance(ap, Quble):
            raise Exception(f"Invalid ASSET_PRICES...Quble expected yet given:{ap}")
        else:
            dates_keyspace = ap.first_time_keyspace(grace=False, exclude_vantage=True)
            RootLib().set_control("ignore_mult", False)
            RootLib().set_control("ignore_add", False)
            ap_shifted = ap.shift1d(
                periods=1,
                keyspace=dates_keyspace,
                original_dates_only=True,
                tfill_max=5,
            )
            arets = (ap / ap_shifted) - 1.0
            return arets

    @RootLib.temp_frame()
    def _ARET_TRI(self):
        atri = self["ASSET_TRI"]  # <-- INCLUDES DIVIDENDS PER SHARE
        atri = self.check_freq_mode(atri)
        if atri is None:
            return None
        elif not isinstance(atri, Quble):
            raise Exception(f"Invalid ASSET_TRI...Quble expected yet given:{atri}")
        elif atri.is_undefined:
            # copy should eliminate address
            return atri.copy()
        elif atri.is_empty or atri.is_nonvariate:
            # copy should eliminate address
            return atri.copy()

        # Isolate the primary valuespace (to avoid mutli-var calc complexities)
        atri = atri.sub_variate(allow_shallow_copy=True)

        dates_keyspace = atri.first_time_keyspace(grace=False, exclude_vantage=True)
        RootLib().set_control("ignore_mult", False)
        RootLib().set_control("ignore_add", False)
        atri_shifted = atri.shift1d(
            periods=1,
            keyspace=dates_keyspace,
            original_dates_only=True,
            tfill_max=5,
        )
        arets = (atri / atri_shifted) - 1.0
        return arets

    def _ARET_RETS_100(self):
        aret100 = self._process_field_request(
            field_name="ASSET_RETURNS_100",
            absent_field_treatment="raise",
            None_treatment="pass",
            type_requirement=(Quble),
        )
        if aret100 is None:
            return None
        elif isinstance(aret100, Quble) and aret100.is_undefined:
            # copy should eliminate address
            return aret100.copy()
        elif aret100.is_empty or aret100.is_nonvariate:
            # copy should eliminate address
            return aret100.copy()

        # Isolate the primary valuespace (to avoid mutli-var calc complexities)
        aret100 = aret100.sub_variate(allow_shallow_copy=True)

        # Compute arets from aret100
        arets = 0.01 * aret100

        if arets.is_variate:
            arets.set_space_info(
                space="<valuespace>", info_type="time_basis", info_value="geo_cume"
            )

        return arets

    def _ARET_NEXT_RETS(self, ret100_flag=False, field_name="ASSET_NEXT_RETS"):
        # NOTE: ASSET_NEXT_RETS IS NEXT PERIOD'S ASSET RETURNS
        afwdret = self._process_field_request(
            field_name=field_name,
            absent_field_treatment="raise",
            None_treatment="pass",
            type_requirement=(Quble),
        )
        if afwdret is None:
            return None
        elif isinstance(afwdret, Quble) and afwdret.is_undefined:
            # copy should eliminate address
            return afwdret.copy()
        elif afwdret.is_empty or afwdret.is_nonvariate:
            # copy should eliminate address
            return afwdret.copy()

        # Isolate the primary valuespace (to avoid mutli-var calc complexities)
        afwdret = afwdret.sub_variate(allow_shallow_copy=True)

        # DO NOT allow dates_keyspaces to be inferred from date_ranges
        dates_keyspace = self._infer_dates_keyspace(
            [afwdret], seed_property_name="dates_keyspace", grace=False
        )

        # Shift (apply delay to) asset fwd returns to get the coincident asset returns
        if ret100_flag:
            arets = 0.01 * afwdret.shift1d(periods=1, keyspace=dates_keyspace)
        else:
            arets = afwdret.shift1d(periods=1, keyspace=dates_keyspace)

        if arets.is_variate:
            arets.set_space_info(
                space="<valuespace>", info_type="time_basis", info_value="geo_cume"
            )

        return arets

    def _ARET_NEXT_RETS_100(self):
        return self._ARET_NEXT_RETS(ret100_flag=True, field_name="ASSET_NEXT_RETS_100")

    def get_horizon(self, output_src_type="<output_src_type>"):
        """
        Procures and validates the horizon setting
        Integer expected
        """
        horizon = self.get_property("horizon", grace=True)

        # Establish output_src_type
        if output_src_type == "<output_src_type>":
            output_mode = self.get_property("output_mode", grace=True)
            (output_src_type, output_src_address) = self._parse_output_mode(output_mode)

        # Coerce horizon to an integer
        if horizon is None:
            horizon = 0 if output_src_type == "COINCIDENT" else 1
        elif isinstance(horizon, int):
            pass
        else:
            horizon = int(horizon)

        # Validate horizon
        if output_src_type == "COINCIDENT":
            if horizon != 0:
                raise Exception(
                    f"horizon:{horizon} must be zero when output_src_type:{output_src_type}"
                )
        elif horizon <= 0:
            raise Exception(
                f"horizon:{horizon} must be positive when output_src_type:{output_src_type}"
            )

        return horizon

    def _OUTPUTS(self, output_name=None, horizon_keyspace="<horizon_keyspace>"):
        """
        Generates output field contents
        (according to output_name arg)
        """
        from qubles.io.base.screen import Screen

        output_mode = self.get_property("output_mode", grace=True)
        (output_src_type, output_src_address) = self._parse_output_mode(output_mode)

        # Get horizon
        horizon = self.get_horizon(output_src_type=output_src_type)

        # Get horizon_keyspace
        if horizon_keyspace == "<horizon_keyspace>":
            horizon_keyspace = self.get_property(
                "horizon_keyspace", grace=True, default_property_value="Hzn"
            )
        if horizon_keyspace is None:
            horizon_keyspace = "Hzn"

        # Create outputs acccoerding to output_name and base_output_name
        if output_name is None:
            return Quble()
        elif output_name == "ASSET_FWD_RETS":
            # Transform asset_returns (if applicable)
            # NOTE: WE HAVE CHOSEN TO NOT APPLY 'SCREEN' field TO ASSET_RETURNS nor RESULTANT ASSET_FWD_RETS
            #       [WE NEED TEMPORAL INFORMATION TO BUILD ASSET_FWD_RETS]
            # ---------------------------------------------------------------
            asset_returns = self["ASSET_RETURNS"]
            if asset_returns is None:
                raise Exception("ASSET_RETURNS not available")
            elif not isinstance(asset_returns, Quble):
                raise Exception(
                    f"Invalid ASSET_RETURNS...Quble expected yet given:{asset_returns}"
                )
            elif asset_returns.is_undefined:
                return Quble.undefined_instance()
            else:
                dates_keyspace = asset_returns.first_non_vantage_time_keyspace(
                    grace=False
                )
                if horizon is None or horizon <= 0:
                    raise Exception(
                        f"Invalid horizon:{horizon}...positive integer required when output_name={output_name}"
                    )

                # Compute forward return according to horizon(s)
                # --------------------------------------------------
                if horizon == 1:
                    outputs = asset_returns
                else:
                    outputs = asset_returns.mgeo_cume1d(
                        periods=horizon,
                        keyspace=dates_keyspace,
                        ignore_missing=True,
                        pct_required=1.0,
                    )

                # In Quble.shift1d(): Negative periods arg reflects accessing FORWARD information
                # ----------------------------------------
                outputs = outputs.shift1d(
                    periods=(-1 * horizon),
                    keyspace=dates_keyspace,
                    tfill_end_mode="unconstrained",
                )
                outputs = outputs.insert_keyspace(
                    keyspace=horizon_keyspace, key=horizon, col_type="int"
                )

        elif output_name != "OUTPUTS":
            raise Exception(f"Invalid output_name:{output_name}")
        else:
            base_output_name = self.base_output_name
            if base_output_name is None:
                raise Exception(f"base_output_name is None")

            # First, seed outputs using self[base_output_name]
            outputs = self[base_output_name]
            if outputs is None:
                raise Exception(f"{base_output_name} not available")
            elif not isinstance(outputs, Quble):
                raise Exception(
                    f"Invalid {base_output_name}...Quble expected yet given:{outputs}"
                )
            elif outputs.is_undefined:
                return Quble.undefined_instance()

            if output_src_type == "COINCIDENT":
                if horizon is None or horizon != 0:
                    raise Exception(
                        f"Invalid horizon:{horizon}...horizon must be zero when output_src_type={output_src_type}"
                    )
                # NOTE: Choosing NOT to insert horizon_keyspace into outputs here
            elif output_src_type != "FWD_HZN":
                raise Exception(
                    f"Invalid output_src_type:{output_src_type} for output_name:{output_name}"
                )
            else:
                if horizon is None or horizon <= 0:
                    raise Exception(
                        f"Invalid horizon:{horizon}...positive integer required when output_src_type={output_src_type}"
                    )

                outputs = outputs.insert_keyspace(
                    keyspace=horizon_keyspace, key=horizon, col_type="int"
                )

        # Access fill/unfill properties
        # ------------------------------
        output_aggr_fill_method = self.get_property(
            "output_aggr_fill_method", grace=True
        )
        output_aggr_fill_pct_required = self.get_property(
            "output_aggr_fill_pct_required", grace=True
        )
        output_aggr_fill_num_required = self.get_property(
            "output_aggr_fill_num_required", grace=True
        )
        output_aggr_fill_max = self.get_property("output_aggr_fill_max", grace=True)
        output_aggr_fill_pct_required_glb = self.get_property(
            "output_aggr_fill_pct_required_glb", grace=True
        )
        output_aggr_fill_num_required_glb = self.get_property(
            "output_aggr_fill_num_required_glb", grace=True
        )
        output_aggr_fill_max_glb = self.get_property(
            "output_aggr_fill_max_glb", grace=True
        )

        output_unfill_group = self.get_property("output_unfill_group", grace=True)
        output_unfill_pct_max = self.get_property("output_unfill_pct_max", grace=True)
        output_unfill_max = self.get_property("output_unfill_max", grace=True)

        # Apply SCREEN (if applicable)
        # -------------------------------
        if "SCREEN" in self.fields():
            screen = self["SCREEN"]
            if screen is None:
                raise Exception("SCREEN not available")
            elif isinstance(screen, Screen):
                screen = screen.apply_screen()
            elif isinstance(screen, DataLib):  # <-- includes Screen objects
                # TODO: How to properly handle DataLib with multiple fields
                # In which case, screen.to_quble() may yield a multi-variate Quble
                screen = screen.to_quble()

            # Make sure screen is now a defined Quble
            if not isinstance(screen, Quble):
                raise Exception("SCREEN is not a Quble")
            elif screen.is_undefined:
                pass
            else:
                if screen.is_variate:
                    screen = screen.variate_to_index()
                outputs = outputs.project(screen)

        # Apply view (if applicable)
        # ----------------------------
        view = RootLib().get_control("view")
        if view is not None:
            outputs = outputs.apply_view(view, allow_shallow_copy=True)

        # Apply (cross-security) aggr_fill (if applicable)
        # NOTE: Perform aggr_fill AFTER applying SCREEN
        # ------------------------------------------------
        security_keyspace = outputs.security_keyspace(grace=False)

        if output_aggr_fill_method is None:
            pass
        elif security_keyspace is None:
            pass
        else:
            outputs = outputs.aggr_fill1d(
                keyspace=security_keyspace,
                aggr_method=output_aggr_fill_method,
                pct_required=output_aggr_fill_pct_required,
                num_required=output_aggr_fill_num_required,
                fill_max=output_aggr_fill_max,
                pct_required_glb=output_aggr_fill_pct_required_glb,
                num_required_glb=output_aggr_fill_num_required_glb,
                fill_max_glb=output_aggr_fill_max_glb,
                view=None,
            )

        # Apply (cross-security) unfill (if applicable)
        # NOTE: Perform unfill AFTER applying aggr_fill
        # ------------------------------------------------
        if security_keyspace is None:
            pass
        elif output_unfill_max is None and output_unfill_pct_max is None:
            pass
        else:
            if output_unfill_group is None:
                keymap = outputs.locate_keymap(output_unfill_group, grace=False)
            else:
                keymap = None

            outputs = outputs.sub_unfill1d(
                keymap=output_unfill_group,
                keyspace=security_keyspace,
                unfill_pct_max=output_unfill_pct_max,
                unfill_max=output_unfill_max,
                view=None,
            )

        # Apply (cross-security) output transform (if applicable)
        # -------------------------------------------------------
        output_transform = self.get_property("output_transform", grace=True)
        if (outputs is not None) and (output_transform is not None):
            outputs = outputs.transform1d(output_transform, keyspace=security_keyspace)

        # Truncate
        # -----------
        output_truncate_min = self.get_property("output_truncate_min", grace=True)
        output_truncate_max = self.get_property("output_truncate_max", grace=True)
        output_truncate_outliers_to_missing = self.get_property(
            "output_truncate_outliers_to_missing",
            grace=True,
            default_property_value=False,
        )
        if output_truncate_min is not None or output_truncate_max is not None:
            outputs = outputs.truncate(
                min_value=output_truncate_min,
                max_value=output_truncate_max,
                outliers_to_missing=output_truncate_outliers_to_missing,
                compress=False,
            )

        outputs.compress(summarize="all", inplace=True)

        return outputs

    @property
    def output_name(self):
        if "ASSET_FWD_RETS" in self.fields():
            return "ASSET_FWD_RETS"
        elif "OUTPUTS" in self.fields():
            return "OUTPUTS"
        else:
            return None

    @property
    def base_output_name(self):
        if "ASSET_RETURNS" in self.fields():
            return "ASSET_RETURNS"
        elif "BASE_OUTPUTS" in self.fields():
            return "BASE_OUTPUTS"
        else:
            return None

    def _TRAINING_PANEL(self):
        """
        Given: "FEATURES", "<base_output_name>" (e.g., "ASSET_RETURNS")
        Returns multilib for one-or-mode of following fields:
            "TRAINING_PANEL",
            "FEATURES", "<output_name>", (e.g., "ASSET_FWD_RETS" or "OUTPUTS")
        Stages multi-variate Quble items for training: panel

        Settings/Context:
        ----------------
        keys_join_op: 'leftmost'
        variate_mode: 'uni'

        Steps:
        ------
            Step #1A: Add "FEATURES" from "BASE_FEATURES" (required field)

            Apply Steps #1A/1B/1C/1D/1E/1F
                - "keys_join_op": "union"
                - "variate_mode": "uni"
                - initial_state=None

            Step #2A: Add "ASSET_FWD_RETS" from "ASSET_RETURNS" (required field)
                - make univariate (if applicable)
                - apply mprod1d(1+"ASSET_RETURNS", hzn)
                - apply shift1d(periods=(-1 * horizon1))
                - time-filling
                - apply screen
                - cross-security filling
                - cross-security transform
                - truncate (optional)
                - DO NOT COMPRESS (?)

            Apply Steps #2A/2B
                - "keys_join_op": "leftmost"
                - "variate_mode": "uni"
                - initial_state=panel_data

            Step #3: Add "SCREEN_BOP"
                - compress ("treat_false_as_null"=True)
                - shift (to beginning-of-period form if needed)

            Apply Step #3
                - "keys_join_op": "rightmost"
                - "variate_mode": "uni"
                - initial_state=panel_data

            Step #4A (Modifier): Impose date ranges on panel so far (if directed)
            Step #4B (Modifier): Apply filter (non-null data requirement)
        """
        output_name = self.output_name
        fields_to_build = []
        fields_to_return = []
        for field in ("TRAINING_PANEL", "FEATURES", output_name):
            if field is None:
                # In case output_name is None
                continue
            elif field in self.field_index:
                fields_to_build.append(field)
                fields_to_return.append(field)
        # When returning "TRAINING_PANEL", we must first build
        #    1) "FEATURES" (features)
        #    2) output_name (Ex: "ASSET_FWD_RETS" or "OUTPUTS")
        if "TRAINING_PANEL" in fields_to_return or "TRAINING_PANEL" in fields_to_build:
            for field in ("FEATURES", output_name):
                if field is None:
                    # In case output_name is None
                    continue
                elif field not in fields_to_build:
                    fields_to_build.append(field)

        # Procure horizon_keyspace
        horizon = self.get_horizon()
        horizon_keyspace = self.get_property(
            "horizon_keyspace", grace=True, default_property_value="Hzn"
        )
        if horizon_keyspace is None:
            horizon_keyspace = "Hzn"

        # ====================
        # STEP #1: "FEATURES"
        # =====================
        if "FEATURES" not in fields_to_build:
            features = None  # <-- Should NOT be referenced below
            features_dates_keyspace = None
        else:
            # NOTE: Screen has already been applied to field: 'FEATURES'
            # We need to build features with start_date adjusted back by the forecast_horizon
            features = self._FEATURES()
            features = self.check_freq_mode(features)
            if features is None:
                raise Exception("FEATURES is None")
            elif not isinstance(features, Quble):
                raise Exception("Invalid features... Quble expected")

            # Apply view (if applicable)
            view = RootLib().get_control("view")
            if view is not None:
                features = features.apply_view(view, allow_shallow_copy=True)

            features_dates_keyspace = features.first_time_keyspace(grace=True)

        # ====================================================
        # STEP #2: output_name ("ASSET_FWD_RETS" or "OUTPUTS"
        # ====================================================
        if output_name is None or output_name not in fields_to_build:
            outputs = None  # <-- Should NOT be referenced below
            outputs_dates_keyspace = None
        else:
            # For temporal regressions w/horizons > 1: apply Holding + Staggering
            outputs = self._OUTPUTS(
                output_name=output_name, horizon_keyspace=horizon_keyspace
            )
            outputs = self.check_freq_mode(outputs)

            if outputs is None:
                raise Exception(f"{output_name} is None")
            elif not isinstance(outputs, Quble):
                raise Exception(f"Quble expected, yet {output_name}: {outputs}")

            # Try to resolve/link any keyspace conflicts
            # Here we ask asset_fwd_rets Quble to link to any relevant features.keyspaces
            outputs_dates_keyspace = outputs.first_time_keyspace(grace=True)

            # Link outputs_dates_keyspace and features_dates_keyspace (if needed)
            if features is None:
                pass
            elif outputs is None:
                pass
            elif (
                not features_dates_keyspace is None
                and outputs_dates_keyspace is not None
            ):
                keyspace_aliases = {
                    "date_aliases": [features_dates_keyspace, outputs_dates_keyspace]
                }
                outputs = outputs.link_keyspaces(
                    features.keyspaces,
                    keyspace_aliases=keyspace_aliases,
                    deep_copy=False,
                )
                # May have changed above (but likely equals features_dates_keyspace)
                outputs_dates_keyspace = outputs.first_time_keyspace(grace=True)

        # =========================
        # STEP #3: TRAINING_PANEL
        # =========================

        if "TRAINING_PANEL" not in fields_to_build:
            panel = None  # <-- Should NOT be referenced below
        else:
            num_stagger = self.get_property("num_stagger", grace=True)
            stagger_keyspace = self.get_property(
                "stagger_keyspace", grace=True, default_property_value="Stagger"
            )

            horizons_per_train = self.get_property(
                "horizons_per_train", grace=True, default_property_value=1
            )
            if horizons_per_train is None:
                horizons_per_train = 1
            elif not isinstance(horizons_per_train, int):
                try:
                    horizons_per_train = int(horizons_per_train)
                except:
                    raise Exception(
                        f"Unable to coerce to integer...horizons_per_train:{horizons_per_train}"
                    )
            if horizons_per_train <= 0:
                raise Exception(
                    f"Invalid horizons_per_train:{horizons_per_train}...positive integer expected"
                )

            # Delay outputs -> outputs_delayed
            if outputs is None:
                outputs_delayed = None
            elif outputs_dates_keyspace is None:
                # Time-agnostic model (no time-variant data present)
                # Here, make sure outputs DOES NOT have a time-keyspace
                if features_dates_keyspace is not None:
                    # NOTE: complementary case is OK
                    raise Exception(
                        "outputs has no time-keyspace, yet features has time-keyspace"
                    )
                outputs_delayed = outputs  # <-- Shallow copy OK
            elif horizon is None or horizon == 0:
                pass
            elif horizon < 0:
                raise Exception(
                    f"Invalid horizon:{horizon}...non-negative integer expected"
                )
            else:
                outputs_delayed = outputs.shift1d(
                    periods=horizon,
                    keyspace=outputs_dates_keyspace,
                    tfill_end_mode="unconstrained",
                )

            # Seed panel with delayed features content
            if features is None:
                panel = None
            elif features_dates_keyspace is None:
                # Time-agnostic model (no time-variant data present)
                panel = features.copy()
            elif horizon is None or horizon == 0:
                panel = features.copy()
            elif horizon < 0:
                raise Exception(
                    f"Invalid horizon:{horizon}...non-negative integer expected"
                )
            elif (
                (horizon == 1)
                and (horizons_per_train == 1)
                and ((num_stagger is None) or (num_stagger <= 1))
            ):
                # Simple case
                panel = features.shift1d(
                    periods=horizon,
                    keyspace=features_dates_keyspace,
                    tfill_end_mode="unconstrained",
                    valuespace="<valuespaces>",
                )
            else:
                regr_windows = [horizons_per_train * horizon]
                # tfill_method=None...do not apply filling internally
                # ==> this setting will intentionally create temporal "gaps" in the data
                panel = features.multi_hold1d(
                    windows=regr_windows,
                    keyspace=features_dates_keyspace,
                    valuespace="<valuespaces>",
                    apply_delay_per_window=True,  # <-- Do apply delay (implicitly unconstrained)
                    window_keyspace=None,  # horizon_keyspace, # <-- Should not be needed for a single window
                    num_stagger=num_stagger,
                    stagger_keyspace=stagger_keyspace,
                    tfill_method=None,
                    force_first_key=False,
                )

            # --------------------------------------------
            # Integrate outputs_delayed into panel
            # --------------------------------------------
            if outputs_delayed is None:
                pass
            elif not isinstance(outputs_delayed, Quble):
                raise Exception(
                    f"Invalid outputs_delayed...type(outputs_delayed):{type(outputs_delayed)}"
                )
            elif outputs_delayed.is_undefined:
                pass
            elif outputs_delayed.is_nonvariate:
                raise Exception(f"Invalid outputs_delayed...variate Quble expected")
            elif panel is None:
                panel = outputs_delayed
            elif not isinstance(panel, Quble):
                raise Exception(f"Invalid panel...type(panel):{type(panel)}")
            elif panel.is_undefined:
                panel = outputs_delayed
            elif output_name in panel.valuespaces:
                raise Exception(
                    f"'{output_name}' already present in panel.valuespaces:{panel.valuespaces}"
                )
            else:
                # Here, the valuespaces will serve to hold variable names
                with ControlContextManager(
                    controls={"variate_mode": "uni", "keys_join_op": "intersection"}
                ) as ccm:
                    panel[output_name] = outputs_delayed.to_univariate(
                        allow_shallow_copy=True, allow_index=False
                    )

        # =======================================
        # STEP #4: APPLY DATE LIMITS & COMPRESS
        # =======================================

        start_date, end_date = self._date_range(grace=True)
        if (start_date is not None) or (end_date is not None):
            # Apply date limits and compression to features

            if isinstance(features, Quble) and features.is_defined:
                features_dates_keyspace = features.first_time_keyspace(
                    grace=True
                )  # <-- re-run
                if features_dates_keyspace is not None:
                    features = features.apply_date_limits(
                        start_date=start_date,
                        end_date=end_date,
                        space=features_dates_keyspace,
                        allow_shallow_copy=True,
                    )
                features.compress(summarize="any", inplace=True)

            # Apply date limits and compression to outputs
            if isinstance(outputs, Quble) and outputs.is_defined:
                outputs_dates_keyspace = outputs.first_time_keyspace(
                    grace=True
                )  # <-- re-run
                if outputs_dates_keyspace is not None:
                    outputs = outputs.apply_date_limits(
                        start_date=start_date,
                        end_date=end_date,
                        space=outputs_dates_keyspace,
                        allow_shallow_copy=True,
                    )
                outputs.compress(summarize="any", inplace=True)

            # Apply date limits and compression to panel
            if isinstance(panel, Quble) and panel.is_defined:
                panel_dates_keyspace = panel.first_time_keyspace(
                    grace=True
                )  # <-- re-run
                if panel_dates_keyspace is not None:
                    # TODO: For rolling training cases, apply BACKWARDS EXTENSION to start_date by the number of
                    # rolling_periods at assoc freq (not easy) before applying date_limits to panel to accommodate trailing window data
                    # NOTE: This change should be done in conjunction with limiting ortho_iteration
                    # for rolling time keyspaces to be >= start_date WITHIN TRAINING builder
                    panel = panel.apply_date_limits(
                        start_date=start_date,
                        end_date=end_date,
                        space=panel_dates_keyspace,
                        allow_shallow_copy=True,
                    )
                panel.compress(summarize="all", inplace=True)

        # ==========================
        # STEP #5: MULTI-BUILD LIB
        # ==========================

        # Create MultiBuildLib to hold multi-Quble reseults
        # [using self's fieldspace here... no need to introduce another fieldspace into the mix & create additional ambiguity]
        multi_build_fields = []
        if "FEATURES" in fields_to_return:
            multi_build_fields.append("FEATURES")
        if output_name is not None and output_name in fields_to_return:
            multi_build_fields.append(output_name)
        if "TRAINING_PANEL" in fields_to_return:
            multi_build_fields.append("TRAINING_PANEL")

        panel_lib = MultiBuildLib(
            fields=multi_build_fields,
            fieldspace=self.get_property("fieldspace"),
            store_mode="virtual",
        )

        if "FEATURES" in fields_to_return:
            panel_lib["FEATURES"] = features
        if output_name is not None and output_name in fields_to_return:
            panel_lib[output_name] = outputs
        if "TRAINING_PANEL" in fields_to_return:
            panel_lib["TRAINING_PANEL"] = panel

        return panel_lib

    # FOR BACKWARDS COMPATIBILITY, SUPPORT _REGR() METHOD (OLD IMPLEMENTATION)
    # AND PASS ALONG TO _REGR_OLS() (NEW IMPLEMENTATION)
    def _REGR(self):
        return self._REGR_OLS()

    @RootLib.temp_frame()
    def _REGR_OLS(self):
        """
        Generates (historical) OLS regression fit
        Returns MultiBuildLib (DataLib) with the following fields:
           'TRAINING_FITNESS': Regression fitness overview
           'TRAINING_PANEL': Regression Panel Data
           'MODEL': Regression Coefficients (per Independent Variable)
           'TRAINING_DETAIL': Combined Regression Details (COEFFS, STD_ERRS, TSTATS, P_VALUES, IC)
        """
        # ===================================================================================================
        #                             Part 1: Qualify / Augment alphas Quble
        # ===================================================================================================

        # Resolve ols_method from model_mode...
        # ---------------------------------------
        model_mode = self.get_property("model_mode")  # <-- No grace here

        model_mode2ols_dict = {
            "OLS": None,
            "OLS_PINV": "pinv",
            "OLS_QR": "qr",
            "OLS_SVD": "svd",
            "OLS_MLE": "mle",
        }
        if (model_mode is None) or not isinstance(model_mode, str):
            ols_method = None
        elif model_mode in model_mode2ols_dict:
            ols_method = model_mode2ols_dict[model_mode]
        else:
            raise Exception(
                f"Invalid (ols) model_mode:{model_mode}...supported values:{model_mode2ols_dict.keys()}"
            )

        # No grace here...Too big of implication to allow not to be specified
        offset_key = self.get_property("offset_key", grace=False)
        stagger_keyspace = self.get_property(
            "stagger_keyspace", grace=True, default_property_value="Stagger"
        )
        fitness_keyspace = self.get_property(
            "fitness_keyspace", grace=True, default_property_value="FITNESS"
        )
        stagger_persist = self.get_property("stagger_persist", grace=True)

        panel = self["TRAINING_PANEL"]

        # Establish security_keyspace, dates_keyspace sample_keyspaces & temporal_training_mode
        # ------------------------------------------------
        # Allows for link conversion. Will throw an error if not supported
        # Here temporal_training_mode = None, True, False or <integer> (>0)
        (
            security_keyspace,
            dates_keyspace,
            sample_keyspaces,
            temporal_training_mode,
        ) = self.process_panel_keyspaces(panel)

        # ===========================================
        # Validate the results of the prep call...
        # ===========================================
        if panel is None:
            raise Exception("No regression data provided")
        elif not isinstance(panel, Quble):
            raise Exception("regression data should be a Quble")
        elif panel.is_undefined:
            ols_details = None
            ols_summary = None
            coeffs = None
        elif "ASSET_FWD_RETS" not in panel.valuespaces:
            raise Exception(
                f"'ASSET_FWD_RETS' absent from panel.valuespaces:{panel.valuespaces}"
            )
        else:
            yxkeys = ["ASSET_FWD_RETS"] + [
                vs for vs in panel.valuespaces if vs != "ASSET_FWD_RETS"
            ]
            if offset_key is not None:
                yxkeys = yxkeys + [offset_key]
            # ================================================================================================
            # Pooled OLS Regression: Regress across (all) dates + assets
            # -----------------------------------------------------------------------------------------------
            # COEFFS keyspaces: feature_keyspace (when present) + feature_ortho_keyspaces (non-dates, non-asset, non-var)
            # FITNESS keyspaces: fitness_keyspace + feature_ortho_keyspaces (non-dates, non-asset, non-var)
            # ===============================================================================================
            if temporal_training_mode == True:
                (ols_details, ols_summary, _, _) = panel.estimate_ols(
                    yxkeys=yxkeys,
                    sample_keyspace=sample_keyspaces,
                    offset_key=offset_key,
                    pct_required=0.0,
                    ignore_missing=True,
                    ols_method=ols_method,
                    view=None,
                    fitted_flag=False,
                    residual_flag=False,
                    detail_keyspace="OLS_DETAIL",
                    summary_keyspace=fitness_keyspace,
                )  # <-- do NOT use working view here
            # ===============================================================================================
            # (Non-Pooled) OLS Regression: Regress across assets (@ each date)
            # -----------------------------------------------------------------------------------------------
            # COEFFS keyspaces: feature_keyspace (when present) + dates_keyspace + feature_ortho_keyspaces (non-dates, non-asset)
            # FITNESS keyspaces: fitness_keyspace + dates_keyspace + feature_ortho_keyspaces (non-dates, non-asset)
            # ===============================================================================================
            elif not temporal_training_mode:  # <-- Will handle False and 0
                (ols_details, ols_summary, _, _) = panel.estimate_ols(
                    yxkeys=yxkeys,
                    sample_keyspace=sample_keyspaces,
                    offset_key=offset_key,
                    pct_required=0.0,
                    ignore_missing=True,
                    ols_method=ols_method,
                    view=None,
                    fitted_flag=False,
                    residual_flag=False,
                    detail_keyspace="OLS_DETAIL",
                    summary_keyspace=fitness_keyspace,
                )  # <-- do NOT use working view here

            elif not isinstance(temporal_training_mode, int) or (
                temporal_training_mode < 0
            ):
                raise Exception(
                    f"sample_keyspaces:{sample_keyspaces} yielded bad temporal_training_mode:{temporal_training_mode}...True,False or integer > 0 expected"
                )
            # ===============================================================================================
            # Pooled, Moving OLS Regression: Regress across (subsets of) dates + assets
            # -----------------------------------------------------------------------------------------------
            # COEFFS keyspaces: feature_keyspace (when present) + dates_keyspace + feature_ortho_keyspaces (non-dates, non-asset, non-var feature_keyspaces)
            # FITNESS keyspaces: fitness_keyspace + dates_keyspace + feature_ortho_keyspaces (non-dates, non-asset, non-var)
            # ===============================================================================================
            else:  # temporal_training_mode > 0
                # Put dates keyspace first in
                # sample_keyspace list/tuple (if necessary)
                # ------------------------------------------
                if (
                    (len(sample_keyspaces) == 2)
                    and (sample_keyspaces[-1] in panel.keyspaces)
                    and panel.is_time_space(sample_keyspaces[-1])
                ):
                    sample_keyspaces = [sample_keyspaces[1], sample_keyspaces[0]]

                # NOTE: When calling mestimate_ols, the first/primary sample keyspace is the roll (moving window) dimension
                (ols_details, ols_summary, _, _) = panel.mestimate_ols(
                    periods=temporal_training_mode,
                    yxkeys=yxkeys,
                    # This was changed from sample_keyspace, not sure if this is correct but old variable was gone!!!
                    sample_keyspace=sample_keyspaces,
                    offset_key=offset_key,
                    pct_required=0.0,
                    ignore_missing=True,
                    ols_method=ols_method,
                    sample_shift=None,
                    view=None,
                    fitted_flag=False,
                    residual_flag=False,
                    detail_keyspace="OLS_DETAIL",
                    summary_keyspace=fitness_keyspace,
                )

            # Collapse & squeeze 'Stagger' dimension (if applicable)...
            # ---------------------------------------------------------------
            if (
                (ols_details is not None)
                and (stagger_keyspace in ols_details.keyspaces)
                and not stagger_persist
            ):
                ols_details = ols_details.mean1d(
                    keyspace=stagger_keyspace, ignore_missing=True, auto_squeeze=True
                )

            if (
                (ols_summary is not None)
                and (stagger_keyspace in ols_summary.keyspaces)
                and not stagger_persist
            ):
                ols_summary = ols_summary.mean1d(
                    keyspace=stagger_keyspace, ignore_missing=True, auto_squeeze=True
                )

            # Create MultiBuildLib to hold multi-Quble reseults
            # [using self's fieldspace here... no need to introduce another fieldspace into the mix & create additional ambiguity]
            training_lib = MultiBuildLib(
                fields=["TRAINING_DETAIL", "MODEL", "TRAINING_FITNESS"],
                fieldspace=self.get_property("fieldspace"),
                store_mode="virtual",
            )
            tfill_max = None

            if ols_details is not None:
                training_lib["TRAINING_DETAIL"] = ols_details
                coeffs = ols_details.get1d(
                    "COEFFS", keyspace="OLS_DETAIL", auto_squeeze=True
                )
                # Assign coeffs filling for temporally-qualified regressions
                if coeffs.is_variate and coeffs.has_time_keyspaces:
                    # Infer tfill_max for time-filling
                    horizon = self.get_horizon()
                    if horizon is None or horizon <= 0:
                        tfill_max = 0
                    else:
                        horizons_per_train = self.get_property(
                            "horizons_per_train", grace=True, default_property_value=1
                        )
                        if horizons_per_train is None:
                            horizons_per_train = 1
                        # We only need to fill one less than horizon
                        tfill_max = max(((horizon * horizons_per_train) - 1), 0)

                    # If tfill_max > 0, apply filling for temporally-qualified training cycles
                    if tfill_max is not None and (tfill_max > 0):
                        # Apply tfill_max to all valuspaces of coeffs
                        coeffs.set_space_info(
                            space=coeffs.valuespaces,
                            info_type="tfill_max",
                            info_value=tfill_max,
                        )

                training_lib["MODEL"] = coeffs

            if ols_summary is not None:
                training_lib["TRAINING_FITNESS"] = ols_summary

            return training_lib

    @RootLib.temp_frame()
    def _TRAIN_NLP(self):
        """
        Generates (historical) estimator fit for the following regression _modes (model_mode):

            'RandomForestRegressor', 'BaggingRegressor', 'GradientBoostingRegressor', 'AdaBoostRegressor'
            'KNeighborsRegressor', 'RadiusNeighborsRegressor', 'SVR', 'NuSVR', 'LinearSVR'

        Returns MultiBuildLib (DataLib) with the following fields:
           'TRAINING_FITNESS': Training Fitness Metrics
           'MODEL': Trained Model
           'TRAINING_DETAIL': Training Fitness Details (Linear Models Only)
           'COEFFS': Training Coeffs (Linear Models Only)
        """
        import time
        from scipy import stats  # <-- For tstats calc

        # ===================================================================================================
        #                             Part 1: Qualify / Augment alphas Quble
        # ===================================================================================================

        num_stagger = self.get_property("num_stagger", grace=True)
        sampling_method = self.get_property("sampling_method", grace=True)
        sampling_period = self.get_property("date_sampling_rolling", grace=True)
        ml_query_timeout = self.get_property("ml_query_timeout", grace=True)
        query_timeout_in_sec = (
            ML_STATEMENT_TIMEOUT_IN_SECONDS
            if ml_query_timeout is None
            else ml_query_timeout
        )
        stagger_keyspace = self.get_property(
            "stagger_keyspace", grace=True, default_property_value="Stagger"
        )
        output_field = self.output_name
        if output_field is None:
            raise Exception(f"output_field needed for training")

        panel = self["TRAINING_PANEL"]
        model_mode = self.get_property("model_mode")  # <-- No grace here

        # Seed the training_lib output
        training_fields = ["MODEL", "TRAINING_FITNESS"]

        # Here, we want a non-trivial offset_key (will only be used if model.intercept_ attribute is present)
        offset_key = self.get_property("offset_key", grace=True)
        if offset_key is None or (
            isinstance(offset_key, str) and (len(offset_key) == 0)
        ):
            offset_key = "OFFSET"

        # Was there a directive to use a model intercept?
        if model_mode not in self.model_constructor_arg_defaults:
            fit_itercept_flag = False
        elif "fit_intercept" not in self.model_constructor_arg_defaults[model_mode]:
            fit_itercept_flag = False
        elif self.has_property("fit_intercept"):
            fit_itercept_flag = self.get_property("fit_intercept", grace=True)
            if fit_itercept_flag is None:
                fit_itercept_flag = self.model_constructor_arg_defaults[model_mode][
                    "fit_intercept"
                ]
        else:
            fit_itercept_flag = self.model_constructor_arg_defaults[model_mode][
                "fit_intercept"
            ]

        if "COEFFS" in self.fields():
            # NOTE: offset key DOES NOT APPLY TO NON-LINEAR METHODS
            # No grace here...Too big of implication to allow not to be specified
            training_fields.append("COEFFS")

        if "TRAINING_DETAIL" in self.fields():
            training_fields.append("TRAINING_DETAIL")

        # Seed training_dict and training_lib
        training_dict = {}
        training_lib = MultiBuildLib(
            fields=training_fields,
            fieldspace=self.get_property("fieldspace"),
            store_mode="virtual",
        )
        for field_name in training_fields:
            training_dict[field_name] = Quble.undefined_instance()
            training_lib[field_name] = training_dict[field_name]

        # Validate training parameters
        # -------------------------------
        if panel is None:
            return training_lib
        elif not isinstance(panel, Quble):
            raise Exception("training data should be Quble")
        elif panel.is_undefined or panel.is_empty:
            return training_lib
        elif output_field not in panel.valuespaces:
            raise Exception(
                f"output_field:{output_field} absent from panel.valuespaces:{panel.valuespaces}"
            )

        # Here, panel.valuespaces represent regression variables. Move output_field to beginning of list
        yxkeys_all_list = [output_field] + [
            vs for vs in panel.valuespaces if vs != output_field
        ]

        fitness_keyspace = self.get_property(
            "fitness_keyspace", grace=True, default_property_value="FITNESS"
        )
        detail_keyspace = self.get_property(
            "detail_keyspace", grace=True, default_property_value="DETAIL"
        )
        # Need to think through following requirement
        if len(yxkeys_all_list) < 2:
            raise Exception(
                f"yxkeys_all_list:{yxkeys_all_list} must contain atleast two elements...dep key (y) & indep key(s) (x and/or offset_key)"
            )

        # Establish security_keyspace, dates_keyspace
        # sample_keyspaces & temporal_regression_mode
        # ------------------------------------------------
        # Here temporal_regression_mode = None, True, False or <integer> (>0)
        (
            security_keyspace,
            dates_keyspace,
            sample_keyspaces,
            temporal_regression_mode,
        ) = self.process_panel_keyspaces(panel)

        # Identify rolling_keyspace (if applicable)
        # [Only relevant when temporal_regression_mode is int]
        # -----------------------------------------------------
        rolling_keyspace = None
        periods = None
        if (temporal_regression_mode == True) or not temporal_regression_mode:
            # Will handle True, False and 0
            pass
        elif isinstance(temporal_regression_mode, int):
            periods = temporal_regression_mode
            if temporal_regression_mode <= 0:
                raise Exception(
                    f"Invalid temporal_regression_mode:{temporal_regression_mode}...positive integer (or None) required"
                )
            for sample_ks in sample_keyspaces:
                if panel.is_time_space(sample_ks):
                    rolling_keyspace = sample_ks
                    break
            if rolling_keyspace is None:
                raise Exception(
                    f"temporal_regression_mode:{periods}, yet rolling_keyspace could not be established"
                )

        # Loop through the orthogonal keys and perform regression for each orthogonal keys
        # ---------------------------------------------
        ortho_keyspaces = panel.ortho_keyspaces(sample_keyspaces)

        # For rolling training, add rolling_keyspace to ortho_keyspaces
        # NOTE: In this case, rolling_keyspace will be in ortho_keyspaces as well as sampling_ks_list
        if rolling_keyspace is not None and periods is not None:
            if rolling_keyspace in ortho_keyspaces:
                raise Exception(
                    f"Internal inconsistency...rolling_keyspace:{rolling_keyspace} present in ortho_keyspaces:{ortho_keyspaces}"
                )
            ortho_keyspaces = ortho_keyspaces + [rolling_keyspace]

        # code using sp begin

        constructor_arg_defaults = Forecast.model_constructor_arg_defaults[model_mode]
        model_constructor_name = Forecast.model_constructor_name[model_mode]

        model_constructor_args = self._model_constructor_args(
            None,
            constructor_arg_defaults,
            model_mode=model_mode,
        )

        if ortho_keyspaces is None or len(ortho_keyspaces) == 0:
            dummy_ortho = True
        else:
            dummy_ortho = False

        coeffs_table_name = generate_random_table_name()
        model_table_name = generate_random_table_name()
        fitness_table_name = generate_random_table_name()
        detail_table_name = generate_random_table_name()
        first_time_ks = panel.first_time_keyspace()
        freq = panel.freq_of_first_time_keyspace()
        calendar_table = RootLib().get_control("calendar_table_name")

        # Current timestamp
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Concatenate elements in self.address and current timestamp
        model_storage_path = (
            ("_".join(list(self.address)) + "_" + current_time)
            .lower()
            .replace("-", "_")
        )
        self.set_property("model_storage_path", model_storage_path)

        nlp_args = {
            "model_constructor_args": model_constructor_args,
            "model_meta": {
                "model_mode": model_mode,
                "model_constructor_name": model_constructor_name,
                "yxkeys_all_list": yxkeys_all_list,
                "offset_key": offset_key,
                "fitness_keyspace": fitness_keyspace,
                "detail_keyspace": detail_keyspace,
            },
            "src_table_name": panel.table_name,
            "ortho_keyspaces": ortho_keyspaces,
            "dummy_ortho": dummy_ortho,
            "model_table_name": model_table_name,
            "fitness_table_name": fitness_table_name,
            "coeffs_table_name": coeffs_table_name,
            "detail_table_name": detail_table_name,
            "model_path": "models/" + model_storage_path,
            "sampling_method": sampling_method,
            "sampling_period": sampling_period if sampling_period is not None else 0,
            "first_time_ks": first_time_ks,
            "freq": freq,
            "calendar_table": calendar_table,
        }

        # overwrite timeout for executing the stored proc

        execute_with_timeout(
            f"call train_nlp({nlp_args})",
            interface="native_ml",
            query_timeout_in_sec=query_timeout_in_sec,
        )

        model_quble = Quble.from_table(model_table_name)
        fitness = Quble.from_table(fitness_table_name)

        try:
            coeffs_quble = Quble.from_table(coeffs_table_name)
        except Exception as e:
            coeffs_quble = Quble.undefined_instance()

        try:
            detail_quble = Quble.from_table(detail_table_name)
        except Exception as e:
            detail_quble = Quble.undefined_instance()

        # use from_table method to create following qubles from table: model, coeffs, fitness and detail qubles
        # Update training_dict items accordingly...
        if model_quble is not None and model_quble.is_defined:
            training_dict["MODEL"] = model_quble

        if coeffs_quble is not None and coeffs_quble.is_defined:
            training_dict["COEFFS"] = coeffs_quble

        if fitness is not None and fitness.is_defined:
            training_dict["TRAINING_FITNESS"] = fitness

        if detail_quble is not None and detail_quble.is_defined:
            training_dict["TRAINING_DETAIL"] = detail_quble

        # Infer tfill_max for time-filling
        horizon = self.get_horizon()
        if horizon is None or horizon <= 0:
            tfill_max = 0
        else:
            horizons_per_train = self.get_property(
                "horizons_per_train", grace=True, default_property_value=1
            )
            if horizons_per_train is None:
                horizons_per_train = 1
            # We only need to fill one less than horizon
            tfill_max = max(((horizon * horizons_per_train) - 1), 0)

        # If tfill_max > 0, apply filling for temporally-qualified training cycles
        if tfill_max is not None and (tfill_max > 0):
            for field_name in training_dict:
                if training_dict[field_name] is None:
                    print(f"Warning...{field_name} is None")
                    continue
                elif (
                    training_dict[field_name].is_variate
                    and training_dict[field_name].has_time_keyspaces
                ):
                    training_dict[field_name].set_space_info(
                        space=training_dict[field_name].valuespaces,
                        info_type="tfill_max",
                        info_value=tfill_max,
                    )

        # (Re)Copy items from the training_dict to training_lib
        for field_name in training_dict.keys():
            if training_dict[field_name] is None:
                training_lib[field_name] = Quble()  # <-- To avoid an error
            elif training_dict[field_name].is_undefined:
                training_lib[field_name] = Quble()  # <-- To avoid an error
            else:
                training_lib[field_name] = training_dict[field_name]

        return training_lib

    def _model_constructor_args(
        self,
        model_dict,
        constructor_arg_defaults,
        model_property_resolve=None,
        model_mode=None,
    ):
        """
        Sets constructor args (dictionary) from using the following priorities...

           1) model_dict (if available)
           2) library's prevailing property assignments
           3) model's default setting (as implemented above)

        model_property_resolve: Controls coordination of model quble (if provided)
                                and associated library property assignments

            None: Do not attempt to coordinate model_coeff with library properties
            'model_attr_to_property': assign model_coeff to library property REGARDLESS if property is pre-assigned
            'model_attr_to_assigned_property': assign model_coeff to library property ONLY IF property is pre-assignment and is in conflict
            'raise_conflict': raise an Exception if model_coeff is in conflict with pre-assigned property

        """
        constructor_args = {}
        for arg_name in constructor_arg_defaults:
            # ---------------------------------------------------
            # CASE 1: arg_name appears in model_dict
            # ---------------------------------------------------
            if model_dict is not None and arg_name in model_dict:
                constructor_args[arg_name] = model_dict[arg_name]
                # Non-resolve directive
                # ------------------------
                if model_property_resolve is None:
                    pass
                # Handle resolve: coeff -> property directive
                # 'model_attr_to_property': assigns model_coeffs param to library REGARDLESS if property is pre-assigned
                # 'model_attr_to_assigned_property': assigns model_coeffs param to library ONLY IF property is pre-assignment and is in conflict
                # -------------------------------------------------------------------------------------------------------
                elif model_property_resolve in (
                    "model_attr_to_property",
                    "model_attr_to_assigned_property",
                ):
                    if (
                        self.has_property(arg_name)
                        and self.get_property(arg_name) != model_dict[arg_name]
                    ):
                        self.set_property(arg_name, model_dict[arg_name])

                    elif not self.has_property(arg_name) and (
                        model_property_resolve == "model_attr_to_property"
                    ):
                        self.set_property(arg_name, model_dict[arg_name])
                # Handle conflict directive
                # ----------------------------
                elif model_property_resolve == "raise_conflict":
                    if (
                        self.has_property(arg_name)
                        and self.get_property(arg_name) != model_dict[arg_name]
                    ):
                        raise Exception(
                            "model_dict[{0}] != property {0} assignment:{1}".format(
                                arg_name, self.get_property(arg_name)
                            )
                        )
                # Handle invalid model_property_resolve
                else:
                    raise Exception(
                        f"Invalid model_property_resolve:{model_property_resolve}"
                    )

            # -------------------------------------------------------
            # CASE 2: arg_name DOES NOT appear in model_dict
            #     ==> Try to use the Forecast's property asssignment
            # -------------------------------------------------------
            else:
                property_value = self.get_property(
                    arg_name,
                    grace=True,
                    default_property_value=constructor_arg_defaults[arg_name],
                )

                # Handle constructor_args_that_expect_int_list but where property has been stored as a string
                # -------------------------------------------------
                if (
                    arg_name in Forecast.constructor_args_that_expect_int_list
                    and isinstance(property_value, str)
                ):
                    property_strlist = property_value.split(",")
                    property_list = []
                    for property_str in property_strlist:
                        property_int = int(property_str)
                        property_list.append(property_int)
                    constructor_args[arg_name] = property_list

                else:
                    constructor_args[arg_name] = property_value

        return constructor_args

    # FOR BACKWARDS COMPATIBILITY, SUPPORT _REGR() METHOD (OLD IMPLEMENTATION)
    # AND PASS ALONG TO _REGR_OLS() (NEW IMPLEMENTATION)
    @RootLib.temp_frame()
    def _PREDICTIONS(self):
        features = self["FEATURES"]
        features = self.check_freq_mode(features)
        model_quble = self["MODEL"]
        model_quble = self.check_freq_mode(model_quble)
        if model_quble is None or features is None:
            return None
        elif not isinstance(model_quble, Quble):
            raise Exception(
                f"model_quble is not a Quble...model_quble type:{type(model_quble)}"
            )
        elif not isinstance(features, Quble):
            raise Exception(
                f"model_quble is a Quble but features is type:{type(features)}"
            )
        elif features.is_undefined or model_quble.is_undefined:
            return Quble(np.nan)  # <-- Return a scalar Quble with null
        # Infer the type of alpha calcuation based on dtype of model_quble
        elif model_quble.is_nonvariate:
            raise Exception(f"model_quble is a non-variate Quble")
        elif model_quble.is_numeric(space="<valuespaces>", summarize="all"):
            return self._PREDICTIONS_OLS(features, model_quble)
        else:
            return self._PREDICTIONS_NLP(features, model_quble)

    def _PREDICTIONS_OLS(self, features, model_quble):
        """
        Indirect Build method for PREDICTIONS (OLS MODELS)
        """
        # Deal with trivial features & model_quble
        # -----------------------------------
        if (features is None) or (model_quble is None):
            return None

        elif not isinstance(features, Quble):
            raise Exception("Invalid FEATURES: Quble (or None) expected")

        elif not isinstance(model_quble, Quble):
            raise Exception("Invalid FEATURES: Quble (or None) expected")

        elif features.is_undefined:
            return features

        elif not features.is_variate or not features.is_numeric(
            space="<valuespaces>", grace=False, summarize="all"
        ):
            raise Exception("features must be a numeric-variate (valued) Quble")

        elif model_quble.is_undefined:
            return model_quble

        elif not model_quble.is_variate or not model_quble.is_numeric(
            space="<valuespaces>", grace=False, summarize="all"
        ):
            raise Exception("model_quble must be a numeric-variate (valued) Quble")

        # Here, valuespaces represent variables
        # In this case, we unpivot as a join fields to create a field-based multi-variate Quble
        # No grace here...Too big of implication to allow not to be specified
        offset_key = self.get_property("offset_key")

        # Defined model_quble_valuespaces_xoffset (excludes offset_key)
        if offset_key is None:
            model_quble_valuespaces_xoffset = model_quble.valuespaces
        elif offset_key not in model_quble.valuespaces:
            raise Exception(
                f"offset_key:{offset_key} absent from model_quble.valuespaces:{model_quble.valuespaces}"
            )
        else:
            model_quble_valuespaces_xoffset = [
                vs for vs in model_quble.valuespaces if vs != offset_key
            ]

        # Make sure features and model_quble share common valuespaces (factor names)
        # [with the exclusion of offset_key within model_quble.valuespaces]
        if set(features.valuespaces) != set(model_quble_valuespaces_xoffset):
            raise Exception(
                f"Inconsistent sets...features.valuespaces:{features.valuespaces} and model_quble_valuespaces_xoffset:{model_quble_valuespaces_xoffset}"
            )

        # Establish join parameters and alpha_expression
        features_srcvs2tgtvs = {}
        model_quble_srcvs2tgtvs = {}
        alpha_expression = ""
        plus_op_str = ""
        for src_vs in model_quble_valuespaces_xoffset:
            # Here, src_vs corresponds to a factor term
            features_tgtvs = "features:" + src_vs
            features_srcvs2tgtvs[src_vs] = features_tgtvs
            model_quble_tgtvs = "coeffs:" + src_vs
            alpha_expression += (
                plus_op_str + '("' + features_tgtvs + '" * "' + model_quble_tgtvs + '")'
            )
            plus_op_str = " + "
            model_quble_srcvs2tgtvs[src_vs] = model_quble_tgtvs

        if offset_key is None:
            pass
        # We already validated that offset_key is in model_quble.valuespaces
        else:
            model_quble_tgtvs = "coeffs:" + offset_key
            model_quble_srcvs2tgtvs[offset_key] = model_quble_tgtvs
            alpha_expression += plus_op_str + '("' + model_quble_tgtvs + '")'
            plus_op_str = " + "

        valuespaces_join_op = [features_srcvs2tgtvs, model_quble_srcvs2tgtvs]

        # May need to (re)think the choice of keys_join_op here
        merged_data = features.join(
            model_quble,
            keys_join_op="intersection",
            keyspaces_join_op="union",
            valuespaces_join_op=valuespaces_join_op,
        )

        # Apply the alpha_expression against the merged_data Quble using the Quble.select method
        alpha = merged_data.select(
            column_names=merged_data.keyspaces,
            column_expressions={"PREDICTIONS": alpha_expression},
            custom_info_overrides={"role": {"PREDICTIONS": "valuespace"}},
        )

        return alpha

    @RootLib.temp_frame()
    def _PREDICTIONS_NLP(self, features, model_quble):
        """
        Indirect Build method for PREDICTIONS (NLP MODELS)
        """
        predictions = Quble.undefined_instance()

        ml_query_timeout = self.get_property("ml_query_timeout", grace=True)
        query_timeout_in_sec = (
            ML_STATEMENT_TIMEOUT_IN_SECONDS
            if ml_query_timeout is None
            else ml_query_timeout
        )

        # Deal with trivial features & model_quble
        # --------------------------------
        if (features is None) or (model_quble is None):
            return None
        elif not isinstance(features, Quble):
            raise Exception("Invalid FEATURES: Quble (or None) expected")
        elif not isinstance(model_quble, Quble):
            raise Exception("Invalid FEATURES: Quble (or None) expected")
        elif features.is_undefined:
            return predictions
        elif not features.is_variate or not features.is_numeric(
            space="<valuespaces>", grace=False, summarize="all"
        ):
            raise Exception("features must be a numeric-variate (valued) Quble")
        elif model_quble.is_undefined:
            return predictions
        elif not model_quble.is_variate:
            raise Exception("model_quble must be a numeric-variate (valued) Quble")

        # Try to resolve/link any keyspace conflicts between features & model_quble
        # [Here we ask model_quble Quble to link.adopt to any relevant features.keyspaces]
        keyspace_aliases = {
            "date_aliases": [
                features.first_time_keyspace(),
                model_quble.first_time_keyspace(),
            ]
        }
        model_quble = model_quble.link_keyspaces(
            features.keyspaces, keyspace_aliases=keyspace_aliases, deep_copy=False
        )

        # ==================================================
        # NOTE ON STORAGE STRUCTURE FOR NON-LINEAR MODELS
        # --------------------------------------------------
        # For 'non-linear' models, the 'coefficients' are not explictly provided for each 'variable'
        # Rather the 'coefficients' are collectively stored inside a collective (clob/blob) model object
        # --------------------------------------------------
        # As such, the model_quble Quble does not support the explicit concept of a variable keyspace/dimension
        # ==================================================

        # Enforce features pivoted form
        # ---------------------------
        # Here, the valuespaces of features Quble represent the model 'variables'
        # We 'unpivot' the features Quble which converts from n-d multi-variate Quble to (n+1)d uni-variate Quble
        features_pivoted = features  # Already pivoted

        # ----------------------------------------
        # Compress the multi-variate features_pivoted
        # Only keep records where ALL valuespaces are NOT NULL (summarize='all')
        # ----------------------------------------
        features_pivoted.compress(summarize="all", inplace=True)
        if features_pivoted.is_empty:
            return predictions

        # left_inner_project method will limit the keys in model_quble to those of features_pivoted for the COMMON keyspaces only
        # ------------------------------
        if not model_quble.is_scalar and not model_quble.is_multiscalar:
            model_quble = model_quble.left_inner_project(features_pivoted)

        # Compress model_quble
        # --------------------
        model_quble.compress(summarize="all", inplace=True)
        if model_quble.is_empty:
            return predictions

        model_mode_property = self.get_property("model_mode", grace=True)
        horizons_per_train = self.get_property(
            "horizons_per_train", grace=True, default_property_value=1
        )
        if horizons_per_train is None:
            horizons_per_train = 1
        elif not isinstance(horizons_per_train, int):
            horizons_per_train = int(horizons_per_train)

        # horizon_keyspace = self.get_property(
        #    "horizon_keyspace", grace=True, default_property_value="Hzn"
        # )
        model_quble_dates_keyspace = model_quble.first_time_keyspace()

        # Build model_quble
        horizon = self.get_horizon()

        # Build predictions
        if model_quble is None or model_quble.is_undefined:
            # In this case, return a trivial Quble
            predictions = Quble()
        elif model_quble.is_index:
            # return predictions
            raise Exception(f"model_quble is a non-variate Quble")
        else:
            # Consider applying time-filling to the model_quble
            if (
                horizon is not None
                and horizon > 0
                and model_quble_dates_keyspace in model_quble.keyspaces
            ):
                # Infer tfill_max for time-filling
                horizons_per_train = self.get_property(
                    "horizons_per_train", grace=True, default_property_value=1
                )
                if horizons_per_train is None:
                    horizons_per_train = 1
                # We only need to fill one less than horizon
                tfill_max = max(((horizon * horizons_per_train) - 1), 0)
                if tfill_max > 0:
                    model_quble = model_quble.fill1d(
                        tfill_max=tfill_max, keyspace=model_quble_dates_keyspace
                    )

            # begin sp
            predictions_table_name = generate_random_table_name()

            nlp_args = {
                "model_table_name": model_quble.table_name,
                "features_table_name": features.table_name,
                "model_keyspaces": model_quble.keyspaces,
                "model_valuespace": model_quble.valuespace,
                "features_keyspaces": features.keyspaces,
                "predictions_table_name": predictions_table_name,
                "model_mode_property": model_mode_property,
                "model_storage_path": "models/"
                + self.get_property("model_storage_path"),
            }

            # overwrite timeout for executing the stored proc
            execute_with_timeout(
                f"call prediction_nlp({nlp_args})",
                interface="native_ml",
                query_timeout_in_sec=query_timeout_in_sec,
            )

            predictions = Quble.from_table(predictions_table_name)

        return predictions

    def _APPLIED_FITNESS(self):
        """
        Returns the "FITNESS" (Quble)
        of the predicted "PREDICTIONS"
        against the "FWD_ASSET_RETS" or "OUTPUTS"
        """
        fitness = Quble.undefined_instance()  # <-- Initialize
        predictions = self["PREDICTIONS"]

        # model_mode = self.get_property("model_mode")  # <-- No grace here

        output_field = self.output_name
        if output_field is None:
            return None

        outputs = self[output_field]
        is_classifier = False  # <-- Initialization

        # Qualify predictions
        # --------------------
        if predictions is None or outputs is None:
            return None
        elif not isinstance(predictions, Quble):
            raise Exception(
                f"predictions is not a Quble...predictions type:{type(predictions)}"
            )
        elif not isinstance(outputs, Quble):
            raise Exception(
                f"predictions is a Quble but outputs is type:{type(outputs)}"
            )
        elif predictions.is_undefined or outputs.is_undefined:
            # return fitness
            return None
        elif predictions.is_empty or outputs.is_empty:
            # return fitness
            return None
        elif not predictions.is_variate:
            raise Exception("predictions must be a variate (valued) Quble")
        elif not predictions.is_numeric(
            space="<valuespaces>", grace=False, summarize="all"
        ):
            is_classifier = True

        # Compress predictions
        # ---------------------
        predictions.compress(summarize="all", inplace=True)
        if predictions.is_empty:
            # return fitness
            return None

        # Qualify outputs
        # -----------------
        if outputs.is_undefined:
            # return fitness
            return None
        elif not outputs.is_variate:
            raise Exception("outputs must be a variate (valued) Quble")
        elif is_classifier and predictions.is_numeric(
            space="<valuespaces>", grace=False, summarize="all"
        ):
            raise Exception(
                f"preductions-variate are numeric yet outputs are not numeric-variate (valued) Quble"
            )

        # Link keyspaces of outputs to predictions
        # -------------------------
        keyspace_aliases = {
            "date_aliases": [
                predictions.first_time_keyspace(),
                outputs.first_time_keyspace(),
            ]
        }
        outputs = outputs.link_keyspaces(
            predictions.keyspaces, keyspace_aliases=keyspace_aliases, deep_copy=False
        )

        # Compress outputs
        # --------------------------
        outputs.compress(summarize="all", inplace=True)
        ykey = outputs.valuespace
        if outputs.is_empty:
            # return fitness
            return None

        # Build bi-variate panel Quble
        RootLib().set_control("variate_mode", "uni")
        RootLib().set_control("keys_join_op", "intersection")
        panel = Quble.undefined_instance()
        panel["PREDICTIONS"] = predictions
        panel[output_field] = outputs

        # ----------------------------------------
        # Compress panel
        # Only keep records where ALL valuespaces are NOT NULL (summarize='all')
        # ----------------------------------------
        panel.compress(summarize="all", inplace=True)
        if panel.is_empty:
            # return fitness
            return None

        fitness_keyspace = self.get_property(
            "fitness_keyspace", grace=True, default_property_value="FITNESS"
        )

        # Establish applicable sampling_keyspaces
        security_keyspace = panel.security_keyspace(grace=False)

        # Use grace=True to allow for time-agnostic model
        dates_keyspace = panel.first_time_keyspace(grace=True)
        if security_keyspace is None and dates_keyspace is None:
            # return fitness
            return None

        sampling_keyspaces = [
            x for x in [security_keyspace, dates_keyspace] if x is not None
        ]
        ortho_keyspaces = panel.ortho_keyspaces(keyspace=sampling_keyspaces, grace=True)

        # FITNESS QUBLE SPACES
        # <security> + <dates> - <sampling> + <fitness keyspace> + <valuespace from asset_fwd_returns>
        # CONSIDER MAKING fitness keys into multiple valuespaces

        # Iterate thorugh the non-asset, non-time keyspaces of panel Quble
        # and compute fitness for wach set of orthogonal key sets
        ortho_index_iterator = DistinctOrthoIndexIterator(
            panel,
            ortho_keyspaces,
            contiguous_flag=False,
            key_ordering=None,
            dummy_instance=None,
        )

        # ================== START: ortho_index_iterator LOOP ===================
        for ortho_ctr, ortho_index1 in enumerate(ortho_index_iterator):
            # Isolate local_panel
            if ortho_index1 is None:
                local_panel = panel
            else:
                local_panel = panel.get(ortho_index1, auto_squeeze=True)

            # Qualify local_panel
            if local_panel.is_undefined:
                continue
            elif local_panel.is_empty:
                continue
            elif local_panel.is_scalar or local_panel.is_multiscalar:
                # Preclude scalars
                continue
            elif local_panel.num_records <= 1:
                continue

            # Build structured array or local_panel Quble
            local_panel_sa = local_panel.to_struct_array(
                column_names=["PREDICTIONS", output_field]
            )

            # --------------------------------------------------
            # FITNESS METRICS: CLASSIFIERS (BINARY OR CLASSES)
            # --------------------------------------------------
            if is_classifier:
                # accuracy_score/balanced_accuracy_score(y_true, y_pred, ...)
                local_accur_scalar = accuracy_score(
                    local_panel_sa[output_field],
                    local_panel_sa["PREDICTIONS"],
                    normalize=True,
                    sample_weight=None,
                )
                local_bal_accur_scalar = balanced_accuracy_score(
                    local_panel_sa[output_field],
                    local_panel_sa["PREDICTIONS"],
                    sample_weight=None,
                    adjusted=False,
                )
                local_hamming_loss_scalar = hamming_loss(
                    local_panel_sa[output_field],
                    local_panel_sa["PREDICTIONS"],
                    sample_weight=None,
                )
                local_num_obs_scalar = len(local_panel_sa)

                if ortho_index1 is None:
                    array_dict = {}
                    array_dict[fitness_keyspace] = np.array(
                        ["ACCUR", "BAL_ACCUR", "HAMMING_LOSS", "NUM_OBS"],
                        dtype=np.unicode_,
                    )
                    array_dict[ykey] = np.array(
                        [
                            local_accur_scalar,
                            local_bal_accur_scalar,
                            local_hamming_loss_scalar,
                            local_num_obs_scalar,
                        ],
                        dtype=float,
                    )
                    local_fitness = Quble.from_array_dict(array_dict, valuespace=ykey)
                    fitness.merge_inplace(
                        local_fitness, self_precedence=True, variate_mode="uni"
                    )
                else:
                    local_accur_quble = ortho_index1.select(
                        column_names=ortho_index1.keyspaces + [fitness_keyspace, ykey],
                        column_expressions={
                            fitness_keyspace: "'ACCUR'",
                            ykey: f"CAST({str(local_accur_scalar)} AS FLOAT)",
                        },
                        custom_info_overrides={"role": {ykey: "valuespace"}},
                    )
                    fitness.merge_inplace(
                        local_accur_quble, self_precedence=True, variate_mode="uni"
                    )

                    local_bal_accur_quble = ortho_index1.select(
                        column_names=ortho_index1.keyspaces + [fitness_keyspace, ykey],
                        column_expressions={
                            fitness_keyspace: "'BAL_ACCUR'",
                            ykey: f"CAST({str(local_bal_accur_scalar)} AS FLOAT)",
                        },
                        custom_info_overrides={"role": {ykey: "valuespace"}},
                    )
                    fitness.merge_inplace(
                        local_bal_accur_quble, self_precedence=True, variate_mode="uni"
                    )

                    local_hamming_loss_quble = ortho_index1.select(
                        column_names=ortho_index1.keyspaces + [fitness_keyspace, ykey],
                        column_expressions={
                            fitness_keyspace: "'HAMMING_LOSS'",
                            ykey: f"CAST({str(local_hamming_loss_scalar)} AS FLOAT)",
                        },
                        custom_info_overrides={"role": {ykey: "valuespace"}},
                    )
                    fitness.merge_inplace(
                        local_hamming_loss_quble,
                        self_precedence=True,
                        variate_mode="uni",
                    )

                    local_num_obs_quble = ortho_index1.select(
                        column_names=ortho_index1.keyspaces + [fitness_keyspace, ykey],
                        column_expressions={
                            fitness_keyspace: "'NUM_OBS'",
                            ykey: f"CAST({str(local_num_obs_scalar)} AS FLOAT)",
                        },
                        custom_info_overrides={"role": {ykey: "valuespace"}},
                    )
                    fitness.merge_inplace(
                        local_num_obs_quble, self_precedence=True, variate_mode="uni"
                    )

            # --------------------------------------
            # FITNESS METRICS: REGRESSION (NUMERIC)
            # --------------------------------------
            else:
                # r2_score/mean_squared_error(y_true, y_pred, ...)
                local_rsq_scalar = r2_score(
                    local_panel_sa[output_field],
                    local_panel_sa["PREDICTIONS"],
                    sample_weight=None,
                    multioutput="uniform_average",
                )
                local_mse_scalar = mean_squared_error(
                    local_panel_sa[output_field],
                    local_panel_sa["PREDICTIONS"],
                    sample_weight=None,
                    multioutput="uniform_average",
                )
                local_num_obs_scalar = len(local_panel_sa)

                if ortho_index1 is None:
                    array_dict = {}
                    array_dict[fitness_keyspace] = np.array(
                        ["RSQ", "MSE", "NUM_OBS"], dtype=np.unicode_
                    )
                    array_dict[ykey] = np.array(
                        [local_rsq_scalar, local_mse_scalar, local_num_obs_scalar],
                        dtype=float,
                    )
                    local_fitness = Quble.from_array_dict(array_dict, valuespace=ykey)
                    fitness.merge_inplace(
                        local_fitness, self_precedence=True, variate_mode="uni"
                    )
                else:
                    local_rsq_quble = ortho_index1.select(
                        column_names=ortho_index1.keyspaces + [fitness_keyspace, ykey],
                        column_expressions={
                            fitness_keyspace: "'RSQ'",
                            ykey: f"CAST({str(local_rsq_scalar)} AS FLOAT)",
                        },
                        custom_info_overrides={"role": {ykey: "valuespace"}},
                    )
                    fitness.merge_inplace(
                        local_rsq_quble, self_precedence=True, variate_mode="uni"
                    )

                    local_mse_quble = ortho_index1.select(
                        column_names=ortho_index1.keyspaces + [fitness_keyspace, ykey],
                        column_expressions={
                            fitness_keyspace: "'MSE'",
                            ykey: f"CAST({str(local_mse_scalar)} AS FLOAT)",
                        },
                        custom_info_overrides={"role": {ykey: "valuespace"}},
                    )
                    fitness.merge_inplace(
                        local_mse_quble, self_precedence=True, variate_mode="uni"
                    )

                    local_num_obs_quble = ortho_index1.select(
                        column_names=ortho_index1.keyspaces + [fitness_keyspace, ykey],
                        column_expressions={
                            fitness_keyspace: "'NUM_OBS'",
                            ykey: f"CAST({str(local_num_obs_scalar)} AS FLOAT)",
                        },
                        custom_info_overrides={"role": {ykey: "valuespace"}},
                    )
                    fitness.merge_inplace(
                        local_num_obs_quble, self_precedence=True, variate_mode="uni"
                    )

        # ================== END: ortho_index_iterator LOOP ===================

        return fitness

    # ------------------------- SUMMARY FIELDS -----------------------------
    def _TRAINING_FITNESS_SUMMARY(self):
        return self._generic_summary("TRAINING_FITNESS")

    def _TRAINING_DETAIL_SUMMARY(self):
        return self._generic_summary("TRAINING_DETAIL")

    def _COEFF_SUMMARY(self):
        return self._generic_summary("MODEL")

    def _IC_SUMMARY(self):
        return self._generic_summary("IC")

    def _STD_ERR_SUMMARY(self):
        return self._generic_summary("STD_ERRS")

    def _TSTAT_SUMMARY(self):
        return self._generic_summary("TSTATS")

    # ------------------------- (CROSS)CORRELATION FIELDS -----------------------------
    def _PREDICTIONS_XCORR(self):
        """Build method for PREDICTIONS_XCORR"""
        predictions = self["PREDICTIONS"]

        if predictions is None:
            return Quble()
        elif not isinstance(predictions, Quble):
            raise Exception("Invalid PREDICTIONS: Quble (or None) expected")
        elif predictions.is_undefined:
            return Quble()

        security_keyspace = predictions.security_keyspace(grace=False)
        # NOTE: dates_keyspace may be None (no dates)
        dates_keyspace = predictions.first_time_keyspace(grace=True)

        # -----------------------------------------------------------------------------------
        # NOTE: DO NOT WANT TO INCLUDE DATES DIMENSION (IF PRESENT) IN CORR OPERATION,
        #       OTHERWISE, WE WILL GET CROSS-ASSET CORRELATIONS BETWEEN DISPARATE DATES
        #       WHICH IS NOT RELEVANT/NOT INTENDED
        #  ==> DO CROSS-ASSET CORRELATION FOR EACH DATE
        #      AND THEN PLACE RESULT IN APPROPRIATE DATE KEY WITHIN dates_keyspace DIMENSION
        # -----------------------------------------------------------------------------------
        non_crossers = (
            [security_keyspace, dates_keyspace]
            if dates_keyspace is not None
            else [security_keyspace]
        )
        cross_keyspaces = predictions.ortho_keyspaces(keyspace=non_crossers)

        if cross_keyspaces is None or len(cross_keyspaces) == 0:
            corr = Quble()
        else:
            corr = predictions.corr1d(
                keyspace=security_keyspace, ortho_keyspaces=dates_keyspace
            )

        return corr

    def _PREDICTIONS_XCORR_SUMMARY(self):
        """Build method for PREDICTIONS_XCORR_SUMMARY"""
        return self._generic_summary("PREDICTIONS_XCORR")

