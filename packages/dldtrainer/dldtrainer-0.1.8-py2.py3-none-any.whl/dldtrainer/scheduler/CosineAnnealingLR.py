# -*-coding: utf-8 -*-
"""
    @Author : panjq
    @E-mail : pan_jinquan@163.com
    @Date   : 2021-08-12 20:27:27
"""

import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
from ..callbacks.callbacks import Callback
from torch.optim import lr_scheduler


class CosineAnnealingLR(Callback):
    def __init__(self,
                 optimizer,
                 epochs,
                 num_steps,
                 lr_init=0.01,
                 ):
        """
        optimizer (Optimizer): Wrapped optimizer.
        t_max (int): Maximum number of iterations.
        eta_min (float): Minimum learning rate. Default: 0.
        last_epoch (int): The index of last epoch. Default: -1.
        verbose (bool): If ``True``, prints a message to stdout for each update. Default: ``False``.
        """
        self.num_steps = num_steps
        t_max = self.num_steps * epochs
        self.scheduler = lr_scheduler.CosineAnnealingLR(optimizer, t_max, eta_min=0, last_epoch=-1, verbose=False)

    def on_epoch_begin(self, epoch, logs: dict = {}):
        self.epoch = epoch

    def on_batch_end(self, batch, logs: dict = {}):
        self.step(epoch=self.epoch, step=batch)

    def step(self, epoch=0, step=0):
        total_step = self.num_steps * epoch + step
        self.scheduler.step(epoch)
