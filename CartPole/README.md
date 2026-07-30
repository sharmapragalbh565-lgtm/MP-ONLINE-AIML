# CartPole Control using Deep Q-Network (DQN)

> **Part of the MP Online AI/ML Internship Program**

---

## 🌟 Overview

The **CartPole Control** project implements a **Deep Q-Network (DQN)** Reinforcement Learning agent to solve the classic `CartPole-v1` control environment from Gymnasium/OpenAI Gym. The goal is to balance a pole vertically on a cart by moving the cart left or right.

---

## 👤 Intern Details

| Field | Details |
|---|---|
| **Name** | Pragalbh Sharma |
| **Registration Number** | 23BCE11286 |
| **MP Online Application Number** | IN26010739 |
| **Batch Number** | 2(B) |
| **Faculty** | Nishant Srivastava Sir |

---

## 🎯 Project Objective

To train a deep reinforcement learning agent using Deep Q-Learning with experience replay and target networks to maintain cart-pole equilibrium for 500 consecutive timesteps.

---

## 🛠️ Tech Stack & Algorithms

- **Framework:** PyTorch (`torch.nn`, `torch.optim`)
- **Environment:** Gymnasium / OpenAI Gym (`CartPole-v1`)
- **Algorithm:** Deep Q-Network (DQN) with Experience Replay & Target Network
- **Epsilon Policy:** Exponential Epsilon-Greedy Decay Strategy
- **Visualization:** Matplotlib, OpenCV, MoviePy

---

## 📊 Training Artifacts & Results

The trained agent achieves maximum rewards (500 timesteps) across evaluation episodes:

- `DQN_CartPole_v1_colab.ipynb` — Full training and evaluation notebook
- `dqn_cartpole_best.pth` — Saved PyTorch model checkpoint
- `dqn_cartpole_gameplay.mp4` — Rendered video demonstration of trained agent
- `episode_reward.png` & `moving_average_reward.png` — Reward progression plots
- `training_loss.png` & `epsilon_decay.png` — Loss convergence and exploration decay charts
