import json
import threading

import requests

def request_api(api_url, params=None):

    response = requests.post(api_url,json=params)

    if response.status_code != 200:
        print(f'请求异常{response.status_code}')
        print(response.text)
    else:
       print(response.text)


if __name__ == '__main__':
    url = "http://127.0.0.1:8888/login"
    num_threads = 10
    threads = []

    for n in range(num_threads):
        data={
            "username":"user"+str(n),
            "password":"password"+str(n),
        }

        json_data=json.dumps({"cc":"11"})
        t = threading.Thread(target=request_api, args=(url,json_data))
        threads.append(t)
        t.start()

    for t in threads:

        t.join()



