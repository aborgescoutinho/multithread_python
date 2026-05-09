import asyncio
import aiohttp
import time

BASE_URL = "https://jsonplaceholder.typicode.com"
EXECUTION_MODE = None

# =========================================================
# GET
# =========================================================

async def get_request(session, post_id):

    url = f"{BASE_URL}/posts/{post_id}"

    async with session.get(
        url,
        timeout=aiohttp.ClientTimeout(total=5)
    ) as response:

        print(
            f"[{EXECUTION_MODE}] [GET] "
            f"{url} - Status: {response.status}"
        )

        return response.status


# =========================================================
# POST
# =========================================================

async def post_request(session, index):

    payload = {
        "title": f"titulo-{index}",
        "body": "conteudo",
        "userId": 1
    }

    url = f"{BASE_URL}/posts"

    async with session.post(
        url,
        json=payload,
        timeout=aiohttp.ClientTimeout(total=5)
    ) as response:

        print(
            f"[{EXECUTION_MODE}] [POST] "
            f"{url} - Status: {response.status}"
        )

        return response.status


# =========================================================
# PATCH
# =========================================================

async def patch_request(session, post_id):

    payload = {
        "title": "titulo atualizado"
    }

    url = f"{BASE_URL}/posts/{post_id}"

    async with session.patch(
        url,
        json=payload,
        timeout=aiohttp.ClientTimeout(total=5)
    ) as response:

        print(
            f"[{EXECUTION_MODE}] [PATCH] "
            f"{url} - Status: {response.status}"
        )

        return response.status


# =========================================================
# DELETE
# =========================================================

async def delete_request(session, post_id):

    url = f"{BASE_URL}/posts/{post_id}"

    async with session.delete(
        url,
        timeout=aiohttp.ClientTimeout(total=5)
    ) as response:

        print(
            f"[{EXECUTION_MODE}] [DELETE] "
            f"{url} - Status: {response.status}"
        )

        return response.status


# =========================================================
# SINGLE THREAD / SEQUENCIAL
# =========================================================

async def run_single_thread():

    global EXECUTION_MODE

    EXECUTION_MODE = "ASYNC SINGLE"

    inicio = time.time()

    async with aiohttp.ClientSession() as session:

        for i in range(1, 50):

            await get_request(session, i)
            await post_request(session, i)
            await patch_request(session, i)
            await delete_request(session, i)

    fim = time.time()

    print("\n===== ASYNC SINGLE =====")
    print(f"Tempo total: {fim - inicio:.2f} segundos")


# =========================================================
# WORKER
# =========================================================

async def worker(session, i):

    await asyncio.gather(
        get_request(session, i),
        post_request(session, i),
        patch_request(session, i),
        delete_request(session, i)
    )


# =========================================================
# ASYNC MULTITASK
# =========================================================

async def run_async_multitask():

    global EXECUTION_MODE

    EXECUTION_MODE = "ASYNC MULTITASK"

    inicio = time.time()

    connector = aiohttp.TCPConnector(
        limit=100,              # máximo de conexões totais
        limit_per_host=50       # máximo por host
    )

    async with aiohttp.ClientSession(
        connector=connector
    ) as session:

        tasks = [
            worker(session, i)
            for i in range(1, 50)
        ]

        await asyncio.gather(*tasks)

    fim = time.time()

    print("\n===== ASYNC MULTITASK =====")
    print(f"Tempo total: {fim - inicio:.2f} segundos")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    asyncio.run(run_single_thread())
    asyncio.run(run_async_multitask())