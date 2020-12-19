import requests
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img = os.path.join(BASE_DIR, 'media/tests/logo.png')
url = 'http://anickone.pythonanywhere.com/products/'
# url = 'http://127.0.0.1:8000/products/'


def create(url, auth, payload, files):
    response = requests.request(
        "POST",
        url,
        auth=auth,
        data=payload,
        files=files)
    obj = response.json()
    return obj['url']


def update(url, auth, payload, files):
    requests.request("PUT", url, auth=auth, data=payload, files=files)


def full_db(num_products, auth):
    fd = open(img, 'rb')
    files = {'logo': fd}
    for i in range(1, num_products + 1):
        payload = {
            "name": f"product name {i}",
            "description": f"description product {i}",
        }
        print(f'create product {i}')
        product_url = create(url, auth, payload, files)
        if i % 2:
            files['logo'].seek(0)
            payload = {
                "name": f"product name {i} update",
                "description": f"description product {i} update",
            }
            update(product_url, auth, payload, files)
        files['logo'].seek(0)


def main():
    print('create products by admin')
    auth = ('admin', 'weyfvbgfhjkm')
    full_db(20, auth)
    print('create products by demo user')
    auth = ('demo', 'weyfvbgfhjkm')
    full_db(10, auth)


if __name__ == "__main__":
    main()
