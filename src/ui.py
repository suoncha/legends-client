import pygame
from config import * 

class UI:
	def __init__(self):
		
		# general 
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		# bar setup 
		self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

		# convert weapon dictionary
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)

		# convert magic dictionary
		self.magic_graphics = []
		for magic in magic_data.values():
			magic = pygame.image.load(magic['graphic']).convert_alpha()
			self.magic_graphics.append(magic)

		self.potionGraphics = pygame.image.load(IMAGES + 'weapons/potion.png').convert_alpha()
		self.potionGraphics = pygame.transform.scale(self.potionGraphics, (84, 77))

		self.keyGraphics = pygame.image.load(IMAGES + 'weapons/key.png').convert_alpha()
		self.keyGraphics = pygame.transform.scale(self.keyGraphics, (46, 20))

	def show_bar(self,current,max_amount,bg_rect,color):
		# draw bg 
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		# drawing the bar
		pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

	def show_exp(self,exp):
		text_surf = self.font.render(str(int(exp)),False,TEXT_COLOR)
		x = self.display_surface.get_size()[0] - 20
		y = self.display_surface.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))

		pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
		self.display_surface.blit(text_surf,text_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

	def selection_box(self,left,top, has_switched):
		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
		if has_switched:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
		else:
			pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
		return bg_rect

	def weapon_overlay(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,730,has_switched)
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(weapon_surf,weapon_rect)

	def magic_overlay(self,magic_index,has_switched):
		bg_rect = self.selection_box(110,730,has_switched)
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(magic_surf,magic_rect)

	def potion_overlay(self, num, has_switched):
		bg_rect = self.selection_box(210,730, has_switched)
		rect = self.potionGraphics.get_rect(center = bg_rect.center)
		self.display_surface.blit(self.potionGraphics, rect)

		text_surf = self.font.render(str(int(num)),False,TEXT_COLOR)
		text_rect = text_surf.get_rect(bottomright = bg_rect.bottomright)
		self.display_surface.blit(text_surf,text_rect)

	def key_overlay(self, hasKey):
		bg_rect = self.selection_box(310,730, 0)
		rect = self.potionGraphics.get_rect(topleft = (330, 760))

		if hasKey: self.display_surface.blit(self.keyGraphics, rect)

	def advanced_health(self, player):
		transition_width = 0
		transition_color = (255, 0, 0)
		health_bar_rect = pygame.Rect(10, 10, player.current_health / player.health_ratio,BAR_HEIGHT)
		
		if player.current_health < player.health:
			player.current_health += player.health_change_speed
			transition_width = int((player.health - player.current_health) / (player.health_ratio))
			transition_color = (0, 255, 0) # green
		if player.current_health > player.health:
			if player.health < player.stats['health'] / 3:
				# if player health lower than max health / 3 than speed up animation speed
				player.current_health -= player.health_change_speed * 5
			else:
				player.current_health -= player.health_change_speed
			transition_width = int((player.current_health - player.health) / (player.health_ratio))
			transition_color = (255, 255, 0) # yellow
			if health_bar_rect.right + transition_width > player.health_bar_length + 5:
					transition_width = player.health_bar_length + 5 - health_bar_rect.right

		transition_bar_rect = pygame.Rect(health_bar_rect.right, 10, transition_width, BAR_HEIGHT)

		# black bg
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, (10, 10, player.health_bar_length, BAR_HEIGHT))
		# health bar
		pygame.draw.rect(self.display_surface, HEALTH_COLOR, health_bar_rect)
		# health bar animation
		pygame.draw.rect(self.display_surface, transition_color, transition_bar_rect)
		# outline
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, (10, 10, player.health_bar_length, BAR_HEIGHT), 3)

	def advanced_magic_bar(self, player):
		transition_width = 0
		transition_color = (255, 0, 0)
		energy_bar_rect = pygame.Rect(10, 34, player.current_energy / player.energy_ratio,BAR_HEIGHT)

		if player.current_energy < player.energy:
			player.current_energy += player.energy_change_speed
			transition_width = int((player.energy - player.current_energy) / (player.energy_ratio))
			transition_color = (0, 255, 0) # green
		if player.current_energy > player.energy:
			player.current_energy -= player.energy_change_speed
			transition_width = int((player.current_energy - player.energy) / (player.energy_ratio))
			transition_color = (255, 255, 0) # yellow
			if energy_bar_rect.right + transition_width > player.energy_bar_length:
					transition_width = player.energy_bar_length - energy_bar_rect.right

		transition_bar_rect = pygame.Rect(energy_bar_rect.right, 34, transition_width, BAR_HEIGHT)

		# black bg
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, (10, 34, player.energy_bar_length, BAR_HEIGHT))
		# energy bar
		pygame.draw.rect(self.display_surface, ENERGY_COLOR, energy_bar_rect)
		# energy bar animation
		pygame.draw.rect(self.display_surface, transition_color, transition_bar_rect)
		# outline
		pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, (10, 34, player.energy_bar_length, BAR_HEIGHT), 3)
		
	def display(self,player):
		self.advanced_health(player) # hp bar with animation
		self.advanced_magic_bar(player)

		self.show_exp(player.exp)

		self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
		self.magic_overlay(player.magic_index,not player.can_switch_magic)
		self.potion_overlay(player.potionNum, not player.can_drink)
		self.key_overlay(player.hasKey)