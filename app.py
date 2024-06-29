import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask import Flask ,send_file

app = Flask(__name__)

@app.route('/bitcoin')
def plot():
    url = 'https://api.coindesk.com/v1/bpi/currentprice.json'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        time_updated = data['time']['updated']
        bpi_data = data['bpi']
        
        df = pd.DataFrame.from_dict(bpi_data, orient='index')
        df['time_updated'] = pd.to_datetime(time_updated)
        
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['rate_float'], marker='o', linestyle='-', color='b')
        
        for index, value in enumerate(df['rate_float']):
            plt.annotate(f"{value:.2f}", (df.index[index], value), textcoords="offset points", xytext=(0,5), ha='center')
        
        plt.title(f'Bitcoin Price Index\nLast Updated: {time_updated}')
        plt.xlabel('Currency')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        
        plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        plt.close()
        
        return f"<img src='data:image/png;base64,{plot_data}'/>"
    
    else:
        return f"Failed to retrieve data. HTTP Status code: {response.status_code}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
