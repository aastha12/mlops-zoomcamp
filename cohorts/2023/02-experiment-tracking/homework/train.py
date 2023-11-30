import os
import pickle
import click

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow


print(f"Tracking URI: {mlflow.get_tracking_uri()}")
mlflow.set_experiment("homework-2")

def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="./output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    with mlflow.start_run():

        mlflow.log_param(key='training data path',value=os.path.join(data_path, "train.pkl"))
        mlflow.log_param(key='validation data path',value=os.path.join(data_path, "val.pkl"))

        mlflow.set_tag(key="developer-name",value="aastha")
        mlflow.set_tag(key="model",value="Random Forest")

        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)

        mlflow.log_metric(key="rmse",value=rmse)


if __name__ == '__main__':
    run_train()
