#!/bin/bash
AGENT="CodeActAgent"

# IMPORTANT: Because Agent's prompt changes fairly often in the rapidly evolving codebase of OpenDevin
# We need to track the version of Agent in the evaluation to make sure results are comparable
AGENT_VERSION=v$(poetry run python -c "import agenthub; from opendevin.controller.agent import Agent; print(Agent.get_cls('$AGENT').VERSION)")
export log_file='log.log'

COMMAND="poetry run python evaluation/webarena/run_infer.py \
  --agent-cls CodeActAgent \
  --llm-config llm \
  -m openai/gpt-4o
  -e SSH_PASSWORD='"hello"'
  --start_task_id 0 \
  --eval-n-limit 1 \
  --max-iterations 18 \
  --data-split validation \
  --max-chars 10000000 \
  --eval-num-workers 1 \
  --eval-note ${AGENT_VERSION}_${LEVELS}"

# Run the command
eval $COMMAND
