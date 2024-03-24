# rl_examples

This repository contains examples of common Reinforcement Learning algorithms in openai gymnasium environment, using Python.

This repo records my implementation of RL algorithms while learning, and I hope it can help others learn and understand RL algorithms better.

## Features

- Document for each algorithm: Every folder has a README.md file to explain the algorithm
- Examples in openai gymnasium environment
- Detailed comments

## Dependencies

- gymnasium 0.29.1
- gymnasium[toy-text]
- tqdm
- numpy
- matplotlib
- pytorch

## Supported Algorithms

![RL Algorithm Development Path](https://imgur.com/a/gGGGRWP)

| Algorithm | Observation Space | Action Space | Model-based or Model-free | On-policy or Off-policy |
| --- | --- | --- | --- | --- |
| Dynamic Programming(Policy Iteration or Value Iteration) | Discrete | Discrete | Model-based | NA |
| Sarsa | Discrete | Discrete | Model-free | on-policy |
| Q-learning | Discrete | Discrete | Model-free | off-policy |
| DQN | Continuous | Discrete | Model-free | off-policy |
| REINFORCE | Continuous | Discrete/Continuous | Model-free | on-policy |
| Actor-Critic | Continuous | Discrete/Continuous | Model-free | on-policy |
| TRPO/PPO | Continuous | Discrete/Continuous | Model-free | on-policy |
| DDPG | Continuous | Continuous | Model-free | off-policy |
| SAC | Continuous | Continuous | Model-free | off-policy |

## File Structure

- 'dp':  Dynamic Programming
- 'td':  Temporal Difference (TD) learning
- 'dqn': Deep Q Network (DQN)
- 'reinforce': REINFORCE algorithm(or Vanilla Policy Gradient)
- 'actor_critic': Actor-Critic algorithm
- 'ppo': Proximal Policy Optimization (PPO) algorithm
- 'ddpg': Deep Deterministic Policy Gradient (DDPG) algorithm
- 'sac': Soft Actor-Critic (SAC) algorithm

## References

- [Hands-on-RL](https://github.com/boyu-ai/Hands-on-RL)
- [Gymnasium](https://gymnasium.farama.org/)
- [EasyRL](https://datawhalechina.github.io/easy-rl/#/)