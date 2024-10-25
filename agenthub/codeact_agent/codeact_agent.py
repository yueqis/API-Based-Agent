import os

from browsergym.core.action.highlevel import HighLevelActionSet
from browsergym.utils.obs import flatten_axtree_to_str

from agenthub.codeact_agent.action_parser import InterleavingResponseParser
from agenthub.codeact_agent.prompt import SYSTEM_PREFIX, API_PROMPT, BROWSING_PREFIX, SYSTEM_SUFFIX, EXAMPLE_PROMPT
from opendevin.core.logger import opendevin_logger as logger
from opendevin.controller.agent import Agent
from opendevin.controller.state.state import State
from opendevin.events.action import (
    Action,
    AgentFinishAction,
    BrowseInteractiveAction,
    CmdRunAction,
    IPythonRunCellAction,
    MessageAction,
)
from opendevin.events.event import EventSource
from opendevin.events.observation import (
    BrowserOutputObservation,
    CmdOutputObservation,
    IPythonRunCellObservation,
)
from opendevin.events.observation.observation import Observation
from opendevin.llm.llm import LLM
from opendevin.runtime.plugins import (
    AgentSkillsRequirement,
    JupyterRequirement,
    PluginRequirement,
)
from opendevin.runtime.tools import RuntimeTool

ENABLE_GITHUB = False
USE_NAV = (
    os.environ.get('USE_NAV', 'true') == 'true'
)  # only disable NAV actions when running webarena and miniwob benchmarks
USE_CONCISE_ANSWER = (
    os.environ.get('USE_CONCISE_ANSWER', 'false') == 'true'
)  # only return concise answer when running webarena and miniwob benchmarks

if not USE_NAV and USE_CONCISE_ANSWER:
    EVAL_MODE = True  # disabled NAV actions and only return concise answer, for webarena and miniwob benchmarks\
else:
    EVAL_MODE = False
EVAL_MODE = True
PROMPT_CACHE = True

GITLAB_URL = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:8023'
SHOPPING_URL = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7770'
SHOPPING_ADMIN_URL = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:7780/admin'
MAP_URL = 'http://miniserver1875.asuscomm.com:3000'
REDDIT_URL = 'http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999'
def get_error_prefix(last_browser_action: str) -> str:
    return f'IMPORTANT! Last action is incorrect:\n{last_browser_action}\nThink again with the current observation of the page.\n'

CONCISE_INSTRUCTION = """\

Here is another example with chain of thought of a valid action when providing a concise answer to user:
"
In order to accomplish my goal I need to send the information asked back to the user. This page list the information of HP Inkjet Fax Machine, which is the product identified in the objective. Its price is $279.49. I will send a message back to user with the answer.
```send_msg_to_user("$279.49")```
"
"""

def get_browse_prompt(error_prefix: str, cur_axtree_txt: str, prev_action_str: str) -> str:
    prompt = f"""\
{error_prefix}

# Current Accessibility Tree:
{cur_axtree_txt}

# Previous Actions:
{prev_action_str if prev_action_str.strip() != '' else 'None.'}

Here is an example with chain of thought of a valid action when clicking on a button:
"
In order to accomplish my goal I need to click on the button with bid 12
```click("12")```
"
""".strip()
    if USE_CONCISE_ANSWER:
        prompt += CONCISE_INSTRUCTION
    return prompt

def action_to_str(action: Action) -> str:
    if isinstance(action, CmdRunAction):
        return f'{action.thought}\n<execute_bash>\n{action.command}\n</execute_bash>'
    elif isinstance(action, IPythonRunCellAction):
        return f'{action.thought}\n<execute_ipython>\n{action.code}\n</execute_ipython>'
    elif isinstance(action, BrowseInteractiveAction):
        return f'{action.thought}\n<execute_browse>\n{action.browser_actions}\n</execute_browse>'
    elif isinstance(action, MessageAction):
        return action.content
    return ''


def get_action_message(action: Action) -> dict[str, str] | None:
    if (
        isinstance(action, BrowseInteractiveAction)
        or isinstance(action, CmdRunAction)
        or isinstance(action, IPythonRunCellAction)
        or isinstance(action, MessageAction)
    ):
        return {
            'role': 'user' if action.source == 'user' else 'assistant',
            'content': action_to_str(action),
        }
    return None


def get_observation_message(obs) -> dict[str, str] | None:
    if isinstance(obs, CmdOutputObservation):
        content = 'OBSERVATION:\n' + truncate_observation(obs.content)
        content += (
            f'\n[Command {obs.command_id} finished with exit code {obs.exit_code}]'
        )
        return {'role': 'user', 'content': content}
    elif isinstance(obs, IPythonRunCellObservation):
        content = 'OBSERVATION:\n' + obs.content
        # replace base64 images with a placeholder
        splitted = content.split('\n')
        for i, line in enumerate(splitted):
            if '![image](data:image/png;base64,' in line:
                splitted[i] = (
                    '![image](data:image/png;base64, ...) already displayed to user'
                )
        content = '\n'.join(splitted)
        content = truncate_observation(content)
        return {'role': 'user', 'content': content}
    elif isinstance(obs, BrowserOutputObservation):
        content = 'OBSERVATION:\n' + truncate_observation(obs.content)
        return {'role': 'user', 'content': content}
    return None


def truncate_observation(observation: str, max_chars: int = 10_000) -> str:
    """
    Truncate the middle of the observation if it is too long.
    """
    if len(observation) <= max_chars:
        return observation
    half = max_chars // 2
    return (
        observation[:half]
        + '\n[... Observation truncated due to length ...]\n'
        + observation[-half:]
    )


def get_in_context_example() -> str:
    return EXAMPLES


class CodeActAgent(Agent):
    VERSION = '1.6'
    """
    The Code Act Agent is a minimalist agent.
    The agent works by passing the model a list of action-observation pairs and prompting the model to take the next step.

    ### Overview

    This agent implements the CodeAct idea ([paper](https://arxiv.org/abs/2402.13463), [tweet](https://twitter.com/xingyaow_/status/1754556835703751087)) that consolidates LLM agents’ **act**ions into a unified **code** action space for both *simplicity* and *performance* (see paper for more details).

    The conceptual idea is illustrated below. At each turn, the agent can:

    1. **Converse**: Communicate with humans in natural language to ask for clarification, confirmation, etc.
    2. **CodeAct**: Choose to perform the task by executing code
    - Execute any valid Linux `bash` command
    - Execute any valid `Python` code with [an interactive Python interpreter](https://ipython.org/). This is simulated through `bash` command, see plugin system below for more details.

    ![image](https://github.com/OpenDevin/OpenDevin/assets/38853559/92b622e3-72ad-4a61-8f41-8c040b6d5fb3)

    ### Plugin System

    To make the CodeAct agent more powerful with only access to `bash` action space, CodeAct agent leverages OpenDevin's plugin system:
    - [Jupyter plugin](https://github.com/OpenDevin/OpenDevin/tree/main/opendevin/runtime/plugins/jupyter): for IPython execution via bash command
    - [SWE-agent tool plugin](https://github.com/OpenDevin/OpenDevin/tree/main/opendevin/runtime/plugins/swe_agent_commands): Powerful bash command line tools for software development tasks introduced by [swe-agent](https://github.com/princeton-nlp/swe-agent).

    ### Demo

    https://github.com/OpenDevin/OpenDevin/assets/38853559/f592a192-e86c-4f48-ad31-d69282d5f6ac

    *Example of CodeActAgent with `gpt-4-turbo-2024-04-09` performing a data science task (linear regression)*

    ### Work-in-progress & Next step

    [] Support web-browsing
    [] Complete the workflow for CodeAct agent to submit Github PRs

    """

    sandbox_plugins: list[PluginRequirement] = [
        # NOTE: AgentSkillsRequirement need to go before JupyterRequirement, since
        # AgentSkillsRequirement provides a lot of Python functions
        # and it need to be initialized before Jupyter for Jupyter to use those functions.
        AgentSkillsRequirement(),
        JupyterRequirement(),
    ]
    runtime_tools: list[RuntimeTool] = [RuntimeTool.BROWSER]
    action_parser = InterleavingResponseParser()

    def __init__(
        self,
        llm: LLM,
    ) -> None:
        """
        Initializes a new instance of the CodeActAgent class.

        Parameters:
        - llm (LLM): The llm to be used by this agent
        """
        super().__init__(llm)
        action_subsets = ['chat', 'bid']
        if USE_NAV:
            action_subsets.append('nav')
        self.action_space = HighLevelActionSet(
            subsets=action_subsets,
            strict=False,  # less strict on the parsing of the actions
            multiaction=True,  # enable to agent to take multiple actions at once
        )
        self.reset()

    def reset(self) -> None:
        """
        Resets the CodeAct Agent.
        """
        super().reset()
        self.cost_accumulator = 0
        self.error_accumulator = 0

    def step(self, state: State) -> Action:
        """
        Performs one step using the CodeAct Agent.
        This includes gathering info on previous steps and prompting the model to make a command to execute.

        Parameters:
        - state (State): used to get updated info and background commands

        Returns:
        - CmdRunAction(command) - bash command to run
        - IPythonRunCellAction(code) - IPython code to run
        - AgentDelegateAction(agent, inputs) - delegate action for (sub)task
        - MessageAction(content) - Message action to run (e.g. ask for clarification)
        - AgentFinishAction() - end the interaction
        """
        history_str = f"{state.history}"
        SYSTEM_PROMPT = SYSTEM_PREFIX + API_PROMPT + BROWSING_PREFIX + SYSTEM_SUFFIX + EXAMPLE_PROMPT

        messages: list[dict[str, str]] = [
            {'role': 'system', 'content': SYSTEM_PROMPT},
        ]
        cur_axtree_txt = ''
        error_prefix = ''
        last_obs = None
        last_action = None
        prev_actions = []
        browse_prompt = get_browse_prompt('', '', '')
        for i, (prev_action, obs) in enumerate(state.history):
            if isinstance(prev_action, BrowseInteractiveAction):
                last_action = prev_action
                last_obs = obs
                # Removing the first action is for webarena only
                if i != 1 and i != 2 and i != 3: prev_actions.append(prev_action.browser_actions)
                if last_obs.error and i > 3:
                # add error recovery prompt prefix
                    error_prefix = get_error_prefix(last_obs.last_browser_action)
                    self.error_accumulator += 1
                    if self.error_accumulator > 10:
                        return MessageAction('Too many errors encountered. Task failed.')
                try:
                    cur_axtree_txt = flatten_axtree_to_str(
                        last_obs.axtree_object,
                        extra_properties=last_obs.extra_element_properties,
                        with_clickable=True,
                        filter_visible_only=True,
                    )
                except Exception as e:
                    logger.error(
                        'Error when trying to process the accessibility tree: %s', e
                    )
                    return MessageAction('Error encountered when browsing.')
                prev_action_str = '\n'.join(prev_actions)
                browse_prompt = get_browse_prompt(error_prefix, cur_axtree_txt, prev_action_str)
            if i == 3:
                browse_prompt = get_browse_prompt('', cur_axtree_txt, '')
                continue
            if i == 1 or i == 2: continue
            if isinstance(prev_action, Action):
                message = get_action_message(prev_action)
                if message:
                    messages.append(message)
            if isinstance(obs, Observation):
                message = get_observation_message(obs)
                if message:
                    messages.append(message)
      
        # logger.info(f"browse_prompt: {browse_prompt}")
        if (
            isinstance(last_action, BrowseInteractiveAction)
            and last_action.browsergym_send_msg_to_user
        ):
            return MessageAction(last_action.browsergym_send_msg_to_user)

        if EVAL_MODE and len(state.history) == 1:
            # for webarena and miniwob++ eval, we need to retrieve the initial observation already in browser env
            # initialize and retrieve the first observation by issuing an noop OP
            # For non-benchmark browsing, the browser env starts with a blank page, and the agent is expected to first navigate to desired websites
            # This message will not be included in `messages` 
            
            ### SHOPPING
            if SHOPPING_URL in history_str:
                logger.info(f"logging in to shopping website")
                action = f'goto("{SHOPPING_URL}/customer/account/login/")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### MAP
            if MAP_URL in history_str:
                logger.info(f"logging in to map website")
                action = f'goto("{MAP_URL}")\n'
                response = f'<execute_browse> {action} </execute_browse>'
            
            ### SHOPPING ADMIN    
            if SHOPPING_ADMIN_URL in history_str:
                logger.info(f"logging in to shopping admin website")
                action = f'goto("{SHOPPING_ADMIN_URL}")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### REDDIT
            if REDDIT_URL in history_str:
                logger.info(f"logging in to reddit website")
                action = f'goto("http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/login?_cookie_check=1727865249")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### GITLAB
            if GITLAB_URL in history_str:
                logger.info(f"logging in to gitlab")
                action = f'goto("{GITLAB_URL}/users/sign_in")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### GITLAB and REDDIT
            if GITLAB_URL in history_str and REDDIT_URL in history_str:
                logger.info(f"logging in to reddit")
                action = f'goto("http://ec2-18-219-239-190.us-east-2.compute.amazonaws.com:9999/login?_cookie_check=1727865249")\n'
                action += 'fill("62", "MarvelsGrantMan136")\n'
                action += 'fill("65", "test1234")\n'
                action += 'click("76")\n'
                response = f'<execute_browse> {action} </execute_browse>'

        elif EVAL_MODE and len(state.history) <= 2:
            
            ### SHOPPING
            if SHOPPING_URL in history_str:
                action = 'fill("1375", "emma.lopez@gmail.com")\n'
                action += 'fill("1380", "Password.123")\n'
                action += 'click("1387")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### MAP
            if MAP_URL in history_str:
                MAP_START_URL = os.environ.get('MAP_START_URL', MAP_URL)
                action = f'goto("{MAP_START_URL}")\n'
                response = f'<execute_browse> {action} </execute_browse>'
                
            ### SHOPPING ADMIN    
            if SHOPPING_ADMIN_URL in history_str:
                action = 'fill("133", "admin")\n'
                action += 'fill("138", "admin1234")\n'
                action += 'click("141")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### REDDIT
            if REDDIT_URL in history_str:
                action = 'fill("62", "MarvelsGrantMan136")\n'
                action += 'fill("65", "test1234")\n'
                action += 'click("76")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### GITLAB
            if GITLAB_URL in history_str:
                action = 'fill("66", "byteblaze")\n'
                action += 'fill("70", "hello1234")\n'
                action += 'click("83")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### GITLAB and REDDIT
            if GITLAB_URL in history_str and REDDIT_URL in history_str:
                logger.info(f"logging in to gitlab")
                action = f'goto("{GITLAB_URL}/users/sign_in")\n'
                response = f'<execute_browse> {action} </execute_browse>'
        
        elif EVAL_MODE and len(state.history) <= 3:
            
            ### SHOPPING
            if SHOPPING_URL in history_str:
                SHOPPING_START_URL = os.environ.get('SHOPPING_START_URL', SHOPPING_URL)
                logger.info(f"opening shopping {SHOPPING_START_URL}")
                task_start_urls = [task_start_url.strip() for task_start_url in SHOPPING_START_URL.split('|AND|')]
                action = ''
                for url in task_start_urls:
                    action += f'goto("{url}")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### SHOPPING ADMIN
            if SHOPPING_ADMIN_URL in history_str:
                SHOPPING_ADMIN_START_URL = os.environ.get('SHOPPING_ADMIN_START_URL', SHOPPING_ADMIN_URL)
                logger.info(f"opening shopping admin {SHOPPING_ADMIN_START_URL}")
                action = f'goto("{SHOPPING_ADMIN_START_URL}")'
                response = f'<execute_browse> {action} </execute_browse>'

            ### MAP
            if MAP_URL in history_str:
                MAP_START_URL = os.environ.get('MAP_START_URL', MAP_URL)
                action = f'goto("{MAP_START_URL}")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### REDDIT
            if REDDIT_URL in history_str:
                REDDIT_START_URL = os.environ.get('REDDIT_START_URL', REDDIT_URL)
                action = f'goto("{REDDIT_START_URL}")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            if SHOPPING_URL in history_str and REDDIT_URL in history_str:
                SHOPPING_START_URL = os.environ.get('SHOPPING_START_URL', SHOPPING_URL)
                logger.info(f"opening shopping {SHOPPING_START_URL}")
                task_start_urls = [task_start_url.strip() for task_start_url in SHOPPING_START_URL.split('|AND|')]
                action = ''
                for url in task_start_urls:
                    action += f'goto("{url}")\n'
                response = f'<execute_browse> {action} </execute_browse>'

            ### GITLAB
            if GITLAB_URL in history_str:
                GITLAB_START_URL = os.environ.get('GITLAB_START_URL', GITLAB_URL)
                logger.info(f"opening gitlab {GITLAB_START_URL}")
                action = f'goto("{GITLAB_START_URL}")'
                response = f'<execute_browse> {action} </execute_browse>'

            ### GITLAB and REDDIT
            if GITLAB_URL in history_str and REDDIT_URL in history_str:
                logger.info(f"logging in to gitlab")
                action = 'fill("66", "byteblaze")\n'
                action += 'fill("70", "hello1234")\n'
                action += 'click("83")\n'
                response = f'<execute_browse> {action} </execute_browse>'


        else:
            messages[-1]['content'] = messages[-1]['content'] + '\n' + browse_prompt
            latest_user_messages = [m for m in messages if m['role'] == 'user']
            if len(latest_user_messages) >= 1:
                latest_user_message = latest_user_messages[-1]
                if latest_user_message:
                    if latest_user_message['content'].strip() == '/exit':
                        return AgentFinishAction()
                    latest_user_message['content'] += (
                        f'\n\nENVIRONMENT REMINDER: You have {state.max_iterations - state.iteration} turns left to complete the task.'
                    )
            for message in messages:
                message['content'] = message['content'].replace('**JavaScript seems to be disabled in your browser.** For the best experience on our site, be sure to turn on Javascript in your browser.', '')
                message['content'] = message['content'].replace('The store will not work correctly when cookies are disabled.', '')
            response = self.llm.completion(
                messages=messages,
                stop=[
                    '</execute_ipython>',
                    '</execute_bash>',
                    '</execute_browse>',
                ],
                temperature=0.0,
            )
            state.num_of_chars += sum(
                len(message['content']) for message in messages
            ) + len(response.choices[0].message.content)        
        
        # for i,message in enumerate(messages):
        #     logger.info(f"{i}: {message}")
        # logger.info(f"response: {response}")

        return self.action_parser.parse(response)

    def search_memory(self, query: str) -> list[str]:
        raise NotImplementedError('Implement this abstract method')
