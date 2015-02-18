from browser import window
from browser.timer import set_interval


FPS = 60

debug = window.console.log
jq = window.jQuery


class Game(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.direction = (4, 2)

        self.paddle1 = Paddle(id=1)
        self.paddle2 = Paddle(id=2)
        self.ball = Ball()

        self.width -= self.ball.width + self.paddle1.width + self.paddle2.width
        self.height -= self.ball.height

        self._things = {
            "paddle1": self.paddle1,
            "paddle2": self.paddle2,
            "ball": self.ball,
        }

    def _collides_x(self):
        x = self.ball.x
        return x < 0 or x > self.width

    def _collides_y(self):
        y = self.ball.y
        return y < 0 or y > self.height

    def step(self):
        if self._collides_x():
            self.direction[0] *= -1

        if self._collides_y():
            self.direction[1] *= -1

        x, y = self.direction

        self.ball.x += x
        self.ball.y += y

    def render(self):
        jq("body").css({'margin': self.ball.width})
        for thing in self._things.values():
            thing.render()


class Paddle(object):

    def __init__(self, width=32, height=160, y=0, id=None):
        assert id is not None

        self.width = width
        self.height = height
        self.y = y
        self.id = id

    def _get_selector(self):
        return "#paddle{}".format(self.id)

    def render(self):
        jq(self._get_selector()).css({
            "top": self.y,
            "width": self.width,
            "height": self.height,
        })


class Ball(object):

    def __init__(self, width=32, height=32, x=0, y=0):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def render(self):
        jq("#ball").css({
            "width": self.width,
            "height": self.height,
            "left": self.x - (self.width / 2),
            "top": self.y - (self.height / 2),
        })


def step(game):
    game.step()
    game.render()


def main():
    jq_window = jq(window)
    width = jq_window.width()
    height = jq_window.height()

    game = Game(width, height)
    set_interval(lambda: step(game), 1000 / float(FPS))


if __name__ == "__main__":
    main()
