# coding=utf-8
import time
from support import log



@log("切换目标阴阳寮")
def choose_group(g, d):
    d.click(300, 180 * (g + 1))
    time.sleep(1)
    return g + 1


def find_under_level(l, d):
    if l > 7:
        l /= 10
    for i in range(l):
        img = 'level_' + str(i) + '.1334x750.png'
        if d.click_image(img, threshold=0.9, timeout=1.0) is not None:
            time.sleep(1)
            d.click_image('attack.1334x750.png', timeout=1.0)
            return True
    return False


@log("寻找低等级目标")
def find_under_level_scroll(l, d):
    while True:
        if find_under_level(l, d):
            return True
        else:
            if d.exists('broken.1334x750.png'):
                break
            d.swipe(600, 540, 600, 180, duration=0.1)
            time.sleep(1)
    return False