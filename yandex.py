import requests


class YANDEXAPIClient:
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources/'
    headers = {
  'Content-Type': 'application/json',
  'Authorization': 'OAuth y0_AgAAAAABnMNfAAq0uAAAAADv9DRBiy5mUYgHS5qp_p4rRHetJ5anXJI'
            }
    def __init__(self, token):
        token = token
        self.headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'OAuth {token}'
                    }
    
    def create_folder(self,path):
        params={'path': path}
        response = requests.put(self.BASE_URL, headers=self.headers, params=params)
        return response.json()
    
    # def upload_files(self, file, url):
    #     params={'path': file,
    #             'url': url}
    #     print(params)
    #     url = f"{self.BASE_URL}upload?path={file}&url={url}"
    #     print(url)
    #     # response = requests.post(url, headers=self.headers)
    #     response = requests.request("POST", url, headers=self.headers)
    #     print(response.status_code)
    #     print(response.json())
    #     return response.status_code
    def upload_files(self, file, file_url):
        # payload = {}
        params={'path': file,
                'url': file_url
              }
        url = f"{self.BASE_URL}upload"
        response = requests.request("POST", url, headers=self.headers, params=params)
        return response.status_code


yandex_oauth_url ='https://oauth.yandex.ru/authorize?response_type=token&client_id=9e41012c8acc438581178ef78642c3da'