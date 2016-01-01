from scene import *
from utilities import *

class SlideMenu (Layer):
    def __init__(self, rect, words, col1, col2, fnt):
        super(SlideMenu, self).__init__(rect)
        self.background = col2
        self.col1 = col1
        self.col2 = col2
        self.fnt = fnt
        dim = rect.h - 2
        self.slider = Slider(Rect(0, 1, dim * len(words), dim), self.frame.x, self.frame.x + self.frame.w, 200)
        self.add_layer(self.slider)
        self.slider.background = Color(.5,.5,.5)

        self.buttons = []
        i = 0
        for word in words:
            self.buttons.append(SelectButton(Rect(i * dim, 0, dim, dim), 20, word, i))
            self.buttons[i].col1 = col2
            self.buttons[i].col2 = col1
            self.slider.add_layer(self.buttons[i])
            self.buttons[i].background = col1
            i += 1

    def update_m(self):
        self.slider.update_s()
        for button in self.buttons:
            if button.selected:
                button.inner.background = self.col1
            else:
                button.inner.background = self.col1
        self.put_text()


    def put_text(self):
        i = 0
        for button in self.buttons:
            if button.selected:
                change_color(self.col2)
                no_fill()
                off = 2
                x = button.frame.x + self.slider.frame.x + self.frame.x + off
                y = button.frame.y + self.slider.frame.y + self.frame.y + off
                w = button.frame.w - 2.0 * off
                h = button.frame.h - 2.0 * off
                rect(x, y, w, h)
            x = self.slider.frame.x
            y = self.frame.y + self.frame.h / 2.0
            w = button.frame.w
            text_lines(button.txt, self.fnt, 10, x + (i + 0.5) * w, y, 37)
            i += 1

    def touch_began(self, touch):
        touch.location.y -= self.frame.y
        self.slider.touch_began(touch)
        touch.location.x -= self.slider.frame.x
        for button in self.buttons:
            button.touch_began(touch)

    def touch_moved(self, touch):
        self.slider.touch_moved(touch)
        for button in self.buttons:
            button.touch_moved(touch)

    def touch_ended(self, touch):
        touch.location.y -= self.frame.y
        self.slider.touch_ended(touch)
        touch.location.x -= self.slider.frame.x
        for button in self.buttons:
            all = button.touch_ended(touch)
            if all:
                for bt in self.buttons:
                    bt.selected = self.buttons[0].selected

class SelectButton (Layer):
    def __init__(self, rect, border, txt, idx):
        super(SelectButton, self).__init__(rect)
        self.selected = False
        self.col1 = Color(1, 1, 1)
        self.col2 = Color(0, .4, .65)
        self.border = border
        self.background = self.col2
        self.inner = Layer(Rect(border, border, self.frame.w - 2*border, self.frame.h - 2*border))
        self.inner.background = self.col2
        self.add_layer(self.inner)
        self.txt = txt
        self.touched = False
        self.idx = idx

    def touch_began(self, touch):
        if not touch.location in self.frame:
            return 0
        else:
            self.touched = True
            if self.idx == 0:
                return 1
            return 0

    def touch_moved(self, touch):
        self.touched = False

    def touch_ended(self, touch):
        if touch.location in self.frame and self.touched:
            self.selected = not self.selected
            if self.idx == 0:
                return 1
        return 0

class Slider (Layer):
    def __init__(self, rect, edge_l, edge_h, over_ex):
        super(Slider, self).__init__(rect)
        self.vel = 0
        self.edge_l = edge_l
        self.edge_h = edge_h
        self.over_ex = over_ex
        self.touch_active = False

    def touch_began(self, touch):
        if not touch.location in self.frame:
            return
        self.vel = 0
        self.touch_active = True

    def touch_moved(self, touch):
        if not self.touch_active:
            return
        prev_x = touch.prev_location.x
        x = touch.location.x
        self.vel = x - prev_x
        if self.frame.x > self.edge_l and self.vel > 0:
            self.vel *= (self.over_ex - self.frame.x) / (self.over_ex - self.edge_l)
        elif self.frame.x + self.frame.w < self.edge_h and self.vel < 0:
            lim = self.over_ex
            pos = self.frame.x
            w = self.frame.w
            edge = self.edge_h
            self.vel *= (pos + w - (edge - lim)) / lim

    def touch_ended(self, touch):
        self.touch_active = False

    def update_s(self):
        # low and high ends of vel adj
        low = .01
        high = .05
        # min and max vel for interpolation
        minv = 1
        maxv = 500
        # adj position by current velocity
        self.frame.x += self.vel

        # pull vel if pos beyond lower edge
        c = .2
        if self.frame.x > self.edge_l and not self.touch_active:
            self.vel = max(self.vel, 0) - c * (self.frame.x - self.edge_l)
        # pull vel if pos beyond upper edge
        elif self.frame.x + self.frame.w < self.edge_h and not self.touch_active:
            self.vel = min(self.vel, 0) + c * (self.edge_h - self.frame.x - self.frame.w)
        # adj velocity for 'friction'
        if abs(self.vel) < .25:
            self.vel = 0
        else:
            adj = high + (high - low) / (maxv - minv) - (high - low) / (maxv - minv) * min(abs(self.vel), maxv)
            self.vel *= (1-adj)
