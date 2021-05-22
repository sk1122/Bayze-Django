import facebook

from models import *

token = AccessTokens.objects.first()

graph = facebook.GraphAPI(access_token=token.token)

site_info = graph.get_object(id="https%3A//mobolic.com", fields="og_object")
print(site_info["og_object"]["description"])