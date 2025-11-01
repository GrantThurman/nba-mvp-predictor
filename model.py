import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

all_df = pd.read_csv("all_data.csv")

features = ["GP",
            "MIN",
            "PTS",
            "PTS_PER_MIN",
            "AST",
            "AST_PER_MIN",
            "REB",
            "REB_PER_MIN",
            "FGA", 
            "FG_PCT", 
            "FG3A", 
            "FG3_PCT", 
            "FTA", 
            "FT_PCT",
            "STL",
            "BLK",
            "EFFICIENCY",
            "PLUS_MINUS", 
            "TEAM_W_PCT"]

X = all_df[features]
y = all_df["MVP_PCT_SHARE"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=5
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("R²: ", r2_score(y_true=y_test, y_pred=y_pred))
print("RMSE: ", np.sqrt(mean_squared_error(y_true=y_test, y_pred=y_pred)))
