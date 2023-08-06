# -*-coding: utf-8 -*-
"""
    @Author : panjq
    @E-mail : pan_jinquan@163.com
    @Date   : 2021-08-12 20:31:19
"""
from .MultiStepLR import MultiStepLR
from .CosineAnnealingLR import CosineAnnealingLR


def get_scheduler(scheduler, optimizer, lr_init, num_epochs, num_steps, **kwargs):
    if scheduler == "multi-step" or scheduler == "multi_step":
        lr_scheduler = MultiStepLR(optimizer,
                                   lr_init=lr_init,
                                   epochs=num_epochs,
                                   num_steps=num_steps,
                                   milestones=kwargs["milestones"],
                                   nums_warn_up=kwargs["nums_warn_up"])
    elif scheduler == "cosine":
        lr_scheduler = CosineAnnealingLR(optimizer,
                                         num_epochs,
                                         num_steps=num_steps,
                                         lr_init=lr_init)
    else:
        raise Exception("Error:{}".format(scheduler))
    return lr_scheduler
