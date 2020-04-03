# Deep-Q-Learning-Agent
This project demonstrates the generalizability of “Deep Q-Learning” in learning control policies from visual outputs of different environments. The model aims to map the end-to-end relation between the visual outputs (rendered 2-d visuals of a game) to the next action (control signals like move up, move right) so as to gain maximum cumulative reward (score). The learning phase of the model involves simultaneously training the model while making predictions at each step (frame to action).

## Performance
### Env: rover_lander_1
| Model | Performance                                                                                                                                                                                                                                                                             | Episode 20                                                                                                                                            | Episode 200                                                                                                                                            | Train Score / episode                                                                                                                                            |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| FCNN  | [Open TensorBoard](https://tensorboard.dev/experiment/HY1DEpDnRoOhkmVAkebOnQ/#scalars&_smoothingWeight=0.96&runSelectionState=eyJjb2xhYi13b3JrZXItMS9zY2FsYXJzLzIwMjAwMzI5LTEzMDcyMi9tZXRyaWNzIjp0cnVlLCJjb2xhYi13b3JrZXItY25uLTEvc2NhbGFycy8yMDIwMDMyOS0xMzA3MjMvbWV0cmljcyI6ZmFsc2V9) | <img src="https://github.com/ArjunInventor/Deep-Q-Learning-Agent/blob/master/gameplay/colab-worker-1_v0_1.gif?raw=true" width="150" height="150">     | <img src="https://github.com/ArjunInventor/Deep-Q-Learning-Agent/blob/master/gameplay/colab-worker-1_v10_1.gif?raw=true" width="150" height="150">     | <img src="https://raw.githubusercontent.com/ArjunInventor/Deep-Q-Learning-Agent/master/metrics/fcnn-env1-score.svg?sanitize=true" height="150">     |
| CNN   | [Open TensorBoard](https://tensorboard.dev/experiment/HY1DEpDnRoOhkmVAkebOnQ/#scalars&_smoothingWeight=0.96&runSelectionState=eyJjb2xhYi13b3JrZXItMS9zY2FsYXJzLzIwMjAwMzI5LTEzMDcyMi9tZXRyaWNzIjpmYWxzZSwiY29sYWItd29ya2VyLWNubi0xL3NjYWxhcnMvMjAyMDAzMjktMTMwNzIzL21ldHJpY3MiOnRydWV9) | <img src="https://github.com/ArjunInventor/Deep-Q-Learning-Agent/blob/master/gameplay/colab-worker-cnn-1_v0_1.gif?raw=true" width="150" height="150"> | <img src="https://github.com/ArjunInventor/Deep-Q-Learning-Agent/blob/master/gameplay/colab-worker-cnn-1_v10_1.gif?raw=true" width="150" height="150"> | <img src="https://raw.githubusercontent.com/ArjunInventor/Deep-Q-Learning-Agent/master/metrics/cnn-env1-score.svg?sanitize=true" height="150">     |

### Env: rover_lander_2
| Model | Performance                                                                                                                                                                                                                                                                             | Episode 20                                                                                                                                            | Episode 200                                                                                                                                            | Train Score / episode                                                                                                                                            |
|-------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| FCNN  | [Open TensorBoard](https://tensorboard.dev/experiment/ZSppV9Z4QvWWkD6xgnXUzA/#scalars&runSelectionState=eyJjb2xhYi13b3JrZXItMi9zY2FsYXJzLzIwMjAwNDAzLTEyMzg1NS9tZXRyaWNzIjp0cnVlLCJjb2xhYi13b3JrZXItY25uLTIvc2NhbGFycy8yMDIwMDQwMy0xMjM4NTgvbWV0cmljcyI6ZmFsc2V9&_smoothingWeight=0.96) | <img src="https://github.com/ArjunInventor/Deep-Q-Learning-Agent/blob/master/gameplay/colab-worker-2_v0_1.gif?raw=true" width="150" height="150">     | <img src="https://github.com/ArjunInventor/Deep-Q-Learning-Agent/blob/master/gameplay/colab-worker-2_v10_1.gif?raw=true" width="150" height="150">     | <img src="https://raw.githubusercontent.com/ArjunInventor/Deep-Q-Learning-Agent/master/metrics/fcnn-env2-score.svg?sanitize=true" height="150">     |
| CNN   | [Open TensorBoard](https://tensorboard.dev/experiment/ZSppV9Z4QvWWkD6xgnXUzA/#scalars&runSelectionState=eyJjb2xhYi13b3JrZXItMi9zY2FsYXJzLzIwMjAwNDAzLTEyMzg1NS9tZXRyaWNzIjpmYWxzZSwiY29sYWItd29ya2VyLWNubi0yL3NjYWxhcnMvMjAyMDA0MDMtMTIzODU4L21ldHJpY3MiOnRydWV9&_smoothingWeight=0.96) | <img src="https://github.com/ArjunInventor/Deep-Q-Learning-Agent/blob/master/gameplay/colab-worker-cnn-2_v0_1.gif?raw=true" width="150" height="150"> | <img src="https://github.com/ArjunInventor/Deep-Q-Learning-Agent/blob/master/gameplay/colab-worker-cnn-2_v10_1.gif?raw=true" width="150" height="150"> | <img src="https://raw.githubusercontent.com/ArjunInventor/Deep-Q-Learning-Agent/master/metrics/cnn-env2-score.svg?sanitize=true" height="150">     |

## Training model
### Local
First, on your local machine run:
```
python train_master.py
```

> Note: Use a port-forwarding tool like [ngrok](https://ngrok.com/) to expose the endpoint created

To moniter logs streamed from remote workers on your local machine, run:
```
tensorboard --logdir logs
```

### Remote

Now, on each remote workstation run:
```
python train_worker.py \
                        --env <ENV_NAME> \
                        --master-endpoint <MASTER_ENDPOINT> \
                        --worker-name <WORKER_NAME>
```

To train using the CNN based model run:
```
python train_worker_cnn.py \
                        --env <ENV_NAME> \
                        --master-endpoint <MASTER_ENDPOINT> \
                        --worker-name <WORKER_NAME>
```

Or, run remote worker from Google Colab - https://colab.research.google.com/github/ArjunInventor/Deep-Q-Learning-Agent/blob/master/train_worker.ipynb


## Testing agent
```
python play.py --model <MODEL_PATH> --env <ENV_NAME>
```
When using a CNN based model, run: 
```
python play_cnn.py --model <MODEL_PATH> --env <ENV_NAME>
```
> Use ```--save-gif``` to save the gameplay as a gif 
