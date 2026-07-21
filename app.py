import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://jsonplaceholder.typicode.com"
EXECUTION_MODE = None

# ---------------- GET ----------------
def get_request(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.get(
        url,
        timeout=5
    )
    print(f"[{EXECUTION_MODE}] [GET] {url} - Status: {response.status_code}")
    return response.status_code

# ---------------- POST ----------------
def post_request(index):
    payload = {
        "title": f"titulo-{index}",
        "body": "conteudo",
        "userId": 1
    }
    url = f"{BASE_URL}/posts"
    response = requests.post(
        url,
        json=payload,
        timeout=5
    )
    print(f"[{EXECUTION_MODE}] [POST] {url} - Status: {response.status_code}")
    return response.status_code

# ---------------- PATCH ----------------
def patch_request(post_id):
    payload = {
        "title": "titulo atualizado"
    }
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.patch(
        url,
        json=payload,
        timeout=5
    )
    print(f"[{EXECUTION_MODE}] [PATCH] {url} - Status: {response.status_code}")
    return response.status_code

# ---------------- DELETE ----------------
def delete_request(post_id):
    url = f"{BASE_URL}/posts/{post_id}"
    response = requests.delete(
        url,
        timeout=5
    )
    print(f"[{EXECUTION_MODE}] [DELETE] {url} - Status: {response.status_code}")
    return response.status_code

# =========================================================
# SINGLE THREAD
# =========================================================

def run_single_thread():
    global EXECUTION_MODE
    EXECUTION_MODE = "SINGLE THREAD"
    inicio = time.time()

    for i in range(1, 50):
        get_request(i)
        post_request(i)
        patch_request(i)
        delete_request(i)

    fim = time.time()

    print("\n===== SINGLE THREAD =====")
    print(f"Total time: {fim - inicio:.2f} seconds")


# =========================================================
# MULTITHREAD
# =========================================================

def worker(i):
    get_request(i)
    post_request(i)
    patch_request(i)
    delete_request(i)

def run_multithread():
    global EXECUTION_MODE
    EXECUTION_MODE = "MULTITHREAD"
    inicio = time.time()

    with ThreadPoolExecutor(max_workers=20) as executor: # number of threads
        executor.map(worker, range(1, 50)) # number of tasks = 101

    fim = time.time()

    print("\n===== MULTITHREAD =====")
    print(f"Total time: {fim - inicio:.2f} seconds")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    #run_single_thread()
    run_multithread()