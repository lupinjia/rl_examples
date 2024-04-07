# Based on the code of Hands-on-RL(https://github.com/boyu-ai/Hands-on-RL/blob/main/)

import gymnasium as gym
from tqdm import tqdm
import torch
import numpy as np
import matplotlib.pyplot as plt

from alg.actor_critic import ActorCritic

# agent hyperparameters
actor_lr = 1e-3
critic_lr = 1e-2
action_dim = 6 # Discretization of action space. Divide action space(-2,2) into 11 bins.
gamma = 0.99
hidden_dim = 128
# training hyperparameters
num_episodes = 1000
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# environment hyperparameters
env_name = "Pendulum-v1"
action_type = "discrete"

def dis_to_con(discrete_action, env, action_dim):
    """
    Convert discrete action to continuous action.
    """
    action_lowbound = env.action_space.low[0] # get the first element from the list
    action_upbound = env.action_space.high[0]
    action_con = action_lowbound + (action_upbound - action_lowbound) * discrete_action / (action_dim - 1)
    return np.array([action_con])

def train_on_policy_agent(env, agent, num_episodes):
    # to record episode returns
    return_list = []
    for i in range(10): # 10 pbars by default
        with tqdm(total=int(num_episodes/10), desc="Iteration %d"%(i)) as pbar:
            for i_episode in range(int(num_episodes/10)): # for each pbar, there are int(num_episodes/10) episodes
                # each episode
                episode_return = 0
                transition_dict = {
                    "states":[],
                    "actions":[],
                    "next_states":[],
                    "rewards":[],
                    "dones":[]
                }
                # reset environment
                state, _ = env.reset()
                terminated, truncated = False, False
                while not terminated and not truncated: # interaction loop
                    # select action
                    action_discrete = agent.take_action(state)
                    action = dis_to_con(action_discrete, env, action_dim)
                    # step the environment
                    next_state, reward, terminated, truncated, _ = env.step(action)
                    # store transition
                    transition_dict["states"].append(state)
                    transition_dict["actions"].append(action_discrete)
                    transition_dict["next_states"].append(next_state)
                    transition_dict["rewards"].append(reward)
                    transition_dict["dones"].append(terminated)
                    # update state
                    state = next_state
                    episode_return += reward
                # episode finished
                return_list.append(episode_return)
                # update agent
                agent.update(transition_dict)
                # show mean return of last 10 episodes, every 10 episodes
                if (i_episode+1) % 10 == 0:
                    pbar.set_postfix({
                        "episode":
                        "%d" % (int(num_episodes/10)*i+i_episode+1),
                        "return":
                        "%.3f" % (np.mean(return_list[-10:]))
                    })
                # update pbar
                pbar.update(1)
    # return return_list
    return return_list

def render_agent(env_name, agent):
    # reset environment
    env = gym.make(env_name, render_mode="human")
    state, _ = env.reset()
    terminated, truncated = False, False
    while not terminated and not truncated: # interaction loop
        # select action
        action_discrete = agent.take_action(state)
        action = dis_to_con(action_discrete, env, action_dim)
        # step the environment
        next_state, reward, terminated, truncated, _ = env.step(action)
        # render environment
        env.render()
        # update state
        state = next_state

def main():
    # create environment
    env = gym.make(env_name)
    # set seeds
    torch.manual_seed(1)
    # create agent
    state_dim = env.observation_space.shape[0]
    agent = ActorCritic(state_dim, hidden_dim, action_dim, actor_lr, critic_lr, gamma, device, action_type)
    # train agent
    return_list = train_on_policy_agent(env, agent, num_episodes)
    # plot return curve
    episodes_list = np.arange(len(return_list))
    plt.plot(episodes_list, return_list)
    plt.xlabel("Episodes")
    plt.ylabel("Return")
    plt.title("Actor-Critic on {}".format(env_name))
    plt.show()
    # render agent
    render_agent(env_name, agent)

if __name__ == "__main__":
    main()
