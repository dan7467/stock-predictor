from autogluon.tabular import TabularPredictor
import pandas as pd
import yfinance as yf

class Predictor:
    
    def __init__(self, train_data):  # consider adding more features for better tabular regression, like season, wars per year, etc.
        self.train_data = pd.DataFrame(train_data, columns=["timestamp", "price"])
        subsample_size = 5000
        if subsample_size is not None and subsample_size < len(self.train_data):
            self.train_data = self.train_data.sample(n=subsample_size, random_state=0)
        tabpfnmix_default = {
            "model_path_classifier": "autogluon/tabpfn-mix-1.0-classifier",
            "model_path_regressor": "autogluon/tabpfn-mix-1.0-regressor",
            "n_ensembles": 1,
            "max_epochs": 10,  # was 30
        }

        self.hyperparameters = {
            "TABPFNMIX": [
                tabpfnmix_default,
            ],
        }

        label = "price"
        problem_type = "regression"

        self.predictor = TabularPredictor(
            label=label,
            problem_type=problem_type,
        )
    
    def fit(self, train_data, label):  # consider adding more features for better tabular regression, like season, wars per year, etc.
        self.predictor.fit(
            train_data=self.train_data,
            hyperparameters=self.hyperparameters,
            raise_on_no_models_fitted=False,
            verbosity=3,
            ag_args_fit={"ag.max_memory_usage_ratio": 0.3}  # <- use only 30% of the memory, remove this when migrating to cloud
        )
        

    def predict(self, test_data):  # consider adding more features for better tabular regression, like season, wars per year, etc.
        # self.test_data = pd.DataFrame(test_data, columns=["timestamp", "price"])
        return self.predictor.predict(test_data)

        
    
    
def fetch_data_as_list(ticker, start_date, end_date, x_axis_property, y_axis_property, training=False):
    # Fetch data from Yahoo Finance
    if training:
        data = yf.download(ticker, period="max", auto_adjust=False)
    else:
        data = yf.download(ticker, start=start_date, end=end_date)
    
    # Reset index to make the Date index a column
    data = data.reset_index()
    
    # Handle MultiIndex in columns
    if isinstance(data.columns, pd.MultiIndex):
        # Flatten the MultiIndex by joining levels with an underscore
        data.columns = ['_'.join(filter(None, col)).strip() for col in data.columns]
    
    # Fix the x_axis_property if it's 'Date', as it doesn't follow the MultiIndex flattening
    if x_axis_property == 'Date':
        x_axis_property = 'Date'

    # Adjust the y_axis_property to include the ticker suffix
    y_axis_property = f"{y_axis_property}_{ticker}"
    
    # Check if columns exist
    if x_axis_property not in data.columns:
        raise KeyError(f"Column '{x_axis_property}' not found in the fetched data. Available columns: {data.columns}")

    if y_axis_property not in data.columns:
        raise KeyError(f"Column '{y_axis_property}' not found in the fetched data. Available columns: {data.columns}")
    
    # Convert the desired columns to a dictionary of lists
    data_dict_of_two_lists = data[[x_axis_property, y_axis_property]].to_dict(orient='list')
    
    # Return list of tuples
    return list(zip(
        map(lambda ts: ts.strftime("%m/%d/%Y, %H:%M:%S") if isinstance(ts, pd.Timestamp) else ts,
            data_dict_of_two_lists[x_axis_property]),
        data_dict_of_two_lists[y_axis_property]
    ))

# Main script
if __name__ == "__main__":
    
    train_data = fetch_data_as_list('MSFT', '2023-01-01', '2024-01-01', 'Date', 'Close', True)
    
    predictor = Predictor(train_data)
    
    predictor.fit(train_data, label="Close")
    
    # Fetch data and prepare it as a DataFrame
    fetched_data = fetch_data_as_list('MSFT', '2023-01-01', '2024-01-01', 'Date', 'Close')
    test_data = pd.DataFrame(fetched_data, columns=['timestamp', 'Close'])
    
    # Generate predictions
    predictions = predictor.predict(test_data)

    # Save predictions to a CSV file (optional)
    predictions.to_csv("predicted_values.csv", index=False)

    # Print predictions
    print(predictions)
