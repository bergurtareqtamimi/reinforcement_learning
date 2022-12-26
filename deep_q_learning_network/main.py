# imports
import random, gym, os, numpy as np
from collections import deque
# tensor flow stuff
from keras.models import Sequential # basic neural network
from keras.layers import Dense
from keras.optimizers import Adam


# parameters
env = gym.make('CartPole-v0')
state_size = env.observation_space.shape[0] # = 4 since we have pole degree, speed of pole rotation, cart position and cart speed
action_size = env.action_space.n # = 2 since you can only move right or left

batch_size = 32
n_episodes = 1001 # number of episodes to train on

outpur_dir = 'cartpole'

if not os.path.exists(outpur_dir): os.makedirs(outpur_dir)


# define agent

class DQNAgent:
    def __init__(self, state_size, action_size) -> None:
        self.state_size = state_size
        self.action_size = action_size

        self.memory = deque(maxlen=2000) # is more than 2000 are added then the oldest pops out

        self.gamma = 0.95 # discount future awards
        self.epsilon = 1.0 # exploration rate
        self.epsilon_decay = 0.995 # to lower epsilone over time
        self.epsilon_min = 0.01
        self.learning_rate = 0.001

        self.model = self.build_model()

    def build_model(self):
        model = Sequential()

        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))

        return model
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    def pick_action(self, state):
        if np.random.rand() <= self.epsilon: return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0]) # return the index that contains the highest value


    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min: self.epsilon *= self.epsilon_decay
    
    def load(self, name):
        self.model.load_weights(name)
    
    def save(self, name):
        self.model.save_weights(name)


agent = DQNAgent(state_size, action_size)


# interaction with environment
done = False
for e in range(n_episodes):

    state = env.reset()[0]
    state = np.reshape(state, [1, state_size])

    for time in range(5000):
        env.render()

        action = agent.pick_action(state)

        next_state, reward, done, _, _ = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])

        reward = reward if not done else -10

        agent.remember(state, action, reward, next_state, done)

        state = next_state
        
        if done: 
            print(f"epidsodes: {e} score: {time} epsilone: {agent.epsilon}")
            break
    
    if len(agent.memory) > batch_size: agent.replay(batch_size)

    if e % 50 == 0: agent.save(outpur_dir + f"weights _{e}.hdf5")
