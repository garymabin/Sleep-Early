# coding=utf-8
from task import *
from steps import *


class Break(Task):
    def __init__(self, time_, level, target, device):
        if not 0 < level < 8:
            raise IOError("Invalid level!!!")
        super(Break, self).__init__(device)
        self.name = 'Public breaking'
        self.start = time.time()
        self.time_ = time_ * 3600
        self.level = level
        self.target = target - 1
        self.broken = [0, 0, 0]
        self.last = 0

    def wait(self):
        begin = self.last + 195
        while time.time() < begin:
            self.d.click_image('busy.1334x750.png', timeout=1.0)
            get_bonus_task(self.d)
            sys.stdout.write('\r')
            sys.stdout.write('%s -> wait until %s' % (now(), now(begin)))
            sys.stdout.flush()
        sys.stdout.write('\n')

    def reopen_breaking(self):
        self.d.click_image('close.1334x750.png', timeout=1.0)
        self.d.click_image('break_icon.1334x750.png', timeout=1.0)
        self.d.click_image('public_tab.1334x750.png', timeout=1.0)
        time.sleep(2)

    @log("切换目标阴阳寮")
    def __choose_group(self):
        x, y = self.position.get('first_target')
        self.target = 1 if self.target == 3 else (self.target + 1)
        self.d.click(x, y * self.target)
        time.sleep(1)
        return self.target

    def __find_under_level(self):
        for i in range(self.level):
            img = 'level_' + str(i) + '.1334x750.png'
            if self.d.click_image(img, method='color', threshold=0.9, timeout=1.0):
                time.sleep(0.5 + get_delay())
                click_once(self.d, 'attack.1334x750.png')
                return True
        return False

    @log2("寻找低等级目标")
    def __find_under_level_scroll(self):
        while True:
            if self.__find_under_level():
                return True
            else:
                if self.d.exists('broken.1334x750.png'):
                    break
                x1, y1 = self.position.get('break_top')
                x2, y2 = self.position.get('break_bottom')
                self.d.swipe(x2, y2, x1, y1)
                time.sleep(0.5 + get_delay())
        return False

    def breaking(self):
        navigate_to_explore_map(self.d)
        for i in range(3):
            self.last = int(time.time())
            self.reopen_breaking()
            self.__choose_group()
            if self.__find_under_level_scroll():
                time.sleep(4.5 + get_delay())
                if not self.d.exists('level_6.1334x750.png', method='color'):
                    fighting(self)
                    self.times += 1
                else:
                    self.d.click_image('breaking.1334x750.png', timeout=1.0)
            else:
                self.broken[self.target - 1] = 1
                print '第%d个阴阳寮刷完了' % self.target
            self.analysis()
            self.wait()
        while 0 in self.broken and time.time() - self.start < self.time_:
            self.last = int(time.time())
            self.reopen_breaking()
            self.__choose_group()
            if self.__find_under_level_scroll():
                self.last = (self.last + int(time.time()) - 15) / 2
                time.sleep(4.5 + get_delay())
                if not self.d.exists('level_6.1334x750.png', method='color'):
                    fighting(self)
                    self.times += 1
                else:
                    self.d.click_image('breaking.1334x750.png', timeout=1.0)
            else:
                self.broken[self.target - 1] = 1
                print '第%d个阴阳寮刷完了' % self.target
            self.analysis()
            self.wait()

    def analysis(self):
        super(Break, self).analysis()
        print '┃%31s%-19s┃' % ('target level: under ', self.level * 10)
        print '┃%25s%-25s┃' % ('broken: ', self.broken)
        print '┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛'
