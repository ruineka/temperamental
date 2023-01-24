import pyglet
from pyglet.window import Window
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.gui import PushButton

pyglet.resource.path = [ 'assets/images' ]
pyglet.resource.reindex()

class HelperButton(PushButton):
    """A button tied to a helper function."""

    def __init__(self, x, y, width, height, label="Button", helper=None, font_size=10, *args, **kwargs):
        self.pressed_img = pyglet.image.SolidColorImagePattern(
            color=(150, 150, 150, 220)
        ).create_image(width, height)
        self.depressed_img = pyglet.image.SolidColorImagePattern(
            color=(250, 250, 250, 220)
        ).create_image(width, height)

        super().__init__(x, y,
                         pressed=self.pressed_img,
                         depressed=self.depressed_img,
                         *args, **kwargs)

        self.helper = helper
        self.label = pyglet.text.Label(label,
                                       x=x + width // 2,
                                       y=y + height // 2,
                                       font_size=font_size,
                                       color=(10, 10, 10, 255),
                                       anchor_x='center',
                                       anchor_y='center',
                                       batch=self._batch,
                                       group=pyglet.graphics.Group(order=4))

    def on_press(self):
        #TODO: Remove this behaviout when there is actual helpers
        if not self.helper:
            print(f"Button '{self.label.text}' pressed but doesnt have any helper.")
        else:
            self.helper.do_action()


class TemperamentalMainGUI(Window):
    """Main window and GUI logic. Manages all events in the main window and
    controllers.

    Connects buttons to helpers to reuse functions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(1280, 800,
                         style=Window.WINDOW_STYLE_OVERLAY,
                         fullscreen=True,
                         *args, **kwargs
                        )
        self._setup_controller_manager()
        self.batch = Batch()
        self._setup_background()
        self._setup_buttons()

    def _setup_background(self):
        self.background = Sprite(
            pyglet.image.SolidColorImagePattern(color=(0, 0, 0, 200)).create_image(
                self.width, self.height
            ),
            batch=self.batch
        )

        #TODO: setup image according to detected gamepad
        pad_background = pyglet.resource.image("oxp-ctr.png")
        pad_background.anchor_x = pad_background.width // 2
        pad_background.anchor_y = pad_background.height // 2
        self.pad_sprite = Sprite(pad_background,
                                 x=self.width // 2,
                                 y=self.height // 2,
                                 batch=self.batch
                                )


    def _setup_buttons(self):
        self.frame = pyglet.gui.Frame(self)

        #TODO: Setup helpers for each button
        # ABXY PAD:
        self.tdp_button_a = HelperButton(self.width // 2 + 580,
                                         self.height // 2 + 30,
                                         100,
                                         40,
                                         font_size=15,
                                         label="TDP A",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_a)

        self.tdp_button_b = HelperButton(self.width // 2 + 580,
                                         self.height // 2 + 100,
                                         100,
                                         40,
                                         font_size=15,
                                         label="TDP B",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_b)

        self.tdp_button_x = HelperButton(self.width // 2 + 580,
                                         self.height // 2 - 48,
                                         100,
                                         40,
                                         font_size=15,
                                         label="TDP X",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_x)

        self.tdp_button_y = HelperButton(self.width // 2 + 580,
                                         self.height // 2 + 168,
                                         100,
                                         40,
                                         font_size=15,
                                         label="TDP Y",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_y)

        # D-PAD
        self.tdp_button_plus = HelperButton(self.width // 2 - 718,
                                         self.height // 2 - 118,
                                         100,
                                         40,
                                         font_size=15,
                                         label="TDP +",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_plus)

        self.tdp_button_minus = HelperButton(self.width // 2 - 718,
                                         self.height // 2 - 18,
                                         100,
                                         40,
                                         font_size=15,
                                         label="TDP -",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_minus)

        # Shoulder buttons
        self.tdp_button_LS = HelperButton(self.width // 2 - 570,
                                         self.height // 2 + 320,
                                         110,
                                         40,
                                         font_size=15,
                                         label="TDP LS",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_LS)

        self.tdp_button_RS = HelperButton(self.width // 2 + 440,
                                         self.height // 2 + 320,
                                         110,
                                         40,
                                         font_size=15,
                                         label="TDP RS",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_RS)

        # Trigger buttons
        self.tdp_button_LT = HelperButton(self.width // 2 - 282,
                                         self.height // 2 + 322,
                                         110,
                                         40,
                                         font_size=15,
                                         label="TDP LT",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_LT)

        self.tdp_button_RT = HelperButton(self.width // 2 + 152,
                                         self.height // 2 + 322,
                                         110,
                                         40,
                                         font_size=15,
                                         label="TDP RT",
                                         batch=self.batch
                                        )
        self.frame.add_widget(self.tdp_button_RT)



    def _setup_controller_manager(self):
        self.control_manager = pyglet.input.ControllerManager()
        self.control_manager.on_connect = self.on_controller_connect
        self.control_manager.on_disconnect = self.on_controller_disconnect

        for controller in self.control_manager.get_controllers():
            controller.open()
            controller.on_button_press = self.on_button_press

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_controller_connect(self, controller):
        print(f"Controller connected: {controller}")
        controller.open()
        controller.on_button_press = self.on_button_press

    def on_controller_disconnect(self, controller):
        print(f"Controller disconnected: {controller}")

    def on_button_press(self, controller, button_name):
        print(f"Pressed button: {button_name}")

    def perf_on_press(self):
        print("Pressed button in GUI")

