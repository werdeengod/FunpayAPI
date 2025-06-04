from funpay import FunpayAPI

golden_key = ''


async def up_lots():
    funpay = await FunpayAPI(golden_key).login()
    data = await funpay.lots.up()
    print(data)


async def get_lots():
    funpay = await FunpayAPI(golden_key).login()
    lots = await funpay.lots.all()
    print(lots)


async def get_reviews():
    funpay = await FunpayAPI(golden_key).login()
    reviews = await funpay.reviews.all()
    print(reviews)


