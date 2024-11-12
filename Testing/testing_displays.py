import unittest
from unittest.mock import patch, MagicMock
import pygame

from Values import Settings as S
from static.data.play_data import gifs
from static.data.play_data.decor import Decorations as decorations
from utils import Imports as I

def find_image_on_screen(screen, image):
    """
    Search for the specified image on the screen.

    Parameters:
        screen (pygame.Surface): The surface representing the screen.
        image (pygame.Surface): The surface representing the image to find.

    Returns:
        tuple: The (x, y) coordinates of the top-left corner of the found image, or None if not found.
    """
    screen_array = pygame.surfarray.array3d(screen)
    image_array = pygame.surfarray.array3d(image)

    # Get dimensions
    screen_height, screen_width, _ = screen_array.shape
    image_height, image_width, _ = image_array.shape

    # Check boundaries to prevent out-of-bounds access
    if image_height > screen_height or image_width > screen_width:
        return None

    # Convert image arrays to uint8 for better performance
    image_array = image_array.astype(I.np.uint8)

    # Iterate over the screen using a sliding window approach
    for y in range(screen_height - image_height + 1):
        for x in range(screen_width - image_width + 1):
            # Extract the region of the screen that matches the size of the image
            region = screen_array[y:y + image_height, x:x + image_width]

            # Use element-wise comparison
            if I.np.array_equal(region, image_array):
                return (y, x)  # Return the top-left corner of the found image

    return None  # Return None if the image is not found

class TestRenderGifs(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((S.SCREEN_WIDTH, S.SCREEN_HEIGHT))  # sets screen mode

        self.decorations = decorations()  # Empty environment initially
        self.gifs = gifs.read_db(self.decorations)

    def tearDown(self):
        pass

    def test_render_levelup(self):
        # Import the function to be tested after patching
        from Render.Background_Render import render_levelup
        # Start the gif
        self.gifs["Level up"].Start_gif("Level up", [S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 20, S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 20 * 2, S.SCREEN_WIDTH / 14, S.SCREEN_HEIGHT / 7])

        # Call the function
        frame1 = render_levelup(self.gifs, self.screen)
        expected_location = (int(S.SCREEN_WIDTH / 2 - S.SCREEN_WIDTH / 10 + I.info.OFFSCREEN[0]), int(S.SCREEN_HEIGHT / 2 - S.SCREEN_HEIGHT / 10 * 2 + I.info.OFFSCREEN[1]))

        # Check if blit was called correctly
        image_location = find_image_on_screen(self.screen, frame1)
        self.assertEqual(image_location, expected_location)


    # def test_display_strikes(self):
    #     from Render.Background_Render import display_strikes
    #
    #     self.gifs["Slashing Strike"].Start_gif("Slashing Strike", 1)
    #     frame = display_strikes(self.screen, self.gifs, 0)
    #     I.T.pause_pygame()
    #     print(frame)
    #     image_location = find_image_on_screen(self.screen, frame)
    #     expected_location = (560 + I.info.OFFSCREEN[0], 340 + I.info.OFFSCREEN[1], 0, 1, 100, 50)
    #     self.assertEqual(image_location, expected_location)



if __name__ == '__main__':
    unittest.main()
