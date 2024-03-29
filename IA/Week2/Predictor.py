import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score

matches = pd.read_csv("C:\Coding\IA\Week2\matches2.csv", index_col = 0)
matches["date"] = pd.to_datetime(matches["date"])
matches["venue_code"] = matches["venue"].astype("category").cat.codes
matches["opp_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].astype("int")
matches["day_code"] = matches["date"].dt.dayofweek
matches["target"] = (matches["result"] == "W").astype("int")

rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=2)
train = matches[matches["date"] < "2022-01-01"]
test = matches[matches["date"] > "2022-01-01"]
predictors = ["venue_code", "opp_code", "hour", "day_code"]
rf.fit(train[predictors],train["target"])
preds = rf.predict(test[predictors])

combined = pd.DataFrame(dict(actual= test["target"], predicted=preds))
precision_score(test["target"],preds)
grouped_matches = matches.groupby("team")
group = grouped_matches.get_group("Liverpool")
def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group
cols = ["gf","ga","sh","sot","dist","fk","pk","pkatt"]
new_cols = [f"{c}_rolling" for c in cols]
matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x,cols,new_cols))
matches_rolling = matches_rolling.droplevel("team")
matches_rolling.index = range(matches_rolling.shape[0])

def make_predictions(data, predictors):
    train = data[data["date"] < '2022-01-01']
    test = data[data["date"] > '2022-01-01']
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], predicted=preds), index=test.index)
    error = precision_score(test["target"], preds)
    return combined, error
combined, error = make_predictions(matches_rolling, predictors + new_cols)
combined = combined.merge(matches_rolling[["date", "team", "opponent", "result"]], left_index=True, right_index=True)

from pathlib import Path  
filepath = Path('C:\Coding\IA\Week2\predictions2.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
combined.to_csv(filepath)  
