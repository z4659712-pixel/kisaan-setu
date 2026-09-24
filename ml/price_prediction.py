import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor


# ============================================================
# KISAAN SETU
# XGBOOST DEMAND FORECASTING
# ============================================================

DATA_PATH = "ml/data/crop_demand.csv"
MODEL_DIR = "ml/models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "demand_model.json"
)

CROP_ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "demand_crop_encoder.pkl"
)

MARKET_ENCODER_PATH = os.path.join(
    MODEL_DIR,
    "demand_market_encoder.pkl"
)


# ============================================================
# TRAIN MODEL
# ============================================================

def train_model():

    print("Loading demand dataset...")

    df = pd.read_csv(DATA_PATH)

    df = df.dropna()

    print(f"Dataset size: {len(df)} rows")


    # --------------------------------------------------------
    # Encode categorical data
    # --------------------------------------------------------

    crop_encoder = LabelEncoder()
    market_encoder = LabelEncoder()

    df["crop"] = crop_encoder.fit_transform(
        df["crop"]
    )

    df["market"] = market_encoder.fit_transform(
        df["market"]
    )


    # --------------------------------------------------------
    # Features
    # --------------------------------------------------------

    features = [
        "crop",
        "market",
        "month",
        "temperature",
        "rainfall",
        "humidity",
        "price",
        "arrival"
    ]

    target = "demand"


    X = df[features]
    y = df[target]


    # --------------------------------------------------------
    # Train / Test split
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
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        min_child_weight=3,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        eval_metric="mae",
        tree_method="hist",
        random_state=42
    )


    print("Training demand forecasting model...")


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

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )


    print("\n==============================")
    print("DEMAND MODEL PERFORMANCE")
    print("==============================")

    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")


    # --------------------------------------------------------
    # Save model
    # --------------------------------------------------------

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model.save_model(
        MODEL_PATH
    )

    joblib.dump(
        crop_encoder,
        CROP_ENCODER_PATH
    )

    joblib.dump(
        market_encoder,
        MARKET_ENCODER_PATH
    )

    print("\nDemand model saved successfully.")


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    model = XGBRegressor()

    model.load_model(
        MODEL_PATH
    )

    crop_encoder = joblib.load(
        CROP_ENCODER_PATH
    )

    market_encoder = joblib.load(
        MARKET_ENCODER_PATH
    )

    return (
        model,
        crop_encoder,
        market_encoder
    )


# ============================================================
# PREDICT DEMAND
# ============================================================

def predict_demand(
    crop,
    market,
    month,
    temperature,
    rainfall,
    humidity,
    price,
    arrival
):

    model, crop_encoder, market_encoder = load_model()


    crop_encoded = crop_encoder.transform(
        [crop]
    )[0]

    market_encoded = market_encoder.transform(
        [market]
    )[0]


    input_data = pd.DataFrame([
        {
            "crop": crop_encoded,
            "market": market_encoded,
            "month": month,
            "temperature": temperature,
            "rainfall": rainfall,
            "humidity": humidity,
            "price": price,
            "arrival": arrival
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

    train_model()

    demand = predict_demand(
        crop="Potato",
        market="Jalpaiguri",
        month=10,
        temperature=24.5,
        rainfall=12.0,
        humidity=75,
        price=2100,
        arrival=1200
    )

    print("\n==============================")
    print("KISAAN SETU DEMAND FORECAST")
    print("==============================")

    print(
        f"Expected demand: {demand:.0f} kg"
    )
