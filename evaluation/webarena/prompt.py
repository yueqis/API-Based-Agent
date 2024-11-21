import requests
from bs4 import BeautifulSoup
import json

def get_extra_user_info(site=''):
    output = ''
    if site == '': return ''
    if 'gitlab' in site: output += 'On gitlab, my *name* is Byte Blaze; My *username* on gitlab is byteblaze; and my *user id* is 2330.'
    if 'shopping' in site and 'shopping_admin' not in site: output += 'On the shopping website, my name is Emma Lopez, and my email is emma.lopez@gmail.com. You should use these information if the task asks about *me*, and you should filter out information about me if the task asks about anything related to me.\n'
    if 'shopping_admin' in site:
        output += "For shopping_admin, your API calling endpoint is `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/rest/default`; "
        output += "However, if you are using Web Browsing, the base URL of the website is `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin` - Be aware of this difference.\n"
        return output
    if 'map' in site: 
        output += 'For the map website, you will be provided with three sets of APIs, each providing different functionalities; '
        output += 'However, if you are using Web Browsing, you should always start from the URL `http://miniserver1875.asuscomm.com:3000` - Be aware of this differences.\n'
        return output
    if 'reddit' in site: output += 'On reddit, my username is MarvelsGrantMan136. '
    return output

def extract_sku_from_shopping_html(url):
    html_response = requests.get(url)
    html_content = html_response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    form_tag = soup.find('form', {'id': 'product_addtocart_form'})
    if form_tag:
        data_product_sku = form_tag.get('data-product-sku')
        return data_product_sku
    return ''

def extract_shopping_admin_product(url):
    return url.split('/')[-2]

def get_task_start_url_prompt(task_start_url, site_name, site_base):
    if 'gitlab' in site_name.lower():
        if task_start_url == site_base: return ''
        new_url = task_start_url.split(site_base)[1][1:]
        return f'\nThis task is related to the project: `{new_url}`.'
    if 'shopping' == site_name.lower():
        with open('/Users/artemis/Desktop/OpenDevin/evaluation/gitlab-mix/workspace_utils.py', 'r') as f: utils_py = f.read()
        task_start_urls = [task_start_url.strip() for task_start_url in task_start_url.split('|AND|')]
        if task_start_url == site_base: task_start_urls = []
        utils_py = utils_py.replace("'html_page_shopping_abcdefg'", f'{task_start_urls}')
        with open('/Users/artemis/Desktop/OpenDevin/workspace/utils.py', 'w') as f:
            f.write(utils_py)
        if task_start_url == site_base: return ''
        if ' |AND| ' in task_start_url:
            prompt = 'This task is related to the following products: '
            skus = {task_start_url: extract_sku_from_shopping_html(task_start_url) for task_start_url in task_start_urls}
            prompt += '; '.join([f'product with sku {skus[task_start_url]} (url: {task_start_url})' for task_start_url in task_start_urls])
            return '\n'+prompt
        else: 
            return f'\nThis task is related to the product with sku {extract_sku_from_shopping_html(task_start_url)}; the url of this product is {task_start_url}'
    if 'shopping_admin' in site_name.lower():
        if task_start_url == site_base: return ''
        return f'\nThis task is related to the product with product id `{extract_shopping_admin_product(task_start_url)}`.'
    if 'map' in site_name.lower(): return ''
    if 'reddit' in site_name.lower():
        if task_start_url == site_base: return ''
        splits = task_start_url.split('/')
        forum = splits[4]
        comment_id = ''
        if len(splits) > 5: comment_id = splits[5]
        if comment_id == '':
            return f'\nThis task is related to the forum {forum}. '
        return f'\nThis task is related to the comment with comment id {comment_id} from the forum {forum}. '
    else: assert 1==2

def get_browsing_prompt(task_start_url):
    if ' |AND| ' in task_start_url:
        task_start_urls = [task_start_url.strip() for task_start_url in task_start_url.split('|AND|')]
        return f"\nFor web browsing, You should start from the URLs {' and '.join(task_start_urls)}, and these webpages are already logged in and opened for you."
    else: return f"\nFor web browsing, You should start from the URL {task_start_url}, and this webpage is already logged in and opened for you."

def get_api_prompt(site_name):
    output = ''
    if 'gitlab' in site_name.lower():
        output += (
            f"\nNote: Before actually using a Gitlab API call, *you should call the `get_api_documentation_gitlab` function in the `utils` module to get detailed API documentation of the API.* "
            "For example, if you want to use the API GET /api/v4/projects/{id}/repository/commits, you should first do: "
            "\n<execute_ipython>\nfrom utils import get_api_documentation_gitlab\nget_api_documentation_gitlab('GET /api/v4/projects/{id}/repository/commits')\n</execute_ipython>"
            "\nThis will provide you with detailed descriptions of the input parameters and example output jsons."
        )
    if 'shopping' in site_name.lower() and 'admin' not in site_name.lower():
        output += (
            f"\nNote: Before actually using an API call, *you should call the `get_api_documentation_shopping` function in the `utils` module to get detailed API documentation of the API.* "
            "This function is defined by get_api_documentation_shopping(apis: list[str]) -> dict, which takes in args apis (list[str]), a list of APIs whose documentations to retrieve. "
            "For example, if you want to use the APIs 'get /V1/carts/mine' and 'get /V1/carts/mine/payment-information', you should first do: "
            "\n<execute_ipython>\nfrom utils import get_api_documentation_shopping\nget_api_documentation_shopping(['get /V1/carts/mine', 'get /V1/carts/mine/payment-information'])\n</execute_ipython>"
            "\nThis will provide you with a json containing openapi documentations of the APIs, describing the input parameters and example output of each API."
        )
    if 'shopping_admin' in site_name.lower():
        output += (
            f"\nNote: Before actually using an API call, *you should call the `get_api_documentation_shopping` function in the `utils` module to get detailed API documentation of the API.* "
            "This function is defined by get_api_documentation_shopping(apis: list[str]) -> dict, which takes in args apis (list[str]), a list of APIs whose documentations to retrieve. "
            "For example, if you want to use the APIs 'get /V1/orders' and 'get /V1/products', you should first do: "
            "\n<execute_ipython>\nfrom utils import get_api_documentation_shopping\nget_api_documentation_shopping(['get /V1/orders', 'get /V1/products'])\n</execute_ipython>"
            "\nThis will provide you with a json containing openapi documentations of the APIs, describing the input parameters and example output of each API."
        )
    return output

def get_initial_prompt(site_name, site_base, task, api_info, api_token='', extra_user_info=''):
    # obtain the intent
    intent = task['intent']
    task_start_url = task['start_url']
    intent = f"Think step by step to perform the following task related to {site_name}. Answer the question: ***{intent}***"
    intent += f'\nThe site URL for {site_name} is {site_base}, use this instead of the normal {site_name} URL. '
    intent += get_task_start_url_prompt(task_start_url, site_name, site_base)
    if api_token != '': intent += f"\nFor API calling, use this access token: {api_token}"
    intent += get_browsing_prompt(task_start_url)
    intent += (
        f"\n{extra_user_info + get_extra_user_info(site_name)}"
        f"\n\nBelow is the list of all APIs you can use and their descriptions:"
        f"\n{api_info}"
    )
    intent += get_api_prompt(site_name)
    intent += (
        '\nIMPORTANT: In general, you must always first try to use APIs to perform the task; however, you should use web browsing when there is no useful API available for the task. '
        'IMPORTANT: After you tried out using APIs, you must use web browsing to navigate to some URL containing contents that could verify whether the results you obtained by API calling is correct. '
    )
    return intent
#print(get_initial_prompt('shopping_admin', 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin', {'intent': 'intent-example', 'start_url': "http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin/catalog/product/edit/id/1481/"}, 'api_info-example', '', 'extra-user-info'))

def get_initial_prompt_multi(sites, task):
    # obtain the intent
    intent = task['intent']
    task_start_url = task['start_url']
    intent = f"Think step by step to perform the following task related to {' and '.join(sites.keys())}. Answer the question: ***{intent}***"
    for site_name in sites.keys(): intent += f'\nThe site URL for {site_name} is {sites[site_name]["site_base"]}, use this instead of the normal {site_name} URL. '
    for site_name in sites.keys():
        if sites[site_name]['site_base'] in task_start_url:
            intent += get_task_start_url_prompt(task_start_url, site_name, sites[site_name]['site_base'])
    for site_name in sites.keys():
        if sites[site_name]['api_token'] != '': intent += f"\nFor API calling on {site_name}, use this access token: {sites[site_name]['api_token']}"
    intent += get_browsing_prompt(task_start_url)
    for site_name in sites.keys():
        intent += '\n' + sites[site_name]['extra_user_info'] + get_extra_user_info(site_name)
    for site_name in sites.keys():
        intent += (
            f"\n\nBelow is the list of all APIs you can use for {site_name} and their descriptions:"
            f"\n{sites[site_name]['api_info']}"
        )
    intent += get_api_prompt(site_name)
    intent += (
        '\nIMPORTANT: In general, you must always first try to use APIs to perform the task; however, you should use web browsing when there is no useful API available for the task. '
        'IMPORTANT: After you tried out using APIs, you must use web browsing to navigate to some URL containing contents that could verify whether the results you obtained by API calling is correct. '
    )
    return intent
sites = {'shopping': {'site_base': 'shopping_site_base', 'api_info': 'shopping_api_info', 'api_token': 'shopping_api_token', 'extra_user_info': 'shopping_extra_user_info'}, 'reddit': {'site_base': 'reddit_site_base', 'api_info': 'reddit_api_info', 'api_token': 'reddit_api_token', 'extra_user_info': 'reddit_extra_user_info'}}
print(get_initial_prompt_multi(sites, {'intent': 'intent-example', 'start_url': "http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin/catalog/product/edit/id/1481/"}))
