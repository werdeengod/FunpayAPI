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
        lots = await funpay.lots.all()
        print(f"Found {len(lots)} active lots")
```

### Using Manual Login
```python
from funpay import FunpayAPI

golden_key = "your_auth_key_here"

async def main():
    funpay = await FunpayAPI(golden_key).login()
    lots = await funpay.lots.all()
    print(f"Found {len(lots)} active lots")
```
## Get Updates
### Blocking startup
```python
import asyncio
from funpay import FunpayAPI

golden_key = 'your_auth_key_here'
runner = FunpayAPI(golden_key).get_runner()

@runner.listener("message")
async def message_handler(update: dict):
    print(update)

if __name__ == "__main__":
    asyncio.run(runner.run_forever())
```
### Background startup
```python
import asyncio
from funpay import FunpayAPI

golden_key = 'your_auth_key_here'
runner = FunpayAPI(golden_key).get_runner()

@runner.listener("message")
async def message_handler(update: dict):
    print(update)
    
async def main():
    await runner.start()

if __name__ == "__main__":
    asyncio.run(main())
```