import json

from openai import OpenAI


def generate_gpt(prompt):
    api_key = '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'
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt,
                        },
                    ],
                }
            ],
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.info(f'error {e}')
        return ''


def obtain_summary_shopping(file, output_json):
    res = {}
    with open(file, 'r') as file:
        data = json.load(file)
    data = data['paths']
    for api in data:
        api_info = data[api]
        for method in api_info:
            if 'description' in api_info[method]:
                res[f'{method} {api}'] = api_info[method]['description']
            else:
                print(f'No description given for api {method} {api}')
    with open(output_json, 'w') as f:
        json.dump(res, f, indent=4)


# obtain_summary_shopping(file = "/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/shopping-admin.json", output_json = "/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/shopping-admin-summary.json")


def parse_shopping(file):
    with open(file, 'r') as f:
        data = json.load(f)
    output = {}
    output['server_url'] = (
        'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770/rest/default'
    )
    paths = data['paths']
    components = data['components']
    for api in paths:
        api_info = paths[api]
        for method in api_info:
            try:
                del api_info[method]['operationId']
                del api_info[method]['summary']
                del api_info[method]['tags']
                for response in api_info[method]['responses']:
                    del api_info[method]['responses'][response]['content'][
                        'application/xml'
                    ]
            except Exception as e:
                print(f'{method} {api} exception {e}')
    for request in components['requestBodies']:
        requestBody = components['requestBodies'][request]
        try:
            del requestBody['content']['application/xml']
        except:
            print(f'{request} exception {e}')
    output['paths'] = paths
    output['components'] = components
    with open(file, 'w') as f:
        json.dump(output, f, indent=2)


# parse_shopping('/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/shopping-admin.json')


def obtain_map_apis():
    with open(
        '/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/map_summary.txt', 'r'
    ) as f:
        content = f.read()
    output = []
    while True:
        first = content.find('<tt>')
        if first == -1:
            break
        first += 4
        content = content[first:]
        second = content.find('</tt>')
        if second == -1:
            break
        output.append(content[:second])
        second += 5
        content = content[second:]
    return output


def get_summary_map(file_path=''):
    output = {}
    with open(
        '/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/map.txt', 'r'
    ) as f:
        f = f.readlines()
    f = [line for line in f if line.strip() != '']
    for i in range(len(f)):
        line = f[i]
        if '==' in line and '===' not in line:
            title = line.replace('=', '').strip()
        if '===' in line and ('====') not in line:
            line = line.replace('=', '').strip()
            first = line.find('<tt>')
            description = line[:first].replace(':', '').strip()
            next_line = f[i + 1].strip()
            description = f'{title} - {description}. {next_line}'
            first = first + 4
            second = line.find('</tt>')
            api = line[first:second]
            output[api] = description
    if file_path != '':
        with open(file_path, 'w') as f:
            json.dump(output, f, indent=4)
    return output


# get_summary_map("/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/map_api.json")

test = """
with requests.Session() as s:
    r = s.get("http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/login")
    soup = BeautifulSoup(r.content, 'html.parser')
    csrf_token = soup.find('input', attrs={'name': '_csrf_token'})['value']
    payload = {'_csrf_token': csrf_token ,'_username':'MarvelsGrantMan136', '_password':'test1234', '_remember_me': 'on'}
    s.post("http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/login_check", data=payload)
    cookie = requests.utils.dict_from_cookiejar(s.cookies)
    print(cookie)
    r = s.get("http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/api/comments/2561511", headers={"X-Experimental-API":"1"})
    print(r.json())
"""


def get_api_reddit():
    with open('prompt.txt', 'r') as f:
        example = f.read()
    with open('/Users/artemis/Downloads/CommentController.php', 'r') as f:
        php = f.read()
    prompt = f'Your task is to write a detailed and descriptive readme file for an API. An example of a good API documentation is: {example}. \n\n\n\nYou should write an as good readme documentation for the API `get /api/comments/`, which is implemented in the following php file:\n{php}'
    prompt = f'explain the code in detail: {php}.\n\n\n\nIf the web server is http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/, how to call the comment API? Give me an example of using python requests library to update a comment using these APIs.'
    prompt += f'\nAn example call to retrieve a specific comment could be: {test}'
    prompt += """\nAnd the returned json of a comment is {'id': 2561511, 'body': 'Fuck that guy', 'timestamp': '2023-03-31T23:59:57+00:00', 'user': {'id': 318070, 'username': '7SlotGrill'}, 'submission': {'id': 133260, 'forum': {'id': 10076, 'name': 'rva'}, 'user': {'id': 90040, 'username': 'whw53'}, 'slug': 'apparently-tim-kaine-is-performing-at-main-line-tomorrow'}, 'parentId': None, 'replyCount': 0, 'visibility': 'visible', 'editedAt': None, 'moderated': False, 'userFlag': 't1_jeh5mg9', 'netScore': -14, 'upvotes': 0, 'downvotes': 0, 'renderedBody': '<p lang="fy" dir="ltr">Fuck that guy</p>\n'}"""
    output = generate_gpt(prompt)
    print(output)


get_api_reddit()
