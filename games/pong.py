import pygame
import pygame.locals
import time

from pygame import surface


class Board(object):
    """
    Plansza do gry. Odpowiada za rysowanie okna gry.
    """

    def __init__(self, width, height):
        """
        Konstruktor planszy do gry. Przygotowuje okienko gry.

        :param width:
        :param height:
        """
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption('Simple Pong')

    def draw(self, *args):
        """
        Rysuje okno gry

        :param args: lista obiektów do narysowania
        """
        background = (230, 255, 255)
        self.surface.fill(background)
        for drawable in args:
            drawable.draw_on(self.surface)

        # dopiero w tym miejscu następuje fatyczne rysowanie
        # w oknie gry, wcześniej tylko ustalaliśmy co i jak ma zostać narysowane
        pygame.display.update()


class PongGame(object):
    """
    Łączy wszystkie elementy gry w całość.
    """

    def __init__(self, width, height):
        pygame.init()
        self.board = Board(width, height)
        # zegar którego użyjemy do kontrolowania szybkości rysowania
        # kolejnych klatek gry
        self.fps_clock = pygame.time.Clock()
        self.ball = Ball(20, 20, width / 2, height / 2)

    def run(self):
        """
            Główna pętla programu
        """
        while not self.handle_events():
            # działaj w pętli do momentu otrzymania sygnału do wyjścia
            # zegar którego użyjemy do kontrolowania szybkości rysowania
            # kolejnych klatek gry
            self.ball.move(self.board)
            self.board.draw(
                self.ball,
            )
            self.fps_clock.tick(30)

    def handle_events(self):
        """
        Obsługa zdarzeń systemowych, tutaj zinterpretujemy np. ruchy myszką

        :return True jeżeli pygame przekazał zdarzenie wyjścia z gry
        """
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True


# Ta część powinna być zawsze na końcu modułu (ten plik jest modułem)
# chcemy uruchomić naszą grę dopiero po tym jak wszystkie klasy zostaną zadeklarowane

class Drawable(object):
    """
    Klasa bazowa dla rysowanych obiektów
    """

    def __init__(self, width, height, x, y, color=(0, 255, 0)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface([width, height], pygame.SRCALPHA, 32).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)


class Ball(Drawable):
    """
    Piłeczka, sama kontroluje swoją prędkość i kierunek poruszania się.
    """

    def __init__(self, width, height, x, y, color=(255, 0, 0), x_speed=3, y_speed=3):
        super(Ball, self).__init__(width, height, x, y, color)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.start_x = x
        self.start_y = y

    def bounce_y(self):
        """
        Odwraca wektor prędkości w osi Y
        """
        self.y_speed *= -1

    def bounce_x(self):
        """
        Odwraca wektor prędkości w osi X
        """
        self.x_speed *= -1

    def reset(self):
        """
        Ustawia piłeczkę w położeniu początkowym i odwraca wektor prędkości w osi Y
        """
        self.rect.move(self.start_x, self.start_y)
        self.bounce_y()

    def move(self, board, *args):
        """
        Przesuwa piłeczkę o wektor prędkości
        """
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.x < 0 or self.rect.x > board.surface.get_width():
            self.bounce_x()

        if self.rect.x < 0 or self.rect.y > board.surface.get_height():
            self.bounce_y()

        for racket in args:
            if self.rect.colliderect(racket.rect):
                self.bounce_y()


class Racket(Drawable):
    """
        Rakietka, porusza się w osi X z ograniczeniem prędkości.
    """

    def __init__(self, width, height, x, y, color=(0, 255, 0), max_speed=10):
        super().__init__(width, height, x, y, color)
        self.max_speed = max_speed
        self.surface.fill(color)

    def move(self, x):
        """
            Przesuwa rakietkę w wyznaczone miejsce.
        """
        delta = x - self.rect.x
        if abs(delta) > self.max_speed:
            delta = self.max_speed if delta > 0 else -self.max_speed
        self.rect.x += delta

        




if __name__ == '__main__':
    board = Board(800, 400)
    board.draw()
    time.sleep(5)
    game = PongGame(800, 400)
    game.run()
