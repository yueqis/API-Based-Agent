import json
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

# Define the date range
today = datetime.strptime('2023-06-12', '%Y-%m-%d')
four_months_ago = today - timedelta(days=4 * 30)  # Approximate 4 months as 120 days

# Format the dates
start_date = four_months_ago.strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')
print(start_date, end_date)

# Define the API endpoint and headers
api_endpoint = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770/rest/default/V1/orders'
headers = {
    'Authorization': 'Bearer eyJraWQiOiIxIiwiYWxnIjoiSFMyNTYifQ.eyJ1aWQiOjEsInV0eXBpZCI6MiwiaWF0IjoxNzIwNjg4MDU1LCJleHAiOjE3MjA2OTE2NTV9.Q6mG84nSe6bQ5QfELQLS93M9cqP5AgXzQCtMqvN0oj0',
    'Content-Type': 'application/json',
}

# Define the query parameters
params = {
    'searchCriteria[filterGroups][0][filters][0][field]': 'status',
    'searchCriteria[filterGroups][0][filters][0][value]': 'complete',
    'searchCriteria[filterGroups][0][filters][0][conditionType]': 'eq',
    'searchCriteria[filterGroups][1][filters][0][field]': 'created_at',
    'searchCriteria[filterGroups][1][filters][0][value]': f'{start_date} 00:00:00',
    'searchCriteria[filterGroups][1][filters][0][conditionType]': 'gteq',
    'searchCriteria[filterGroups][2][filters][0][field]': 'created_at',
    'searchCriteria[filterGroups][2][filters][0][value]': f'{end_date} 23:59:59',
    'searchCriteria[filterGroups][2][filters][0][conditionType]': 'lteq',
    'searchCriteria[filterGroups][3][filters][0][field]': 'customer_email',
    'searchCriteria[filterGroups][3][filters][0][value]': 'emma.lopez@gmail.com',
    'searchCriteria[filterGroups][3][filters][0][conditionType]': 'eq',
}

# Make the API call
# response = requests.get(api_endpoint, headers=headers, params=params)
# print(len(response.json()['items']))
# with open("test.json", "w") as f:
#     json.dump(response.json(), f, indent=4)


def get_shopping_admin_auth_token():
    ENDPOINT = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770'
    response = requests.post(
        url=f'{ENDPOINT}/rest/default/V1/integration/admin/token',
        headers={'content-type': 'application/json'},
        data=json.dumps({'username': 'admin', 'password': 'admin1234'}),
    )
    return response.json()


def get_shopping_customer_auth_token():
    ENDPOINT = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770'
    response = requests.post(
        url=f'{ENDPOINT}/rest/default/V1/integration/customer/token',
        headers={'content-type': 'application/json'},
        data=json.dumps(
            {'username': 'emma.lopez@gmail.com', 'password': 'Password.123'}
        ),
    )
    return response.json()


def post_cart():
    api_endpoint = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770/rest/default/V1/carts/mine'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_shopping_customer_auth_token()}',
    }
    response = requests.post(api_endpoint, headers=headers)
    print(response)
    return response.json()


def add_cart(sku='B00CPTR7WS'):
    quote_id = post_cart()
    payload = {'cartItem': {'sku': sku, 'qty': 1, 'quote_id': quote_id}}
    api_endpoint = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770/rest/default/V1/carts/mine/items'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_shopping_customer_auth_token()}',
    }
    response = requests.post(api_endpoint, headers=headers, json=payload)
    print(response)
    print(response.json())


def get_product_by_sku(sku):
    api_endpoint = f'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770/rest/default/V1/products/{sku}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_shopping_admin_auth_token()}',
    }
    response = requests.get(api_endpoint, headers=headers)
    response = response.json()
    print(response)


# get_product('B00CPTR7WS')


def get_product_by_name(name):
    api_endpoint = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770/rest/default/V1/search'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_shopping_admin_auth_token()}',
    }
    search_params = {
        'searchCriteria[requestName]': 'quick_search_container',
        'searchCriteria[filterGroups][0][filters][0][field]': 'search_term',  # "name",
        'searchCriteria[filterGroups][0][filters][0][value]': name,
        'fields': 'items[price,name,sku]',
        # "searchCriteria[filterGroups][0][filters][0][conditionType]": "eq",
    }
    response = requests.get(api_endpoint, headers=headers, params=search_params)
    response = response.json()
    print(response)


with requests.Session() as s:
    r = s.get('http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/login')
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('input', attrs={'name': '_csrf_token'})['value']
    payload = {
        '_csrf_token': csrf_token,
        '_username': 'MarvelsGrantMan136',
        '_password': 'test1234',
        '_remember_me': 'on',
    }
    r1 = s.post(
        'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/login_check',
        data=payload,
    )
    cookie = requests.utils.dict_from_cookiejar(s.cookies)
    print(cookie)
    # s.cookies.update(cookie)
    # r = s.get("http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/comments/2561511", headers={"X-Experimental-API":"1"})
    # print(r.json())

    # commented_id = 2402719
    # comment_update_url = f"http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/comments/{commented_id}"
    # updated_comment_data = {
    #     "body": "New comment body content"
    # }
    # headers = {
    #     "X-Experimental-API": "1",
    #     "Content-Type": "application/json",
    # }
    # data_payload = updated_comment_data
    # response = s.post(comment_update_url, cookies=s.cookies, headers=headers, json=data_payload)
    # print(response)
    # print(response.text)
    forum_name = 'new_forum_test'
    new_forum_url = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/submissions/2'
    forum_data = {
        'name': forum_name,
        'title': forum_name,
        'sidebar': forum_name,
        'description': forum_name,
    }
    headers = {
        'X-Experimental-API': '1',
        'Content-Type': 'application/json',
    }
    data_payload = forum_data
    response = s.put(
        new_forum_url, cookies=s.cookies, headers=headers, json=data_payload
    )
    print(response)
    print(response.text)
