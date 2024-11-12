import unittest
from unittest.mock import patch

import pygame  # Assuming we use pygame Rect objects

from Backend.Play import walking, hit_by_mob_walking  # Example imports
from static.data.play_data.decor import Decorations as decorations
from utils import Imports as I
from Values import Settings as S
from Backend.Play import keypress_handle

class TestWalkingFunction(unittest.TestCase):

    def setUp(self):
        # Set up initial test environment
        # I.pg.init()
        pygame.display.init()  # Initialize the display to prevent freezing
        pygame.display.set_mode((1, 1), pygame.NOFRAME)  # Create a tiny window, no need for display
        pygame.key.set_repeat(1, 1)  # Make sure keys work quickly in the test environment

        I.info.ENTRY_POS = (180, 370)
        self.rooms = I.rooms.Room()
        self.rooms.select_room("Village_10_10")
        I.info.CURRENT_ROOM = {"name": "Village_10_10", "Spells": True, "Backpack": True, "Running": True,"Mobs": self.rooms.mobs, "Type": self.rooms.type}
        self.data = {}
        self.data["Window size"] = (S.SCREEN_WIDTH, S.SCREEN_HEIGHT)  # Defines the size of the window (The rest is black)
        self.data["Zoom"] = (S.SCREEN_WIDTH / 4, S.SCREEN_HEIGHT / 4)  # Defines how zoomed in to the picture the view is
        if self.rooms.type == "Village":
            values = self.rooms.name.split("_")
            self.data["Zoom"] = (S.SCREEN_WIDTH / 4, S.SCREEN_HEIGHT / 4)  # Defines how zoomed in to the picture the view is
            root_dir = I.os.path.dirname(I.os.path.dirname(I.os.path.abspath(__file__)))  # Adjust if necessary
            self.data["Image"] = I.pg.image.load(root_dir + "/" + S.DECOR_PATH[self.rooms.background + "_" + values[1] + "_" + values[2]]).convert_alpha()  # uploads the background image with transparent convert
        else:
            self.data["Zoom"] = (S.SCREEN_WIDTH / 15, S.SCREEN_HEIGHT / 15)  # Defines how zoomed in to the picture the view is
            self.data["Image"] = I.pg.image.load(S.DECOR_PATH[self.rooms.background]).convert_alpha()  # uploads the background image with transparent convert

        self.data["Image_rect"] = self.data["Image"].get_rect()  # Gets the rect of image
        self.data["Zoom_rect"] = I.pg.Rect(I.info.ENTRY_POS[0], I.info.ENTRY_POS[1], *self.data["Zoom"])  # creates a rect based on zoomed in picture (basicly makes a window)
        self.data["Player"] = {"health": 100, "mana": 50, "dead": False}

        I.info.OFFSCREEN = [0, 0]  # No offscreen movement initially
        I.info.FAST = 1  # Regular walking speed
        self.decorations = decorations()  # Empty environment initially

    def test_basic_movement(self):
        """Test walking in all directions without any collisions."""
        collide = [False]

        dx, dy = 1, 0  # Walk right
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 181)  # 1 pixel movement
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # No vertical movement


        dx, dy = -1, 0 # Test walking left
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)  # Back to initial position
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # No vertical movement

        dx, dy = 0, 1 # Test walking down
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)  # No horizontal movement
        self.assertEqual(self.data["Zoom_rect"].y, 371)  # 1 pixel movement

        dx, dy = 0, -1 # Test walking up
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)  # No horizontal movement
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # Back to initial position


        dx, dy = 1, 1 # Test walking diagonally down-right
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 181)
        self.assertEqual(self.data["Zoom_rect"].y, 371)

        dx, dy = 1, -1 # Test walking diagonally up-right
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 182)
        self.assertEqual(self.data["Zoom_rect"].y, 370)

        dx, dy = -1, 1 # Test walking diagonally down-left
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 181)
        self.assertEqual(self.data["Zoom_rect"].y, 371)

        dx, dy = -1, -1 # Test walking diagonally up-left
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)
        self.assertEqual(self.data["Zoom_rect"].y, 370)

    def test_collisions(self):
        """Test collisions with decorations blocking movement."""
        # Create a mock decoration rect to block the right
        decoration_rect = pygame.Rect(160, 60, 10, 23)
        right_rect = I.pg.Rect(159 + I.info.OFFSCREEN[0] / 4, 82 + I.info.OFFSCREEN[1] / 4, S.SCREEN_WIDTH / 400, S.SCREEN_HEIGHT / 150)
        self.decorations.displayed_rects.append(decoration_rect)
        collide = ["Tree_M_1", decoration_rect, 0]

        # Attempt to move right into the decoration
        dx, dy = 1, 0
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)  # No movement due to collision
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # No vertical movement
        self.assertEqual(right_rect.collidelist(self.decorations.displayed_rects), 0)  # collision

        # Attempt to move left
        dx, dy = -1, 0
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 179)  # one pixel movement
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # No vertical movement

        # Check that movement in other directions is still possible
        dx, dy = 0, 1  # Move down
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 179)  # No horizontal movement
        self.assertEqual(self.data["Zoom_rect"].y, 371)  # Successful downward movement

        # Check that movement in other directions is still possible
        dx, dy = 0, -1  # Move up
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 179)  # No horizontal movement
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # Successful upward movement

        dx, dy = 1, 1  # Move right-down into collision
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 179)  # No movement due to collision
        self.assertEqual(self.data["Zoom_rect"].y, 371)  # Successful downward movement

        dx, dy = 1, -1  # Move right-up into collision
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 179)  # No movement due to collision
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # Successful upward movement


        self.decorations.displayed_rects = []

    def test_hit_by_mob(self):
        """Test knockback when hit by an aggressive mob."""
        collide = ["mob_collide", {"current_pos": pygame.Rect(150, 100, 50, 50)}]

        # Simulate player getting hit by the mob from the right

        initial_position = self.data["Zoom_rect"].x
        hit_by_mob_walking(self.data, collide)
        self.assertNotEqual(self.data["Zoom_rect"].x, initial_position)


    def test_running(self):
        """Test running (faster movement) when I.info.FAST is 2."""
        I.info.FAST = 2  # Running speed
        collide = [False]

        dx, dy = 1, 0  # Walk right
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 182)  # 1 pixel movement
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # No vertical movement

        dx, dy = -1, 0  # Test walking left
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)  # Back to initial position
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # No vertical movement

        dx, dy = 0, 1  # Test walking down
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)  # No horizontal movement
        self.assertEqual(self.data["Zoom_rect"].y, 372)  # 1 pixel movement

        dx, dy = 0, -1  # Test walking up
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)  # No horizontal movement
        self.assertEqual(self.data["Zoom_rect"].y, 370)  # Back to initial position

        dx, dy = 1, 1  # Test walking diagonally down-right
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 182)
        self.assertEqual(self.data["Zoom_rect"].y, 372)

        dx, dy = 1, -1  # Test walking diagonally up-right
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 184)
        self.assertEqual(self.data["Zoom_rect"].y, 370)

        dx, dy = -1, 1  # Test walking diagonally down-left
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 182)
        self.assertEqual(self.data["Zoom_rect"].y, 372)

        dx, dy = -1, -1  # Test walking diagonally up-left
        walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        self.assertEqual(self.data["Zoom_rect"].x, 180)
        self.assertEqual(self.data["Zoom_rect"].y, 370)

    @patch('pygame.key.get_pressed')
    def test_walking_buttons(self, mock_get_pressed):
        """Test movement and keypresses."""
        screen = None  # Mock your screen if needed
        data = {
            "Player": {
                "dead": True
            }
        }

        # Create an instance of ScancodeWrapper with all keys unpressed (False)
        no_keys_pressed = pygame.key.ScancodeWrapper([False] * 512)

        # Test case where no keys are pressed
        mock_get_pressed.return_value = no_keys_pressed
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (0, 0))  # No keys should be pressed

        # Simulate pressing LEFT key
        keys = [False] * 512
        keys[80] = True  # Simulate pressing LEFT key
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (-1, 0))  # dx should be -1, dy should be 0

        # Simulate pressing RIGHT key
        keys = [False] * 512
        keys[79] = True  # Simulate pressing RIGHT key
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (1, 0))  # dx should be 1, dy should be 0

        # Simulate pressing UP key
        keys = [False] * 512
        keys[82] = True  # Simulate pressing UP key
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (0, -1))  # dx should be 0, dy should be -1

        # Simulate pressing DOWN key
        keys = [False] * 512
        keys[81] = True  # Simulate pressing DOWN key
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (0, 1))  # dx should be 0, dy should be 1

        # Simulate pressing DOWN-LEFT key
        keys = [False] * 512
        keys[81] = True  # Simulate pressing DOWN key
        keys[80] = True  # Simulate pressing LEFT key
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (-1, 1))  # dx should be -1, dy should be 1

        # Simulate pressing DOWN-RIGHT key
        keys = [False] * 512
        keys[81] = True  # Simulate pressing DOWN key
        keys[79] = True  # Simulate pressing RIGHT key
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (1, 1))  # dx should be 1, dy should be 1

        # Simulate pressing UP-LEFT key
        keys = [False] * 512
        keys[82] = True  # Simulate pressing UP key
        keys[80] = True  # Simulate pressing LEFT key
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (-1, -1))  # dx should be -1, dy should be -1

        # Simulate pressing UP-RIGHT key
        keys = [False] * 512
        keys[82] = True  # Simulate pressing UP key
        keys[79] = True  # Simulate pressing RIGHT key
        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (1, -1))  # dx should be 1, dy should be -1

        # Simulate pressing UP-RIGHT-DOWN-RIGHT key
        keys = [False] * 512
        keys[79] = True  # Simulate pressing RIGHT key
        keys[80] = True  # Simulate pressing UP key
        keys[81] = True  # Simulate pressing UP key
        keys[82] = True  # Simulate pressing UP key

        mock_get_pressed.return_value = pygame.key.ScancodeWrapper(keys)
        dx, dy = keypress_handle(screen, data, 0, 0, 0, 0, 0, 0)
        self.assertEqual((dx, dy), (0, 0))  # dx should be 0, dy should be 0

    def tearDown(self):
        # Cleanup if necessary
        pygame.display.quit()
        pass


class TestMapChangeFunction(unittest.TestCase):
    def setUp(self):

        # Set up initial test environment
        pygame.display.init()  # Initialize the display to prevent freezing
        pygame.display.set_mode((1, 1), pygame.NOFRAME)  # Create a tiny window, no need for display
        pygame.key.set_repeat(1, 1)  # Make sure keys work quickly in the test environment

        self.rooms = I.rooms.Room()
        self.rooms.select_room("Village_10_10")
        I.info.CURRENT_ROOM = {"name": "Village_10_10", "Spells": True, "Backpack": True, "Running": True, "Mobs": self.rooms.mobs, "Type": self.rooms.type}
        self.data = {}
        self.data["Window size"] = (S.SCREEN_WIDTH, S.SCREEN_HEIGHT)  # Defines the size of the window (The rest is black)
        self.data["Zoom"] = (S.SCREEN_WIDTH / 4, S.SCREEN_HEIGHT / 4)  # Defines how zoomed in to the picture the view is
        if self.rooms.type == "Village":
            values = self.rooms.name.split("_")
            self.data["Zoom"] = (
            S.SCREEN_WIDTH / 4, S.SCREEN_HEIGHT / 4)  # Defines how zoomed in to the picture the view is
            root_dir = I.os.path.dirname(I.os.path.dirname(I.os.path.abspath(__file__)))  # Adjust if necessary
            self.data["Image"] = I.pg.image.load(root_dir + "/" + S.DECOR_PATH[self.rooms.background + "_" + values[1] + "_" + values[2]]).convert_alpha()  # uploads the background image with transparent convert
        else:
            self.data["Zoom"] = (S.SCREEN_WIDTH / 15, S.SCREEN_HEIGHT / 15)  # Defines how zoomed in to the picture the view is
            self.data["Image"] = I.pg.image.load(S.DECOR_PATH[self.rooms.background]).convert_alpha()  # uploads the background image with transparent convert

        self.data["Image_rect"] = self.data["Image"].get_rect()  # Gets the rect of image
        self.data["Zoom_rect"] = I.pg.Rect(I.info.ENTRY_POS[0], I.info.ENTRY_POS[1], *self.data["Zoom"])  # creates a rect based on zoomed in picture (basicly makes a window)
        self.data["Player"] = {"health": 100, "mana": 50, "dead": False}

        I.info.OFFSCREEN = [0, 0]  # No offscreen movement initially

    def test_room_transitions(self):
        """Test moving between different rooms (e.g., from Village to House1)."""
        from Render.Background_Render import handle_map_walk
        self.rooms.select_room("House1")
        I.info.CURRENT_ROOM = {"name": "House1", "Spells": True, "Backpack": True, "Running": True,"Mobs": self.rooms.mobs, "Type": self.rooms.type}

        handle_map_walk(self.data, self.rooms, 0, 0, 0, 0)
        self.assertEqual(self.rooms.name, "House1") # no room changes occurred

        self.rooms.select_room("Village_10_10")
        I.info.CURRENT_ROOM = {"name": self.rooms.name, "Spells": True, "Backpack": True, "Running": True,"Mobs": self.rooms.mobs, "Type": self.rooms.type}
        self.data["Zoom_rect"].y = 0
        I.info.OFFSCREEN = (0, -360)

        handle_map_walk(self.data, self.rooms, 0, 0, 0, 0)
        self.assertEqual(self.rooms.name, "Village_10_9") # room changed

        self.data["Zoom_rect"].y = 820
        I.info.OFFSCREEN = (0, 370)
        handle_map_walk(self.data, self.rooms, 0, 0, 0, 0)
        self.assertEqual(self.rooms.name, "Village_10_10") # room changed back

        self.data["Zoom_rect"].x = 0
        I.info.OFFSCREEN = (-640, 0)
        handle_map_walk(self.data, self.rooms, 0, 0, 0, 0)
        self.assertEqual(self.rooms.name, "Village_9_10") # room changed


        self.data["Zoom_rect"].x = 680
        I.info.OFFSCREEN = (660, 0)
        handle_map_walk(self.data, self.rooms, 0, 0, 0, 0)
        self.assertEqual(self.rooms.name, "Village_10_10") # room changed back

        # dx, dy = 1, 0  # Move right
        # walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        # self.assertEqual(self.data["Zoom_rect"].x, 101)  # Movement should be within small room
        #
        # I.info.CURRENT_ROOM["Type"] = "Village"  # Simulate large room
        # dx, dy = 1, 0  # Move right
        # walking(dx, dy, collide, self.data, self.decorations, self.rooms)
        # self.assertEqual(self.data["Zoom_rect"].x, 102)  # Continue scrolling large room

    def tearDown(self):
        # Cleanup if necessary
        pygame.display.quit()
        pass

if __name__ == '__main__':
    unittest.main()