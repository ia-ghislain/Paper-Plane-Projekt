# -*- coding: utf-8 -*-
'''A simple parallax rendering module'''

#    Copyright (C) , 2012 Åke Forslund (ake.forslund@gmail.com)
#
#    Permission to use, copy, modify, and/or distribute this software for any
#    purpose with or without fee is hereby granted, provided that the above
#    copyright notice and this permission notice appear in all copies.
#
#    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import pygame

class _subsurface:
	'''Container class for subsurface'''
	def __init__(self, surface, factor):
		self.scroll = 0
		self.factor = factor
		self.surface = surface

class ParallaxSurface:
	'''Class handling parallax scrolling of a series of surfaces'''
	def __init__(self, size, colorkey_flags = 0):
		self.colorkey_flags = colorkey_flags
		self.scroller = 0
		self.transition_img = []
		self.transition_active = False
		self.transition_delay = False
		self.transition_i = 0
		self.levels = []
		self.levels_id = {}
		self.size = size
		self.opt =  {
						"orientation":"horizontal",
						"direction":"left"
					}
		# print "parllaxSurface inited!"
	def chg_size(self,size):
		self.size = size
	def update(self, image_path, scroll_factor,size = (0,0)):
		self.rem(image_path)
		self.add(image_path, scroll_factor,size)
	def rem(self, image_path):
		if(image_path in self.levels_id):
			elem_id = self.levels_id[image_path]
			del self.levels[elem_id]
			del self.levels_id[image_path]
	def add(self, image_path, scroll_factor,size = (0,0)):
		'''Adds a parallax level, first added level is the
		   deepest level, i.e. furthest back into the \"screen\".

		   image_path is the path to the image to be used
		   scroll_factor is the slowdown factor for this parallax level.'''
		try:
			image = (pygame.image.load(image_path))
		except:
			message = "couldn't open image:" + image_path
			raise SystemExit, message
		if ".png" in image_path:
			image = image.convert_alpha()
		else:
			image = image.convert()
		if len(self.levels) > 0:
			image.set_colorkey((0xff, 0x00, 0xea), self.colorkey_flags)
		if(size[0] != 0 and size[1] != 0):
			image = pygame.transform.scale(image, size)
			self.chg_size(size)
		self.levels_id[image_path] = len(self.levels)
		self.levels.append(_subsurface(image, scroll_factor))

	def add_transition(self, image_path, scroll_factor,size = (0,0)):
		'''Adds a parallax level, first added level is the
		   deepest level, i.e. furthest back into the \"screen\".

		   image_path is the path to the image to be used
		   scroll_factor is the slowdown factor for this parallax level.'''
		try:
			image = (pygame.image.load(image_path))
		except:
			message = "couldn't open image:" + image_path
			raise SystemExit, message
		if ".png" in image_path:
			image = image.convert_alpha()
		else:
			image = image.convert()
		if len(self.levels) > 0:
			image.set_colorkey((0xff, 0x00, 0xea), self.colorkey_flags)
		if(size[0] != 0 and size[1] != 0):
			image = pygame.transform.scale(image, size)
			self.chg_size(size)
		p = _subsurface(image, scroll_factor)
		self.transition_img.append(p)
	
	def remove_transition(self,elem_id=False):
		if(elem_id == False or elem_id not in self.transition_img):
			self.transition_img = []
		else:
			del self.transition_img[elem_id]

	def enable_transition(self,delay=False):
		if(len(self.transition_img) % 2 <> 0):
			self.transition_img.append(self.transition_img[len(self.transition_img) - 1])
		self.transition_active = True
		self.transition_delay = delay
		if(len(set(self.transition_img)) == 1 or len(self.transition_img) <= 0):
			self.reset_transition()

	def disable_transition(self):
		self.transition_active = False

	def reset_transition(self):
		self.disable_transition()
		self.remove_transition()

	def is_transition_active(self):
		if(len(self.transition_img) > 1 and len(set(self.transition_img)) <> 1):
			if(self.transition_delay and self.levels[0].scroll == 0):
				return True
			elif(not self.transition_delay):
				return True
		return False

	def add_colorkeyed_surface(self, surface, scroll_factor,color_key = (0xff, 0x00, 0xea)):
		surface = surface.convert()
		if len(self.levels) > 0:
			surface.set_colorkey(color_key, self.colorkey_flags)
		self.levels.append(_subsurface(surface, scroll_factor))
		
	def add_surface(self, surface, scroll_factor):
		surface = surface.convert_alpha()
		if len(self.levels) > 0:
			surface.set_colorkey((0xff, 0x00, 0xea), self.colorkey_flags)
		self.levels.append(_subsurface(surface, scroll_factor))

	def draw(self, surface):
		''' This draws all parallax levels to the surface
			provided as argument '''
		s_width  = self.size[0]
		s_height = self.size[1]
		if(self.is_transition_active()): #Array not the same
			# print "Transition active"
			# print len(self.transition_img),self.scroller,self.transition_img[0].scroll,s_height,self.transition_img[0].scroll*s_height
			lvl = self.transition_img[0]
			lvl_next = self.transition_img[1]
			self.__blit_transition(lvl,lvl_next,surface,s_width,s_height)
			if(self.opt["orientation"] == "vertical" and self.transition_img[0].scroll == 0): #self.scroller >= (self.transition_img[0].scroll*s_height)):
				# print "Removing..."
				del self.transition_img[0]
			elif(self.opt["orientation"] == "horizontal" and self.scroller >= (self.transition_img[0].scroll*s_width)):
				del self.transition_img[0]
		else:
			for lvl in self.levels:
				self.__blit(lvl,surface,s_width,s_height)

	def __blit_transition(self,lvl,lvl_next,surface,s_width,s_height):
		if(self.opt["orientation"] == "vertical"):
			if(self.opt["direction"] == "bottom"):
				surface.blit(lvl.surface, (0, 0), (0, -lvl.scroll, s_width, s_height))
				surface.blit(lvl_next.surface, (0, lvl_next.scroll - lvl_next.surface.get_height()))
			else:
				surface.blit(lvl.surface, (0, 0), (0, lvl.scroll, s_width, s_height))
				surface.blit(lvl_next.surface, (0,lvl_next.surface.get_height() - lvl_next.scroll))
		else:
			if(self.opt["direction"] == "left"):
				surface.blit(lvl.surface, (0, 0), (lvl.scroll, 0, s_width, s_height))
				surface.blit(lvl_next.surface, (lvl_next.surface.get_width() - lvl_next.scroll, 0),(0, 0, lvl_next.scroll, s_height))
			else:
				surface.blit(lvl.surface, (0, 0), (-lvl.scroll, 0, s_width, s_height))
				surface.blit(lvl_next.surface, (lvl_next.scroll - lvl_next.surface.get_width(), 0),(0, 0, -lvl_next.scroll, s_height))

	def __blit(self,lvl,surface,s_width,s_height):
		if(self.opt["orientation"] == "vertical"):
			if(self.opt["direction"] == "bottom"):
				surface.blit(lvl.surface, (0, 0), (0, -lvl.scroll, s_width, s_height))
				surface.blit(lvl.surface, (0, lvl.scroll - lvl.surface.get_height()))
			else:
				surface.blit(lvl.surface, (0, 0), (0, lvl.scroll, s_width, s_height))
				surface.blit(lvl.surface, (0,lvl.surface.get_height() - lvl.scroll))
		else:
			if(self.opt["direction"] == "left"):
				surface.blit(lvl.surface, (0, 0), (lvl.scroll, 0, s_width, s_height))
				surface.blit(lvl.surface, (lvl.surface.get_width() - lvl.scroll, 0),(0, 0, lvl.scroll, s_height))
			else:
				surface.blit(lvl.surface, (0, 0), (-lvl.scroll, 0, s_width, s_height))
				surface.blit(lvl.surface, (lvl.scroll - lvl.surface.get_width(), 0),(0, 0, -lvl.scroll, s_height))

	def scroll(self, offset,opt={"orientation":"horizontal","direction":"left"}):
		'''scroll moves each surface _offset_ pixels / assigned factor'''
		if(isinstance(opt, dict)):
			self.opt.update(opt) # Merge given array & default array
		self.scroller = (self.scroller + offset)
		if(self.is_transition_active()):
			for lvl in self.transition_img:
				if(lvl.factor <> False):
					if(self.opt["orientation"] == "vertical"):
						lvl.scroll = (self.scroller / lvl.factor) % lvl.surface.get_height()
					else:
						lvl.scroll = (self.scroller / lvl.factor) % lvl.surface.get_width()
		else:
			for lvl in self.levels:
				if(lvl.factor <> False):
					if(self.opt["orientation"] == "vertical"):
						lvl.scroll = (self.scroller / lvl.factor) % lvl.surface.get_height()
					else:
						lvl.scroll = (self.scroller / lvl.factor) % lvl.surface.get_width()
