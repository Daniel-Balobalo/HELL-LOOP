import pygame
import random

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 # 0:idle, 1:run, 2:jump, 3:fall, 4:attack1, 5:attack2, 6:takehit, 7:die
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 100))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True
        
        # AI specific attributes
        self.ai_move_delay = 0
        self.ai_current_dx = 0
        self.ai_last_action = None
        self.ai_reaction_time = 0
        self.ai_difficulty = "hard"

    def load_images(self, sprite_sheet, animation_steps):
        # Extract images from spritesheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)             
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list
    
    # Set AI Move Method
    def ai_move(self, target, screen_width, screen_height, surface, round_over):
        if not self.alive or round_over or self.attacking:
            return

        dx = 0
        self.running = False

        distance = abs(self.rect.centerx - target.rect.centerx)
        in_attack_range = distance < 150

        if self.ai_move_delay <= 0:
            self.ai_move_delay = random.randint(10, 30)

            if in_attack_range:
                if random.random() < 0.7:  # Attack
                    self.attack_type = random.choice([1, 2])
                    self.attack(surface, target)
                else:  # Back off
                    self.ai_current_dx = -8 if self.flip else 8
            else:
                if self.rect.centerx < target.rect.centerx:
                    self.ai_current_dx = random.uniform(4, 8)
                else:
                    self.ai_current_dx = random.uniform(-8, -4)

            if random.random() < 0.2 and not self.jump:
                self.vel_y = -25
                self.jump = True
        else:
            self.ai_move_delay -= 1

        dx = self.ai_current_dx
        self.running = True if dx != 0 else False

        self.vel_y += 2
        dy = self.vel_y

        if self.rect.left + dx < 0:
            dx = 0
        if self.rect.right + dx > screen_width:
            dx = 0

        if self.rect.bottom + dy > screen_height - 45:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 45 - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

            
    # Set Move Method    
    def move(self, Screen_Width, Screen_Height, surface, target, round_over):
        speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        
        # Get Keypresses
        key = pygame.key.get_pressed()
        
        # Can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False:
            
            # Check Player 1 Controls
            if self.player == 1:
            
                # Movement
                if key[pygame.K_a]:
                    dx = -speed
                    self.running = True
                if key[pygame.K_d]:
                    dx = speed
                    self.running = True
                
                # Jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                    
                # Attack
                if key[pygame.K_k] or key[pygame.K_l]:
                    self.attack(surface, target)
                    # Determine which attack type was used
                    if key[pygame.K_k]:
                        self.attack_type = 1
                    if key[pygame.K_l]:
                        self.attack_type = 2
            elif self.player == 2:
                self.ai_move(target, Screen_Width, Screen_Height, surface, round_over)
            
        self.vel_y += gravity
        dy += self.vel_y
            
        # Ensure Player Stays on Screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > Screen_Width:
            dx = Screen_Width - self.rect.right
        if self.rect.bottom + dy > Screen_Height - 45:
            self.vel_y = 0
            self.jump = False
            dy = Screen_Height - 45 - self.rect.bottom
            
        # Ensure Players Face Each Other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
            
        # Apply Attack Cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Update Player Position
        self.rect.x += dx
        self.rect.y += dy
        
    # Handle Animation Updates
    def update(self):
        # Check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(7) # 7:die
        
        elif self.hit == True:
            self.update_action(6) # 6:takehit
            
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(4) # 4:attack1
            elif self.attack_type == 2:
                self.update_action(5) # 5:attack2
                
        elif self.jump == True:
            self.update_action(2) # 2:jump
        
        elif self.running == True:
            self.update_action(1) # 1:run
            
        else:
            self.update_action(0) # 0:idle
            
        animation_cooldown = 40
        # Update Image
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # If the player is dead, then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # Check if an attack was executed
                if self.action == 4 or self.action == 5:
                    self.attacking = False
                    self.attack_cooldown = 20
                # Check if Damage was Taken
                if self.action == 6:
                    self.hit = False
                    # If both are in the clash state, the attack is stopped.
                    self.attacking = False
                    self.attack_cooldown = 20

    # Set Attack Method    
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            # Execute Attack
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True
    
    def update_action(self, new_action):
        # Check if the New Action is different from the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
    # Set Draw Method    
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0]* self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))