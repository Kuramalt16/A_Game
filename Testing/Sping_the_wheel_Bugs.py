import pygame
import random
import math
import os

# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spin the Wheel - Bug Fix Picker")

# Basic Colors (initial set)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Base colors for creating unique colors
BASE_COLORS = [RED, GREEN, BLUE, YELLOW]


def generate_random_color():
    """Generates a random color in RGB format."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to split text into multiple lines
def split_text(text, font, max_width):
    words = text.split(' ')  # Split the text into words
    lines = []
    current_line = ""

    for word in words:
        # Try to add the word to the current line
        test_line = current_line + " " + word if current_line else word
        text_width, _ = font.size(test_line)  # Get the width of the text if this word is added

        # If adding the word exceeds the max width, start a new line
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word  # Start a new line with the current word

    # Add the last line
    if current_line:
        lines.append(current_line)

    return lines



# Load bugs from file
def load_bugs(file_name):
    bugs = []
    with open(file_name, "r") as file:
        lines = file.readlines()
        current_id = ""
        current_priority = ""
        for line in lines:
            line = line.strip()
            if line.startswith("* DESC:"):
                describtion = line.replace("* DESC:", "").strip()
            if line.startswith("* ID:"):
                current_id = line.replace("* ID:", "").strip()
            elif line.startswith("* PRIORITY:"):
                current_priority = line.replace("* PRIORITY:", "").strip().upper()
                if current_id and current_priority:
                    if current_priority == "LOW":
                        bugs.append((current_id, describtion))
                    elif current_priority == "MEDIUM":
                        bugs.extend([(current_id, describtion)] * 2)
                    elif current_priority == "HIGH":
                        bugs.extend([(current_id, describtion)] * 3)
    return bugs


# Generate enough unique colors by modifying RGB values
def generate_colors(num_colors):
    # Start with the base colors
    colors = BASE_COLORS.copy()

    # Use a set to track the unique colors (set handles duplicates automatically)
    color_set = set(colors)
    # Keep generating new colors until we have enough unique ones
    while len(color_set) < num_colors:
        # Generate a new color by modifying RGB values randomly
        # r, g, b = random.choice(BASE_COLORS)

        # Randomly increment or decrement each RGB component
        # r = (r + random.choice([5, -5])) % 250
        # g = (g + random.choice([5, -5])) % 250
        # b = (b + random.choice([10, -10])) % 250
        # if b < 100:
        #     b += 100
        # if r < 30:
        #     r += 50
        # if g < 30:
        #     g += 50

        new_color = generate_random_color()

        # Check if the color is not black or white
        if new_color not in [(0, 0, 0), (1, 0, 0),(0, 1, 0), (0, 0, 1), (255, 255, 255), (255, 255, 254), (255, 254, 255), (254, 255, 255)]:
            # Add the new color to the set if it's not already present
            color_set.add(new_color)

        # Avoid going into an infinite loop in case it's hard to find unique colors
        if len(color_set) > num_colors + 20:  # A small buffer to stop the loop if it's taking too long
            break

    # Convert the set back to a list and return it
    return list(color_set)[:num_colors]



# Draw the wheel
def draw_wheel(surface, entries, angle, colors):
    num_entries = len(entries)
    center = (WIDTH // 2, HEIGHT // 2)
    radius = 200

    # Map each color to a bug ID
    color_map = {}  # Color -> Bug ID mapping
    for i, entry in enumerate(entries):
        # Calculate segment angles
        entry = entry[0]
        start_angle = angle + (2 * math.pi * i / num_entries)
        end_angle = angle + (2 * math.pi * (i + 1) / num_entries)

        # Assign a color to the segment
        color = colors[i % len(colors)]  # Cycle through colors if more entries than colors
        color_map[color] = entry

        # Draw the colored segments
        pygame.draw.polygon(
            surface,
            color,
            [
                center,
                (
                    center[0] + math.cos(start_angle) * radius,
                    center[1] + math.sin(start_angle) * radius,
                ),
                (
                    center[0] + math.cos(end_angle) * radius,
                    center[1] + math.sin(end_angle) * radius,
                ),
            ],
        )

        # Draw the text in the middle of the segment
        mid_angle = (start_angle + end_angle) / 2
        text_x = center[0] + math.cos(mid_angle) * radius * 0.7
        text_y = center[1] + math.sin(mid_angle) * radius * 0.7
        font = pygame.font.Font(None, 16)
        text = font.render(str(entry), True, BLACK)
        text_rect = text.get_rect(center=(text_x, text_y))
        surface.blit(text, text_rect)

    return color_map


# Draw the arrow
def draw_arrow(surface, center):
    arrow_color = BLACK
    arrow_points = [
        (center[0]+220, center[1] - 20),  # Tip of the arrow
        (center[0]+190, center[1]),  # Left corner
        (center[0]+220, center[1] + 20),  # Right corner
    ]
    pygame.draw.polygon(surface, arrow_color, arrow_points)


# Draw the button
def draw_button(surface, center):
    button_color = RED
    button_rect = pygame.Rect(center[0] - 50, center[1] - 25, 100, 50)
    pygame.draw.rect(surface, "black", button_rect, 4)
    button_rect = pygame.Rect(center[0] - 50 + 4, center[1] + 4 - 25, 92, 42)
    pygame.draw.rect(surface, "red", button_rect)

    font = pygame.font.Font(None, 36)
    text = font.render("Press Me", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    surface.blit(text, text_rect)

    return button_rect


# Main Game Loop
def main(key):

    running = True
    clock = pygame.time.Clock()
    count = 100
    # Load bugs
    # path = os.path.abspath(__file__).replace("Testing\\Sping_the_wheel_Bugs.py", "Bugs.txt")
    if key != "MAIN":
        local_path = os.getcwd()
        what_to_spin = {"Bugs": local_path.replace("Testing", "Bugs.txt"),
                        "Draw": local_path.replace("Testing", "Draw.txt"),
                        "Features": local_path.replace("Testing", "Features.txt")
                        }
        path = what_to_spin[key]
        bugs = load_bugs(path)
    else:
        bugs = [(1, "Features"), (2, "Bugs"), (3, "Bugs"), (4, "Bugs"), (5, "Bugs"), (6, "Bugs"), (7, "Draw"), (8, "Draw"), (9, "Draw")]
    random.shuffle(bugs)
    # Generate enough unique colors for the number of bugs
    colors = generate_colors(len(bugs))
    # Wheel state
    current_angle = 0
    angular_velocity = 0
    spinning = False
    selected_bug = ""

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not spinning:
                mouse_pos = pygame.mouse.get_pos()
                if button.collidepoint(mouse_pos):
                    angular_velocity = random.random()
                    spinning = True
                    selected_bug = ""

        # Rotate the wheel if spinning


        # Draw the wheel
        color_map = draw_wheel(screen, bugs, current_angle, colors)
        if spinning:
            current_angle += angular_velocity
            angular_velocity *= 0.99  # Gradual slowdown
            if angular_velocity < 0.01:  # Stop when slow enough
                angular_velocity = 0
                spinning = False

                # Normalize angle to [0, 2π)
                normalized_angle = (-current_angle % (2 * math.pi))

                # Determine the color at the arrow's position
                segment_angle = (2 * math.pi) / len(bugs)
                corrected_angle = (normalized_angle + segment_angle / 2) % (2 * math.pi)

                # Check which color is under the arrow
                # selected_color = colors[int(corrected_angle // segment_angle) % len(colors)]
                selected_color = screen.get_at((580, 300))
                selected_color = (selected_color[0], selected_color[1], selected_color[2])
                # Find the bug corresponding to the selected color
                selected_bug = color_map[selected_color]
        # Draw the arrow
        draw_arrow(screen, (WIDTH // 2, HEIGHT // 2))

        # Draw the button
        button = draw_button(screen, (WIDTH // 2, HEIGHT // 2))

        # Display the selected bug after the wheel stops
        if not spinning and selected_bug:
            for id, bug_desc in bugs:
                if selected_bug == id:
                    break
                else:
                    bug_desc = ""
            font_id = pygame.font.Font(None, 36)  # For ID text
            font_desc = pygame.font.Font(None, 20)  # For description text

            # Render the texts
            text = font_id.render(f"{key} (ID): {selected_bug}", True, BLACK)
            text1 = f"{key}:{bug_desc}"

            # Define the maximum width for the description
            max_width = WIDTH - 40  # Leave some margin (e.g., 20 pixels on each side)

            # Split the description text into multiple lines if necessary
            desc_lines = split_text(text1, font_desc, max_width)

            # Draw the ID text
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 100))

            # Draw the description text, each line on a new line
            y_offset = HEIGHT - 50
            for line in desc_lines:
                text_line = font_desc.render(line, True, BLACK)
                screen.blit(text_line, (WIDTH // 2 - text_line.get_width() // 2, y_offset))
                y_offset += text_line.get_height() + 5  # Add some spacing between lines


        pygame.display.flip()
        clock.tick(60)
        if selected_bug and key == "MAIN":
            count -= 1
            if count == 0:
                return bug_desc
    pygame.quit()



key = main("MAIN")
main(key)



