from .order import Order
from .constant import API_TYPE


class Payment(object):

    def __init__(self, base_url, token=None, apiType=API_TYPE.REDIRECT ,provider='Ksher', mid=None, timeout=10, verify=True):
        # remove suffix with /
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        
        self.order = Order(base_url,
                            apiType=apiType, 
                            token=token, 
                            provider=provider, 
                            mid=mid, 
                            timeout=timeout,
                            verify=verify)
        