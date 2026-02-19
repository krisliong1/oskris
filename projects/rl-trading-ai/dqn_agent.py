"""
DQN Agent - 深度Q网络强化学习交易Agent
完全本地运行，不需要任何API或云端服务
"""

import numpy as np
import random
import json
import os
from collections import deque


class ReplayBuffer:
    """经验回放缓冲区"""
    
    def __init__(self, capacity=50000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            np.array(states),
            np.array(actions),
            np.array(rewards, dtype=np.float32),
            np.array(next_states),
            np.array(dones, dtype=np.float32)
        )
    
    def __len__(self):
        return len(self.buffer)


class NeuralNetwork:
    """
    纯NumPy实现的神经网络（不需要PyTorch/TensorFlow）
    完全本地，零依赖
    """
    
    def __init__(self, input_dim, hidden_dims, output_dim, lr=0.001):
        self.lr = lr
        self.layers = []
        
        # 构建网络层
        dims = [input_dim] + hidden_dims + [output_dim]
        for i in range(len(dims) - 1):
            # He初始化
            w = np.random.randn(dims[i], dims[i+1]) * np.sqrt(2.0 / dims[i])
            b = np.zeros(dims[i+1])
            self.layers.append({'w': w, 'b': b})
        
        # Adam优化器参数
        self.m = [{'w': np.zeros_like(l['w']), 'b': np.zeros_like(l['b'])} for l in self.layers]
        self.v = [{'w': np.zeros_like(l['w']), 'b': np.zeros_like(l['b'])} for l in self.layers]
        self.t = 0
    
    def forward(self, x):
        """前向传播"""
        self.activations = [x]
        
        for i, layer in enumerate(self.layers):
            z = x @ layer['w'] + layer['b']
            if i < len(self.layers) - 1:  # 隐藏层用ReLU
                x = np.maximum(0, z)
            else:  # 输出层线性
                x = z
            self.activations.append(x)
        
        return x
    
    def backward(self, target, output):
        """反向传播 + Adam优化"""
        self.t += 1
        batch_size = target.shape[0]
        
        # 输出层梯度
        delta = (output - target) / batch_size
        
        for i in range(len(self.layers) - 1, -1, -1):
            a = self.activations[i]
            
            # 计算梯度
            dw = a.T @ delta
            db = np.sum(delta, axis=0)
            
            # 传播到前一层
            if i > 0:
                delta = delta @ self.layers[i]['w'].T
                # ReLU导数
                delta = delta * (self.activations[i] > 0).astype(float)
            
            # Adam更新
            beta1, beta2, eps = 0.9, 0.999, 1e-8
            
            self.m[i]['w'] = beta1 * self.m[i]['w'] + (1 - beta1) * dw
            self.m[i]['b'] = beta1 * self.m[i]['b'] + (1 - beta1) * db
            self.v[i]['w'] = beta2 * self.v[i]['w'] + (1 - beta2) * dw**2
            self.v[i]['b'] = beta2 * self.v[i]['b'] + (1 - beta2) * db**2
            
            m_hat_w = self.m[i]['w'] / (1 - beta1**self.t)
            m_hat_b = self.m[i]['b'] / (1 - beta1**self.t)
            v_hat_w = self.v[i]['w'] / (1 - beta2**self.t)
            v_hat_b = self.v[i]['b'] / (1 - beta2**self.t)
            
            self.layers[i]['w'] -= self.lr * m_hat_w / (np.sqrt(v_hat_w) + eps)
            self.layers[i]['b'] -= self.lr * m_hat_b / (np.sqrt(v_hat_b) + eps)
    
    def copy_from(self, other):
        """从另一个网络复制权重"""
        for i in range(len(self.layers)):
            self.layers[i]['w'] = other.layers[i]['w'].copy()
            self.layers[i]['b'] = other.layers[i]['b'].copy()
    
    def save(self, path):
        """保存模型"""
        data = {
            'layers': [{'w': l['w'].tolist(), 'b': l['b'].tolist()} for l in self.layers],
            'lr': self.lr
        }
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def load(self, path):
        """加载模型"""
        with open(path, 'r') as f:
            data = json.load(f)
        for i, l in enumerate(data['layers']):
            self.layers[i]['w'] = np.array(l['w'])
            self.layers[i]['b'] = np.array(l['b'])


class DQNAgent:
    """
    DQN强化学习交易Agent
    
    核心思想: AI通过与市场环境交互，自己学会什么时候买、什么时候卖
    不需要人告诉它规则，它自己从数据中学习最优策略
    """
    
    def __init__(self, state_dim, action_dim, config=None):
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # 默认配置
        default_config = {
            'hidden_dims': [256, 128, 64],
            'lr': 0.0005,
            'gamma': 0.99,           # 折扣因子（重视长期收益）
            'epsilon_start': 1.0,     # 初始探索率
            'epsilon_end': 0.01,      # 最终探索率
            'epsilon_decay': 0.995,   # 探索率衰减
            'batch_size': 64,
            'buffer_size': 50000,
            'target_update': 10,      # 目标网络更新频率
            'min_buffer': 1000,       # 最小经验数才开始学习
        }
        
        self.config = {**default_config, **(config or {})}
        
        # Q网络和目标网络
        self.q_network = NeuralNetwork(
            state_dim, 
            self.config['hidden_dims'], 
            action_dim,
            self.config['lr']
        )
        self.target_network = NeuralNetwork(
            state_dim,
            self.config['hidden_dims'],
            action_dim,
            self.config['lr']
        )
        self.target_network.copy_from(self.q_network)
        
        # 经验回放
        self.memory = ReplayBuffer(self.config['buffer_size'])
        
        # 探索参数
        self.epsilon = self.config['epsilon_start']
        
        # 训练统计
        self.train_step = 0
        self.losses = []
    
    def select_action(self, state, training=True):
        """
        选择动作（epsilon-greedy策略）
        训练时有概率随机探索，测试时完全用学到的策略
        """
        if training and random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        
        q_values = self.q_network.forward(state.reshape(1, -1))
        return np.argmax(q_values[0])
    
    def store_transition(self, state, action, reward, next_state, done):
        """存储经验"""
        self.memory.push(state, action, reward, next_state, done)
    
    def learn(self):
        """从经验中学习"""
        if len(self.memory) < self.config['min_buffer']:
            return 0
        
        # 采样
        states, actions, rewards, next_states, dones = \
            self.memory.sample(self.config['batch_size'])
        
        # 计算当前Q值
        current_q = self.q_network.forward(states)
        
        # 计算目标Q值 (Double DQN)
        next_q = self.q_network.forward(next_states)
        next_actions = np.argmax(next_q, axis=1)
        
        target_next_q = self.target_network.forward(next_states)
        
        # TD目标
        target = current_q.copy()
        for i in range(len(states)):
            if dones[i]:
                target[i, actions[i]] = rewards[i]
            else:
                target[i, actions[i]] = rewards[i] + \
                    self.config['gamma'] * target_next_q[i, next_actions[i]]
        
        # 反向传播
        output = self.q_network.forward(states)
        self.q_network.backward(target, output)
        
        # 计算loss
        loss = np.mean((target - output) ** 2)
        self.losses.append(loss)
        
        self.train_step += 1
        
        # 更新目标网络
        if self.train_step % self.config['target_update'] == 0:
            self.target_network.copy_from(self.q_network)
        
        # 衰减探索率
        self.epsilon = max(
            self.config['epsilon_end'],
            self.epsilon * self.config['epsilon_decay']
        )
        
        return loss
    
    def save(self, path):
        """保存Agent"""
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
        self.q_network.save(path)
        # 保存元数据
        meta = {
            'epsilon': self.epsilon,
            'train_step': self.train_step,
            'config': self.config
        }
        meta_path = path.replace('.json', '_meta.json')
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
        print(f"[✓] 模型已保存: {path}")
    
    def load(self, path):
        """加载Agent"""
        self.q_network.load(path)
        self.target_network.copy_from(self.q_network)
        meta_path = path.replace('.json', '_meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                meta = json.load(f)
            self.epsilon = meta.get('epsilon', 0.01)
            self.train_step = meta.get('train_step', 0)
        print(f"[✓] 模型已加载: {path}")
