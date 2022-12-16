from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import math

def run_model(df, features, labels):
	X = df[features]
	y = df[labels]
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 21)
	sc = StandardScaler()
	X_train = sc.fit_transform(X_train)
	X_test = sc.transform(X_test)
	regr = LinearRegression()
	regr.fit(X_train, y_train)
	y_pred=regr.predict(X_test)
	score = regr.score(X_test, y_test)
	mse = mean_squared_error(y_test, y_pred)
	mrse = math.sqrt(mse)
	return score, mse, mrse