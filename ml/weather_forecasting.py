import os

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error

from xgboost import XGBRegressor


# ============================================================
# KISAAN SETU
# WEATHER FORECASTING
# XGBOOST
# ============================================================

DATA_PATH = "ml/data/weather_data.csv"

MODEL_DIR = "ml/models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "weather_model.json"
)


# ============================================================
# TRAIN WEATHER MODEL
# ============================================================

def train_weather_model():

    print("Loading weather dataset...")

    df = pd.read_csv(
        DATA_PATH
    )

    df = df.dropna()


    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    features = [
        "temperature",
        "humidity",
        "pressure",
        "wind_speed",
        "rainfall"
    ]

    target = "next_day_rainfall"


    X = df[features]

    y = df[target]


    # --------------------------------------------------------
    # Split
    # --------------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )


    # --------------------------------------------------------
    # XGBoost
    # --------------------------------------------------------

    model = XGBRegressor(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        eval_metric="mae",
        random_state=42
    )


    print("Training weather model...")


    model.fit(
        X_train,
        y_train,
        eval_set=[
            (X_test, y_test)
        ],
        verbose=False
    )


    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5


    print("\n==============================")
    print("WEATHER MODEL PERFORMANCE")
    print("==============================")

    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")


    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model.save_model(
        MODEL_PATH
    )

    print(
        "\nWeather model saved successfully."
    )


# ============================================================
# PREDICT RAINFALL
# ============================================================

def predict_rainfall(
    temperature,
    humidity,
    pressure,
    wind_speed,
    rainfall
):

    model = XGBRegressor()

    model.load_model(
        MODEL_PATH
    )


    input_data = pd.DataFrame([
        {
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "wind_speed": wind_speed,
            "rainfall": rainfall
        }
    ])


    prediction = model.predict(
        input_data
    )


    return float(
        prediction[0]
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    train_weather_model()

    rainfall = predict_rainfall(
        temperature=27.5,
        humidity=78,
        pressure=1005,
        wind_speed=12,
        rainfall=8
    )

    print("\n==============================")
    print("NEXT-DAY RAINFALL FORECAST")
    print("==============================")

    print(
        f"Expected rainfall: {rainfall:.2f} mm"
    )
