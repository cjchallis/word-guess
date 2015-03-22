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

class MyScene (Scene):
	def setup(self):
		# This will be called before the first frame is drawn.
		sound.set_volume(1.0)
		self.phrase = ''
		self.list_path = './Lists/'
		self.count_path = './Counts/'
		
		self.master_list = MasterList(self.list_path, self.count_path)
		
		names = os.listdir(self.list_path)
		topics = []
		topics.append('All')
		self.lists = []
		self.files = []
		i = 0
		for l in names:
			f = open(self.list_path + l, 'r')
			topics.append(f.readline())
			self.lists.append(f.readlines())
			
		self.not_empty_list = False
		self.touch_disabled = False
		self.root_layer = Layer(self.bounds)
		self.center = self.bounds.center()
		self.bckgrnd = Color(0, .4, .65)
		self.team1_color = Color(1, 1, 1)
		self.team2_color = Color(1, 1, 1)
		self.guess_offset = 50
		self.guess_size = 60
		self.team_x = 100
		self.team_y = self.center.y - 50
		self.team_w = 100
		self.team_h = 50
		self.circ_x = 100
		self.circ_y = self.center.y
		self.circ_t = 7
		self.circ_r = 25
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
		
		self.point_given = False
		
		self.b_w = 250
		self.b_h = 125
		self.b_low = 0
		self.the_button = Layer(Rect(self.center.x - self.b_w/2, self.center.y-self.b_low - self.b_h/2, self.b_w, self.b_h))
		self.the_button.background = Color(1, 1, 1)
		
		self.word = 0
		self.word_list = []
		
		self.buzz = 'Error'
		self.beep = '8ve-beep-timber'
		self.t1_snd = '8ve-beep-metallic'
		sound.load_effect(self.buzz)
		sound.load_effect(self.beep)
		sound.load_effect(self.t1_snd)
		self.beep_delay = [1, .5, .25, .125, .0625]
		self.beep_idx = 0
		self.speed_delay = 15
		
		self.guessing = False

		self.mode = 'intro'
		self.modes = {'intro'  : self.intro,
		              'cats'   : self.cats,
		              'pts'    : self.pts,
		              'guess'  : self.guess,
		              'won'    : self.won,
		              'another': self.another
		              }
		
		topics = ['All']
		topics.extend([l.topic for l in self.master_list.word_lists])
		
		h = self.bounds.h - 120
		temp_rect = Rect(0, self.center.y - h / 2.0, self.bounds.w, h)
		self.menu = SlideMenu(temp_rect, topics, Color(0, .4, .65), Color(1, 1, 1), 'AppleSDGothicNeo-Thin')
		self.test = False
		
		self.done_cats = Rect(self.center.x - 60, 0, 120, 50)
		
		
	def draw(self):
		# Update and draw our root layer. For a layer-based scene, this
		# is usually all you have to do in the draw method.
		
		background(0, .4, .65)
		
		self.root_layer.update(self.dt)
		self.root_layer.draw()
		# choose what to draw according to current mode
		self.modes[self.mode]()

	def intro(self):
		text('Word Generator', self.fnt1, 80, self.center.x, self.center.y)
	
	def cats(self):
		for i in range(1, len(self.menu.buttons)):
			self.master_list.word_lists[i-1].selected = self.menu.buttons[i].selected
		self.change_color(Color(1,1,1))
		text('Choose Categories:', self.fnt1, 40, self.center.x, self.bounds.h - 35)
		self.not_empty_list = False
		for button in self.menu.buttons:
			self.not_empty_list = self.not_empty_list or button.selected
		if self.not_empty_list:
			text('Done', self.fnt1, 40, self.center.x, 25)
		stroke_weight(1)
		stroke(1,1,1)		
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
		word = self.word_list[self.word]
		word = self.phrase
		self.text_lines(word, 14, 75, 60)
		
		fill(1,1,1)
		rect(0, 0, 10, self.t1pts * self.bounds.h / 7.0)
		rect(self.bounds.w - 10, 0, 10, self.t2pts * self.bounds.h / 7.0)
		
		stroke(0, .4, .65)
		stroke_weight(1)
		for i in range(1,7):
			h = i / 7.0 * self.bounds.h
			line(0, h, 10, h)
			line(self.bounds.w - 10, h, self.bounds.w, h)
		change_color(Color(1,1,1))
		
	def pts(self):
		if self.point_given:
			txt = 'Start'
			text(txt, self.fnt1, 80, self.center.x, self.center.y - self.b_low)
			self.change_color(Color(1,1,1))
		else:
			text_lines(self.phrase, self.fnt1, 15, self.center.x, self.center.y + 75, 50 )
			if not self.touch_disabled:
				text('Team 1', self.fnt1, 40, self.team_x, self.team_y)
				text('Team 2', self.fnt1, 40, self.bounds.w - self.team_x, self.team_y)
				text('Draw', self.fnt1, 40, self.draw_x, self.draw_y)
			
		fill(1,1,1)
		rect(0, 0, 10, self.t1pts * self.bounds.h / 7.0)
		rect(self.bounds.w - 10, 0, 10, self.t2pts * self.bounds.h / 7.0)
		
		stroke(0, .4, .65)
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
		if self.touch_disabled:
			return
		if self.mode == 'intro':
			self.mode = 'cats'
			self.root_layer.add_layer(self.menu)
			return
		elif self.mode == 'cats':
			if touch.location in self.done_cats and self.not_empty_list:
				self.word_list = []
				for i in range(1, len(self.menu.buttons)):
					if self.menu.buttons[i].selected:
						self.word_list.extend(self.lists[i-1])
				self.word_list = random.sample(self.word_list, len(self.word_list))
				self.mode = 'pts'
				self.point_given = True
				self.menu.remove_layer()
				self.phrase = self.master_list.get_word()
			self.menu.touch_began(touch)
			self.test = True
		elif self.mode == 'guess':
			self.word = (self.word + 1) % len(self.word_list)
			self.phrase = self.master_list.get_word()
			return
		elif self.mode == 'pts':
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
		elif self.mode == 'another':
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
		time = random.randint(40, 60)
		self.delay(time, self.time_up)
		self.beeps()
		self.delay(self.speed_delay, self.speed_up)
		self.point_given = False
		self.word = (self.word + 1) % len(self.word_list)
		self.phrase = self.master_list.get_word()
	
	# what to do when a team wins
	def win(self, who):
		self.not_empty_list = False
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
	
	def change_color(self, col):
		tint(col.r, col.g, col.b)
	
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
		
'''
def text_lines(txt, fnt, w, x, y, size1):
		lines = textwrap.wrap(txt, w)
		i = 0
		size = size1
		for l in lines:
			text(l, fnt, size, x, y + size * ((len(lines)-1.0)/2.0 - i))
			i += 1

def change_color(col):
	tint(col.r, col.g, col.b)
'''
		
run(MyScene(), LANDSCAPE)
