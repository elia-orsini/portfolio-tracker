import requests
import json

base = "https://api.covalenthq.com"
key = "ckey_c9ff6042010f4c8e923c9e21615"
address = "0x734269BF7aC3F3f644Bd4037EDcE162316117625"

url = base + "/v1/56/address/" + address + "/balances_v2/?key=" + key
result = requests.get(url).json()

tokens = [[token['balance'], token['contract_decimals'], token['quote_rate'], token['contract_address'], token['contract_ticker_symbol']] for token in result['data']["items"]]
tokens_values = []
for token in tokens:
	if token[4] == 'ETH':
		continue
	divider = len(token[0]) - int(token[1])
	integer = int(token[0][:divider]) if token[0][:divider] else 0
	decimals = int(token[0][divider : divider + 3]) / 1000 if token[0][divider : divider + 3] else 0
	value = integer + decimals
	
	if token[2]:
		tokens_values.append([token[4], value, value * token[2]])
#print(tokens_values)
#print(sum(map(lambda t: t[2], tokens_values)))


url = base + "/v1/1/address/" + address + "/portfolio_v2/?key=" + key
result = requests.get(url).json()

prices_range = []

for token_price in result['items']:
	temp = []
	for price_point in token_price['holdings']:
		temp.append(price_point['close']['quote'])
	prices_range.append(temp)

portfolio_value = []
for i in range(30):
	temp = 0
	for p in prices_range:
		temp += p[i]
	portfolio_value.append(str(temp))

portfolio_value = ' '.join(portfolio_value)
times = map(lambda i: str(i), range(30))
times = ' '.join(times)




from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def output():
    return render_template("index.html", weeklyValues=portfolio_value, weeklyTimes=times)

if __name__ == "__main__":
	app.run()








