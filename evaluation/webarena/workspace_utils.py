import json
import os
import re


def replace_substrings(match):
    return '1234567'


# input yaml formatted api, get md file for that api
def get_md_by_api(api):
    yaml_api_sub = re.sub(r'\{[^}]+\}', '1234567', api)
    method = yaml_api_sub.split(' ')[0]
    if '/api/v4/' not in yaml_api_sub:
        return None
    yaml_api = (yaml_api_sub.split(' ')[1]).split('/api/v4/')[1]
    entries = os.listdir('gitlab_api')
    for entry in entries:
        md_file = os.path.join('gitlab_api', entry)
        if not (os.path.isfile(md_file) and md_file.endswith('.md')):
            continue
        with open(md_file, 'r') as file:
            data = file.read()
        test = re.sub(r':\w+', replace_substrings, data)
        if (
            f'{method.upper()} {yaml_api}\n' in test
            or f'{method.upper()} /{yaml_api}\n' in test
        ):
            if f'{method.upper()} {yaml_api}\n' in test:
                mdapi_sub = f'{method.upper()} {yaml_api}\n'
            if f'{method.upper()} /{yaml_api}\n' in test:
                mdapi_sub = f'{method.upper()} /{yaml_api}\n'
            index = test.find(mdapi_sub)
            start = data.rfind('## ', 0, index)
            end = data.find('## ', start + 3)
            if end == -1:
                return (data[start:]).strip()
            else:
                return (data[start:end]).strip()
    return f'No such API found: {api}.'


def get_api_documentation_gitlab(api: str) -> str:
    """
    Returns the markdown documentation of the given API.
    Args: api: str: The API whose documentations to retrieve. For example, 'get /api/v4/projects/{id}/repository/commits'.
    """
    return get_md_by_api(api)


def get_shopping_readme():
    with open('shopping_readme/performing-searches.md', 'r') as f:
        searchCriteriaDoc = f.read()
    with open('shopping_readme/retrieve-filtered-responses.md', 'r') as f:
        retrieveFilteredDoc = f.read()
    with open('shopping_readme/search-endpoint.md', 'r') as f:
        searchDoc = f.read()
    with open('shopping_readme/order-create-quote.md', 'r') as f:
        quoteDoc = f.read()
    with open('shopping_readme/order-add-items.md', 'r') as f:
        itemDoc = f.read()
    with open('shopping_readme/order-shipping-cost.md', 'r') as f:
        shipCostDoc = f.read()
    with open('shopping_readme/order-shipping-billing.md', 'r') as f:
        shipBillDoc = f.read()
    with open('shopping_readme/order-create-order.md', 'r') as f:
        orderDoc = f.read()
    return (
        searchCriteriaDoc,
        retrieveFilteredDoc,
        searchDoc,
        quoteDoc,
        itemDoc,
        shipCostDoc,
        shipBillDoc,
        orderDoc,
    )


def get_shopping_html_api_doc(html_page):
    shopping_html_api_doc = {
        'description': f'Retrieve the content in the HTML page {html_page}',
        'responses': {
            '200': {
                'description': '200 Success.',
                'content': {
                    'text/plain:': {
                        'schema': {
                            'type': 'string',
                            'example': "<!doctype html>\n<html lang='en'>\n ..... SOME HTML CONTENT ..... </html>\n",
                        }
                    }
                },
            },
            'default': {
                'description': 'Unexpected error',
                'content': {
                    'text/plain:': {
                        'schema': {'$ref': '#/components/schemas/error-response'}
                    }
                },
            },
        },
    }
    return shopping_html_api_doc


def get_api_documentation_shopping(
    apis: list[str], html_pages='html_page_shopping_abcdefg'
):
    file = 'shopping-admin.json'
    output = {}
    output['server_url'] = (
        'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/rest/default'
    )
    paths = {}
    components = {}
    with open(file, 'r') as f:
        data = json.load(f)
    if isinstance(apis, str):
        apis = [apis]
    if html_pages != []:
        for html_page in html_pages:
            paths[html_page] = {'get': get_shopping_html_api_doc(html_page)}
    for api in apis:
        if 'V1/carts/mine' in api:
            if 'get /V1/products' not in apis:
                apis.append('get /V1/products')
            if 'post /V1/carts/mine' not in apis:
                apis.append('post /V1/carts/mine')
            break
    for api in apis:
        method = api.split(' ')[0]
        method = method.lower()
        call = api.split(' ')[1]
        if not call.startswith('/'):
            call = '/' + call
        if call[1] == 'v':
            call = call[0] + 'V' + call[2:]
        try:
            path = data['paths'][call][method]
            if call in paths:
                paths[call][method] = path
            else:
                paths[call] = {method: path}
        except Exception:
            print(f'API {api} does not exist')
    paths_str = str(paths)
    while True:
        new = False
        for component in data['components']['requestBodies']:
            if f"'#/components/requestBodies/{component}'" in paths_str + str(
                components
            ):
                if component not in components:
                    components[component] = data['components']['requestBodies'][
                        component
                    ]
                    new = True
        for component in data['components']['schemas']:
            if f"'#/components/schemas/{component}'" in paths_str + str(components):
                if component not in components:
                    components[component] = data['components']['schemas'][component]
                    new = True
        if new == False:
            break
    output['paths'] = paths
    output['components'] = components
    output = str(output)
    (
        searchCriteriaDoc,
        retrieveFilteredDoc,
        searchDoc,
        quoteDoc,
        itemDoc,
        shipCostDoc,
        shipBillDoc,
        orderDoc,
    ) = get_shopping_readme()
    doc = (
        'Below is some specific explanations and examples on how to use search and filter responses.\n'
        + retrieveFilteredDoc
    )
    if 'searchCriteria' in output:
        doc += searchCriteriaDoc
    elif 'get /V1/products' in apis:
        doc += searchCriteriaDoc
    if 'get /V1/search' in apis or 'get /V1/products' in apis:
        doc += searchDoc
    if '/V1/carts/mine' in output:
        doc += quoteDoc
        doc += itemDoc
    if 'estimate-shipping-methods' in output:
        doc += shipCostDoc
    if 'payment' in output or 'order' in output:
        doc += orderDoc
    if 'shipping' in output or 'billing' in output:
        doc += shipBillDoc
    doc += '\n'
    return doc + output


test = get_api_documentation_shopping(['get /V1/orders'])
with open('test.txt', 'w') as f:
    f.write(test)


def get_api_documentation_map(api: str) -> str:
    file = 'map.txt'
    with open(file, 'r') as f:
        f = f.readlines()
    f = [line for line in f if line.strip() != '']
    title = ''
    output = ''
    output += f[0]
    api_start_index = 0
    title_start_index = 0
    for i in range(len(f)):
        line = f[i]
        if '===' in line and ('====') not in line and f'<tt>{api}</tt>' in line:
            api_start_index = i
            break
    for i in range(api_start_index, 0, -1):
        line = f[i]
        if '==' in line and '===' not in line:
            title_start_index = i
            break
    title_end_index = api_start_index
    for i in range(title_start_index + 1, api_start_index, 1):
        line = f[i]
        if ('===' in line and ('====') not in line) or (
            '==' in line and ('===') not in line
        ):
            title_end_index = i
            break
    title = ''.join(f[title_start_index:title_end_index])
    api_end_index = len(f)
    for i in range(api_start_index + 1, len(f), 1):
        line = f[i]
        if ('===' in line and ('====') not in line) or (
            '==' in line and ('===') not in line
        ):
            api_end_index = i
            break
    api_doc = ''.join(f[api_start_index:api_end_index])
    return title + api_doc

from bs4 import BeautifulSoup
import requests

BASE_URL = "http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999"
# create a session and login
s = requests.Session()
r = s.get(f"{BASE_URL}/login")
soup = BeautifulSoup(r.content, 'html.parser')
csrf_token = soup.find('input', attrs={'name': '_csrf_token'})['value']

payload = {'_csrf_token': csrf_token ,'_username':'MarvelsGrantMan136', '_password':'test1234', '_remember_me': 'on'}

s.post(f"{BASE_URL}/login_check", data=payload)

# APIs regarding subscriptions
def subscribe_forum(forum_name):
    # forum_name: str, forum_name, e.g. "relationship_advice"
    r = s.get(f"{BASE_URL}/f/{forum_name}")
    soup = BeautifulSoup(r.content, 'html.parser')

    csrf_token = soup.find('form', {'class': 'subscribe-form'}).find('input', attrs={'name': 'token'})['value']

    r = s.post(f"{BASE_URL}/f/{forum_name}/subscribe.json", files=dict(token=(None, csrf_token)))
    return r.json()

def unsubscribe_forum(forum_name):
    # forum_name: str, forum_name, e.g. "relationship_advice"
    r = s.get(f"{BASE_URL}/f/{forum_name}")
    soup = BeautifulSoup(r.content, 'html.parser')

    csrf_token = soup.find('form', {'class': 'subscribe-form'}).find('input', attrs={'name': 'token'})['value']

    r = s.post(f"{BASE_URL}/f/{forum_name}/unsubscribe.json", files=dict(token=(None, csrf_token)))
    return r.json()

# APIs regarding voting submissions
def get_submission_votes(submission_id):
    # submission_id: int, submission id
    r = s.get(f"{BASE_URL}/{submission_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    votes = int(soup.find('span', {'class': 'vote__net-score'}).contents[0].replace('−', '-'))
    return votes

def upvote_submission(submission_id):
    # submission_id: int, submission id
    r = s.get(f"{BASE_URL}/{submission_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'data-vote-route-value': 'submission_vote'}).find('input', attrs={'name': 'token'})['value']

    r = s.post(f"{BASE_URL}/sv/{submission_id}.json", files=dict(token=(None, csrf_token), choice=(None, 1)))
    return r.json()

def downvote_submission(submission_id):
    # submission_id: int, submission id
    r = s.get(f"{BASE_URL}/{submission_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'data-vote-route-value': 'submission_vote'}).find('input', attrs={'name': 'token'})['value']

    r = s.post(f"{BASE_URL}/sv/{submission_id}.json", files=dict(token=(None, csrf_token), choice=(None, -1)))
    return r.json()

def unvote_submission(submission_id):
    # submission_id: int, submission id
    r = s.get(f"{BASE_URL}/{submission_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'data-vote-route-value': 'submission_vote'}).find('input', attrs={'name': 'token'})['value']

    r = s.post(f"{BASE_URL}/sv/{submission_id}.json", files=dict(token=(None, csrf_token), choice=(None, 0)))
    return r.json()

def get_all_comments():
    r = s.get("http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/comments", headers={"X-Experimental-API":"1"})
    return r.json()

def get_comment_by_id(comment_id):
    # comment_id: int, comment id
    r = s.get(f"http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/comments/{comment_id}", headers={"X-Experimental-API":"1"})
    return r.json()

def update_comment_by_id(comment_id, new_comment_content):
    comment_update_url = f"http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/comments/{comment_id}"
    updated_comment_data = {
        "renderedBody": new_comment_content
    }
    headers = {
        "X-Experimental-API": "1",
        "Content-Type": "application/json",
    }
    data_payload = updated_comment_data
    response = s.put(comment_update_url, cookies=s.cookies, headers=headers, json=data_payload)
    return response.text

# APIs regarding voting comments under a submission
def get_comment_votes(submission_id, comment_id):
    # submission_id: int, submission id
    # comment_id: int, comment id
    r = s.get(f"{BASE_URL}/{submission_id}")
    redir_url = r.url.rsplit('/', 1)[0]

    r = s.get(f"{redir_url}/-/comment/{comment_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    votes = int(soup.find('form', attrs={'data-vote-route-value': 'comment_vote'}).find('span', {'class': 'vote__net-score'}).contents[0].replace('−', '-'))
    return votes

def upvote_comment(submission_id, comment_id):
    # submission_id: int, submission id
    # comment_id: int, comment id
    r = s.get(f"{BASE_URL}/{submission_id}")
    redir_url = r.url.rsplit('/', 1)[0]

    r = s.get(f"{redir_url}/-/comment/{comment_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'data-vote-route-value': 'comment_vote'}).find('input', attrs={'name': 'token'})['value']
    r = s.post(f"{BASE_URL}/cv/{comment_id}.json", files=dict(token=(None, csrf_token), choice=(None, 1)))
    return r.json()

def downvote_comment(submission_id, comment_id):
    # submission_id: int, submission id
    # comment_id: int, comment id
    r = s.get(f"{BASE_URL}/{submission_id}")
    redir_url = r.url.rsplit('/', 1)[0]

    r = s.get(f"{redir_url}/-/comment/{comment_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'data-vote-route-value': 'comment_vote'}).find('input', attrs={'name': 'token'})['value']
    r = s.post(f"{BASE_URL}/cv/{comment_id}.json", files=dict(token=(None, csrf_token), choice=(None, -1)))
    return r.json()

def unvote_comment(submission_id, comment_id):
    # submission_id: int, submission id
    # comment_id: int, comment id
    r = s.get(f"{BASE_URL}/{submission_id}")
    redir_url = r.url.rsplit('/', 1)[0]

    r = s.get(f"{redir_url}/-/comment/{comment_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'data-vote-route-value': 'comment_vote'}).find('input', attrs={'name': 'token'})['value']
    r = s.post(f"{BASE_URL}/cv/{comment_id}.json", files=dict(token=(None, csrf_token), choice=(None, 0)))
    return r.json()

# API posting comment under a submission
def post_comment(submission_id, comment):
    # submission_id: int, submission id
    # comment: str, comment content
    r = s.get(f"{BASE_URL}/{submission_id}")
    redir_url = r.url.rsplit('/', 1)[0]

    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'class': 'comment-form'}).find('input', attrs={'name': f'reply_to_submission_{submission_id}[_token]'})['value']
    payload = {f'reply_to_submission_{submission_id}[_token]': (None, csrf_token), 
               f'reply_to_submission_{submission_id}[comment]': (None, comment),
               f'reply_to_submission_{submission_id}[userFlag]': (None, 'none'),
               f'reply_to_submission_{submission_id}[email]': (None, '')}
    r = s.post(f"{redir_url}/-/comment", files=payload)
    return r.url

# API replying comment under a comment
def reply_comment(submission_id, comment_id, comment):
    # submission_id: int, submission id
    # comment_id: int, comment id to reply to
    # comment: str, comment content
    r = s.get(f"{BASE_URL}/{submission_id}")
    redir_url = r.url.rsplit('/', 1)[0]

    r = s.get(f"{redir_url}/-/comment/{comment_id}")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'class': 'comment-form'}).find('input', attrs={'name': f'reply_to_comment_{comment_id}[_token]'})['value']
    payload = {f'reply_to_comment_{comment_id}[_token]': (None, csrf_token), 
               f'reply_to_comment_{comment_id}[comment]': (None, comment),
               f'reply_to_comment_{comment_id}[userFlag]': (None, 'none'),
               f'reply_to_comment_{comment_id}[email]': (None, '')}
    r = s.post(f"{redir_url}/-/comment/{comment_id}", files=payload)
    return r.url

def get_forum_by_id(forum_id):
    # forum_id: int, forum id
    r = s.get(f"http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/forums/arlingtonva", headers={"X-Experimental-API":"1"})
    return r.json()

def create_forum(forum_name, title, sidebar, description):
    # forum_name: str, forum name
    # title: str, title
    # sidebar: str, sidebar
    # description: str, description
    new_forum_url = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/forums'
    forum_data = {
        'name': forum_name,
        'title': title,
        'sidebar': sidebar,
        'description': description,
    }
    headers = {
        'X-Experimental-API': '1',
        'Content-Type': 'application/json',
    }
    data_payload = forum_data
    response = s.post(
        new_forum_url, cookies=s.cookies, headers=headers, json=data_payload
    )
    return response.json()

def update_forum(forum_id, forum_name, title, sidebar, description):
    # forum_id: int, forum id
    # forum_name: str, forum name
    # title: str, title
    # sidebar: str, sidebar
    # description: str, description
    new_forum_url = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/forums'
    forum_data = {
        'name': forum_name,
        'title': title,
        'sidebar': sidebar,
        'description': description,
    }
    headers = {
        'X-Experimental-API': '1',
        'Content-Type': 'application/json',
    }
    data_payload = forum_data
    response = s.put(
        new_forum_url, cookies=s.cookies, headers=headers, json=data_payload
    )
    return response.json()

def get_submission_by_id(submission_id):
    # submission_id: int, submission id
    r = s.get(f"http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/submissions/{submission_id}", headers={"X-Experimental-API":"1"})
    return r.json()

#API updating bio for current user profile
def update_bio(bio):
    # bio: str, bio content
    r = s.get(f"{BASE_URL}/user/MarvelsGrantMan136/edit_biography")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('form', attrs={'name': 'user_biography'}).find('input', attrs={'name': 'user_biography[_token]'})['value']
    payload = {'user_biography[_token]': csrf_token, 'user_biography[biography]': bio}
    print(payload)
    r = s.post(f"{BASE_URL}/user/MarvelsGrantMan136/edit_biography", data=payload)
    if r.status_code == 200:
        return {"updated": True}
    return {"updated": False}