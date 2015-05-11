from browser import timer
from browser import window


def log(*xs):
    return window.console.log(*map(str, xs))

jq = window.jQuery

FPS = 60
PADDLE_MOVESPEED = 40

KEYCODE_W = 87
KEYCODE_S = 83
KEYCODE_UP = 38
KEYCODE_DOWN = 40


class Game(object):

    def __init__(self, window_width, window_height):
        self.dead = False
        self.score = (0, 0)

        self.direction = (4, 6)

        self.canvasContext = self._create_canvas()

        self.paddle1 = Paddle(self.canvasContext, self, id=1)
        self.paddle2 = Paddle(self.canvasContext, self, id=2)

        self._things = {
            "paddle1": self.paddle1,
            "paddle2": self.paddle2,
        }

        self.ball_width = 32
        self.ball_height = 32

        self.width = window_width - self.ball_width * 3
        self.height = window_height - self.ball_height

        self._throw_ball()

        self._init_events()

    def _throw_ball(self):
        self.ball = Ball(
            self.canvasContext,
            self.width / 2, self.height / 2,
            self.ball_width, self.ball_height,
        )
        self._things["ball"] = self.ball

    def _onKeyDown(self, event):
        kc = event.keyCode

        paddles_to_keycodes = {
            self.paddle1: (KEYCODE_W, KEYCODE_S, ),
            self.paddle2: (KEYCODE_UP, KEYCODE_DOWN, ),
        }

        for paddle, (kc_up, kc_down) in paddles_to_keycodes.items():
            if kc == kc_up:
                paddle.moveTop()
            elif kc == kc_down:
                paddle.moveBottom()

    def _init_events(self):
        jq(window).keydown(self._onKeyDown)

    def _collides_x(self):
        x = self.ball.x
        return x < 0 or x > self.width

    def _collides_y(self):
        y = self.ball.y
        return y < 0 or y > self.height

    def _get_closest_paddle(self, x):
        if x > self.width / 2:
            return self.paddle2
        else:
            return self.paddle1

    def _die(self, loser_paddle):
        loser_id = loser_paddle.id - 1
        winner_id = loser_id ^ 1
        self.score[winner_id] += 1

        self._throw_ball()

    def step(self):
        if not self.dead and self._collides_x():
            paddle = self._get_closest_paddle(self.ball.x)
            if paddle.collides(self.ball):
                self.direction[0] *= -1
            else:
                self._die(paddle)

        if not self.dead and self._collides_y():
            self.direction[1] *= -1

        x, y = self.direction

        self.ball.x += x
        self.ball.y += y

    def _create_canvas(self):
        return window.document.getElementById("canvas").getContext("2d")

    def render(self):
        self.canvasContext.canvas.width = window.innerWidth
        self.canvasContext.canvas.height = window.innerHeight

        for thing in self._things.values():
            thing.render()

        jq("title").text("Pong ({}:{})".format(*self.score))


class Paddle(object):

    def __str__(self):
        return "<Paddle: {}>".format(self.id)

    def __init__(self, canvasContext, game, width=32, height=160, y=0, id=None):
        assert id is not None

        self.canvasContext = canvasContext
        self.game = game
        self.width = width
        self.height = height
        self.y = y
        self.id = id
        self.side = "left" if self.id == 1 else 'right'

    def render(self):
        self.canvasContext.fillStyle = "pink"
        if self.side == "right":
            x = self.game.width + (self.width * 2)
        else:
            x = 0
        self.canvasContext.fillRect(x, self.y, self.width, self.height)

    def moveTop(self):
        self.y -= PADDLE_MOVESPEED
        self.y = max(self.y, 0 - self.game.ball.height / 2)

    def moveBottom(self):
        self.y += PADDLE_MOVESPEED
        self.y = min(
            self.y, self.game.height -
            self.height + self.game.ball.height / 2
        )

    def collides(self, ball):
        return abs(ball.y - (self.y + self.height / 2)) < self.height / 2


class Ball(object):

    def __init__(self, canvasContext, x=0, y=0, width=32, height=32):
        self.canvasContext = canvasContext
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self):
        self.canvasContext.fillStyle = "blue"
        self.canvasContext.fillRect(self.x, self.y, self.width, self.height)

def step(game):
    game.step()
    game.render()


def main():
    jq_window = jq(window)
    width = jq_window.width()
    height = jq_window.height()

    game = Game(width, height)
    timer.set_interval(lambda: step(game), 1000 / float(FPS))

main()
