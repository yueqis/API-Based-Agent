import collections
import html
import json
import os
import random
import re
import string
import subprocess
import tempfile
import time
import urllib

import openai
import requests
from bs4 import BeautifulSoup

from opendevin.core.logger import LOG_FILENAME
from opendevin.core.logger import opendevin_logger as logger

LOG_FILENAME = f'logs/{LOG_FILENAME}'
"""base class for evaluation"""
os.environ['REDDIT'] = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999'
os.environ['SHOPPING'] = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770'
os.environ['SHOPPING_ADMIN'] = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin'
os.environ['GITLAB'] = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023'
os.environ['WIKIPEDIA'] = 'WIKIPEDIA'
os.environ['MAP'] = 'http://miniserver1875.asuscomm.com:3000'
os.environ['HOMEPAGE'] = 'HOMEPAGE'
os.environ['OPENAI_API_KEY'] = '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'

import csv

from playwright.sync_api import sync_playwright
from webarena.evaluation_harness.helper_functions import (
    llm_fuzzy_match,
    llm_ua_match,
)

gitlab_token = 'glpat-CHYP5UVWMSkB_zcMocVx'

def get_shopping_customer_auth_token():
    ENDPOINT = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770'
    response = requests.post(
        url = f'{ENDPOINT}/rest/default/V1/integration/customer/token',
        headers = {
            'content-type': 'application/json'
        },
        data = json.dumps({
            'username': 'emma.lopez@gmail.com',
            'password': 'Password.123'
        })
    )
    return response.json()

def get_shopping_admin_auth_token():
    ENDPOINT = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770'
    response = requests.post(
        url = f'{ENDPOINT}/rest/default/V1/integration/admin/token',
        headers = {
            'content-type': 'application/json'
        },
        data = json.dumps({
            'username': 'admin',
            'password': 'admin1234'
        })
    )
    return response.json()

def get_shopping_admin_admin_auth_token():
    ENDPOINT = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780'
    response = requests.post(
        url = f'{ENDPOINT}/rest/default/V1/integration/admin/token',
        headers = {
            'content-type': 'application/json'
        },
        data = json.dumps({
            'username': 'admin',
            'password': 'admin1234'
        })
    )
    return response.json()

def parse_test_file():
    json_file_path = '/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/test.raw.json'
    with open(json_file_path, 'r') as file:
        file = file.read()
        file = file.replace('__GITLAB__', 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023')
        file = file.replace('__SHOPPING__', 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770')
        file = file.replace('__SHOPPING_ADMIN__', 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin')
        file = file.replace('__MAP__', 'http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000')
        file = file.replace('__REDDIT__', 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999')
        data = json.loads(file)
    return data

def get_gitlab_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['gitlab']: output.append(dat)
    return output
gitlab_tests_non_url = get_gitlab_test()

def get_web_results_by_sites(site = ['gitlab']):
    count = 0
    for task in parse_test_file():
        if task['sites'] == site and 'url_match' in task['eval']['eval_types'] and get_web_results(task['task_id']): count += 1
    print(count)

def get_all_gitlab_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if dat['sites'] == ['gitlab']:
            if 'program_html' in dat['eval']['eval_types']:
                program_html_match = dat['eval']['program_html']
                for match in program_html_match:
                    if 'url' in match and match['url'] == 'last': include = False
            if include: output.append(dat)
    return output
gitlab_tests = get_all_gitlab_test()

def get_shopping_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['shopping']: output.append(dat)
    return output
shopping_tests = get_shopping_test()

def get_shopping_admin_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if dat['sites'] == ['shopping_admin']: output.append(dat)
    return output
shopping_admin_tests = get_shopping_admin_test()

def get_map_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['map']: output.append(dat)
    return output
map_tests = get_map_test()

def get_reddit_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if dat['sites'] == ['reddit'] and 'url_match' not in dat['eval']['eval_types']:
            if 'program_html' in dat['eval']['eval_types']:
                program_html_match = dat['eval']['program_html']
                for match in program_html_match:
                    if 'url' in match and match['url'] == 'last': include = False
            if include: output.append(dat)
    return output
reddit_tests = get_reddit_test()

def get_gitlab_reddit_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if (dat['sites'] == ['reddit', 'gitlab'] or dat['sites'] == ['gitlab', 'reddit']) and 'url_match' not in dat['eval']['eval_types']:
            if 'program_html' in dat['eval']['eval_types']:
                program_html_match = dat['eval']['program_html']
                for match in program_html_match:
                    if 'url' in match and match['url'] == 'last': include = False
            if include: output.append(dat)
    return output
gitlab_reddit_tests = get_gitlab_reddit_test()

def get_shopping_reddit_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if (dat['sites'] == ['reddit', 'shopping'] or dat['sites'] == ['shopping', 'reddit']) and 'url_match' not in dat['eval']['eval_types']:
            if 'program_html' in dat['eval']['eval_types']:
                program_html_match = dat['eval']['program_html']
                for match in program_html_match:
                    if 'url' in match and match['url'] == 'last': include = False
            if include: output.append(dat)
    return output
shopping_reddit_tests = get_shopping_reddit_test()

def get_shopping_admin_map_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if (dat['sites'] == ['map', 'shopping_admin'] or dat['sites'] == ['shopping_admin', 'map']) and 'url_match' not in dat['eval']['eval_types']:
            if 'program_html' in dat['eval']['eval_types']:
                program_html_match = dat['eval']['program_html']
                for match in program_html_match:
                    if 'url' in match and match['url'] == 'last': include = False
            if include: output.append(dat)
    return output
shopping_admin_map_tests = get_shopping_admin_map_test()

def get_wikipedia_map_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if (dat['sites'] == ['map', 'wikipedia'] or dat['sites'] == ['wikipedia', 'map']) and 'url_match' not in dat['eval']['eval_types']:
            if 'program_html' in dat['eval']['eval_types']:
                program_html_match = dat['eval']['program_html']
                for match in program_html_match:
                    if 'url' in match and match['url'] == 'last': include = False
            if include: output.append(dat)
    return output
wikipedia_map_tests = get_wikipedia_map_test()

def get_wikipedia_gitlab_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if (dat['sites'] == ['gitlab', 'wikipedia'] or dat['sites'] == ['wikipedia', 'gitlab']) and 'url_match' not in dat['eval']['eval_types']:
            if 'program_html' in dat['eval']['eval_types']:
                program_html_match = dat['eval']['program_html']
                for match in program_html_match:
                    if 'url' in match and match['url'] == 'last': include = False
            if include: output.append(dat)
    return output
wikipedia_gitlab_tests = get_wikipedia_gitlab_test()

def get_task_by_task_id(task_id):
    for test in parse_test_file():
        if test['task_id'] == task_id: return test
    return None

def get_tests(start_task_id):
    task = get_task_by_task_id(start_task_id)
    sites = task['sites']
    if sites == ['gitlab']: tests = gitlab_tests
    if sites == ['shopping']: tests = shopping_tests
    if sites == ['shopping_admin']: tests = shopping_admin_tests
    if sites == ['map']: tests = map_tests
    if sites == ['reddit']: tests = reddit_tests
    if sites == ['reddit', 'gitlab'] or sites == ['gitlab', 'reddit']: tests = gitlab_reddit_tests
    if sites == ['reddit', 'shopping'] or sites == ['shopping', 'reddit']: tests = shopping_reddit_tests
    if sites == ['map', 'shopping_admin'] or sites == ['shopping_admin', 'map']: tests = shopping_admin_map_tests
    if sites == ['map', 'wikipedia'] or sites == ['wikipedia', 'map']: tests = wikipedia_map_tests
    if sites == ['gitlab', 'wikipedia'] or sites == ['wikipedia', 'gitlab']: tests = wikipedia_gitlab_tests
    for idx in range(len(tests)):
        test = tests[idx]
        if test['task_id'] == start_task_id:
            return tests[idx:]
    return []

def output_gitlab_test_json(file, test):
    with open(file, 'w') as f:
        json.dump(test, f, indent=4)

def get_gitlab_apis():
    api_file_path = 'evaluation/gitlab/api/gitlab_api.txt'
    with open(api_file_path, 'r') as file:
        api_file = file.read()
    return api_file
gitlab_api_file = get_gitlab_apis()

def get_shopping_apis(shopping_html_pages = []):
    api_file_path = '/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/shopping-admin-summary.json'
    with open(api_file_path, 'r') as file:
        api_file = json.load(file)
    if shopping_html_pages == []: return api_file
    new_api_file = {}
    for shopping_html_page in shopping_html_pages:
        new_api_file[shopping_html_page] = f'Retrieve the content in the HTML page {shopping_html_page}'
    new_api_file.update(api_file)
    return new_api_file

def get_map_apis():
    api_doc = ''
    dir = '/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/map/'
    with open(dir+'http.md', 'r') as file:
        api_doc += 'Below is all the documentation on how to use the http://metis.lti.cs.cmu.edu:{profile}/{service}/v1/test/ endpoints.\n'
        api_doc += file.read()
    api_doc += '\nBelow is all the documentation on how to use the http://metis.lti.cs.cmu.edu:8085/ endpoints.\n'
    files_osm = ['Search.md', 'Lookup.md', 'Reverse.md', 'Output.md', 'Faq.md']
    for f in files_osm:
        file_path = dir+f
        with open(file_path, 'r') as file:
            api_doc += file.read()
    api_doc += '\nBelow is a list of editing API you could use for fetching and saving raw geodata from/to the OpenStreetMap database APIs. '
    api_doc += 'For the following APIs, you should use the endpoint http://miniserver1875.asuscomm.com:3000/. '
    api_doc += 'To find out more about the `http://miniserver1875.asuscomm.com:3000/` APIs you could do `from utils import get_api_documentation_map` and then use get_api_documentation_map(API) to learn more about the API.\n'
    with open(dir+'map_api.json', 'r') as file:
        api_doc += file.read()
    return api_doc
map_api_file = get_map_apis()

def get_reddit_apis():
    with open('/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/reddit.md', 'r') as f:
        f = f.read()
    return f
reddit_api_file = get_reddit_apis()

with open('evaluation/gitlab/merged_log.txt', 'r', encoding='utf-8') as file:
    log = file.read()
def get_web_results(task_id):
    for line in log.strip().split('\n'):
        if f'/{task_id}.json' in line:
            if ('[Result] (PASS)' in line): return True
            if ('[Result] (FAIL)' in line): return False
    return False

def get_api_results(task_id, file_path = '/Users/artemis/Desktop/OpenDevin/evaluation/evaluation_outputs/outputs/gitlab/CodeActAgent/gpt-4o_maxiter_8_N_v1.6_/output_gpt-4o.jsonl'):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            row = json.loads(line.strip())
            if row.get('task_id') == task_id:
                correct = row['correct']
                return correct
    return False

def get_gitlab_initial_prompt(task):
    # obtain the intent
    intent = task['intent']
    task_start_url = task['start_url']
    if task_start_url != 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023':
        new_url = task_start_url.split('http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023/')[1]
        intent += f'\nThis task is related to the project: `{new_url}`; if you are using web browsing, then the project URL is: `{task_start_url}`'
    user_prompt_1 = f'Think step by step to perform the task related to Gitlab usage: {intent}.\n'
    user_prompt_1 += 'Your Gitlab endpoint is `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023`. You should use `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023/` instead of `https://gitlab.com/`.\n'
    user_prompt_1 += 'You could complete the task through two ways: browsing and API calling.\n'
    user_prompt_1 += 'For browsing, use the following login credentials: username - byteblaze, password - hello1234\n'
    user_prompt_1 += "To complete the task, for each step you could either perform 'Web Browsing' or 'API Calling'.\n"
    user_prompt_1 += 'For Web Browsing, you should do <execute_browse> YOUR_COMMAND </execute_browse>. You should explain which steps you would like to perform using web browsing thoroughly. '
    user_prompt_1 += 'Web Browsing is generally useful when there are no useful APIs available for the task or when an URL is required for the task.\n'
    user_prompt_1 += 'If you decide to use web browsing, then you need to make sure that the URL you are going to satisfy the constraints of the task. For example, if the task asks you to provide the best product, then you would likely need to update the URL you are browsing such that it sorts the products and put the best product at the top.'
    user_prompt_1 += 'When appropriate, you should try to provide an ending url webpage, where you should use web browsing to browse to a result page when finishing the task, such that we could validate whether you are doing the task correctly. '
    user_prompt_1 += "To call APIs, you must generate and execute *python*'s code to use API calls through the requests library. The requests library is already installed for you. "
    user_prompt_1 += 'To perform the task, you should try to parse and understand the response of the API calls, without generating code to process the response. I.e., you do not need to use python to process the response from API calling; instead you should parse the API response manually and ensure the relevant information is correctly extracted and utilized. '
    user_prompt_1 += f'You should use my gitlab access token {gitlab_token}. My gitlab username is byteblaze, my name is Byte Blaze, and my user id is 2330.\n'
    user_prompt_1 += 'Make good use of HTTP headers when making API calls, and be careful of the input parameters to each api call.\n'
    user_prompt_1 += 'These are all the information you have for now, and you should not assume any additional information or ask for any user input.\n'
    user_prompt_1 += "IMPORTANT: The information provided might be incomplete or ambiguous. For example, if the I want to search for a repo 'xyz', then 'xyz' could be the name of the repo, it could be the path of the repo, or it could also be the first three characters of the repo's full name. "
    user_prompt_1 += 'Thus, your code should *cover all potential cases* that the user might be indicating and be careful about nuances.\n'
    user_prompt_1 += 'Additionally, the response json obtained through the API calls will only include the first `per-page`-many instances, so make sure that you looked at all instances but not only the first `per-page`-many instances.\n'
    user_prompt_1 += 'I will provide with you a list of API calls that you can use.\n'
    user_prompt_1 += 'You should first do `from utils import get_api_documentation_gitlab` using python to be able to use this function. '
    user_prompt_1 += "This function is defined by get_api_documentation_gitlab(api: str) -> str, which has args api (str): The API whose documentations to retrieve. For example, 'get /api/v4/projects/{id}/repository/commits'. "
    user_prompt_1 += 'This function returns the readme documentation of an API that provides you with details instructions on how to use the API.\n'
    user_prompt_1 += 'If you think an API is relevant to the task, you should call get_api_documentation_gitlab(api) to get more details on how to use this API. You should execute get_api_documentation_gitlab yourself without waiting for the user to execute it.\n'
    user_prompt_1 += 'When you think you finished the task, respond with `Finish[answer]` where you include your answer in `[]` if the user asks for an answer; otherwise respond with Finish[]. If you would like to provide an URL, you should respond with `URL[{url}]` if \n'
    user_prompt_1 += 'Below is the list of all APIs you can use and their descriptions:\n'
    user_prompt_1 += f'{gitlab_api_file}\n'
    return user_prompt_1
#print(get_initial_prompt("How many commits did kilian make to a11yproject on 3/5/2023?"))

def extract_sku_from_shopping_html(url):
    html_response = requests.get(url)
    html_content = html_response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    form_tag = soup.find('form', {'id': 'product_addtocart_form'})
    if form_tag:
        data_product_sku = form_tag.get('data-product-sku')
        return data_product_sku
    return ''

def get_shopping_initial_prompt(task):
    intent = task['intent']
    intent = intent.strip()
    if intent.endswith('.') or intent.endswith('?'): intent = intent[:len(intent)-1]
    task_start_url = task['start_url']
    with open('/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/workspace_utils.py', 'r') as f:
        utils_py = f.read()
    if task_start_url != 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770':
        if ' |AND| ' in task_start_url:
            task_start_urls = task_start_url.split('|AND|')
            task_start_urls = [task_start_url.strip() for task_start_url in task_start_urls]
            intent += f"\nIf you are using web browsing, this task is about the following URLs: `{' and '.join(task_start_urls)}`. "
            for task_start_url in task_start_urls:
                sku = extract_sku_from_shopping_html(task_start_url)
                intent += f'For the URL {task_start_url}, the `sku` of the product in the URL is {sku}. '
        else:
            intent += f'\nIf you are using web browsing, this task is about the following URL: `{task_start_url}`. '
            sku = extract_sku_from_shopping_html(task_start_url)
            intent += f'The `sku` of the product in this URL is {sku}. '
            task_start_urls = [task_start_url]
        shopping_api_file = get_shopping_apis(task_start_urls)
        utils_py = utils_py.replace("'html_page_shopping_abcdefg'", f'{task_start_urls}')
        with open('/Users/artemis/Desktop/OpenDevin/workspace/utils.py', 'w') as f:
            f.write(utils_py)
    else:
        shopping_api_file = get_shopping_apis()
        utils_py = utils_py.replace("'html_page_shopping_abcdefg'", '[]')
        with open('/Users/artemis/Desktop/OpenDevin/workspace/utils.py', 'w') as f:
            f.write(utils_py)
    user_prompt_1 = f'Think step by step to perform the following task related to an E-Commerce shopping website named One Stop Market. Answer the question: **{intent}**.\n'
    user_prompt_1 += "Your One Stop Market endpoint is `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770`. If you are using Web Browsing, you should start with the URL `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770/customer/account/login/`, signing in using the following login credentials: 'Email': 'emma.lopez@gmail.com', 'Password': 'Password.123'\n"
    user_prompt_1 += "To complete the task, for each step you could either perform 'Web Browsing' or 'API Calling'.\n"
    user_prompt_1 += 'For Web Browsing, you should do <execute_browse> YOUR_COMMAND </execute_browse>. You should explain which steps you would like to perform using web browsing thoroughly. '
    user_prompt_1 += 'Web Browsing is generally useful when there are no useful APIs available for the task or when an URL is required for the task.\n'
    user_prompt_1 += 'If you decide to use web browsing, then you need to make sure that the URL you are going to satisfy the constraints of the task. For example, if the task asks you to provide the best product, then you would likely need to update the URL you are browsing such that it sorts the products and put the best product at the top.'
    user_prompt_1 += 'When appropriate, you should try to provide an ending url webpage, where you should use web browsing to browse to a result page when finishing the task, such that we could validate whether you are doing the task correctly. '
    user_prompt_1 += "In case you would like to perform API calling through python's requests library, the requests library is already installed for you. "
    #user_prompt_1 += f"To call APIs, you must generate and execute *python*'s code to use API calls through the requests library. The requests library is already installed for you. "
    user_prompt_1 += 'The responses from API calling could be very long. Therefore, the best way is to first read the dimensions of the response, and if the response is indeed very long, then you could first try to understand the first element of the response to get a sense of how the response would be like, and then use python code to parse the full response to obtain the answer of the task; if the response is very short, then you could manually read and parse the response without using code. '
    #user_prompt_1 += f"To perform the task, you should try to parse and understand the response of the API calls by generating code to process the response. I.e., you should try to use python to process the response from API calling and obtain the correct answer from the response. "
    user_prompt_1 += 'Ensure that relevant information is correctly extracted and utilized. '
    user_prompt_1 += f'You should always use my admin access token {get_shopping_admin_auth_token()} in general. Only when using the endpoints that contains `/V1/carts/mine` in the API, you should use my customer access token {get_shopping_customer_auth_token()}. My customer access token does not have access to any other endpoints. For example, for the API endpoint `V1/products` you should use my admin token; for the `/V1/carts/mine/items` endpoint, you should use my customer token.\n'
    user_prompt_1 += 'Before checking the carts or even adding anything to the carts, you should first create the shopping cart using the endpoint `post /V1/carts/mine`.\n'
    user_prompt_1 += '*Note that I am Emma Lopez, and my email is emma.lopez@gmail.com.* You should use these information if the task asks about *me*, and you should filter out information about me if the task asks about anything related to me.\n'
    user_prompt_1 += 'Make good use of HTTP params when making API calls, and be careful of the input parameters to each api call to match *all* the requirements of the task.\n'
    user_prompt_1 += 'These are all the information you have for now, and you should not assume any additional information or ask for any user input.\n'
    user_prompt_1 += "IMPORTANT: My request is human-like. In other words, the information provided might be incomplete or ambiguous. For example, if the I want to search for a item 'abc xyz', then 'abc xyz' could be the full name of the item, it could be the description of the item, or it could also be that 'abc' is the description of the item while 'xyz' is three characters of the item's full name. "
    user_prompt_1 += 'Thus, your code should *cover all potential cases* that the user might be indicating and be careful about nuances.\n'
    user_prompt_1 += 'IMPORTANT: In the task I specified some conditions/requirements that you *must* meet to perform the task. Make sure your code must meet *every* condition I specified in the task. '
    #user_prompt_1 += f"Additionally, the response json obtained through the API calls will only include the first `per-page`-many instances, so make sure that you looked at all instances but not only the first `per-page`-many instances.\n"
    user_prompt_1 += 'I will provide with you a list of API calls that you can use.\n'
    user_prompt_1 += "Among these APIs, if the API contains 'mine', then it is specifically about information of me; if the API does not contain 'mine', then it is about the whole shopping website, and you should filter out information specifically needed for the task. "
    user_prompt_1 += 'You should first do `from utils import get_api_documentation_shopping` using python to be able to use this function. '
    user_prompt_1 += "This function is defined by get_api_documentation_shopping(apis: list[str]) -> dict, which has args apis (list[str]): The APIs whose documentations to retrieve. For example, ['get /V1/carts/mine', 'get /V1/carts/mine/payment-information']. "
    user_prompt_1 += 'This function returns a json containing openapi documentation of the APIs, which will provide you with detailed instructions on how to use the APIs.\n'
    user_prompt_1 += 'In the json with openapi documentation of the APIs, the list of api calls that you query for will be under the key `paths`. It will contain detailed documentation of what input parameters are supported by the APIs, and you should make good use of these parameters to satisfy my request. '
    user_prompt_1 += 'In the json, I will also provide you the types of return values and example return values of the api calls under the `components` field, so you should be able to find the answer to the task through parsing the potential returned response from the api call(s). '
    user_prompt_1 += 'If you think an API is relevant to the task, you could call get_api_documentation_shopping(api) to get more details on how to use this API. You should execute get_api_documentation_shopping yourself without waiting for the user to execute it.\n'
    user_prompt_1 += 'If from carefully reading the documentation of APIs, you think none of the APIs I provided could solve the task, you should try fetching the content of the html pages provided directly using API calling, and parse the content of the html pages to find the answer. Note that the HTML pages could be very long, so you should try to first search for relevant details in the HTML pages instead of reading the content directly. However, in general, you should aviod extracting the HTML content directly. ' #Note: this is the *only* case that you can use an API that is not provided in the list of API below. In all other cases, you should only use APIs I provided.\n"
    user_prompt_1 += 'When you think you finished the task, respond with `Finish[answer]` where you include your answer in `[]` if the user asks for an answer; otherwise respond with Finish[].\n'
    user_prompt_1 += "Be careful that the way you parse the response should *match* the format of the types of example responses. You should be able to find the correct component referred to from the '$ref' field. \n"
    user_prompt_1 += 'Below is a dictionary where the keys of the dict are the names of the APIs and values of the dict are the descriptions of the key. You should determine whether you should use an API to solve the task through reading its description.\n'
    user_prompt_1 += f'{shopping_api_file}\n'
    #user_prompt_1 += get_shopping_readme()
    return user_prompt_1

def get_shopping_admin_initial_prompt(task):
    intent = task['intent']
    intent = intent.strip()
    if intent.endswith('.') or intent.endswith('?'): intent = intent[:len(intent)-1]
    task_start_url = task['start_url']
    with open('/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/workspace_utils.py', 'r') as f:
        utils_py = f.read()
    if task_start_url != 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin':
        if ' |AND| ' in task_start_url:
            task_start_urls = task_start_url.split('|AND|')
            task_start_urls = [task_start_url.strip() for task_start_url in task_start_urls]
            intent += f"\nIf you are using web browsing, this task is about the following URLs: `{' and '.join(task_start_urls)}`. "
            #for task_start_url in task_start_urls:
            #    sku = extract_sku_from_shopping_html(task_start_url)
            #    intent += f"For the URL {task_start_url}, the `sku` of the product in the URL is {sku}. "
        else:
            intent += f'\nIf you are using web browsing, this task is about the following URL: `{task_start_url}`. '
            #sku = extract_sku_from_shopping_html(task_start_url)
            #intent += f"The `sku` of the product in this URL is {sku}. "
            task_start_urls = [task_start_url]
        shopping_api_file = get_shopping_apis(task_start_urls)
        utils_py = utils_py.replace("'html_page_shopping_abcdefg'", f'{task_start_urls}')
        with open('/Users/artemis/Desktop/OpenDevin/workspace/utils.py', 'w') as f:
            f.write(utils_py)
    else:
        shopping_api_file = get_shopping_apis()
        utils_py = utils_py.replace("'html_page_shopping_abcdefg'", '[]')
        with open('/Users/artemis/Desktop/OpenDevin/workspace/utils.py', 'w') as f:
            f.write(utils_py)
    user_prompt_1 = f'Think step by step to perform the following task related to an E-Commerce shopping admin website named One Stop Market. Answer the question: **{intent}**.\n'
    user_prompt_1 += "Your One Stop Market admin endpoint is `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780`. If you are using Web Browsing, you should start with the URL `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin`, signing in using the following login credentials: 'Username': 'admin', 'Password': 'admin1234'.\n"
    user_prompt_1 += "To complete the task, for each step you could either perform 'Web Browsing' or 'API Calling'.\n"
    user_prompt_1 += 'For Web Browsing, you should do <execute_browse> YOUR_COMMAND </execute_browse>. You should explain which steps you would like to perform using web browsing thoroughly. '
    user_prompt_1 += 'Web Browsing is generally useful when there are no useful APIs available for the task or when an URL is required for the task.\n'
    user_prompt_1 += 'If you decide to use web browsing, then you need to make sure that the URL you are going to satisfy the constraints of the task. For example, if the task asks you to provide the best product, then you would likely need to update the URL you are browsing such that it sorts the products and put the best product at the top.'
    user_prompt_1 += 'When appropriate, you should try to provide an ending url webpage, where you should use web browsing to browse to a result page when finishing the task, such that we could validate whether you are doing the task correctly. '
    user_prompt_1 += "In case you would like to perform API calling through python's requests library, the requests library is already installed for you. "
    #user_prompt_1 += f"To call APIs, you must generate and execute *python*'s code to use API calls through the requests library. The requests library is already installed for you. "
    user_prompt_1 += 'The responses from API calling could be very long. Therefore, the best way is to first read the dimensions of the response, and if the response is indeed very long, then you could first try to understand the first element of the response to get a sense of how the response would be like, and then use python code to parse the full response to obtain the answer of the task; if the response is very short, then you could manually read and parse the response without using code. '
    #user_prompt_1 += f"To perform the task, you should try to parse and understand the response of the API calls by generating code to process the response. I.e., you should try to use python to process the response from API calling and obtain the correct answer from the response. "
    user_prompt_1 += 'Ensure that relevant information is correctly extracted and utilized. '
    user_prompt_1 += f'You should use my admin access token {get_shopping_admin_admin_auth_token()}.\n'
    user_prompt_1 += 'Make good use of HTTP params when making API calls, and be careful of the input parameters to each api call to match *all* the requirements of the task.\n'
    user_prompt_1 += 'These are all the information you have for now, and you should not assume any additional information or ask for any user input.\n'
    user_prompt_1 += "IMPORTANT: My request is human-like. In other words, the information provided might be incomplete or ambiguous. For example, if the I want to search for a item 'abc xyz', then 'abc xyz' could be the full name of the item, it could be the description of the item, or it could also be that 'abc' is the description of the item while 'xyz' is three characters of the item's full name. "
    user_prompt_1 += 'Thus, your code should *cover all potential cases* that the user might be indicating and be careful about nuances.\n'
    user_prompt_1 += 'IMPORTANT: In the task I specified some conditions/requirements that you *must* meet to perform the task. Make sure your code must meet *every* condition I specified in the task. '
    #user_prompt_1 += f"Additionally, the response json obtained through the API calls will only include the first `per-page`-many instances, so make sure that you looked at all instances but not only the first `per-page`-many instances.\n"
    user_prompt_1 += 'I will provide with you a list of API calls that you can use.\n'
    user_prompt_1 += 'You should first do `from utils import get_api_documentation_shopping` using python to be able to use this function. '
    user_prompt_1 += "This function is defined by get_api_documentation_shopping(apis: list[str]) -> dict, which has args apis (list[str]): The APIs whose documentations to retrieve. For example, ['get /V1/carts/mine', 'get /V1/carts/mine/payment-information']. "
    user_prompt_1 += 'This function returns a json containing openapi documentation of the APIs, which will provide you with detailed instructions on how to use the APIs.\n'
    user_prompt_1 += 'In the json with openapi documentation of the APIs, the list of api calls that you query for will be under the key `paths`. It will contain detailed documentation of what input parameters are supported by the APIs, and you should make good use of these parameters to satisfy my request. '
    user_prompt_1 += 'In the json, I will also provide you the types of return values and example return values of the api calls under the `components` field, so you should be able to find the answer to the task through parsing the potential returned response from the api call(s). '
    user_prompt_1 += 'If you think an API is relevant to the task, you could call get_api_documentation_shopping(api) to get more details on how to use this API. You should execute get_api_documentation_shopping yourself without waiting for the user to execute it.\n'
    user_prompt_1 += 'If from carefully reading the documentation of APIs, you think none of the APIs I provided could solve the task, you should try fetching the content of the html pages provided directly using API calling, and parse the content of the html pages to find the answer. Note that the HTML pages could be very long, so you should try to first search for relevant details in the HTML pages instead of reading the content directly. However, in general, you should aviod extracting the HTML content directly. ' #Note: this is the *only* case that you can use an API that is not provided in the list of API below. In all other cases, you should only use APIs I provided.\n"
    user_prompt_1 += 'When you think you finished the task, respond with `Finish[answer]` where you include your answer in `[]` if the user asks for an answer; otherwise respond with Finish[].\n'
    user_prompt_1 += "Be careful that the way you parse the response should *match* the format of the types of example responses. You should be able to find the correct component referred to from the '$ref' field. \n"
    user_prompt_1 += 'Below is a dictionary where the keys of the dict are the names of the APIs and values of the dict are the descriptions of the key. You should determine whether you should use an API to solve the task through reading its description.\n'
    user_prompt_1 += f'{shopping_api_file}\n'
    #user_prompt_1 += get_shopping_readme()
    return user_prompt_1

def get_map_initial_prompt(task):
    return 'Go to the URL http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/search?query=hotels%20near%20carnegie%20mellon%20university'
    intent = task['intent']
    task_start_url = task['start_url']
    if task_start_url != 'http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000':
        intent += f'\nIf you are using Web Browsing, you should start with this URL: `{task_start_url}`.'
    else: intent += '\nIf you are using Web Browsing, you should start with this URL: http://miniserver1875.asuscomm.com:3000'
    user_prompt_1 = f'Think step by step to perform the task related to the Open Street Map website: {intent}.\n'
    #user_prompt_1 += f"Your Open Street Map website endpoint is `http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000`. You should use `http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/` instead of `https://www.openstreetmap.org/`.\n"
    user_prompt_1 += "To complete the task, for each step you could either perform 'Web Browsing' or 'API Calling'.\n"
    user_prompt_1 += 'For Web Browsing, you should do <execute_browse> YOUR_COMMAND </execute_browse>. You should explain which steps you would like to perform using web browsing thoroughly. '
    user_prompt_1 += 'Web Browsing is generally useful when there are no useful APIs available for the task or when an URL is required for the task.\n'
    user_prompt_1 += 'When appropriate, you should try to provide an ending url webpage, where you should use web browsing to browse to a result page when finishing the task, such that we could validate whether you are doing the task correctly. '
    user_prompt_1 += 'To call APIs, you must generate code to use API calls.'
    user_prompt_1 += 'To perform the task, you should try to parse and understand the response of the API calls, with/without generating code to process the response. I.e., you do not need to use python to process the response from API calling; instead you could parse the API response manually and ensure that relevant information is correctly extracted and utilized. '
    user_prompt_1 += 'You should not need to use any access tokens to perform the task.\n'
    user_prompt_1 += 'Make good use of HTTP headers when making API calls, and be careful of the input parameters to each api call.\n'
    user_prompt_1 += 'These are all the information you have for now, and you should not assume any additional information or ask for any user input.\n'
    user_prompt_1 += "IMPORTANT: The information provided might be incomplete or ambiguous. For example, if the I want to search for a location 'xyz', then 'xyz' could be the full name of the location, or it could also be the first three characters of the location's full name. "
    user_prompt_1 += 'Thus, your code should *cover all potential cases* that the user might be indicating and be careful about nuances.\n'
    user_prompt_1 += 'I will provide with you a documentation of API calls that you can use.\n'
    #user_prompt_1 += f"IMPORTANT: You will have three website endpoint servers you could use: http://router.project-osrm.org/ and https://nominatim.openstreetmap.org/. You should first use the https://nominatim.openstreetmap.org/ website endpoints to search for information on locations, and then use http://router.project-osrm.org/ endpoints to route. "
    #user_prompt_1 += f"You should first do `from utils import get_api_documentation_map` using python to be able to use this function. "
    #user_prompt_1 += "This function is defined by get_api_documentation_map(api: str) -> str, which has args api (str): The API whose documentations to retrieve. For example, 'GET /api/0.6/map'. "
    #user_prompt_1 += f"This function returns a str containing documentation of the API, which will provide you with detailed instructions on how to use the API.\n"
    #user_prompt_1 += f"If you think an API is relevant to the task, you could call get_api_documentation_map(api) to get more details on how to use this API. You should execute get_api_documentation_map yourself without waiting for the user to execute it.\n"
    #user_prompt_1 += f"If you think none of the APIs I provided could solve the task and you want to fetch the content of some html pages, you can also use API calling to fetch the content of html pages. Note: this is the *only* case that you can use an API that is not provided in the list of API below. In all other cases, you should only use APIs I provided.\n"
    user_prompt_1 += 'When you think you finished the task, respond with `Finish[answer]` where you include your answer in `[]` if the user asks for an answer; otherwise respond with Finish[].\n'
    user_prompt_1 += "Be careful that the way you parse the response should *match* the format of the types of example responses. You should be able to find the correct component referred to from the '$ref' field. \n"
    user_prompt_1 += 'Below are all the APIs you could use and their descriptions.\n'
    user_prompt_1 += f'{map_api_file}\n'
    return user_prompt_1

def get_reddit_initial_prompt(task):
    intent = task['intent']
    task_start_url = task['start_url']
    if task_start_url != 'http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:9999':
        intent += f'This task is about the following URL: `{task_start_url}`.'
    user_prompt_1 = f'Think step by step to perform the task related to Reddit: {intent}.\n'
    user_prompt_1 += 'Your reddit endpoint is `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999`.\n'
    user_prompt_1 += 'You should complete the task through performing *API calling*.\n'
    user_prompt_1 += 'To call APIs, you must generate code to use API calls.'
    user_prompt_1 += 'To perform the task, you should try to parse and understand the response of the API calls, with/without generating code to process the response. I.e., you do not need to use python to process the response from API calling; instead you could parse the API response manually and ensure that relevant information is correctly extracted and utilized. '
    user_prompt_1 += 'You should not need to use any access tokens to perform the task.\n'
    user_prompt_1 += 'Note that I am MarvelsGrantMan136.\n'
    user_prompt_1 += 'Make good use of HTTP headers when making API calls, and be careful of the input parameters to each api call.\n'
    user_prompt_1 += 'These are all the information you have for now, and you should not assume any additional information or ask for any user input.\n'
    user_prompt_1 += "IMPORTANT: The information provided might be incomplete or ambiguous. For example, if the I want to search for a submission post 'xyz', then 'xyz' could be the full title of the submission, or it could also be the first three characters of the submission's full name. "
    user_prompt_1 += 'Thus, your code should *cover all potential cases* that the user might be indicating and be careful about nuances.\n'
    user_prompt_1 += 'I will provide with you a documentation of API calls that you can use.\n'
    user_prompt_1 += 'If from carefully reading the documentation of APIs, you think none of the APIs I provided could solve the task, you should try fetching the content of the html pages provided directly using API calling, and parse the content of the html pages to find the answer. Note that the HTML pages could be very long, so you should try to first search for relevant details in the HTML pages instead of reading the content directly. However, in general, you should aviod extracting the HTML content directly. ' #Note: this is the *only* case that you can use an API that is not provided in the list of API below. In all other cases, you should only use APIs I provided.\n"
    user_prompt_1 += 'When you think you finished the task, respond with `Finish[answer]` where you include your answer in `[]` if the user asks for an answer; otherwise respond with Finish[].\n'
    user_prompt_1 += "Be careful that the way you parse the response should *match* the format of the types of example responses. You should be able to find the correct component referred to from the '$ref' field. \n"
    user_prompt_1 += 'Below are all the APIs you could use and their descriptions.\n'
    user_prompt_1 += f'{reddit_api_file}\n'
    return user_prompt_1

def get_reddit_gitlab_initial_prompt(task):
    # obtain the intent
    intent = task['intent']
    user_prompt_1 = f'Think step by step to perform the task related to Gitlab usage and Reddit usage: {intent}.\n'
    user_prompt_1 += 'Your Gitlab endpoint is `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023`. You should use `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023/` instead of `https://gitlab.com/`.\n'
    user_prompt_1 += 'Your Reddit endpoint is `http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999`.\n'
    user_prompt_1 += 'You should complete the task through performing API calling.\n'
    user_prompt_1 += "To call APIs, you must generate and execute *python*'s code to use API calls through the requests library. The requests library is already installed for you. "
    user_prompt_1 += 'To perform the task, you should try to parse and understand the response of the API calls, without generating code to process the response. I.e., you do not need to use python to process the response from API calling; instead you should parse the API response manually and ensure the relevant information is correctly extracted and utilized. '
    user_prompt_1 += f'For Gitlab, you should use my gitlab access token {gitlab_token}. For Gitlab, my username is byteblaze, my name is Byte Blaze, and my user id is 2330.\n'
    user_prompt_1 += 'For reddit, you should not need any access tokens. For Reddit, I am MarvelsGrantMan136.\n'
    user_prompt_1 += 'Make good use of HTTP headers when making API calls, and be careful of the input parameters to each api call.\n'
    user_prompt_1 += 'These are all the information you have for now, and you should not assume any additional information or ask for any user input.\n'
    user_prompt_1 += "IMPORTANT: The information provided might be incomplete or ambiguous. For example, if the I want to search for a repo 'xyz', then 'xyz' could be the name of the repo, it could be the path of the repo, or it could also be the first three characters of the repo's full name. "
    user_prompt_1 += 'Thus, your code should *cover all potential cases* that the user might be indicating and be careful about nuances.\n'
    user_prompt_1 += 'Additionally, the response json obtained through the API calls will only include the first `per-page`-many instances, so make sure that you looked at all instances but not only the first `per-page`-many instances.\n'
    user_prompt_1 += 'I will provide with you a list of API calls that you can use.\n'
    user_prompt_1 += 'You should first do `from utils import get_api_documentation_gitlab` using python to be able to use this function. '
    user_prompt_1 += "This function is defined by get_api_documentation_gitlab(api: str) -> str, which has args api (str): The API whose documentations to retrieve. For example, 'get /api/v4/projects/{id}/repository/commits'. "
    user_prompt_1 += 'This function returns the readme documentation of an API that provides you with details instructions on how to use the API.\n'
    user_prompt_1 += 'For Gitlab, if you think an API is relevant to the task, you should call get_api_documentation_gitlab(api) to get more details on how to use this API. You should execute get_api_documentation_gitlab yourself without waiting for the user to execute it.\n'
    user_prompt_1 += 'For Reddit, there is no need to call get_api_documentation_gitlab(api), as the full documentation of all Reddit APIs is provided already.\n'
    user_prompt_1 += 'If from carefully reading the documentation of APIs, you think none of the APIs I provided could solve the task, you should try fetching the content of the html pages provided directly using API calling, and parse the content of the html pages to find the answer. Note that the HTML pages could be very long, so you should try to first search for relevant details in the HTML pages instead of reading the content directly. However, in general, you should aviod extracting the HTML content directly. ' #Note: this is the *only* case that you can use an API that is not provided in the list of API below. In all other cases, you should only use APIs I provided.\n"
    user_prompt_1 += 'When you think you finished the task, respond with `Finish[answer]` where you include your answer in `[]` if the user asks for an answer; otherwise respond with Finish[].\n'
    user_prompt_1 += 'Below is a dictionary where the keys are the names of all Gitlab APIs you can use and the values are the descriptions of the APIs:\n'
    user_prompt_1 += f'{gitlab_api_file}\n\n'
    user_prompt_1 += 'Below are all the Reddit APIs you could use and their descriptions.\n'
    user_prompt_1 += f'{reddit_api_file}\n'
    return user_prompt_1

def get_wikipedia_prompt():
    prompt = 'Additionally, you could use wikipedia to help you complete the task. Your wikipedia endpoint is `http://metis.lti.cs.cmu.edu:8888/search?pattern=top+computer+science+school+in+massachusetts&books.name=wikipedia_en_all_maxi_2022-05`. Below is the documentation of this endpoint. \n'
    with open('/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/api/wikipedia.rst', 'r') as f:
        prompt += f.read()
    return prompt

def get_initial_prompt(task):
    sites = task['sites']
    if sites == ['gitlab']: return get_gitlab_initial_prompt(task)
    if sites == ['shopping']: return get_shopping_initial_prompt(task)
    if sites == ['shopping_admin']: return get_shopping_admin_initial_prompt(task)
    if sites == ['map']: return get_map_initial_prompt(task)
    if sites == ['reddit']: return get_reddit_initial_prompt(task)
    if sites == ['reddit', 'gitlab'] or sites == ['gitlab', 'reddit']: return get_reddit_gitlab_initial_prompt(task)
    if sites == ['map', 'wikipedia'] or sites == ['wikipedia', 'map']: return get_map_initial_prompt(task) + '\n' + get_wikipedia_prompt()
    if sites == ['gitlab', 'wikipedia'] or sites == ['wikipedia', 'gitlab']: return get_gitlab_initial_prompt(task) + '\n' + get_wikipedia_prompt()
    return ''

def generate(prompt):
    openai.api_key = os.environ['OPENAI_API_KEY']
    client = openai.OpenAI(api_key = os.environ['OPENAI_API_KEY'])
    messages = [
        {'role': 'user', 'content': prompt},
    ]
    response = client.chat.completions.create(  # type: ignore
        model='gpt-4o',
        messages=messages,
        temperature=0.7,
        max_tokens=64,
        top_p=0.5,
    )
    return response.choices[0].message.content

def api_or_web_prompt(intent):
    prompt = f'You will perform a task related to Gitlab usage: {intent}.\n'
    prompt += 'You now have two choices of how to perform the task: API Calling or Web Browsing.\n'
    prompt += 'For API calling, you will be provided API documentations (e.g., `get /api/v4/projects/{id}/repository/commits` is an API). '
    prompt += "To call APIs, you must generate and execute *python*'s code to use API calls through the requests library. The requests library is already installed for you.\n"
    prompt += 'For Web Browsing, you will be able to browse the Gitlab website to perform the task with <execute_browse> and </execute_browse>. '
    prompt += "For example, <execute_browse> Tell me the usa's president using google search </execute_browse>.\n"
    prompt += 'To perform the task, your first step is to determine which method you would like to choose: API Calling or Web Browsing. You should choose exactly one choice.\n'
    prompt += 'After choosing which method you would like to use, I will provide with you further instructions on how to use that method to perform the task.\n'
    prompt += 'Respond with `API` if you would like to choose API Calling; respond with `Web` if you would like to choose Web Browsing.'
    return prompt

# output = []
# with open(output_file, 'r', newline='', encoding='utf-8') as csvfile:
#     reader = csv.DictReader(csvfile)
#     data = list(reader)
#     for row in data:
#         if str(row['api']) == 'True':
#             output.append(row)

# count = {'string_match': 0, 'program_html': 0, 'url_match': 0}
# for row in output:
#     for eval_type in list(count.keys()):
#         if eval_type in row['eval_types']: count[eval_type] += 1

def choice(output_file = '/Users/artemis/Desktop/OpenDevin/evaluation/evaluation_outputs/outputs/gitlab/CodeActAgent/gpt-4o_maxiter_8_N_v1.6_/choice.csv'):
    field_names = ['task_id', 'choice', 'correct', 'theoretical']
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
    for task in all_tests:
        task_id = task['task_id']
        intent = task['intent']
        prompt = api_or_web_prompt(intent)
        choice = generate(prompt)
        theoretical = get_api_results(task_id) or get_web_results(task_id)
        if 'api' in choice.lower(): output = {'task_id': task_id, 'choice': 'api', 'correct': get_api_results(task_id), 'theoretical': theoretical}
        elif 'web' in choice.lower(): output = {'task_id': task_id, 'choice': 'web', 'correct': get_web_results(task_id), 'theoretical': theoretical}
        else: output = {'task_id': task_id, 'choice': 'none', 'correct': False, 'theoretical': theoretical}
        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writerow(output)
        print(f'finished {task_id}: {choice}')

def generate_random_string(length=4):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def sort_jsonl_by_task_id(jsonl_file):
    with open(jsonl_file, 'r') as f:
        lines = f.readlines()
    data = [json.loads(line) for line in lines]
    sorted_data = sorted(data, key=lambda x: x['task_id'])
    with open(jsonl_file, 'w') as f:
        for entry in sorted_data:
            f.write(json.dumps(entry) + '\n')

def save_code(code):
    code_file_path = generate_random_string()
    code_file_path = 'workspace/' + code_file_path
    with open(code_file_path, 'w') as f:
        f.write(code)
    return code_file_path

def get_code(response):
    response = response.replace('https://gitlab.com', 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023')
    pattern = r'```python\n(.*?)```'
    matches = re.findall(pattern, response, re.DOTALL)
    code = '\n'.join(matches)
    return save_code(code)

def run_output(file_name, old_token = None, new_token = None):
    if old_token != None and new_token != None:
        with open(file_name, 'r') as f:
            f = f.read()
            new_content = f.replace(old_token, new_token)
        with open(file_name, 'w') as f:
            f.write(new_content)
    try:
        result = subprocess.run(
            ['python', file_name],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f'Error occurred in running code in {file_name}: {e}')
        return (f'{e.stdout}\n{e.stderr}').strip()

def clean_answer(answer: str) -> str:
    answer = answer.strip()
    if answer.startswith("'") and answer.endswith("'"):
        answer = answer[1:-1]
    elif answer.startswith('"') and answer.endswith('"'):
        answer = answer[1:-1]
    return answer.lower()

def exact_match(ref: str, pred: str) -> float:
    pattern = r'Finish\[(.*?)\]'
    match = re.search(pattern, pred)
    if match: pred = match.group(1)
    return float(clean_answer(pred) == clean_answer(ref))

def must_include(ref: str, pred: str, tokenize: bool = False) -> float:
    clean_ref = clean_answer(ref)
    clean_pred = clean_answer(pred)
    return float(clean_ref in clean_pred)

def fuzzy_match(ref: str, pred: str, intent: str) -> float:
    return llm_fuzzy_match(pred, ref, intent)

def ua_match(ref: str, pred: str, intent: str) -> float:
    return llm_ua_match(pred, ref, intent)

def string_match(configs, pred) -> float:
    score = 1.0
    for approach, value in configs['eval']['reference_answers'].items():
        match approach:
            case 'exact_match':
                score *= exact_match(ref=value, pred=pred)

            case 'must_include':
                assert isinstance(value, list)
                for must_value in value:
                    score *= must_include(
                        ref=must_value,
                        pred=pred,
                        tokenize=(len(value) == 1),
                    )
            case 'fuzzy_match':
                intent = configs['intent']
                if value == 'N/A':
                    # if the instruction only asks the model to generate N/A when encountering an unachievable task
                    # without more concrete reasons
                    score *= exact_match(ref=value, pred=pred)
                    # if the instruction also asks the model to generate the reason why the task is unachievable
                    # this should be the default as it will prevent false positive N/A`
                    if score != 1:
                        score = 1.0 * ua_match(
                            intent=configs['intent'],
                            ref=configs['eval']['string_note'],
                            pred=pred,
                        )
                else:
                    assert isinstance(value, list)
                    for reference in value:
                        score *= fuzzy_match(
                            ref=reference, pred=pred, intent=intent
                        )
    return score

def get_url(history: str, response: str) -> str:
    while True:
        start_idx = history.rfind('Open pages: [')
        if start_idx == -1: break
        counter = 1
        start_idx += len('Open pages: [')
        for i in range(start_idx, len(history), 1):
            if counter != 0:
                if history[i] == '[': counter += 1
                if history[i] == ']': counter -= 1
            if counter == 0 and start_idx != i: return history[start_idx:i]
            elif counter == 0: break
        history = history[:(start_idx-len('Open pages: ['))]
    return ''

def clean_url(url: str) -> str:
    url = str(url)
    if url.startswith('"') or url.startswith("'"):
        url = url.replace('"', '')
        url = url.replace("'", '')
    url = url.rstrip('/')
    return url

def parse_url(url: str) -> tuple[str, dict[str, list[str]]]:
    """Parse a URL into its base, path, and query components."""
    url = urllib.parse.unquote(url)
    parsed_url = urllib.parse.urlparse(url)
    base_path = parsed_url.netloc + parsed_url.path
    query = urllib.parse.parse_qs(parsed_url.query)
    return base_path, query

def parse_urls(urls: list[str]) -> tuple[list[str], dict[str, set[str]]]:
    """Parse a list of URLs."""
    base_paths = []
    queries = collections.defaultdict(set)
    for url in urls:
        base_path, query = parse_url(url)
        base_paths.append(base_path)
        for k, v in query.items():
            queries[k].update(v)
    return base_paths, queries

def url_match(configs, response, history) -> float:
    pred = get_url(history, response)
    pred = clean_url(pred)
    ref_urls = configs['eval']['reference_url'].split(' |OR| ')
    ref_urls = [clean_url(url) for url in ref_urls]
    matching_rule = configs['eval'].get('url_note', 'GOLD in PRED')
    if matching_rule == 'GOLD in PRED':
        ref_base_paths, ref_queries = parse_urls(ref_urls)
        pred_base_paths, pred_query = parse_url(pred)
        logger.info(f'ref_base_paths: {ref_base_paths}')
        logger.info(f'pred_base_paths: {pred_base_paths}')
        logger.info(f'ref_queries: {ref_queries}')
        logger.info(f'pred_query: {pred_query}')
        base_score = float(
            any(
                [
                    ref_base_path.strip('/') in pred_base_paths.strip('/')
                    for ref_base_path in ref_base_paths
                ]
            )
        )
        query_score = 1.0
        for k, possible_values in ref_queries.items():
            query_score *= float(
                any(
                    possible_ref_value in pred_query.get(k, [])
                    for possible_ref_value in possible_values
                )
            )
        score = base_score * query_score
        return score
    else: raise ValueError(f'Unknown matching rule: {matching_rule}')

def program_html(configs, config_file, pred, page, history) -> float:
    targets = configs['eval']['program_html']
    score = 1.0
    # TODO: Modify to take into account evaluations of other sites
    for target in targets:
        target_url: str = target['url']  # which url to check
        if target_url.startswith('func'):
            func = target_url.split('func:')[1]
            last_url = get_url(history, pred)
            last_url = clean_url(last_url)
            logger.info(f'last_url is {last_url}')
            if last_url == '': return 0.0
            page.goto(last_url)
            time.sleep(3)
            func = func.replace('__last_url__', page.url)
            target_url = eval(func)
        locator: str = target['locator']  # js element locator
        if target_url != 'last':
            page.goto(target_url)
            time.sleep(3)
        else:
            last_url = get_url(history, pred)
            last_url = clean_url(last_url)
            logger.info(f'last_url is {last_url}')
            if last_url == '': return 0.0
            page.goto(last_url)
            time.sleep(3)
        try:
            if not locator.strip():
                selected_element = page.content()
            elif locator.startswith('document.') or locator.startswith('[...document.'):
                if 'prep_actions' in target:
                    try:
                        for prep_action in target['prep_actions']:
                            page.evaluate(f'() => {prep_action}')
                    except Exception:
                        pass
                try:
                    selected_element = str(page.evaluate(f'() => {locator}'))
                    if not selected_element: selected_element = ''
                except Exception:
                    # the page is wrong, return empty
                    selected_element = ''
            elif locator.startswith('func:'):  # a helper function
                func = locator.split('func:')[1]
                func = func.replace('__page__', 'page')
                selected_element = eval(func)
            else: raise ValueError(f'Unknown locator: {locator}')
        except Exception as e:
            logger.info(f'exception in program_html: {e}')
            selected_element = ''
        selected_element = html.unescape(selected_element)
        if 'exact_match' in target['required_contents']:
            required_contents = target['required_contents']['exact_match']
            cur_score = exact_match(
                ref=required_contents, pred=selected_element
            )
            score *= float(cur_score)
        elif 'must_include' in target['required_contents']:
            required_contents = target['required_contents']['must_include']
            assert isinstance(required_contents, list)
            for content in required_contents:
                content_or = content.split(' |OR| ')
                cur_score = any(
                    [
                        must_include(
                            ref=content,
                            pred=selected_element,
                            tokenize=False,
                        )
                        for content in content_or
                    ]
                )
                score *= float(cur_score)
        else:
            raise ValueError(
                f"Unknown required_contents: {target['required_contents'].keys()}"
            )
    #time.sleep(20)
    #env.context_manager.__exit__()
    return score

def html_match(configs, pred, page, history) -> float:
    # log in to gitlab
    temp_dir = tempfile.mkdtemp()
    config_file = f"{temp_dir}/{configs['task_id']}.json"
    with open(config_file, 'w') as f:
        json.dump(configs, f)
    score = program_html(configs, config_file, pred, page, history)
    return score

def check_correctness(task, response):
    # use the answer if the task requires string_match + exact_match;
    # use the response (the final message from the agent) if the task requires string_match but not exact_match
    # do not use response nor answer if the task requires program_html match or url_match
    score = 1.0
    # string match
    if 'string_match' in task['eval']['eval_types']:
        string_match_score = string_match(task, response)
        if (string_match_score != 1.0):
            response = response.replace('"', '')
            response = response.replace("'", '')
            response = response.replace(' ', '')
            string_match_score = string_match(task, response)
        score *= string_match_score
    # url match
    #timestamp = datetime.now().strftime('%Y-%m-%d')
    file_name = LOG_FILENAME
    with open(file_name,'r') as f: history = f.read()
    #with open('workspace/browse-gitlab.log','r') as f: history = f.read()
    #with open('workspace/browse-gitlab.log','w') as f: f.write('')
    if 'url_match' in task['eval']['eval_types']: score *= url_match(task, response, history)
    if score != 1.0: return False
    if 'program_html' not in task['eval']['eval_types']: return score == 1.0
    # setup context manager
    context_manager = sync_playwright()
    playwright = context_manager.__enter__()
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    sites = task['sites']
    if 'gitlab' in sites:
        username = 'byteblaze'
        password = 'hello1234'
        GITLAB_URL = os.environ['GITLAB']
        page.goto(f'{GITLAB_URL}/users/sign_in')
        page.get_by_test_id('username-field').click()
        page.get_by_test_id('username-field').fill(username)
        page.get_by_test_id('username-field').press('Tab')
        page.get_by_test_id('password-field').fill(password)
        page.get_by_test_id('sign-in-button').click()
        context.storage_state(path='/Users/artemis/Desktop/OpenDevin/evaluation/.auth/gitlab_state.json')
    if 'shopping' in sites:
        username = 'emma.lopez@gmail.com'
        password = 'Password.123'
        SHOPPING = os.environ['SHOPPING']
        page.goto(f'{SHOPPING}/customer/account/login/')
        page.get_by_label('Email', exact=True).fill(username)
        page.get_by_label('Password', exact=True).fill(password)
        page.get_by_role('button', name='Sign In').click()
        context.storage_state(path='/Users/artemis/Desktop/OpenDevin/evaluation/.auth/shopping_state.json')
    if 'shopping_admin' in sites:
        username = 'admin'
        password = 'admin1234'
        SHOPPING_ADMIN = os.environ['SHOPPING_ADMIN']
        page.goto(f'{SHOPPING_ADMIN}')
        # page.get_by_placeholder("user name").fill(username)
        # page.get_by_placeholder("password").fill(password)
        page.get_by_label('Username', exact=True).fill(username)
        page.get_by_label('Password', exact=True).fill(password)
        page.get_by_role('button', name='Sign in').click()
        context.storage_state(path='/Users/artemis/Desktop/OpenDevin/evaluation/.auth/shopping_admin_state.json')
    if 'reddit' in sites:
        username = 'MarvelsGrantMan136'
        password = 'test1234'
        REDDIT = os.environ['REDDIT']
        page.goto(f'{REDDIT}/login')
        page.get_by_label('Username').fill(username)
        page.get_by_label('Password').fill(password)
        page.get_by_role('button', name='Log in').click()
        context.storage_state(path='/Users/artemis/Desktop/OpenDevin/evaluation/.auth/reddit_state.json')
    if 'program_html' in task['eval']['eval_types']: score *= html_match(task, response, page, history)
    context_manager.__exit__()
    return score == 1.0
