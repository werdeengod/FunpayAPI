from funpay import FunpayAPI


golden_key = ''


async def up_lots():
    async with FunpayAPI(golden_key) as funpay:
        data = await funpay.lot_service.up()
        print(data)


async def get_lots():
    async with FunpayAPI(golden_key) as funpay:
        lots = await funpay.account_service.lots()
        print(lots)


async def get_reviews():
    async with FunpayAPI(golden_key) as funpay:
        reviews = await funpay.account_service.reviews()
        print(reviews)
