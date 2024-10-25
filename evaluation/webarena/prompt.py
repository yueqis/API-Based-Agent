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

def check(src, tar):
    output = []
    with open(src) as f: f = f.readlines()
    src = []
    for row in f: src.append(json.loads(row))
    with open(tar) as f: f = f.readlines()
    tar = []
    for row in f: tar.append(json.loads(row))
    for row in src:
        if row['correct'] == False: continue
        for col in tar:
            if row['task_id'] == col['task_id'] and col['correct'] == False: output.append(col)
    return output

def check_api_correct():
    with open('/Users/artemis/Desktop/OpenDevin/evaluation/gitlab-mix/test.raw.json') as f: data = json.load(f)
    res = {}
    output = {}
    for row in data:
        sites = '_'.join(row['sites'])
        if sites not in output: output[sites] = {'browse': 0, 'api': 0, 'both': 0}
    for site in output:
        file = f'/Users/artemis/Desktop/OpenDevin/evaluation/evaluation_outputs/outputs/gitlab/CodeActAgent/gpt-4o_maxiter_10_N_v1.6_/output_{site}_gpt-4o.jsonl'
        try: 
            with open(file) as f: f = f.readlines()
            print(f"opened {file}")
        except: 
            print(f"file {file} un openable")
            continue
        for row in f:
            row = json.loads(row)
            res[row['task_id']] = row['correct']
    return res

def stat(task_id):
    with open(f'/Users/artemis/Desktop/OpenDevin/evaluation/evaluation_outputs/outputs/gitlab-mix/CodeActAgent/gpt-4o-2024-05-13_maxiter_18_N_v1.6_/logs/instance_{task_id}.log') as f:
        log = f.read()
        num_browsing = log.count('BrowseInteractiveAction') - 3
        num_coding = log.count('IPythonRunCellAction')
        return ((num_browsing > 0), (num_coding) > 0)

def stats():
    with open('/Users/artemis/Desktop/OpenDevin/evaluation/gitlab-mix/test.raw.json') as f: data = json.load(f)
    output = {}
    for row in data:
        sites = '_'.join(row['sites'])
        if sites not in output: output[sites] = {'browse': 0, 'api': 0, 'both': 0}
    res = {}
    print(output)
    check_api_correct_d = check_api_correct()
    for site in output:
        file = f'/Users/artemis/Desktop/OpenDevin/evaluation/evaluation_outputs/outputs/gitlab-mix/CodeActAgent/gpt-4o-2024-05-13_maxiter_18_N_v1.6_/output_{site}_gpt-4o-2024-05-13.jsonl'
        try: 
            with open(file) as f: f = f.readlines()
            print(f"opened {file}")
        except: 
            print(f"file {file} un openable")
            continue
        for row in f:
            row = json.loads(row)
            res[row['task_id']] = row['correct']
            #res[row['task_id']] = True
    print(res)
    for row in data:
        try: 
            id = int(row['task_id'])
            sites = '_'.join(row['sites'])
            browse, api = stat(id)
            if browse and api and res[id]: 
                output[sites]['both'] += 1
            elif browse and res[id]: output[sites]['browse'] += 1
            elif api and res[id]: output[sites]['api'] += 1
            elif not res[id] and check_api_correct_d[id]:
                print(f"{id} different!")
            else: 
                #output[sites]['browse'] += 1
                #print(f"id error {id}")
                continue
        except: 
            continue
            #print(f"not found: {id}")
    print(output)
#stats()


#{'shopping_admin': {'browse': 2, 'api': 1, 'both': 72}, 'map': {'browse': 2, 'api': 2, 'both': 46}, 'shopping': {'browse': 17, 'api': 3, 'both': 28}, 'reddit': {'browse': 2, 'api': 0, 'both': 24}, 'gitlab': {'browse': 1, 'api': 17, 'both': 61}, 'map_wikipedia': {'browse': 0, 'api': 0, 'both': 0}, 'wikipedia_map': {'browse': 0, 'api': 0, 'both': 0}, 'gitlab_reddit': {'browse': 0, 'api': 0, 'both': 0}, 'gitlab_wikipedia': {'browse': 0, 'api': 0, 'both': 0}, 'shopping_reddit': {'browse': 0, 'api': 0, 'both': 0}, 'reddit_gitlab': {'browse': 0, 'api': 0, 'both': 0}, 'map_shopping_admin': {'browse': 0, 'api': 0, 'both': 0}}

#{'shopping_admin': {'browse': 4, 'api': 2, 'both': 176}, 'map': {'browse': 4, 'api': 5, 'both': 100}, 'shopping': {'browse': 72, 'api': 14, 'both': 101}, 'reddit': {'browse': 18, 'api': 1, 'both': 87}, 'gitlab': {'browse': 14, 'api': 38, 'both': 128}, 'map_wikipedia': {'browse': 0, 'api': 0, 'both': 0}, 'wikipedia_map': {'browse': 0, 'api': 0, 'both': 0}, 'gitlab_reddit': {'browse': 0, 'api': 0, 'both': 0}, 'gitlab_wikipedia': {'browse': 0, 'api': 0, 'both': 0}, 'shopping_reddit': {'browse': 0, 'api': 0, 'both': 0}, 'reddit_gitlab': {'browse': 0, 'api': 0, 'both': 0}, 'map_shopping_admin': {'browse': 0, 'api': 0, 'both': 0}}

def get_step_cost(jsonl_file_path):
    with open(jsonl_file_path) as f: lines = f.readlines()
    data = []
    for line in lines: data.append(json.loads(line))
    steps = 0
    costs = 0
    for row in data:
        cost = row['metrics']['costs']
        steps += len(cost)
        costs += row['metrics']['accumulated_cost']
    print(steps / len(data))
    print(costs / len(data))
#get_step_cost('/Users/artemis/Desktop/OpenDevin/evaluation/evaluation_outputs/outputs/gitlab-mix/CodeActAgent/gpt-4o-2024-05-13_maxiter_18_N_v1.6_/output_reddit_gpt-4o-2024-05-13.jsonl')

def sort_jsonl(input_file, output_file, sort_key="task_id"):
    # Read the JSONL file line by line and load JSON objects
    data = []
    with open(input_file, 'r') as f:
        for line in f:
            json_obj = json.loads(line)
            data.append(json_obj)

    # Sort the data by the specified key
    sorted_data = sorted(data, key=lambda x: x.get(sort_key, 0))  # 0 is default if key is missing

    # Write the sorted data back to a new JSONL file
    with open(output_file, 'w') as f_out:
        for json_obj in sorted_data:
            f_out.write(json.dumps(json_obj) + '\n')

file = '/Users/artemis/Desktop/OpenDevin/evaluation/evaluation_outputs/outputs/gitlab-mix/CodeActAgent/gpt-4o-2024-05-13_maxiter_18_N_v1.6_/output_gitlab_gpt-4o-2024-05-13.jsonl'
sort_jsonl(file, file)