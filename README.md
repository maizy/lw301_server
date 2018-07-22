# Emulate cloud server for Oregon Scientific LW301

## Installation

```
python3 setup.py install
```

## Usage

```
lw301_server
```

Available options:

```
lw301_server --help
```

## Catch LW301 traffic

_TODO_

### DNS

Domains resolved by LW301:

* `static.oregonscientific.com` – some init routines
* `gateway.weather.oregonscientific.com` - sending data
* `blackbox-c.infra.idtcsd.net` - ?


## API

### GET /api/history/temperature

```js
{
    "history": [
        {
            "timestamp": 1532271317,
            "utc_datetime": "2018-07-22 17:55:17",
            "value": {
                "celsius": 22.1,
                "channel": 1,
                "mac": "00001234abcd"
            }
        },
        // ...
    ],
    "measurement": "temperature"
}
```

### GET /api/history/humidity

```js
{
    "history": [
        {
            "timestamp": 1532271317,
            "utc_datetime": "2018-07-22 17:55:17",
            "value": {
                "channel": 1,
                "mac": "00001234abcd",
                "relative": 79
            }
        },
        // ...
    ],
    "measurement": "humidity"
}
```


### GET /api/history/pressure

```js
{
    "history": [
        {
            "timestamp": 1532271186,
            "utc_datetime": "2018-07-22 17:53:06",
            "value": {
                "hPa": 982,
                "mac": "00001234abcd",
                "mmHg": 736
            }
        },
        // ...
    ],
    "measurement": "pressure"
}
```


## Licence

Apache License 2.0
