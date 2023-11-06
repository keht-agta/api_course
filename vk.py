import requests


class VKAPIClient:
    API_BASE_URL = 'https://api.vk.com/method/'
    def __init__(self, token,user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return {
        'access_token': self.token,
        'v': '5.131'
        }
    
    def _build_url(self, api_metod):
        return f'{self.API_BASE_URL}/{api_metod}'
    
    def get_profile_photos(self):
        params = self.get_common_params()
        params.update({'owner_id': self.get_user_info()[0], 'album_id':'profile', 'extended': 1})
        response = requests.get(self._build_url('photos.get'), params=params)
        return response.json()
    
    def get_user_info(self):
        params = self.get_common_params()
        params.update({'user_id': self.user_id})
        response = requests.get(self._build_url('users.get'), params=params).json()
        user_id = response.get('response',{})[0].get('id',{})
        first_name = response.get('response',{})[0].get('first_name', {})
        last_name = response.get('response',{})[0].get('last_name',{})
        return user_id, first_name, last_name
    
url = 'https://oauth.vk.com/authorize?client_id=51776408&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=status%2Cphotos&response_type=token'



