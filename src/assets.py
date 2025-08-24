"""ASCII assets for the Hangman game.

This module provides the Asset class which stores the ASCII gallows art for
each life state and emoticon strings used for end-game screen
"""


class Assets:
    """Container for ASCII art and emoticons used in the UI"""

    def __init__(self) -> None:
        self.gallows = [
            [
                "*---*   ",
                "|   |   ",
                "|   O   ",
                "|  \\|/  ",
                "|   |   ",
                "|  / \\  ",
            ],
            [
                "*---*   ",
                "|   |   ",
                "|   O   ",
                "|  \\|/  ",
                "|   |   ",
                "|    \\  ",
            ],
            [
                "*---*   ",
                "|   |   ",
                "|   O   ",
                "|  \\|/  ",
                "|   |   ",
                "|       ",
            ],
            [
                "*---*   ",
                "|   |   ",
                "|   O   ",
                "|   |/  ",
                "|   |   ",
                "|       ",
            ],
            [
                "*---*   ",
                "|   |   ",
                "|   O   ",
                "|   |   ",
                "|   |   ",
                "|       ",
            ],
            [
                "*---*   ",
                "|   |   ",
                "|   O   ",
                "|       ",
                "|       ",
                "|       ",
            ],
            [
                "*---*   ",
                "|   |   ",
                "|       ",
                "|       ",
                "|       ",
                "|       ",
            ],
        ]

        self.sad = "(づ•́ ᵔ •̀)づ"
        self.happy = "✺◟(＾∇＾)◞✺"

    def get_gallows(self, life: int) -> list[str]:
        """Returns the gallow frame for the given life count.

        Parameters:
            - life: int
                Current life count

        Returns:
            - list[str]
                List of strings representing the ASCII art
        """
        # to make sure idx < 7
        idx = max(0, min(6, life - 1))
        return self.gallows[idx]

    def get_emoticon(self, won: bool) -> str:
        """Return the emoticon for a win or loss screen

        Parameters:
            - won : bool
                True -> won -> show 'happy'
                False -> did not win -> show 'sad'

        Returns:
            - str
                The emoticon string, either happy or sad
        """
        return self.happy if won else self.sad
