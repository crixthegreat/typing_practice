#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/4 12:03:59

import random
import cocos
import pyglet
import sys

class Game(object):
    
    game_status = 'menu'
    default_color = (0, 0, 0, 255)
    game_level = 'normal'
    
    def __init__(self, prac_len = 20, level = 'Normal'):

        self.level = level
        self.prac_len = prac_len
        self.game_init()
        self.status = 'menu'

    def game_init(self):

        print('game initialising...')
        pass

    @staticmethod
    def show_highscore(tLayer):
        pass

    @staticmethod
    def write_highscore():
        pass

class Menu(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, game):


        super(Menu, self).__init__()
        self.keys_pressed = set()
        
        self.game = game
        self.start_timer = 0
        self.time_passed = 0
        self.schedule(self.Timer_Refresh)

        
        self.image = pyglet.resource.image('menu.png')
        print('menu initialised')
        Game.show_highscore(self)

        self.level_label = cocos.text.Label(self.game.level,
            font_size = 26,
            font_name = 'Verdana', 
            bold = True, 
            color = Game.default_color, 
            x = 455, y = 240)

        self.add(self.level_label)



    def draw(self):

        self.image.blit(0,0)

    def do_actions(self):

        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]

        if 'ENTER' in key_names:
            print('menu pressed Enter')
            self.visible = False
            self.game.status = 'main'
        elif 'LEFT' in key_names:
            if self.game.level != 'Normal':
                self.game.level = 'Normal'
                self.level_label.element.text = self.game.level
        elif 'RIGHT' in key_names:
            if self.game.level != 'Hard':
                self.game.level = 'Hard'
                self.level_label.element.text = self.game.level


    def on_key_press(self, key, modifiers):
        
        if Game.game_status == 'menu':
            self.keys_pressed.add(key)
            self.do_actions()
            self.keys_pressed.remove(key)


    def Timer_Refresh(self, dt):
        """A simple on_time event
        dt means the time passed after the last event
        use the StartTimer and 'dt' to set the time interval
        use the TimePassed the calculate the time passed of the game
        """
        self.start_timer += dt
        self.time_passed += dt
        if self.start_timer > 1:  # timer_interval
            self.StartTimer = 0
            if self.game.status == 'menu':
                self.visible = True



    def get_name(self):
        
        _ = self.name

        return _
        

class Main_screen(cocos.layer.Layer):
    

    is_event_handler = True
    
    def __init__(self, game):


        super(Main_screen, self).__init__()

        self.start_timer = 0
        self.time_passed = 0
        self.game_started = False

        self.default_color = (0, 0, 0, 255)
        
        self.schedule(self.Timer_Refresh)

        self.keys_pressed = set()
        self.visible = False
        self.game = game

        #self.prac_len = menu.prac_len
        #self.level = menu.level

        self.image = pyglet.resource.image('main_screen.png')
        print('main screen initialised')
        Game.show_highscore(self)

        self.Time_Label = cocos.text.Label('00:00',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 345, y = 175)

        self.add(self.Time_Label)

        self.BestTime_Label = cocos.text.Label('99:59',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 585, y = 173)
    
        self.add(self.BestTime_Label)


        self.prac_label = cocos.text.Label('GET READY 3',
            font_size = 32,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 155, y = 375)
    
        self.add(self.prac_label)

        self.input_label = cocos.text.Label('>>>',
            font_size = 32,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 135, y = 240)
    
        self.add(self.input_label)



    def draw(self):

        self.image.blit(0,0)


    def on_key_press(self, key, modifiers):
        
        _str='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if self.game.status == 'main':
            self.keys_pressed.add(key)
            key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]

            if 'SPACE' in key_names:
                print('Main_screen pressed Enter')
                self.visible = False
                self.game.status = 'menu'
                self.game_started = False
            elif self.game_started and (key_names[0] in _str) and len(self.input_label.element.text) < self.game.prac_len:
                self.input_label.element.text += key_names[0]

            self.keys_pressed.remove(key)


    def Timer_Refresh(self, dt):
        """A simple on_time event
        dt means the time passed after the last event
        use the StartTimer and 'dt' to set the time interval
        use the TimePassed the calculate the time passed of the game
        """
        self.start_timer += dt
        self.time_passed += dt
        if self.start_timer > 1:  # timer_interval
            if self.game.status == 'main':
                self.start_timer = 0
                self.Time_Label.element.text = str(int(self.time_passed // 60)) + ' : ' + str(int(self.time_passed % 60)) 
                self.visible = True
                if int(self.time_passed) <4 and self.game_started == False:
                    self.prac_label.element.text = 'GET READY ' + str(int(3 - self.time_passed))
                else:
                    if self.game_started == False:
                        self.time_passed = 0
                        _str = []
                        if self.game.level == 'Normal':
                            print('Normal game started')
                            for _ in range(self.game.prac_len):
                                _str.append(chr(random.randint(97,122))) 
                            random.shuffle(_str)
                            _str = ''.join(_str)
                        elif self.game.level == 'Hard':
                            print('Hard game started')
                            for _ in range(26):
                                _str.append(chr(97 + _))
                                _str.append(chr(65 + _))
                            random.shuffle(_str)
                            _str = _str[:self.game.prac_len]
                            _str = ''.join(_str)
                        else:
                            print('unknown game level')
                            sys.exit()

                        self.prac_label.element.text = _str 
                        self.game_started = True


class High_score(Game):


    def get_input(self, name, score):
        pass

    def show_score(self):
        pass

    def write_score(self, name, score):
        pass



if __name__ == '__main__':


    cocos.director.director.init(width = 800, height = 600, caption = 'Typing practice game by Crix for Judy')
    my_game = Game()
    my_menu = Menu(my_game)
    my_screen = Main_screen(my_game)
    main_scene = cocos.scene.Scene(my_menu, my_screen)
    print ('game initialised')
    cocos.director.director.run(main_scene)

    print('game end')



