#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/4 12:03:59

import random
import cocos
import pyglet
import sys
import json

class Game(object):
    
    default_color = (0, 0, 0, 255)
    highlight_color = (200, 30, 30, 255)
    highscore_file = 'highscore.tp'
    
    def __init__(self, prac_len = 20, level = 'Normal', name = 'Judy'):

        self.level = level
        self.prac_len = prac_len
        self.game_init()
        self.status = 'menu'
        self.name = name

    def game_init(self):

        print('game initialising...')
        pass

    def get_highscore(self):
        """get the fifth high score from the record file

        """


        with open(Game.highscore_file) as _file:
            try:
                _data = json.load(_file)
            except:
                print('open file failed')

            data_normal = sorted(_data[0:5])
            data_hard = sorted(_data[5:])
            if self.level == 'Normal':
                return data_normal[4][0]
            elif self.level == 'Hard':
                return data_hard[4][0]
            else:
                print('wrong game level')

    def refresh_highscore(self, normal_highscore_label, hard_highscore_label):
        _data = self.show_highscore()
        for _ in range(5):
            normal_highscore_label[_].element.text = _data[_][1] + ' ' * (10 - len(_data[_][1])) + str(_data[_][0] // 60) + ':' + str(_data[_][0] % 60) 
        for _ in range(5):
            hard_highscore_label[_].element.text = _data[5 + _][1] + ' ' * (10 - len(_data[5 + _][1])) + str(_data[5 + _][0] // 60) + ':' + str(_data[5 + _][0] % 60) 

    def show_highscore(self):

        with open(Game.highscore_file) as _file:
            try:
                _data = json.load(_file)
            except:
                print('open file failed')
            return _data

    def write_highscore(self, name, highscore):
        with open(Game.highscore_file) as _file:
            try:
                _data = json.load(_file)
            except:
                print('open file failed')

            data_normal = sorted(_data[0:5])
            data_hard = sorted(_data[5:])
            
            if self.level == 'Normal':
                _ = data_normal
            elif self.level == 'Hard':
                _ = data_hard
            else:
                print('wrong game level')

            _ = _ + [[highscore, name[:10]]]
            print(' _ before sorted', _)
            _ = sorted(_)
            print(' _ after sorted', _)
            _ = _[:5]
            print(' _ after trimed', _)

            if self.level == 'Normal':
                _data = _ + data_hard
            elif self.level == 'Hard':
                _data = data_normal + _

            print(_, _data)

        with open(Game.highscore_file, 'w') as _file:
            try:
                json.dump(_data, _file)
            except:
                print('write file failed')
        


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

        _data = self.game.show_highscore()
        print('_data = ', _data)
        self.normal_highscore_label = []
        self.hard_highscore_label = []

        for _ in range(5):
            print('normal', _)
            self.normal_highscore_label.append(cocos.text.Label(_data[_][1] + ' ' * (10 - len(_data[_][1])) + str(_data[_][0] // 60) + ':' + str(_data[_][0] % 60), 
               font_size = 16, 
               font_name = 'Verdana', 
               bold = False, 
               color = Game.default_color, 
               x = 220, y = 110 - (_ * 25)))
            self.add(self.normal_highscore_label[_])

        for _ in range(5):
            print('hard', _)
            self.hard_highscore_label.append(cocos.text.Label(_data[5 + _][1] + ' ' * (10 - len(_data[5 + _][1])) + str(_data[5 + _][0] // 60) + ':' + str(_data[5 + _][0] % 60), 
               font_size = 16, 
               font_name = 'Verdana', 
               bold = False, 
               color = Game.default_color, 
               x = 450, y = 110 - (_ * 25)))
            self.add(self.hard_highscore_label[_])

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

        print('menu keys: ',key_names)       
        if 'ENTER' in key_names:
            print('menu pressed Enter')
            self.visible = False
            self.keys_pressed.pop()
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
        if self.game.status == 'menu':
            self.keys_pressed.add(key)
            self.do_actions()

    def on_key_release(self, key, modifiers):

        if self.game.status == 'menu' and len(self.keys_pressed) > 0:
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
                self.game.refresh_highscore(self.normal_highscore_label, self.hard_highscore_label)
        

class Main_screen(cocos.layer.Layer):
    

    is_event_handler = True
    
    def __init__(self, game):


        super(Main_screen, self).__init__()

        self.game = game
        self.default_color = (0, 0, 0, 255)
        self.image = pyglet.resource.image('main_screen.png')
        print('main screen initialised')
        
        self.Time_Label = cocos.text.Label('00:00',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 165, y = 205)
        self.add(self.Time_Label)

        self.BestTime_Label = cocos.text.Label('99:59',
            font_size = 16,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 555, y = 205)
        self.add(self.BestTime_Label)

        self.prac_label = cocos.text.Label('GET READY 3',
            font_size = 32,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 155, y = 395)
        self.add(self.prac_label)

        self.input_label = cocos.text.Label('',
            font_size = 32,
            font_name = 'Verdana', 
            bold = False, 
            color = self.default_color, 
            x = 135, y = 260)
        self.add(self.input_label)

        _data = self.game.show_highscore()
        print('_data = ', _data)
        self.normal_highscore_label = []
        self.hard_highscore_label = []

        for _ in range(5):
            print('normal', _)
            self.normal_highscore_label.append(cocos.text.Label(_data[_][1] + ' ' * (10 - len(_data[_][1])) + str(_data[_][0] // 60) + ':' + str(_data[_][0] % 60), 
               font_size = 16, 
               font_name = 'Verdana', 
               bold = False, 
               color = Game.default_color, 
               x = 220, y = 110 - (_ * 25)))
            self.add(self.normal_highscore_label[_])

        for _ in range(5):
            print('hard', _)
            self.hard_highscore_label.append(cocos.text.Label(_data[5 + _][1] + ' ' * (10 - len(_data[5 + _][1])) + str(_data[5 + _][0] // 60) + ':' + str(_data[5 + _][0] % 60), 
               font_size = 16, 
               font_name = 'Verdana', 
               bold = False, 
               color = Game.default_color, 
               x = 450, y = 110 - (_ * 25)))
            self.add(self.hard_highscore_label[_])


        self.game_init()

        
        self.start_timer = 0
        self.schedule(self.Timer_Refresh)

        self.keys_pressed = set()
        self.visible = False
        self.game = game


    
    def game_init(self):

        self.time_passed = 0
        self.game_started = False
        self.input_label.element.text = ''

    def draw(self):

        self.image.blit(0,0)


    def on_key_press(self, key, modifiers):
        
        _str='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if self.game.status == 'main' or self.game.status == 'highscore':
            self.keys_pressed.add(key)
            key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]

            if 'SPACE' in key_names:
                print('Main_screen pressed SPACE')
                self.visible = False
                self.keys_pressed.pop()
                self.game.status = 'menu'
                self.game_init()
            elif 'BACKSPACE' in key_names:
                _str = self.input_label.element.text
                self.input_label.element.text = _str[:len(_str) - 1]
            elif 'ENTER' in key_names:
                if self.game.status == 'main' and self.game_started:
                    if self.input_label.element.text != self.prac_label.element.text:
                        print('the game mode is: ' + self.game.status)
                        print('you failed')
                        self.game_init()
                    else:
                        print('bingo!')
                        if self.time_passed <= self.game.get_highscore():
                            self.prac_label.element.text = 'HIGH SCORE! NAME:'
                            self.input_label.element.text = self.game.name
                            self.game.status = 'highscore'
                            print('now game changes into ' + self.game.status + ' mode')
                elif self.game.status == 'highscore':
                    self.game.name = self.input_label.element.text
                    self.game.write_highscore(self.game.name, int(self.time_passed))
                    print('highscore saved', self.game.name, self.time_passed)
                    self.game.status = 'main'
                    self.game.show_highscore()
                    self.game_init()

            elif self.game_started and len(self.input_label.element.text) < self.game.prac_len:
                print('main screen key pressed', key_names)
                if len(key_names) > 1 and ('LSHIFT' in key_names) and (key_names[1] in _str or key_names[0] in _str):
                    if key_names[0] in _str:
                        self.input_label.element.text += key_names[0]
                    else:
                        self.input_label.element.text += key_names[1]
                elif len(key_names) == 1 and (key_names[0] in _str):
                    self.input_label.element.text += key_names[0].lower()


    def on_key_release(self, key, modifiers):
        if (self.game.status == 'main' or self.game.status == 'highscore')and len(self.keys_pressed) > 0:
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
                self.game.refresh_highscore(self.normal_highscore_label, self.hard_highscore_label)

                # count down SFX    
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


if __name__ == '__main__':


    cocos.director.director.init(width = 800, height = 600, caption = 'Typing practice game by Crix for Judy')
    my_game = Game()
    my_menu = Menu(my_game)
    my_screen = Main_screen(my_game)
    main_scene = cocos.scene.Scene(my_menu, my_screen)
    print ('game initialised')
    cocos.director.director.run(main_scene)

    print('game end')



