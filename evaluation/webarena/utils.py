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
import csv
import openai
import requests
from bs4 import BeautifulSoup
from opendevin.core.logger import opendevin_logger as logger
from prompt import get_initial_prompt, get_initial_prompt_multi

"""base class for evaluation"""
os.environ['REDDIT'] = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999'
os.environ['SHOPPING'] = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770'
os.environ['SHOPPING_ADMIN'] = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin'
os.environ['GITLAB'] = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023'
os.environ['WIKIPEDIA'] = 'WIKIPEDIA'
os.environ['MAP'] = 'http://miniserver1875.asuscomm.com:3000'
os.environ['HOMEPAGE'] = 'HOMEPAGE'
os.environ['OPENAI_API_KEY'] = ''

from playwright.sync_api import sync_playwright
from webarena.evaluation_harness.helper_functions import (
    llm_fuzzy_match,
    llm_ua_match,
    shopping_get_latest_order_url,
    shopping_get_sku_latest_review_author,
    shopping_get_sku_latest_review_rating,
    gitlab_get_project_memeber_role,
    reddit_get_post_url,
)

gitlab_token = 'glpat-KygcYjwtD2JfA6wU4wBd'

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
    json_file_path = 'API-Based-Agent/evaluation/webarena/test.raw.json'
    with open(json_file_path, 'r') as file:
        file = file.read()
        file = file.replace('__GITLAB__', os.getenv('GITLAB'))
        file = file.replace('__SHOPPING__', os.getenv('SHOPPING'))
        file = file.replace('__SHOPPING_ADMIN__', os.getenv('SHOPPING_ADMIN'))
        file = file.replace('__MAP__', os.getenv('MAP'))
        file = file.replace('__REDDIT__', os.getenv('REDDIT'))
        data = json.loads(file)
    return data

def get_all_gitlab_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['gitlab']: output.append(dat)
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
        if dat['sites'] == ['reddit']: output.append(dat)
    return output
reddit_tests = get_reddit_test()

def get_gitlab_reddit_test():
    data = parse_test_file()
    output = []
    for dat in data:
        include = True
        if (dat['sites'] == ['reddit', 'gitlab'] or dat['sites'] == ['gitlab', 'reddit']):
            output.append(dat)
    return output
gitlab_reddit_tests = get_gitlab_reddit_test()

def get_shopping_reddit_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if (dat['sites'] == ['reddit', 'shopping'] or dat['sites'] == ['shopping', 'reddit']):
            output.append(dat)
    return output
shopping_reddit_tests = get_shopping_reddit_test()

def get_shopping_admin_map_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if (dat['sites'] == ['map', 'shopping_admin'] or dat['sites'] == ['shopping_admin', 'map']): 
            output.append(dat)
    return output
shopping_admin_map_tests = get_shopping_admin_map_test()

def get_wikipedia_map_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if (dat['sites'] == ['map', 'wikipedia'] or dat['sites'] == ['wikipedia', 'map']):
            output.append(dat)
    return output
wikipedia_map_tests = get_wikipedia_map_test()

def get_wikipedia_gitlab_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if (dat['sites'] == ['gitlab', 'wikipedia'] or dat['sites'] == ['wikipedia', 'gitlab']):
            output.append(dat)
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

def get_gitlab_apis():
    api_file_path = 'API-Based-Agent/evaluation/webarena/api/gitlab_api.txt'
    with open(api_file_path, 'r') as file:
        api_file = file.read()
    return api_file

def get_shopping_apis(shopping_html_pages = []):
    api_file_path = 'API-Based-Agent/evaluation/webarena/api/shopping-admin-summary.json'
    with open(api_file_path, 'r') as file:
        api_file = json.load(file)
    shopping_html_pages = [shopping_html_page for shopping_html_page in shopping_html_pages if shopping_html_page != os.getenv('SHOPPING')]
    if shopping_html_pages == []: return api_file
    new_api_file = {}
    for shopping_html_page in shopping_html_pages:
        new_api_file[shopping_html_page] = f'Retrieve the content in the HTML page {shopping_html_page}'
    new_api_file.update(api_file)
    return new_api_file

def get_map_apis():
    api_doc = ''
    dir = 'API-Based-Agent/evaluation/webarena/api/map/'
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

def get_reddit_apis():
    with open('API-Based-Agent/evaluation/webarena/api/reddit.md', 'r') as f:
        f = f.read()
    return f

def get_initial_prompt_from_task(task):
    sites = task['sites']
    if sites == ['gitlab'] or ('gitlab' in sites and 'wikipedia' in sites): 
        site_name = 'gitlab'
        site_base = os.getenv('GITLAB')
        os.environ['GITLAB_START_URL'] = task['start_url']
        logger.info(f"os.environ['GITLAB_START_URL']: {os.environ['GITLAB_START_URL']}")
        return get_initial_prompt(site_name, site_base, task, get_gitlab_apis(), gitlab_token)
    if sites == ['shopping']: 
        site_name = 'shopping'
        site_base = os.getenv('SHOPPING')
        shopping_api_file = get_shopping_apis()
        os.environ['SHOPPING_START_URL'] = task['start_url']
        logger.info(f"os.environ['SHOPPING_START_URL']: {os.environ['SHOPPING_START_URL']}")
        admin_token = get_shopping_admin_auth_token()
        customer_token = get_shopping_customer_auth_token()
        extra_user_info = f'You should always use my access token {admin_token} in general. However, only when using the endpoints that contains `/V1/carts/mine` in the API, you must use this access token: {customer_token}, which you must not use for any other endpoints. For example, for the API endpoint `V1/products` you should use {admin_token}; while for the `/V1/carts/mine/items` endpoint, you should use {customer_token}.\n'
        return get_initial_prompt(site_name, site_base, task, shopping_api_file, '', extra_user_info)
    if sites == ['shopping_admin']:
        site_name = 'shopping_admin'
        site_base = os.getenv('SHOPPING_ADMIN')
        shopping_api_file = get_shopping_apis()
        os.environ['SHOPPING_ADMIN_START_URL'] = task['start_url']
        logger.info(f"os.environ['SHOPPING_ADMIN_START_URL']: {os.environ['SHOPPING_ADMIN_START_URL']}")
        admin_token = get_shopping_admin_admin_auth_token()
        return get_initial_prompt(site_name, site_base, task, shopping_api_file, admin_token, '')
    if sites == ['map'] or ('map' in sites and 'wikipedia' in sites):
        site_name = 'map'
        site_base = os.getenv('MAP')
        map_api_file = get_map_apis()
        os.environ['MAP_START_URL'] = task['start_url']
        logger.info(f"os.environ['MAP_START_URL']: {os.environ['MAP_START_URL']}")
        return get_initial_prompt(site_name, site_base, task, map_api_file, '', '')
    if sites == ['reddit']:
        site_name = 'reddit'
        site_base = os.getenv('REDDIT')
        reddit_api_file = get_reddit_apis()
        os.environ['REDDIT_START_URL'] = task['start_url']
        logger.info(f"os.environ['REDDIT_START_URL']: {os.environ['REDDIT_START_URL']}")
        return get_initial_prompt(site_name, site_base, task, reddit_api_file, '', '')
    if sites == ['map', 'shopping_admin']:
        shopping_admin_site = {'site_base': os.getenv('SHOPPING_ADMIN'), 'api_info': get_shopping_apis(), 'api_token': get_shopping_admin_admin_auth_token(), 'extra_user_info': ''}
        map_site = {'site_base': os.getenv('MAP'), 'api_info': get_map_apis(), 'api_token': '', 'extra_user_info': ''}
        sites = {'shopping_admin': shopping_admin_site, 'map': map_site}
        return get_initial_prompt_multi(sites, task)
    if sites == ['shopping', 'reddit']:
        shopping_site = {'site_base': os.getenv('SHOPPING'), 'api_info': get_shopping_apis(), 'api_token': get_shopping_admin_auth_token(), 'extra_user_info': ''}
        reddit_site = {'site_base': os.getenv('REDDIT'), 'api_info': get_reddit_apis(), 'api_token': '', 'extra_user_info': ''}
        sites = {'shopping': shopping_site, 'reddit': reddit_site}
        return get_initial_prompt_multi(sites, task)
    if sites == ['gitlab', 'reddit'] or sites == ['reddit', 'gitlab']:
        gitlab_site = {'site_base': os.getenv('GITLAB'), 'api_info': get_gitlab_apis(), 'api_token': gitlab_token, 'extra_user_info': ''}
        reddit_site = {'site_base': os.getenv('REDDIT'), 'api_info': get_reddit_apis(), 'api_token': '', 'extra_user_info': ''}
        sites = {'gitlab': gitlab_site, 'reddit': reddit_site}
        return get_initial_prompt_multi(sites, task)
    return ''

def clean_answer(answer: str) -> str:
    answer = answer.strip()
    if answer.startswith("'") and answer.endswith("'"):
        answer = answer[1:-1]
    elif answer.startswith('"') and answer.endswith('"'):
        answer = answer[1:-1]
    return answer.lower()

def exact_match(ref: str, pred: str) -> float:
    pattern = r'Finish\[(.*?)\]'
    matches = re.findall(pattern, pred)
    if matches != []: pred = matches[-1]
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
    for target in targets:
        target_url: str = target['url']  # which url to check
        if target_url.startswith('func'):
            func = target_url.split('func:')[1]
            last_url = get_url(history, pred)
            last_url = clean_url(last_url)
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
    return score

def html_match(configs, pred, page, history) -> float:
    temp_dir = tempfile.mkdtemp()
    config_file = f"{temp_dir}/{configs['task_id']}.json"
    with open(config_file, 'w') as f:
        json.dump(configs, f)
    score = program_html(configs, config_file, pred, page, history)
    return score

def check_correctness(task, response, log_file):
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
    with open(log_file, 'r') as f: history = f.read()
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
        context.storage_state(path='API-Based-Agent/evaluation/.auth/gitlab_state.json')
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