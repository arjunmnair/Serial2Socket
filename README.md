# Serial2Socket

Access a device connected to a serial port on multiple devices through sockets. 

Example serial devices :
- Arduino (serial monitor)
- STM32
- Any other embedded device which can be accessed through a serial port.

## Requirements

- python3
- pip
- virtualenv (optional)

## Setup

- Create the virtualenv and activate it (optional) :

```bash
python3 -m virtualenv venv
source venv/bin/activate
```

- Install the requirements :

```bash
pip install -r requirements.txt
```

## Run

### Server side

- If a virtualenv was used, activate it (optional) :

```bash
source venv/bin/activate
```

- Run the application :

```bash
python3 Serial2Socket.py <serial_port> <serial_baudrate> <socket_port>
```

### Client side

Any sort of tool that can connect to a socket connection can be used. I use `nc`.

```bash
stty -icanon -echo && nc <ip> <port>
```

For example, if Serial2Socket is running locally at port 20000:

```bash
stty -icanon -echo && nc localhost 20000
```


## Donate

If this tool helped you and if you would like to make a donation :

- BTC : bc1qsgk9h2awez0yhfjz4c0hr02d4mhdldjdv8xvyk
- ETH : 0xEA4e5f988E8019EB324934403585cf1886952EB7
- XMR : 46CGrvx3a4cBrM4nvJXSJZjbWcdTfCDJZhjomRBgG3yVfCJLK84BguTDHnJwrZgmrqSJ6u8ZtRXv8ayNLdSiH4cjApgg4CX
