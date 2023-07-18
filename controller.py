from pyPS4Controller.controller import Controller


class MyController(Controller):
    def __init__(self):
        super().__init__('/dev/input/js0', False)
        self.controls = {
            # Buttons top
            'l1_hold': False,
            'l1': False,
            'l2_hold': False,
            'l2': False,
            'l2_value': 0,
            'r1_hold': False,
            'r1': False,
            'r2_hold': False,
            'r2': False,
            'r2_value': 0,
            # Buttons left
            'up_hold': False,
            'up': False,
            'down_hold': False,
            'down': False,
            'left_hold': False,
            'left': False,
            'right_hold': False,
            'right': False,
            # Buttons right
            'x_hold': False,
            'x': False,
            'square_hold': False,
            'square': False,
            'triangle_hold': False,
            'triangle': False,
            'circle_hold': False,
            'circle': False,
            # Buttons midle
            'share': False,
            'options': False,
            'ps': False,
            # Left stick
            'move_x': 0,
            'move_y': 0,
            # Right stick
            'look_x': 0,
            'look_y': 0,
        }

    def get_inputs(self):
        result = self.controls.copy()

        self.controls['l1'] = False
        self.controls['l2'] = False
        self.controls['r1'] = False
        self.controls['r2'] = False

        self.controls['x'] = False
        self.controls['square'] = False
        self.controls['triangle'] = False
        self.controls['circle'] = False

        self.controls['up'] = False
        self.controls['down'] = False
        self.controls['left'] = False
        self.controls['right'] = False

        self.controls['share'] = False
        self.controls['options'] = False
        self.controls['ps'] = False

        return result

    # X Cross
    def on_x_press(self):
        self.controls['x_hold'] = True
        self.controls['x'] = True

    def on_x_release(self):
        self.controls['x_hold'] = False

    # [] Square
    def on_square_press(self):
        self.controls['square_hold'] = True
        self.controls['square'] = True

    def on_square_release(self):
        self.controls['square_hold'] = False

    # /\ Triangle
    def on_triangle_press(self):
        self.controls['triangle_hold'] = True
        self.controls['triangle'] = True

    def on_triangle_release(self):
        self.controls['triangle_hold'] = False

    # O Circle
    def on_circle_press(self):
        self.controls['circle_hold'] = True
        self.controls['circle'] = True

    def on_circle_release(self):
        self.controls['circle_hold'] = False

    # Up - UpDown - Down
    def on_up_arrow_press(self):
        self.controls['up_hold'] = True
        self.controls['up'] = True

    def on_up_down_arrow_release(self):
        self.controls['up_hold'] = False
        self.controls['down_hold'] = False

    def on_down_arrow_press(self):
        self.controls['down_hold'] = True
        self.controls['down'] = True

    # Left - LeftRight - Right
    def on_left_arrow_press(self):
        self.controls['left_hold'] = True
        self.controls['left'] = True

    def on_left_right_arrow_release(self):
        self.controls['left_hold'] = False
        self.controls['right_hold'] = False

    def on_right_arrow_press(self):
        self.controls['right_hold'] = True
        self.controls['right'] = True

    # L1
    def on_L1_press(self):
        self.controls['l1_hold'] = True
        self.controls['l1'] = True

    def on_L1_release(self):
        self.controls['l1_hold'] = False

    # R1
    def on_R1_press(self):
        self.controls['r1_hold'] = True
        self.controls['r1'] = True

    def on_R1_release(self):
        self.controls['r1_hold'] = False

    # L2
    def on_L2_press(self, value):
        self.controls['l2_hold'] = True
        self.controls['l2'] = True
        self.controls['l2_value'] = value

    def on_L2_release(self):
        self.controls['l2_hold'] = False
        self.controls['l2_value'] = 0

    # R2
    def on_R2_press(self, value):
        self.controls['r2_hold'] = True
        self.controls['r2'] = True
        self.controls['r2_value'] = value

    def on_R2_release(self):
        self.controls['r2_hold'] = False
        self.controls['r2_value'] = 0

    # L3
    def on_L3_up(self, value):
        self.controls['move_x'] = value

    def on_L3_down(self, value):
        self.controls['move_x'] = value

    def on_L3_left(self, value):
        self.controls['move_y'] = value

    def on_L3_right(self, value):
        self.controls['move_y'] = value

    def on_L3_y_at_rest(self):
        self.controls['move_y'] = 0

    def on_L3_x_at_rest(self):
        self.controls['move_x'] = 0

    def on_L3_press(self):
        self.controls['move_y'] = 0
        self.controls['move_x'] = 0

    def on_L3_release(self):
        pass

    # R3
    def on_R3_up(self, value):
        self.controls['look_x'] = value

    def on_R3_down(self, value):
        self.controls['look_x'] = value

    def on_R3_left(self, value):
        self.controls['look_y'] = value

    def on_R3_right(self, value):
        self.controls['look_y'] = value

    def on_R3_y_at_rest(self):
        self.controls['look_y'] = 0

    def on_R3_x_at_rest(self):
        self.controls['look_x'] = 0

    def on_R3_press(self):
        self.controls['look_y'] = 0
        self.controls['look_x'] = 0

    def on_R3_release(self):
        pass

    # Option
    def on_options_press(self):
        self.controls['options_hold'] = True
        self.controls['options'] = True

    def on_options_release(self):
        self.controls['options_hold'] = False

    # Share
    def on_share_press(self):
        self.controls['share_hold'] = True
        self.controls['share'] = True

    def on_share_release(self):
        self.controls['share_hold'] = False

    # PS
    def on_playstation_button_press(self):
        self.controls['ps_hold'] = True
        self.controls['ps'] = True

    def on_playstation_button_release(self):
        self.controls['ps_hold'] = False
