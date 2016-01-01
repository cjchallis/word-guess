from scene import *
from master import *
from slide_menu import *
from utilities import *
from math import sqrt
from functools import partial
import textwrap
import os
import random
import sound
import time

blue = Color(0, .4, .65)
white = Color(1, 1, 1)

class MyScene (Scene):
    def setup(self):
        # This will be called before the first frame is drawn.
        self.set_colors()
        self.make_list()
        self.make_buttons()
        self.set_sounds()
        self.set_modes()
        self.make_menu()

    def stop(self):
        text('I will never stop.', self.fnt1, 40, self.center.x, self.center.y)
        sound.play_effect(self.beep)
        

    def set_colors(self):
        self.bckgrnd = blue
        self.team1_color = white
        self.team2_color = white
        self.txt_col = white

    def make_list(self):
        self.phrase = ''
        self.list_path = './Lists/'
        self.count_path = './Counts/'
        self.master_list = MasterList(self.list_path, self.count_path)

    def make_buttons(self):
        self.root_layer = Layer(self.bounds)
        self.center = self.bounds.center()
        self.guess_offset = 50
        self.guess_size = 60
        self.team_x = 100
        self.team_y = self.center.y - 50
        self.team_w = 100
        self.team_h = 50
        self.draw_x = self.center.x
        self.draw_y = self.center.y - 50
        self.draw_w = 100
        self.draw_h = 50
        self.t1pts = 0
        self.t2pts = 0
        self.fnt1 = 'AppleSDGothicNeo-Thin'
        self.fnt2 = 'AppleSDGothicNeo-Regular'

        self.change = Rect(self.center.x - 50, self.center.y - 90, 100, 50)
        self.again = Rect(self.center.x - 50, self.center.y + 40, 100, 50)

        self.team1_button = Rect(self.team_x - self.team_w * .5, self.team_y - self.team_h * .5, self.team_w, self.team_h)

        self.team2_button = Rect(self.bounds.w - self.team_x - self.team_w * .5, self.team_y - self.team_h * .5, self.team_w, self.team_h)

        self.draw_button = Rect(self.draw_x - self.draw_w * .5, self.draw_y - self.draw_h * .5, self.draw_w, self.draw_h)

        self.b_w = 250
        self.b_h = 125
        self.b_low = 0
        self.the_button = Layer(Rect(self.center.x - self.b_w/2, self.center.y-self.b_low - self.b_h/2, self.b_w, self.b_h))
        self.the_button.background = self.txt_col

        self.done_cats = Rect(self.center.x - 60, 0, 120, 50)

    def set_sounds(self):
        sound.set_volume(1.0)
        self.buzz = 'Error'
        self.beep = '8ve-beep-timber'
        self.t1_snd = '8ve-beep-metallic'
        sound.load_effect(self.buzz)
        sound.load_effect(self.beep)
        sound.load_effect(self.t1_snd)
        self.beep_delay = [.5, .35, .24, .15, .11]
        self.beep_idx = 0
        self.speed_delay = 15

    def set_modes(self):
        self.empty_list = True
        self.touch_disabled = False
        self.point_given = False
        self.guessing = False
        self.mode = 'intro'
        self.modes = {'intro'  : self.intro,
                      'cats'   : self.cats,
                      'pts'    : self.pts,
                      'guess'  : self.guess,
                      'won'    : self.won,
                      'another': self.another
                      }
        self.touches = {'intro'  : self.i_touch,
                        'cats'   : self.c_touch,
                        'pts'    : self.p_touch,
                        'guess'  : self.g_touch,
                        'won'    : self.w_touch,
                        'another': self.a_touch
                        }

    def make_menu(self):
        topics = ['All']
        topics.extend([l.topic for l in self.master_list.word_lists])
        h = self.bounds.h - 120
        temp_rect = Rect(0, self.center.y - h / 2.0, self.bounds.w, h)
        self.menu = SlideMenu(temp_rect, topics, self.bckgrnd, self.txt_col, 'AppleSDGothicNeo-Thin')
        self.test = False

    def draw(self):
        # Update and draw our root layer. For a layer-based scene, this
        # is usually all you have to do in the draw method.

        background(self.bckgrnd.r, self.bckgrnd.g, self.bckgrnd.b)

        self.root_layer.update(self.dt)
        self.root_layer.draw()
        # choose what to draw according to current mode
        self.modes[self.mode]()

    def intro(self):
        text('Word Generator', self.fnt1, 70, self.center.x, self.center.y)

    def cats(self):
        for i in range(1, len(self.menu.buttons)):
            self.master_list.word_lists[i-1].selected = self.menu.buttons[i].selected
        change_color(self.txt_col)
        text('Choose Categories:', self.fnt1, 40, self.center.x, self.bounds.h - 35)
        self.empty_list = not any(b.selected for b in self.menu.buttons)
        if not self.empty_list:
            text('Done', self.fnt1, 40, self.center.x, 25)
        stroke_weight(1)
        change_stroke(white)
        offset = 60
        line(0, offset, self.bounds.w, offset)
        line(0, self.bounds.h - offset, self.bounds.w, self.bounds.h - offset)
        self.menu.update_m()

    def text_lines(self, txt, w, size1, size2):
        w = w + len(txt) / 12.0
        lines = textwrap.wrap(txt, w)
        i = 0
        size = size1 - len(txt)/2
        if len(txt) < 9:
            size = size1 * 1.2
        for l in lines:
            text(l, self.fnt1, size, self.center.x, self.center.y + size * ((len(lines)-1.0)/2.0 - i))
            i += 1

    def guess(self):
        word = self.phrase
        self.text_lines(word, 14, 75, 60)

        change_stroke(white)
        fill(1,1,1)
        rect(0, 0, 10, self.t1pts * self.bounds.h / 7.0)
        rect(self.bounds.w - 10, 0, 10, self.t2pts * self.bounds.h / 7.0)

        change_stroke(blue)
        stroke_weight(1)
        for i in range(1,7):
            h = i / 7.0 * self.bounds.h
            line(0, h, 10, h)
            line(self.bounds.w - 10, h, self.bounds.w, h)
        change_color(white)

    def pts(self):
        if self.point_given:
            txt = 'Start'
            text(txt, self.fnt1, 80, self.center.x, self.center.y - self.b_low)
            change_color(white)
        else:
            text_lines(self.phrase, self.fnt1, 15, self.center.x, self.center.y + 75, 50 )
            if not self.touch_disabled:
                text('Team 1', self.fnt1, 40, self.team_x, self.team_y)
                text('Team 2', self.fnt1, 40, self.bounds.w - self.team_x, self.team_y)
                text('Draw', self.fnt1, 40, self.draw_x, self.draw_y)

        change_stroke(white)
        fill(1,1,1)
        rect(0, 0, 10, self.t1pts * self.bounds.h / 7.0)
        rect(self.bounds.w - 10, 0, 10, self.t2pts * self.bounds.h / 7.0)

        change_stroke(blue)
        stroke_weight(1)
        for i in range(1,7):
            h = i / 7.0 * self.bounds.h
            line(0, h, 10, h)
            line(self.bounds.w - 10, h, self.bounds.w, h)
        change_color(Color(1,1,1))

    def won(self):
        pass

    def another(self):
        text('Play Again', self.fnt1, 40, self.center.x, self.center.y + 60)
        text('Change Categories', self.fnt1, 40, self.center.x, self.center.y - 60)

    def touch_began(self, touch):
        if not self.touch_disabled:
            self.touches[self.mode](touch)

    def i_touch(self, touch):
        self.mode = 'cats'
        self.root_layer.add_layer(self.menu)

    def c_touch(self, touch):
        if touch.location in self.done_cats and not self.empty_list:
            self.mode = 'pts'
            self.point_given = True
            self.menu.remove_layer()
            self.phrase = self.master_list.get_word()
        self.menu.touch_began(touch)
        self.test = True

    def g_touch(self, touch):
        self.phrase = self.master_list.get_word()

    def p_touch(self, touch):
        if touch.location in self.team1_button and not self.point_given:
            self.t1pts += 1
            self.point_given = True
            sound.play_effect(self.t1_snd)
            if self.t1pts == 7:
                self.mode = 'won'
                self.win("Team 1")
        elif touch.location in self.team2_button and not self.point_given:
            self.t2pts +=1
            self.point_given = True
            sound.play_effect(self.t1_snd)
            if self.t2pts == 7:
                self.mode = 'won'
                self.win("Team 2")
        elif touch.location in self.the_button.frame and self.point_given:
            self.start_guessing()
        elif touch.location in self.draw_button and not self.point_given:
            self.point_given = True

    def w_touch(self):
        pass

    def a_touch(self, touch):
        if touch.location in self.again:
            self.mode = 'pts'
        if touch.location in self.change:
            self.mode = 'cats'

    def touch_moved(self, touch):
        if self.mode == 'cats':
            self.menu.touch_moved(touch)

    def touch_ended(self, touch):
        if self.mode == 'cats' and self.test:
            self.menu.touch_ended(touch)
        self.test = False

    def toggle_touch(self):
        self.touch_disabled = not self.touch_disabled

    def start_guessing(self):
        self.mode = 'guess'
        self.beep_idx = 0
        time = random.randint(2,3)
        self.delay(time, self.time_up)
        self.beeps()
        self.delay(self.speed_delay, self.speed_up)
        self.point_given = False
        self.phrase = self.master_list.get_word()

    # what to do when a team wins
    def win(self, who):
        self.empty_list = True
        self.song()
        font_size = 100 if self.size.w > 700 else 50
        text_layer = TextLayer(who + " Wins!", self.fnt1, font_size)
        text_layer.frame.center(self.bounds.center())
        overlay = Layer(self.bounds)
        overlay.background = Color(0, 0, 0, 0)
        overlay.add_layer(text_layer)
        self.add_layer(overlay)
        overlay.animate('background', Color(0.0, 0.2, 0.3, 0.7))
        text_layer.animate('scale_x', 1.3, 0.3, autoreverse=True)
        text_layer.animate('scale_y', 1.3, 0.3, autoreverse=True)
        self.touch_disabled = True
        self.root_layer.animate('scale_x', 0.0, delay=2.0,
                                curve=curve_ease_back_in)
        self.root_layer.animate('scale_y', 0.0, delay=2.0,
                                curve=curve_ease_back_in,
                                completion=self.new_game)

    def new_game(self):
        self.mode = 'another'
        self.t1pts = 0
        self.t2pts = 0
        self.touch_disabled = False
        self.root_layer.sublayers = []
        self.root_layer.animate('scale_x', 1.0)
        self.root_layer.animate('scale_y', 1.0)

    def time_up(self):
        self.mode = 'pts'
        sound.play_effect(self.buzz)
        self.delay(.25, partial(sound.play_effect, self.buzz))
        self.delay(.5, partial(sound.play_effect, self.buzz))
        self.toggle_touch()
        self.delay(1.5, self.toggle_touch)

    def beeps(self):
        sound.play_effect(self.beep)
        if self.mode == 'guess':
            self.beep_idx = min(self.beep_idx, len(self.beep_delay) - 1)
            self.delay(self.beep_delay[self.beep_idx], self.beeps)

    def speed_up(self):
        if self.mode != 'guess':
            return
        self.beep_idx += 1
        if self.beep_idx < len(self.beep_delay) - 1:
            self.delay(self.speed_delay, self.speed_up)

    def song(self):
        beat = .15
        self.delay(beat, partial(sound.play_effect, 'Piano_C4'))
        self.delay(2*beat, partial(sound.play_effect, 'Piano_E4'))
        self.delay(3*beat, partial(sound.play_effect, 'Piano_G4'))
        self.delay(7*beat, partial(sound.play_effect, 'Piano_G3'))
        self.delay(9*beat, partial(sound.play_effect, 'Piano_C4'))

run(MyScene(), LANDSCAPE)
