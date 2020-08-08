"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

Aion Ashby and Maxine Nzegwu NETIDs: aea99 and man227
4 December 2018
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _background: Background color of the game [GRectangle]
    _accumulate: Integer to divide by to speed up the game for multiple waves
    [int > 0]
    _roundlives: Lives left in the round [int >= 0 and <=3]
    _roundscore: Score of the game [int >=0]
    """
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._background = GRectangle(x = 400, y = 350, width = GAME_WIDTH, \
        height = GAME_HEIGHT, fillcolor = 'black')
        self._state = STATE_INACTIVE
        if self._state == STATE_INACTIVE:
            self._wave = None
            self._text = GLabel(text = "Press 'P' to Play" ,
                font_name = 'RetroGame.ttf', halign = 'center',
                    valign = 'middle', font_size = 65, linecolor = 'white',
                        x=400,y=350)
        else:
            self._text = None
            self._wave = Wave(self.input)

        self._accumulate = 1

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        curr_keys = self.input.is_key_down('p')
        numkeys = self.input.key_count

        if curr_keys == True and numkeys >= 1:
            self._state = STATE_NEWWAVE
            score = 0
            lives = 3
            speed = ALIEN_SPEED
            if self._wave is not None:
                score = self._wave.getscore()
                lives = self._wave.getlives()
                self._wave.setlives(lives)
                self._wave.setscore(score)
            self._wave = Wave(score,lives,speed)
            self._state = STATE_ACTIVE
            self._text = None

        if self._state == STATE_ACTIVE:
            self._wave.update(self.input,dt)

        self._hitship()
        self._liveslost()
        self._barrierline()
        self._winner()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        self._background.draw(self.view)

        if self._text is not None:
            self._text.draw(self.view)
        if self._wave is not None:
            self._wave.draw(self.view)

        if self._state == STATE_CONTINUE:
            if self._wave is not None:
                self._wave.getdrawship(self.view)

    def _hitship(self):
        """
        Determines if the ship disappears from the screen

        If the ship is hit self._state is changed to STATE_PAUSED and a text
        screen pops up asking the player to 'Press S to Continue'. If the player
        presses 's', self._state is changed to STATE_CONTINUE and then there is
        a check to make sure that there is a ship on the screen. The text
        disappears and there is a check to see that the ship/player still
        has lives left.
        """
        if self._wave is not None:
            if self._wave.getship() is None:
                self._state = STATE_PAUSED
                self._text = GLabel(text = "Press S to continue" ,
                    font_name = 'RetroGame.ttf', halign = 'center',
                        valign = 'middle', font_size = 35, linecolor = 'white',
                            x=400,y=350)
                if self.input.is_key_down('s'):
                    self._state = STATE_CONTINUE

                if self._state == STATE_CONTINUE and \
                self._wave.getdrawship(self.view) == True:
                    self._text = None
                    if self._wave.getlives() > 0:
                        self._state = STATE_ACTIVE

    def _liveslost(self):
        """
        Determines if all the lives of the ship are lost

        If all the lives of the ship are lost the self._state changes to
        STATE_COMPLETE and "YOU LOST" text displays on the screen
        """
        if self._wave is not None:
            if self._wave.getlives() == 0:
                self._state = STATE_COMPLETE
                self._text = GLabel(text = "YOU LOST" ,
                    font_name = 'RetroGame.ttf', halign = 'center',
                        valign = 'middle', font_size = 35,linecolor = 'white',
                            x=400,y=350)

    def _barrierline(self):
        """
        Determines if an alien or aliens have past the defense line

        If an alien or aliens has passed the defense line, the player/ship has
        lost the game and self._state is changed to STATE_COMPLETE and a
        "YOU LOST" text is displayed on screen.
        """
        if self._wave is not None:
            if self._wave._hitline():
                self._state = STATE_COMPLETE
                self._text = GLabel(text = "YOU LOST" ,
                    font_name = 'RetroGame.ttf', halign = 'center',
                        valign = 'middle', font_size = 35, linecolor = 'white',
                            x=400,y=350)

    def _winner(self):
        """
        Determines if all the aliens are no longer on the screen.

        If all the aliens are off the screen then the ship/player has won the
        game. Self._state is changed to complete and a "YOU WIN" text is
        displayed also asking if the player would like to play again(player is
        to select 'A' if they do). If the player selects 'A' then the self._text
        becomes none and a new wave of aliens appear on screen.
        """
        if self._wave is not None:
            if self._wave.getcountaliens() == 0:
                self._roundlives = self._wave.getlives()
                self._roundscore = self._wave.getscore()
                self._state = STATE_COMPLETE
                self._text = GLabel(text = "YOU WIN! Click A to play again!" ,
                    font_name = 'RetroGame.ttf', halign = 'center',
                        valign = 'middle', font_size = 35,linecolor = 'white',
                            x=400,y=350)
                if self.input.is_key_down('a'):
                    self._accumulate *= 2
                    self._text = None
                    lives = self._wave.getlives()
                    score = self._wave.getscore()
                    speed = ALIEN_SPEED/(self._accumulate)
                    self._wave = Wave(score = score, lives = lives, \
                    speed = speed)
                    self._wave.setlives(lives)
                    self._wave.setscore(score)
                    self._wave.setspeed(speed)
                    self._state = STATE_ACTIVE
    # HELPER METHODS FOR THE STATES GO HERE
