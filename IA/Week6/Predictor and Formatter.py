import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score

matches = pd.read_csv("C:\Coding\IA\Week6\matches2.csv", index_col = 0)
matches["date"] = pd.to_datetime(matches["date"])
matches["venue_code"] = matches["venue"].astype("category").cat.codes
matches["opp_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].astype("int")
matches["day_code"] = matches["date"].dt.dayofweek
matches["target"] = (matches["result"] == "W").astype("int")
matches["season"] = matches["season"].astype("category").cat.codes

rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=2)
train = matches[matches["date"] < "2022-05-05"]
test = matches[matches["date"] > "2022-05-05"]
predictors = ["venue_code", "opp_code", "hour", "day_code","season"]
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
    train = data[data["date"] < '2022-08-13']
    test = data[data["date"] > '2022-08-13']
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], predicted=preds), index=test.index)
    error = precision_score(test["target"], preds)
    return combined, error
combined, error = make_predictions(matches_rolling, predictors + new_cols)
combined = combined.merge(matches_rolling[["date", "team", "opponent", "result"]], left_index=True, right_index=True)

combined["date"] = pd.to_datetime(combined["date"])
combined = combined[["date","team","opponent","predicted", "actual"]]
combined["predicted"] = combined["predicted"].map({1:"win",0:"lose or draw"})
combined["actual"] = combined["actual"].map({1:"win",0:"lose or draw"})

class MissingDict(dict):
    __missing__ = lambda self, key: key

map_values = {"Brighton and Hove Albion": "Brighton", "Manchester Utd": "Manchester United", "Newcastle Utd": "Newcastle United", "Tottenham Hotspur": "Tottenham", "West Ham United": "West Ham", "Wolverhampton Wanderers": "Wolves","Sheffield Utd": "Sheffield United","Nott'ham Forest":"Nottingham Forest"}  
mapping = MissingDict(**map_values)
combined["team"] = combined["team"].map(mapping)

combined.to_csv("C:\Coding\IA\Week6\FormattedDF.csv")

print(error)