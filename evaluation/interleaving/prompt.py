def get_gitlab_initial_prompt(task, gitlab_token='', gitlab_api_file=''):
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