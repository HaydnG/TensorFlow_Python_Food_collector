from collections import deque

import game
import agent
import numpy as np
import random
import helper

episodes = 10000

def main():
    epsilon = 1  # Epsilon-greedy algorithm in initialized at 1 meaning every step is random at the start
    max_epsilon = 1  # You can't explore more than 100% of the time
    min_epsilon = 0.01  # At a minimum, we'll always explore 1% of the time
    decay = 0.01

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    game_count = 0

    env = game.Game()
    game_agent = agent.Agent(env)

    target_game_agent = agent.Agent(env)

    replay_memory = deque(maxlen=50_000)

    steps_to_update_target_model = 0

    for episode in range(episodes):
        game_count +=1
        total_training_rewards = 0

        env.reset()

        observation = env.get_state()

        done = False
        while not done:
            steps_to_update_target_model += 1

            random_number = np.random.rand()
            # 2. Explore using the Epsilon Greedy Exploration Strategy
            action = 0
            if random_number <= epsilon:
                action = random.randint(0, 1)
            else:
                # Exploit best known action
                # model dims are (batch, env.observation_space.n)
                encoded = game_agent.encode_observation(observation, env.observations)
                encoded_reshaped = encoded.reshape([1, encoded.shape[0]])
                predicted = game_agent.model.predict(encoded_reshaped).flatten()

                action = np.argmax(predicted).item()


            new_observation, reward, done, food_count, miss_count = env.step(action)
            replay_memory.append([observation, action, reward, new_observation, done])

            # 3. Update the Main Network using the Bellman Equation
            if steps_to_update_target_model % 2 == 0 or done:
                game_agent.train(replay_memory, target_game_agent.model, done)

            observation = new_observation
            total_training_rewards += reward

            if done:

                plot_scores.append(total_training_rewards)
                total_score += total_training_rewards
                mean_score = total_score / game_count


                plot_mean_scores.append(mean_score)
                if game_count % 5 == 0:
                    helper.plot(plot_scores, plot_mean_scores)

                print('Total training rewards: {} after n steps = {} with final reward = {} - Food Count: {} - Miss Count: {} - Epsilon: {}'.format(
                    total_training_rewards, episode, reward, food_count, miss_count, epsilon))
                total_training_rewards += 1

                if steps_to_update_target_model >= 15:
                    print('Copying main network weights to the target network weights')
                    target_game_agent.model.set_weights(game_agent.model.get_weights())
                    steps_to_update_target_model = 0
                break

        epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-decay * episode)

main()

# env = game.Game()
#
#
# while env.running:
#     env.step([])
