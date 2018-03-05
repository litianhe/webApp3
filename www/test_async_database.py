import asyncio
import aiomysql


async def test_example(loop):
    conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                  #user='root', password='PASSW0RD',
                                  user='www-data', password='www-data',
                                  db='awesome',loop=loop)

    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM blogs")
        print(cur.description)
        r = await cur.fetchall()
        print(r)
    conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))