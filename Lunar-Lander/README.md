# Lunar Lander Autonomous Landing using Deep Q-Network (DQN)

> **Part of the MP Online AI/ML Internship Program**

---

## 🌟 Overview

The **Lunar Lander** project develops a **Deep Q-Network (DQN)** Reinforcement Learning agent to autonomously land a spacecraft safely on a designated landing pad in the `LunarLander-v2` Gymnasium environment.

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

To train an autonomous RL agent using Deep Q-Learning to control main and side thrusters, achieving soft landings between designated flags while minimizing fuel consumption and preventing crashes.

---

## 🛠️ Tech Stack & Algorithms

- **Framework:** PyTorch (`torch.nn`, `torch.optim`)
- **Environment:** Gymnasium / OpenAI Gym (`LunarLander-v2`)
- **Algorithm:** Deep Q-Network (DQN) with Replay Memory & Target Q-Network Update
- **Epsilon Policy:** Epsilon-Greedy Exploration with Decay
- **Visualization:** Matplotlib, OpenCV, Video Rendering

---

## 📊 Training Artifacts & Results

The trained agent achieves scores exceeding +200 points (indicating successful soft landing):

- `LunarLander_DQN.ipynb` — Full training and evaluation notebook
- `best_model.pth` — Saved PyTorch model weights
- `gameplay.mp4` — Video recording of autonomous landing gameplay
- `episode_reward.png` & `moving_average_reward.png` — Episodic reward trajectory plots
- `training_loss.png` & `epsilon_decay.png` — Loss curves and exploration decay rate
