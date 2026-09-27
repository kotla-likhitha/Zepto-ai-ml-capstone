# Analytics Pipeline — Titanic Dataset

## Objective

This module performs exploratory data analysis, predictive modeling, model evaluation, hyperparameter tuning, and a regression side-task using the Titanic dataset.

## Dataset

The Titanic dataset was loaded through Seaborn in the EDA notebook and saved as `titanic.csv` as an offline fallback.

The modeling notebook uses this saved CSV and does not independently reload the raw dataset from the network.

## Part A — Exploratory Data Analysis

The EDA includes:

- Dataset structure and summary statistics
- Missing-value percentage analysis
- Missing-value handling based on the required percentage thresholds
- Age and fare histograms
- Age and fare box plots
- IQR-based outlier analysis
- Fare mean, median, and mode
- Survival rates by sex
- Survival rates by passenger class
- Survival rates by sex and passenger class
- Six-variable correlation matrix and heatmap
- Multivariate data-story visualizations
- Standardization check for age and fare

## Part B — Predictive Modeling

The classification target is `survived`.

The features used for classification are:

- `pclass`
- `sex`
- `age`
- `sibsp`
- `parch`
- `fare`
- `embarked`

A stratified 80/20 train-test split was used so that the survived/not-survived class proportions remain similar in both sets.

### Preprocessing

Numeric features use:

- Median imputation
- StandardScaler

Categorical features use:

- Most-frequent imputation
- One-hot encoding

The preprocessing is implemented using `ColumnTransformer` and `Pipeline`, ensuring that preprocessing is fitted only on the training data.

### Classification Models

Three classifiers were trained:

1. Logistic Regression
2. Decision Tree
3. Random Forest

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 score
- ROC/AUC
- Confusion matrices
- ROC curves

The Decision Tree was also visualized using `plot_tree`.

## Imbalance Handling

Three approaches were compared:

1. Baseline Logistic Regression
2. Logistic Regression with `class_weight="balanced"`
3. Logistic Regression with SMOTE applied only to the training data

Precision, recall, and F1 score were compared across the three approaches.

## Hyperparameter Tuning

Random Forest was tuned using GridSearchCV over:

- `n_estimators`
- `max_depth`
- `max_features`

The Random Forest was created with `oob_score=True`, and the best parameters and OOB score were reported.

## Regression Side Task

A multivariate Linear Regression model was used to predict `fare`.

The regression model was evaluated using:

- MAE
- RMSE
- R²
- Adjusted R²

A residual plot was also created to examine heteroscedasticity.

## Saved Model

The file `best_pipeline.joblib` contains the complete fitted pipeline, including preprocessing and the final estimator.

The saved pipeline was reloaded with `joblib.load()` and tested on raw input data.

## Files

| File | Description |
|---|---|
| `01_eda.ipynb` | Part A: EDA, cleaning and data story |
| `02_modeling.ipynb` | Part B: predictive modeling and regression |
| `titanic.csv` | Offline dataset used by the modeling notebook |
| `best_pipeline.joblib` | Saved complete ML pipeline |
| `README.md` | Analytics module documentation |

## How to Run

1. Open `01_eda.ipynb` and run the notebook from beginning to end.
2. Confirm that `titanic.csv` is created.
3. Open `02_modeling.ipynb`.
4. Run the notebook from beginning to end.
5. The final complete model pipeline is saved as `best_pipeline.joblib`.

## Final Results

The final classification model comparison, imbalance comparison, Random Forest tuning results, regression metrics, residual analysis, and model recommendation are included in `02_modeling.ipynb`.
