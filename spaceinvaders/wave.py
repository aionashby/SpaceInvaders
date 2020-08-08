"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Aion Ashby and Maxine Nzegwu NETIDs: aea99 and man227
4 December 2018
"""
from game2d import *
from consts import *
from models import *
import random


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _direction: Determination of whether the aliens will move to the right
        or left [bool]
        _amountaliens: Amount of aliens on the screen as the game runs
        [int >= 0]
        _step: Amount of steps taken by aliens [int >= 0]
        _score: The score the player has earned during the game [int >=0]
        _iscore: Score the player earned the previous game
        _showlives: The word 'Lives: ' followed by the number of lives left for
        the ship [GLabel]
        _aliens: A 2D list of Alien objects [list]
        _ship: A Ship object [instance of Ship]
        _dline: Defense line that the Ship is protecting [instance of GPath]
        _time: Time passed since update was last called
        _bolts: List of Bolt objects [list]
        _bolttime: A random time interval determining when the aliens
        shoot out their bolts [int >= 0 and <= BOLT_RATE]
        _lives: The lives the player has left [int >= 0 and <= 3]
        _speed: The speed of the game [float >= 0]
        _namescore: The word 'Score' on the upper left side
        of the screen [GLabel]
        _writescore: The score on the upper left side
        of the screen [GLabel]
        _showlives: The word 'Lives' on the upper right side of the of the
        screen followed by the amount of lives the player has left [GLabel]
    """
    def setspeed(self, speed):
        """
        Sets the speed of the aliens.

        Parameter Speed: The speed of the alien.
        Precondition: Is a float >= 0
        """
        self._speed = speed

    def getship(self):
        """
        Returns the ship.
        """
        return self._ship

    def setdrawship(self, view):
        """
        Creates a new ship object and draws it to the screen.

        Parameter View: view is a valid instance of GView
        Precondition: the game view, used in drawing
        """
        self._ship = Ship()
        self._ship.draw(view)

    def getdrawship(self, view):
        """
        Returns True if there is a ship on the screen.

        Allows app to access self._ship.

        Parameter View: view is a valid instance of GView
        Precondition: the game view, used in drawing
        """
        self.setdrawship(view)
        return True

    def getscore(self):
        """
        Returns the current score of the game.
        """
        return self._score

    def setlives(self,lives):
        """
        Sets the current lives of the ship.

        Parameter Lives: The number of lives the ship has.
        Precondition: Is an int between >= 0 and <= 3
        """
        self._lives = lives

    def setscore(self,score):
        """
        Sets score to the previous score.

        Parameter Score: The score of the game.
        Precondition: Is an int >= 0
        """
        self._score = score

    def getlives(self):
        """
        Returns the amount of lives the player has.
        """
        return self._lives

    def getcountaliens(self):
        """
        Returns the amount of aliens left on the screen.
        """
        return self._amountaliens

    def __init__(self,score = 0,lives = 3, speed = ALIEN_SPEED):
        """
        Initializes a new wave.

        Parameter Score: The score of the game.
        Precondition: Is an int >= 0

        Parameter Lives: The lives the player has.
        Precondition: Is an int >= 0 and <= 3

        Parameter Speed: The speed the aliens move at
        Precondition: Is a float >= 0
        """
        self._aliens = self._fill_alien()
        self._ship = Ship()
        self._dline = self._make_line()
        self._time = 0
        self._direction = True
        self._bolts = []
        self._bolttime = random.randint(0, BOLT_RATE)
        self._lives = lives
        self._amountaliens = ALIEN_ROWS*ALIENS_IN_ROW
        self._step = 0
        self._score = score
        self._iscore = score
        self._speed = speed
        self._namescore = GLabel(text = "Score: ", font_name = 'RetroGame.ttf',
            halign = 'left', valign = 'top', font_size = 35,
                linecolor = 'white', x = 90 , y = 675)
        self._writescore = GLabel(text = str(self._score), \
        font_name = 'RetroGame.ttf',
            halign = 'left', valign = 'top', font_size = 35,
                linecolor = 'white', x = 250, y = 675)
        self._showlives = GLabel(text = "Lives:  " + str(self._lives),
            font_name = 'RetroGame.ttf', halign = 'right', valign = 'top',
                font_size = 35,linecolor = 'white', x = 690, y = 675)

    def update(self,input,dt):
        """
        Animates a single frame of the game.

        Parameter input: The user input, used to control the ship and change
        state
        Precondition: input is an instance of GInput that is inherited from
        GameApp

        Paraemeter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._ship_right(input)
        self._ship_left(input)
        self._shoot_bolt(input)
        if self._step == self._bolttime:
            self.column = random.randint(0,ALIENS_IN_ROW-1)
            if self._lowest(self.column) is not None:
                self._bolttime = random.randint(1, BOLT_RATE)
                self._bolts.append(Bolt(self._lowest(self.column).x, \
                self._lowest(self.column).y, -BOLT_SPEED))
                self._step = 0
        self._move_bolt()
        self._hit()
        self._shiphit()
        self.getcountaliens()
        self._bottommost()
        self._scorekeeper()
        self.getlives()
        self.getscore()
        if self._time < self._speed:
            self._time = self._time + dt
        if self._time > self._speed and self._direction == True:
            self._move_right()
            self._step +=1
        if self._time > self._speed and self._direction == False:
            self._move_left()
            self._step +=1
        self._delete_bolt()

    def _fill_alien(self):
        """
        Returns a 2D list of alien objects with ALIEN_ROWS row and
        ALIENS_IN_ROW columns

        Each row alternates aliens every two columns, and the aliens are
        ALIEN_H_SEP away from each other horizontally and ALIEN_V_SEP away
        from each other vertically. The list of aliens begin ALIEN_CEILING
        away from the top of the game window.
        """
        finalrow = []
        counter = ALIEN_ROWS
        x = ALIEN_H_SEP
        y = GAME_HEIGHT - ALIEN_CEILING
        for rows in range(ALIEN_ROWS):
            row = []
            x = 0
            for alien in range(ALIENS_IN_ROW):
                x = x + ALIEN_WIDTH + ALIEN_H_SEP
                if counter % 6 == 0 or counter % 6 == 1:
                    row.append(Alien(x,y,source = 'alien2.png'))
                elif counter % 6 == 2 or counter % 6 == 3:
                    row.append(Alien(x,y,source = 'alien1.png'))
                elif counter % 6 == 4 or counter % 6 == 5:
                    row.append(Alien(x,y,source = 'alien3.png'))
            y = y - ALIEN_V_SEP - ALIEN_HEIGHT
            counter = counter + 1
            finalrow.append(row)
        return finalrow

    def _hit(self):
        """
        Registers when an alien is hit with a player bolt

        If the alien is hit with a player bolt the alien disappears and the bolt
        is deleted. Then self._amountaliens is decreased by 1.
        """
        for row in range(len(self._aliens)):
            for y in range(len(self._aliens[0])):
                for x in range(len(self._bolts)):
                    if self._aliens[row][y] is not None:
                        if self._aliens[row][y].collides(self._bolts[x]):
                            if self._isPlayerBolt(x):
                                self._aliens[row][y] = None
                                del self._bolts[x]
                                self._amountaliens -= 1
                                self._score = self._scorekeeper()
                                self._writescore = GLabel(\
                                text = str(self._score), \
                                font_name = 'RetroGame.ttf',\
                                font_size = 35,linecolor = 'red', \
                                x = 250, y = 675)

    def _make_line(self):
        """
        Returns a new GPath object that creates a defense line.
        """
        return GPath(points = [0,DEFENSE_LINE,800,DEFENSE_LINE],
            linewidth = 2, linecolor = 'white')

    def draw(self, view):
        """
        Draws the game objects in the invaders class on to the screen

        Parameter view: the game view used in drawing
        Precondition: view is an instance of GView that is inherited from
        GAMEAPP
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)

        if self._ship is not None:
            self._ship.draw(view)
        self._dline.draw(view)

        for x in self._bolts:
            x.draw(view)

        if self._score is not None:
            self._namescore.draw(view)
            self._writescore.draw(view)

        if self._showlives is not None:
            self._showlives.draw(view)

    def _shiphit(self):
        """
        Checks to see if the ship has been hit.

        The ship is set to none and disappears from the screen. The lives
        decrease by 1, which displays on the screen.
        """
        for x in range(len(self._bolts)):
            if self._ship is not None:
                if self._ship.pbolt_collides(self._bolts[x]):
                    if self._isAlienBolt(x):
                        del self._bolts[x]
                        self._lives -= 1
                        self._showlives = GLabel(
                            text = "Lives:  " + str(self._lives),
                                font_name = 'RetroGame.ttf', halign = 'right',
                                    valign = 'top', font_size = 35,
                                        linecolor = 'white', x = 690, y = 675)
                        self._ship = None

    def _lowest(self, column):
        """
        Returns the last index in the acc list, which contains the lowest alien
        in a column.

        Finds the lowest alien in each column. Goes through each column and
        finds the lowest alien in the column, as long as the alien is not None

        Parameter column: The column being checked for lowest alien
        Precondition: An int between 0 and ALIENS_IN_ROW-1
        """
        acc = []
        for x in range(ALIEN_ROWS):
            if self._aliens[x][column] is not None:
                acc.append(self._aliens[x][column])
        if len(acc)!=0:
            return acc[len(acc)-1]

    def _PlayerBolt(self):
        """
        Returns True if a player bolt is currently on the screen, and
        returns False otherwise.
        """
        bolts = []
        for bolt in self._bolts:
            if bolt.getVelocity() > 0:
                bolts.append(True)
            else:
                bolts.append(False)
        if True in bolts:
            return True
        else:
            return False

    def _isPlayerBolt(self,bolt):
        """
        Returns True if the bolt is a player bolt.

        Checks to see if the bolt was shot by the ship. If the bolt has a
        positive velocity, the bolt is a ship bolt and returns True.

        Parameter bolt: the position of the bolt
        Precondition: bolt is an int within the range 0 to len(self._bolts-1)
        and the int is >= 0.
        """
        if self._bolts[bolt].getVelocity() > 0:
            return True

    def _isAlienBolt(self,bolt):
        """
        Returns True if the bolt was shot by an alien

        If the bolt has a neative velocity, the bolt is an alien bolt
        and returns True

        Parameter bolt: the position of the bolt
        Precondition: bolt is an int within the range 0 to len(self._bolts-1)
        """
        if self._bolts[bolt].getVelocity() < 0:
            return True

    def _move_bolt(self):
        """
        Moves the bolts by increments of the velocity
        """
        for bolt in self._bolts:
            bolt.move()

    def _delete_bolt(self):
        """
        Deletes the bolt when it goes off screen
        """
        toofar = []
        for x in range(len(self._bolts)):
            if self._bolts[x].y > GAME_HEIGHT:
                toofar.append(x)
        for y in toofar:
            del self._bolts[y]

    def _move_right(self):
        """
        Moves the aliens to the right

        The aliens move to the right by incraments of ALIEN_H_WALK until
        they reach the edge of the screen, in which case they will move
        down ALIEN_V_SEP distance.
        """
        right = self._right_most()
        if right is not None:
            if right > GAME_WIDTH - ALIEN_WIDTH:
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.y = alien.y - ALIEN_V_SEP
                            self._direction = False
            else:
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.x = alien.x + ALIEN_H_WALK
            self._time = 0

    def _move_left(self):
        """
        Moves the aliens to the left

        The aliens move to the left by incraments of ALIEN_H_WALK until they
        reach the edge of the screen, in which case they will move down
        ALIEN_V_SEP distance.
        """
        left = self._left_most()
        if left is not None:
            if left < 0 + ALIEN_WIDTH:
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.y = alien.y - ALIEN_V_SEP
                            self._direction = True
            else:
                for row in self._aliens:
                    for alien in row:
                        if alien is not None:
                            alien.x = alien.x - ALIEN_H_WALK
            self._time = 0

    def _right_most(self):
        """
        Returns the biggest x value of an alien.

        Finds the right most alien on the screen.
        """
        temp = []
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    temp.append(alien.x)
        if temp != []:
            return max(temp)

    def _left_most(self):
        """
        Returns the smallest x value of an alien.

        Finds the left most alien on the screen.
        """
        temp = []
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    temp.append(alien.x)
        if temp != []:
            return min(temp)

    def _ship_right(self,input):
        """
        Moves the ship to the right when the 'right' arrow key is pressed.

        Increments the x position of the ship by SHIP_MOVEMENT

        Parameter Input: The user input, used to control the ship and change
        state
        Precondition: Is an instance of GInput; it is inherited from GameApp
        """
        if self._ship is not None:
            if input.is_key_down('right') and self._ship.x < GAME_WIDTH - \
            SHIP_WIDTH/2:
                self._ship.x = self._ship.x + SHIP_MOVEMENT

    def _ship_left(self,input):
        """
        Moves the ship to the left when the 'left' arrow key is pressed.

        Increments the x position of the ship by -SHIP_MOVEMENT

        Parameter Input: The user input, used to control the ship and change
        state
        Precondition: Is an instance of GInput; it is inherited from GameApp
        """
        if self._ship is not None:
            if input.is_key_down('left') and self._ship.x > 0 + \
            SHIP_WIDTH/2:
                self._ship.x = self._ship.x - SHIP_MOVEMENT

    def _shoot_bolt(self,input):
        """
        Shoots a bolt from the ship when the spacebar is pressed.

        Verifies that the bolt was not a playerbolt and shoots a bolt from the
        top of the ship.

        Parameter Input: The user input, used to control the ship and change
        state
        Precondition: Is an instance of GInput; it is inherited from GameApp
        """
        if input.is_key_down('spacebar'):
            if self._PlayerBolt() == False:
                self._bolts.append(Bolt(self._ship.x, self._ship.y + \
                (SHIP_HEIGHT/2), BOLT_SPEED))

    def _scorekeeper(self):
        """
        Returns a score to the alien hit based on the row the alien is in.

        The topmost row of aliens have values of 15. The middle rows have values
        of 10. The bottommost rows have values of 5. If the game only has one
        row, the aliens have values of 5. If the game has two rows of aliens,
        the bottom row has a value of 5 and the top row has a value of 15.
        """
        score = self._iscore
        newlist = []
        for row in range(len(self._aliens)):
            newlist.append(row)
        for row in range(len(self._aliens)):
            for y in range(len(self._aliens[0])):
                if self._aliens[row][y] is None:
                    high = max(newlist)
                    low = min(newlist)
                    if row == high and self._aliens[row][y] is None:
                        score = score + 5
                    elif row == 0 and self._aliens[row][y] is None:
                        score = score + 15
                    else:
                        score = score + 10
        return score

    def _hitline(self):
        """
        Returns True if the position of the bottommost alien is below the
        defense line.
        """
        hitline = self._bottommost()
        if hitline is not None:
            if hitline < DEFENSE_LINE + (ALIEN_HEIGHT-15):
                return True

    def _bottommost(self):
        """
        Returns the smallest y value of an alien.

        Finds the bottomost alien on the screen.
        """
        temp = []
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    temp.append(alien.y)
        if temp != []:
            return min(temp)








    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS

    # HELPER METHODS FOR COLLISION DETECTION
