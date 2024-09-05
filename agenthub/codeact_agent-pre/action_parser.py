import re

from opendevin.controller.action_parser import ActionParser, ResponseParser
from opendevin.events.action import (
    Action,
    AgentDelegateAction,
    AgentFinishAction,
    CmdRunAction,
    IPythonRunCellAction,
    MessageAction,
)


class CodeActResponseParser(ResponseParser):
    """
    Parser action:
        - CmdRunAction(command) - bash command to run
        - IPythonRunCellAction(code) - IPython code to run
        - AgentDelegateAction(agent, inputs) - delegate action for (sub)task
        - MessageAction(content) - Message action to run (e.g. ask for clarification)
        - AgentFinishAction() - end the interaction
    """

    def __init__(
        self,
    ):
        # Need pay attention to the item order in self.action_parsers
        self.action_parsers = [
            CodeActActionParserFinish(),
            CodeActActionParserCmdRun(),
            CodeActActionParserIPythonRunCell(),
            CodeActActionParserAgentDelegate(),
        ]
        self.default_parser = CodeActActionParserMessage()

    def parse(self, response: str) -> Action:
        action_str = self.parse_response(response)
        return self.parse_action(action_str)

    def parse_response(self, response) -> str:
        action = response.choices[0].message.content
        for lang in ['bash', 'ipython', 'browse']:
            if f'<execute_{lang}>' in action and f'</execute_{lang}>' not in action:
                action += f'</execute_{lang}>'
        return action

    def parse_action(self, action_str: str) -> Action:
        for action_parser in self.action_parsers:
            if action_parser.check_condition(action_str):
                return action_parser.parse(action_str)
        return self.default_parser.parse(action_str)


class CodeActActionParserFinish(ActionParser):
    """
    Parser action:
        - AgentFinishAction() - end the interaction
    """

    def __init__(
        self,
    ):
        self.finish_command = None

    def check_condition(self, action_str: str) -> bool:
        self.finish_command = re.search(r'<finish>.*</finish>', action_str, re.DOTALL)
        return self.finish_command is not None

    def parse(self, action_str: str) -> Action:
        assert (
            self.finish_command is not None
        ), 'self.finish_command should not be None when parse is called'
        thought = action_str.replace(self.finish_command.group(0), '').strip()
        return AgentFinishAction(thought=thought)


class CodeActActionParserCmdRun(ActionParser):
    """
    Parser action:
        - CmdRunAction(command) - bash command to run
        - AgentFinishAction() - end the interaction
    """

    def __init__(
        self,
    ):
        self.bash_command = None

    def check_condition(self, action_str: str) -> bool:
        self.bash_command = re.search(
            r'<execute_bash>(.*?)</execute_bash>', action_str, re.DOTALL
        )
        return self.bash_command is not None

    def parse(self, action_str: str) -> Action:
        assert (
            self.bash_command is not None
        ), 'self.bash_command should not be None when parse is called'
        thought = action_str.replace(self.bash_command.group(0), '').strip()
        # a command was found
        command_group = self.bash_command.group(1).strip()
        if command_group.strip() == 'exit':
            return AgentFinishAction()
        return CmdRunAction(command=command_group, thought=thought)


class CodeActActionParserIPythonRunCell(ActionParser):
    """
    Parser action:
        - IPythonRunCellAction(code) - IPython code to run
    """

    def __init__(
        self,
    ):
        self.python_code = None
        self.jupyter_kernel_init_code: str = 'from agentskills import *'

    def check_condition(self, action_str: str) -> bool:
        self.python_code = re.search(
            r'<execute_ipython>(.*?)</execute_ipython>', action_str, re.DOTALL
        )
        return self.python_code is not None

    def parse(self, action_str: str) -> Action:
        assert (
            self.python_code is not None
        ), 'self.python_code should not be None when parse is called'
        code_group = self.python_code.group(1).strip()
        thought = action_str.replace(self.python_code.group(0), '').strip()
        return IPythonRunCellAction(
            code=code_group,
            thought=thought,
            kernel_init_code=self.jupyter_kernel_init_code,
        )


class CodeActActionParserAgentDelegate(ActionParser):
    """
    Parser action:
        - AgentDelegateAction(agent, inputs) - delegate action for (sub)task
    """

    def __init__(
        self,
    ):
        self.agent_delegate = None

    def check_condition(self, action_str: str) -> bool:
        self.agent_delegate = re.search(
            r'<execute_browse>(.*)</execute_browse>', action_str, re.DOTALL
        )
        return self.agent_delegate is not None

    def parse(self, action_str: str) -> Action:
        assert (
            self.agent_delegate is not None
        ), 'self.agent_delegate should not be None when parse is called'
        thought = action_str.replace(self.agent_delegate.group(0), '').strip()
        browse_actions = self.agent_delegate.group(1).strip()
        with open("/Users/artemis/Desktop/OpenDevin/workspace/log-gitlab.log", 'r') as f:
            log = f.read()
        credentials = "" 
        credentials += "My Gitlab username is byteblaze and password is hello1234. "
        credentials += "My e-commerce shopping website login email is emma.lopez@gmail.com and my password is Password.123. "
        credentials += "My shopping admin username is admin and password is admin1234. "
        credentials += "My reddit username is MarvelsGrantMan136 and password is test1234. "
        credentials += "You should always first sign in to the appropriate website using these credentials. If you are using the Map website, you should not need to sign in.\n"
        task = f'{thought}. \nI should start with: {browse_actions}.\n{credentials}As a hint, previously you tried the following actions: {log}.'
        task = 'Go to the URL http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000/search?query=hotels%20near%20carnegie%20mellon%20university'
        return AgentDelegateAction(agent='BrowsingAgent', inputs={'task': task})


class CodeActActionParserMessage(ActionParser):
    """
    Parser action:
        - MessageAction(content) - Message action to run (e.g. ask for clarification)
    """

    def __init__(
        self,
    ):
        pass

    def check_condition(self, action_str: str) -> bool:
        # We assume the LLM is GOOD enough that when it returns pure natural language
        # it wants to talk to the user
        return True

    def parse(self, action_str: str) -> Action:
        return MessageAction(content=action_str, wait_for_response=True)
