import collections
import json
import urllib


def parse_test_file():
    json_file_path = '/Users/artemis/Desktop/OpenDevin/evaluation/gitlab/test.raw.json'
    with open(json_file_path, 'r') as file:
        file = file.read()
        file = file.replace(
            '__GITLAB__',
            'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023',
        )
        file = file.replace(
            '__SHOPPING__',
            'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770',
        )
        file = file.replace(
            '__SHOPPING_ADMIN__',
            'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin',
        )
        file = file.replace(
            '__MAP__', 'http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000'
        )
        file = file.replace(
            '__REDDIT__',
            'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999',
        )
        data = json.loads(file)
    return data


def get_task_by_task_id(task_id):
    for test in parse_test_file():
        if test['task_id'] == task_id:
            return test
    return None


def get_all_gitlab_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['gitlab']:
            output.append(dat)
    return output


gitlab_tests = get_all_gitlab_test()


def get_map_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['map']:
            output.append(dat)
    return output


map_tests = get_map_test()


def get_shopping_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['shopping']:
            output.append(dat)
    return output


shopping_tests = get_shopping_test()


def get_shopping_admin_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['shopping_admin']:
            output.append(dat)
    return output


shopping_admin_tests = get_shopping_admin_test()


def get_reddit_test():
    data = parse_test_file()
    output = []
    for dat in data:
        if dat['sites'] == ['reddit']:
            output.append(dat)
    return output


reddit_tests = get_reddit_test()


def get_web_results(task_id):
    with open('merged_log.txt', 'r', encoding='utf-8') as file:
        log = file.read()
    for line in log.strip().split('\n'):
        if f'/{task_id}.json' in line:
            if '[Result] (PASS)' in line:
                return True
            if '[Result] (FAIL)' in line:
                return False
    return False


def get_theoretical(tests, api_result_file):
    with open(api_result_file, 'r') as f:
        f = f.readlines()
    results = []
    count = 0
    for line in f:
        results.append(json.loads(line))
    for task in tests:
        task_id = task['task_id']
        for line in results:
            if line['task_id'] == task_id:
                api_correct = line['correct']
        if 'url_match' in task['eval']['eval_types']:
            api_correct = False
        web_correct = get_web_results(task_id)
        if api_correct or web_correct:
            count += 1
    print(count)


# get_theoretical(reddit_tests, '/Users/artemis/Desktop/OpenDevin/evaluation/evaluation_outputs/outputs/gitlab/CodeActAgent/gpt-4o_maxiter_10_N_v1.6_/output_reddit_gpt-4o.jsonl')


def parse_log(tests, log_file):
    with open(log_file, 'r') as f:
        text = f.read()
    text = text.split('Loading llm config from llm')
    text = text[1:]
    print(len(text))
    saved = []
    for idx in range(len(tests)):
        task = tests[idx]
        task_id = task['task_id']
        intent = task['intent']
        for log_idx in range(len(text) - 1, -1, -1):
            log = text[log_idx].strip()
            if (
                f'opendevin:INFO: run_infer.py:267 - Finished evaluation for instance {task_id}'
                in log
            ):
                with open(
                    f'/Users/artemis/Desktop/OpenDevin/logs/interleaving/{task_id}.log',
                    'w',
                ) as f:
                    f = f.write(log)
                    print(
                        f'{log_idx} saved log for task_id {task_id}; {intent}; {log.splitlines()[1]}'
                    )
                    saved.append(task_id)
                break
            if (
                f'opendevin:INFO: run_infer.py:265 - Finished evaluation for instance {task_id}'
                in log
            ):
                with open(
                    f'/Users/artemis/Desktop/OpenDevin/logs/interleaving/{task_id}.log',
                    'w',
                ) as f:
                    f = f.write(log)
                    print(
                        f'{log_idx} saved log for task_id {task_id}; {intent}; {log.splitlines()[1]}'
                    )
                    saved.append(task_id)
                break
            # print(f'index mismatch! {task_id}; {intent}; {log.splitlines()[1]}; retry')
    missed = [task['task_id'] for task in tests if task['task_id'] not in saved]
    print(f'missed: {missed}')


def get_stats(tests):
    total = {'string_match': 0, 'program_html': 0, 'url_match': 0}
    count_api = {'string_match': 0, 'program_html': 0, 'url_match': 0}
    count_web = {'string_match': 0, 'program_html': 0, 'url_match': 0}
    count_both = {'string_match': 0, 'program_html': 0, 'url_match': 0}
    correct_api = {'string_match': 0, 'program_html': 0, 'url_match': 0}
    correct_web = {'string_match': 0, 'program_html': 0, 'url_match': 0}
    count_correct = 0
    for task in tests:
        task_id = task['task_id']
        log = f'/Users/artemis/Desktop/OpenDevin/logs/webarena_logs/{task_id}.log'
        try:
            with open(log, 'r') as f:
                log = f.read()
        except:
            log = ''
        if 'import requests' in log:
            use_api = True
        else:
            use_api = False
        if 'BrowsingAgent' in log:
            use_web = True
        else:
            use_web = False
        is_correct = 'Correct: True' in log
        if is_correct:
            count_correct += 1
        for eval_type in task['eval']['eval_types']:
            total[eval_type] += 1
            if use_api:
                count_api[eval_type] += 1
                if is_correct:
                    correct_api[eval_type] += 1
            if use_web:
                count_web[eval_type] += 1
                if is_correct:
                    print(task_id)
                    correct_web[eval_type] += 1
            if use_api and use_web:
                count_both[eval_type] += 1
    print(f'total: {total}')
    print(f'count_api: {count_api}')
    print(f'count_web: {count_web}')
    print(f'count_both: {count_both}')
    print(f'total_correct: {count_correct}')
    print(f'correct_api: {correct_api}')
    print(f'correct_web: {correct_web}')


# parse_log(shopping_admin_tests, '/Users/artemis/Desktop/OpenDevin/logs/shopping-admin-interleaving.log')
get_stats(shopping_admin_tests)


def get_url(history: str, response: str) -> str:
    while True:
        start_idx = history.rfind('Open pages: [')
        if start_idx == -1:
            break
        counter = 1
        start_idx += len('Open pages: [')
        for i in range(start_idx, len(history), 1):
            if counter != 0:
                if history[i] == '[':
                    counter += 1
                if history[i] == ']':
                    counter -= 1
            if counter == 0 and start_idx != i:
                return history[start_idx:i]
            elif counter == 0:
                break
        history = history[: (start_idx - len('Open pages: ['))]
    return ''


def clean_url(url: str) -> str:
    url = str(url)
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
        print(f'ref_base_paths: {ref_base_paths}')
        print(f'pred_base_paths: {pred_base_paths}')
        print(f'ref_queries: {ref_queries}')
        print(f'pred_query: {pred_query}')
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
    else:
        raise ValueError(f'Unknown matching rule: {matching_rule}')


def check_url_match(task_id):
    log = f'/Users/artemis/Desktop/OpenDevin/logs/webarena_logs/{task_id}.log'
    try:
        with open(log, 'r') as f:
            log = f.read()
    except:
        log = ''
    task = get_task_by_task_id(task_id)
    score = url_match(task, '', log)
    return score == 1.0


# task_ids = [task['task_id'] for task in get_shopping_admin_test() if task['eval']['eval_types'] == ['url_match']]
# for task_id in task_ids:
#     print(task_id, check_url_match(task_id))
