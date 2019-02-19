from sklearn.ensemble import RandomForestRegressor


def get_model(training_data, assessed_data):
    n_features = len(training_data[0])
    model = RandomForestRegressor(n_estimators=10, max_features=n_features, max_depth=None, min_samples_split=2, n_jobs=-1)
    model.fit(training_data, assessed_data)
    return model
