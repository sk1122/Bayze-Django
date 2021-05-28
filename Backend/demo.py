from lion.models import User
from tiger.models import AccessTokens

user = User.objects.filter(email='punekar.satyam@gmail.com').first()
token = AccessTokens.objects.first().token

def store_pages(token, user):
	graph = facebook.GraphAPI(access_token=token) # GraphAPI is FB's API for Querying
	page_data = graph.get_object('me/accounts') # Get data from https://graph.facebook.com/me/accounts
	resp = graph.get_object('me', 'accounts&page=' + page_data['paging']['cursors']['next'])
	print(resp)

	for page in page_data.get('data', {}):
		page_id = page["id"]
		page_name = page["name"]
		category = page["category_list"]

		# Check if Page already exists
		page_data = FacebookPages.objects.filter(page_id=page_id).first()

		if page_data is None:
			page_data = FacebookPages.objects.create(user=user, page_id=page_id, page=page_name, category=category)
		else:
			page_data.page_id = page_id
			page_data.page = page_name
			page_data.category = category

store_pages(token, user)