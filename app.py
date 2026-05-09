import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://jsonplaceholder.typicode.com"

# ---------------- GET ----------------
def get_request(post_id):
    response = requests.get(
        f"{BASE_URL}/posts/{post_id}",
        timeout=5
    )

    return response.status_code

# ---------------- POST ----------------
def post_request(index):
    payload = {
        "title": f"titulo-{index}",
        "body": "conteudo",
        "userId": 1
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=5
    )

    return response.status_code

# ---------------- PATCH ----------------
def patch_request(post_id):
    payload = {
        "title": "titulo atualizado"
    }

    response = requests.patch(
        f"{BASE_URL}/posts/{post_id}",
        json=payload,
        timeout=5
    )

    return response.status_code


# ---------------- DELETE ----------------
def delete_request(post_id):
    response = requests.delete(
        f"{BASE_URL}/posts/{post_id}",
        timeout=5
    )

    return response.status_code


# =========================================================
# SINGLE THREAD
# =========================================================

def run_single_thread():
    inicio = time.time()

    for i in range(1, 21):
        get_request(i)
        post_request(i)
        patch_request(i)
        delete_request(i)

    fim = time.time()

    print("\n===== SINGLE THREAD =====")
    print(f"Tempo total: {fim - inicio:.2f} segundos")


# =========================================================
# MULTITHREAD
# =========================================================

def worker(i):
    get_request(i)
    post_request(i)
    patch_request(i)
    delete_request(i)



def run_multithread():
    inicio = time.time()

    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(worker, range(1, 21))

    fim = time.time()

    print("\n===== MULTITHREAD =====")
    print(f"Tempo total: {fim - inicio:.2f} segundos")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    run_single_thread()
    run_multithread()