import numpy as np

class QLearning:
    def __init__(self, env, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.env = env
        try:
            self.num_obs = self.env.observation_space.n
        except: # for blackjack env
            obs_space = self.env.observation_space 
            self.num_obs = 1
            for obs in obs_space:
                self.num_obs *= obs.n
        self.num_action = self.env.action_space.n
        self.Q_table = np.zeros([self.num_obs, self.num_action]) # init Q(s,a) table
        self.epsilon = epsilon # epsilon in epsilon-greedy policy
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor
    
    def take_action(self, obs):  # 选取下一步的操作,具体实现为epsilon-贪婪
        if np.random.random() < self.epsilon:
            action = np.random.randint(self.num_action) # encourage exploration
        else:
            action = np.argmax(self.Q_table[obs])
        return action
    
    def update(self, s0, a0, r, s1): # update Q table, using the Q value generated by greedy policy(off-policy).
        td_error = r + self.gamma * self.Q_table[s1].max(
        ) - self.Q_table[s0, a0]
        self.Q_table[s0, a0] += self.alpha * td_error