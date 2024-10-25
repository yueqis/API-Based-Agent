# Beyond Browsing: API-Based Web Agents

[Homepage](https://yueqis.github.io/API-Based-Agent/) | [Github](https://github.com/yueqis/API-Based-Agent)
| [Arxiv](https://arxiv.org/abs/2410.16464) | [PDF](https://arxiv.org/pdf/2410.16464)

## Brief Summary
This project explores a novel approach to web agents by enabling them to use APIs in addition to traditional web-browsing techniques. By leveraging API calls, agents can perform tasks more efficiently and accurately, especially on websites with comprehensive API support.
 - API-Based Agent: The API-based agent leverages application programming interfaces (APIs) to interact directly with web services, bypassing traditional web-browsing actions like simulated clicks.
 - Hybrid Agent: a agent that combines the power of API-Based Agent and traditional Web-Based Agent, capable of interleaving API calls and Web Browsing.
 - Real-World Web Task Evaluation and Analysis: On WebArena, a real-world web task benchmark, our hybrid agent achieve sota performance among task-agnostic models.

## Setting Up

We employed [OpenHands](https://github.com/All-Hands-AI/OpenHands) as our primary evaluation framework for developing and testing our agents, as it is an open-source platform designed for creating AI agents that interact with both software and web environments. Thus, the setting up procedures follow that of OpenHands.

To setup, follow the instructions in [SETUP.md](https://github.com/yueqis/API-Based-Agent/blob/main/SETUP.md).

## Experiments

To run experiments, do:

```bash
bash evaluation/webarena/scripts/run_infer.sh
```

In `evaluation/webarena/scripts/run_infer.sh`, you could change `start_task_id` and `eval-n-limit`, where `start_task_id` is the `task_id` you would like to start with in WebArena. This also represent the specific website from WebArena you are evaluating. For example, the task with `task_id=0` is a shopping admin task, so if you specify `start_task_id=0`, then it will run shopping admin tasks; the task with `task_id=10` is a shopping admin task, so if you specify `start_task_id=10`, then it will run map tasks.
`eval-n-limit` is the number of instances to evaluate on starting from `start_task_id`.


## Citation
```
@article{song2024browsingapibasedwebagents,
  title={Beyond Browsing: API-Based Web Agents},
  author={Yueqi Song and Frank Xu and Shuyan Zhou and Graham Neubig},
  journal={arXiv preprint arXiv:2410.16464},
  year={2024},
  url={https://arxiv.org/abs/2410.16464}
}
```
