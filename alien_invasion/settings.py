class Settings():
    def __init__(self):
        self.screen_width=1200
        self.screen_height=700
        self.bg_color=(230,230,230)
        self.ship_limit=3
        #bullet settings
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=250,0,250
        self.allowed_bullets=3
        #alien settings
        self.fleet_drop_speed=5

        self.speedup_scale=1.3
        self.score_scale=1.5
        self.high_score=0
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        self.ship_speed_factor=1.5
        self.bullet_speed=5
        self.alien_speed_factor=1
        self.fleet_direction=1
        self.alien_points=50
    def increase_speed(self):
        self.ship_speed_factor *=self.speedup_scale
        self.bullet_speed *=self.speedup_scale
        self.alien_speed_factor *=self.speedup_scale
        self.alien_points =int(self.alien_points*self.score_scale)



        

