# coding=utf-8
import time
from support import *


@log("继续")
def continue_(task, times=4):
    for t in range(times):
        task.d.click(*task.position.get('screen_bottom'))
        time.sleep(1.5)
    return True


@log("是否在战斗中")
@sure
def is_fighting(d):
    if d.exists('fighting.1334x750.png'):
        return True
    if d.exists('ready.1334x750.png'):
        return True
    return False


@log("是否在选择式神")
@sure
def is_switching(d):
    if d.exists('switching.1334x750.png'):
        return True
    return False


@log("等待准备")
def is_not_ready(d):
    if d.exists('not_ready.1334x750.png'):
        return True
    return False


@log("战斗准备完毕")
def get_ready(d):
    while is_switching(d):
        pass
    if is_not_ready(d):
        d.click_image('ready_icon.1334x750.png', offset=(0, -1.5))
    return True


def fighting(task, times=4):
    while not is_fighting(task.d):
        get_ready(task.d)
    while is_fighting(task.d):
        pass
    continue_(task, times)
    return True