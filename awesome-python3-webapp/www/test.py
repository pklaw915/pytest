import orm
from models import User
import asyncio


async def test_models(loop):
    await orm.create_pool(loop=loop, user='root', password='password', database='awesome')
    #u = User(name='Test', email='test@example.com', passwd='125241', image='about:blank')
    #await u.save()
    users = await User.findAll()
    print(users)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_models(loop))

