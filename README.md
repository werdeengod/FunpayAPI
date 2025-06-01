# FunpayAPI

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A simple yet powerful Python library for interacting with FunPay (funpay.com) marketplace API.

## Features

- ✅ Account authentication
- 📦 Lot management
- ⭐ Review handling
- 🔄 Automatic session management
- 🚀 Async/await support

## Quick Start

### Using Context Manager
```python
from funpay import FunpayAPI

golden_key = "your_auth_key_here"

async def main():
    async with FunpayAPI(golden_key) as funpay:
        # Get all your lots
        lots = await funpay.lots.get()
        print(f"Found {len(lots)} active lots")
```

### Using Manual Login
```python
from funpay import FunpayAPI

golden_key = "your_auth_key_here"

async def main():
    funpay = await FunpayAPI(golden_key).login()
    lots = await funpay.lots.get()
    print(f"Found {len(lots)} active lots")
```

### Using decorator for get updates
```python
from funpay import FunpayAPI

golden_key = "your_auth_key_here"
funpay = FunpayAPI(golden_key)

@funpay.order_listener
async def order_listener(update: dict):
    print(update)
```