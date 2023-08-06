# pybitflyer2 - a wrapper interface of Bitflyer lightning API

inspired by Ruby bitflyer gem https://github.com/unhappychoice/bitflyer

## Usage

See https://lightning.bitflyer.jp/docs for details.

## Requirements

- Python 3

## The Installation

From Pypi with the Python package manager:

```sh    
pip install pybitflyer2
```

## Examples

### HTTP API

See [http_public.py](https://github.com/fkshom/pybitflyer2/blob/master/src/pybitflyer2/http_public.py) / [http_private.rb](https://github.com/fkshom/pybitflyer2/blob/master/src/pybitflyer2/http_private.py) for method definition.

```py
from pybitflyer2 import Bitflyer
public_client = Bitflyer.http_public_client()
print(public_client.ticker(product_code='BTC_JPY'))

private_client = BitFlyer.http_private_client('YOUR_API_KEY', 'YOUR_API_SECRET')
private_client.send_child_order(
    product_code='BTC_JPY',
    child_order_type='LIMIT',
    side='BUY',
    price=30_000,
    size=0.1,
    minute_to_expire=10000,
    time_in_force='GTC',
)
#=> { "child_order_acceptance_id": "JRF20150707-050237-639234" }

private_client.cancel_child_order(
  "product_code": "BTC_JPY",
  "child_order_acceptance_id": "JRF20150707-033333-099999"
)
#=> None
```

### Realtime API

#### Public events

Channel name format is like `{event_name}_{product_code}`. You can set handler to get realtime events.

{event_name} and {product_code} is defined at [realtimeclient.py](https://github.com/fkshom/pybitflyer2/blob/master/src/bitflyer2/realtimeclient.py).

#### Private events

To subscribe to the private child_order_events and parent_order_events, pass your API key and secret when creating the realtime_client.

```py
import time
from pybitflyer2 import Bitflyer

def on_ticker_received(ticker):
    print(ticker)

def on_open():
    print('opened')

def on_error(err):
    print(err)

def on_message(msg):
    print(msg)

def on_close():
    print('closed')

client = Bitflyer.realtime_client()
client.subscribe(channel='lightning_ticker_BTC_JPY', handler=on_ticker_received)
client.subscribe(channel='lightning_ticker_ETH_JPY', handler=on_ticker_received)
client.on('open', handler=on_open)
client.on('error', handler=on_error)
client.on('message', handler=on_message)
client.on('close', handler=on_close)
client.start()

while True:
    time.sleep(1)
```

```json
# lightning_ticker_BTC_JPY
{
      "product_code": "BTC_JPY",
      "timestamp": "2019-04-11T05:14:12.3739915Z",
      "state": "RUNNING",
      "tick_id": 25965446,
      "best_bid": 580006,
      "best_ask": 580771,
      "best_bid_size": 2.00000013,
      "best_ask_size": 0.4,
      "total_bid_depth": 1581.64414981,
      "total_ask_depth": 1415.32079982,
      "market_bid_size": 0,
      "market_ask_size": 0,
      "ltp": 580790,
      "volume": 6703.96837634,
      "volume_by_product": 6703.96837634
}
```

```py
import time
from pybitflyer2 import Bitflyer

def on_ticker_received(ticker):
    print(ticker)

def on_private_event_received(event):
    print(event)

def on_open():
    print('opened')

def on_error(err):
    print(err)

def on_message(msg):
    print(msg)

def on_close():
    print('closed')

client = Bitflyer.realtime_client('YOUR_API_KEY', 'YOUR_API_SECRET')
client.subscribe(channel='lightning_ticker_BTC_JPY', handler=on_ticker_received)
client.subscribe(channel='lightning_ticker_ETH_JPY', handler=on_ticker_received)
client.subscribe(channel='child_order_events', handler=on_private_event_received)
client.on('open', handler=on_open)
client.on('error', handler=on_error)
client.on('message', handler=on_message)
client.on('close', handler=on_close)

while True:
    time.sleep(1)
```

```json
# child_order_events
[
    {
        "product_code": "BTC_JPY",
        "child_order_id": "JOR20150101-070921-038077",
        "child_order_acceptance_id": "JRF20150101-070921-194057",
        "event_date": "2015-01-01T07:09:21.9301772Z",
        "event_type": "ORDER",
        "child_order_type": "LIMIT",
        "side": "SELL",
        "price": 500000,
        "size": 0.12,
        "expire_date": "2015-01-01T07:10:21"
    }
]
```

## Contributing

Bug reports and pull requests are welcome on GitHub at https://github.com/fkshom/pybitflyer2. This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the Contributor Covenant code of conduct.

## License

The gem is available as open source under the terms of the MIT License.
