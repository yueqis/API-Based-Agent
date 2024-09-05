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
        'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770/rest/default'
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
