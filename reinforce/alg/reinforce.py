import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

class PolicyNetDiscrete(nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(PolicyNetDiscrete, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc2 = torch.nn.Linear(hidden_dim, action_dim)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return F.softmax(self.fc2(x), dim=1)

class PolicyNetContinuous(nn.Module):
    def __init__(self, state_dim, hidden_dim, action_dim):
        super(PolicyNetContinuous, self).__init__()
        self.fc1 = torch.nn.Linear(state_dim, hidden_dim)
        self.fc_mu = torch.nn.Linear(hidden_dim, action_dim)   # mean value of gaussian distribution
        self.fc_std = torch.nn.Linear(hidden_dim, action_dim)  # standard deviation of gaussian distribution
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        mu = self.fc_mu(x)
        std = F.softplus(self.fc_std(x))  # ensure std is positive
        return mu, std
    
class REINFORCE:
    def __init__(self, state_dim, hidden_dim, action_dim, learning_rate, gamma,
                 device, action_type='discrete'):
        self.action_type = action_type
        if action_type == 'discrete':
            self.policy_net = PolicyNetDiscrete(state_dim, hidden_dim, action_dim).to(device)
        elif action_type == 'continuous':
            self.policy_net = PolicyNetContinuous(state_dim, hidden_dim, action_dim).to(device)
        self.optimizer = torch.optim.Adam(self.policy_net.parameters(),
                                          lr=learning_rate)
        self.action_dim = action_dim
        self.state_dim = state_dim
        self.gamma = gamma
        self.device = device

    def take_action(self, state):  # randomly sample an action according to the probability distribution
        state = torch.tensor(state, dtype=torch.float).view(1, -1).to(self.device) # 将state再包一层list后转为tensor
                                                                         # 这样就可以得到1*state_dim的tensor
                                                                         # 但这个方法会引起警告UserWarning: Creating a tensor from a list 
                                                                         # of numpy.ndarrays is extremely slow. Please consider converting the
                                                                         # list to a single numpy.ndarray with numpy.array() before converting to a tensor.
        if self.action_type == 'discrete':
            probs = self.policy_net(state)
            action_dist = torch.distributions.Categorical(probs) # Categorical Distribution(https://en.wikipedia.org/wiki/Categorical_distribution)
                                                                # Categorical是多项分布的特例, 相当于只进行1次试验的多项分布
            action = action_dist.sample() # Categorical采样时会根据概率分布在[0,n-1]之间采样一个动作
            return action.item()  # discrete action, return scalar
        else:
            mu, std = self.policy_net(state)
            action_dist = torch.distributions.Normal(mu, std)  # Gaussian Distribution
            action = action_dist.sample()
            return [action.item()]  # continuous action, return vector

    def update(self, transition_dict):
        reward_list = transition_dict['rewards']
        state_list = transition_dict['states']
        action_list = transition_dict['actions']

        G = 0
        self.optimizer.zero_grad()
        for i in reversed(range(len(reward_list))):  # Back to Front, calc G
            reward = reward_list[i]
            state = torch.tensor(state_list[i],
                                 dtype=torch.float).view(1, -1).to(self.device)
            action = torch.tensor(action_list[i]).view(-1, 1).to(self.device)
            if self.action_type == 'discrete':
                log_prob = torch.log(self.policy_net(state).gather(1, action))  # calc log probability of action
            else:
                mu, std = self.policy_net(state)
                action_dist = torch.distributions.Normal(mu, std)
                log_prob = action_dist.log_prob(action)
            G = self.gamma * G + reward  # calculate return starting from this step
            loss = -log_prob * G         # loss of each step
            loss.backward()              # The gradient will be accumulated in each step
        self.optimizer.step()