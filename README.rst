## Example SDK usage - Python
> The below code covers a scenario for some back-end system where some process must fetch stock data from a database (e.g. MySQL) and process this data so that it is in a format required by the client to display, based on a ticker symbol and fetching and processing this data is expensive. Caching the data provides a way of speeding up this process.
 
```python
from GhostDB.cache import Cache

cache = Cache("my_ghostdb.conf")

def getStockData(ticker_smbl):
    # Fetch data from cache
    stock_data = cache.get(ticker_smbl)

    if not stock_data:
        # Fetch from MySQL.
        # After any processing, we can 
        # assume our computed value is stored in
        # a variable called stock_data
    
        # Store result in cache
        cache.put(ticker_smbl, stock_data)
    return stock_data

return getStockData("AMZN")

```
