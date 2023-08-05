import tensorflow_hub as hub
import tensorflow as tf


class FaceGeneration():
    """
    Image generator based on tensorflow reimplementation of Progressive GANs[1].
    Maps from a 512-dimensional latent space to images. During training, the latent space vectors were sampled from a normal distribution.
    Module takes <Tensor(tf.float32, shape=[?, 512])>, representing a batch of latent vectors as input, and outputs <Tensor(tf.float32, shape=[?, 128, 128, 3])> representing a batch of RGB images.
    URL: https://tfhub.dev/google/progan-128/1
    """
    def __init__(self):
        self.module = hub.load("https://tfhub.dev/google/progan-128/1").signatures['default']

    def infer(self, num_samples=1, size=512):
        noise = tf.random.normal([num_samples, size])
        return self.module(noise)['default']
