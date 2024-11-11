import pygame
import subprocess
import sys
import os


class ChessLauncher:
    def __init__(self):
        # Load the custom font with a larger size for the title
        pygame.init()
        self.WINDOW_SIZE = (600, 400)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.background_image = pygame.image.load(r"imagesfonts\background.jpg")
        self.background_image = pygame.transform.scale(
            self.background_image, (600, 400)
        )

        pygame.display.set_caption("Chess Game Launcher")

        # Initialize font
        self.font = pygame.font.SysFont("Arial", 32)

        # Define buttons
        self.buttons = [
            {
                "text": "Multiplayer",
                "rect": pygame.Rect(200, 100 + 50, 200, 50),
                "file": "Multiplayer.py",
                "color": (0, 128, 255),  # Blue color
            },
            {
                "text": "Stockfish",
                "rect": pygame.Rect(200, 175 + 50, 200, 50),
                "file": "Stockfish.py",
                "color": (0, 255, 128),  # Green color
            },
            {
                "text": "Custom Engine",
                "rect": pygame.Rect(200, 250 + 50, 200, 50),
                "file": "CustomEngine.py",
                "color": (255, 128, 0),  # Orange color
            },
        ]

    def draw_button(self, button, hover=False):
        # Draw button background
        color = (128, 128, 128) if hover else (255, 255, 255)
        pygame.draw.rect(self.screen, color, button["rect"])

        # Draw button text
        text = self.font.render(button["text"], True, (0, 0, 0))
        text_rect = text.get_rect(center=button["rect"].center)
        self.screen.blit(text, text_rect)

    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))

            # Draw title
            fontt = pygame.font.Font(r"imagesfonts\ScaryHalloweenFont.ttf", 60)
            title = fontt.render("Chess Game", True, (255, 255, 255))
            title_rect = title.get_rect(center=(300, 50))
            self.screen.blit(title, title_rect)

            # Handle events
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.buttons:
                        if button["rect"].collidepoint(mx, my):
                            # Run the corresponding Python file
                            try:
                                # Get the directory of the current script
                                current_dir = os.path.dirname(os.path.abspath(__file__))
                                # Construct the full path to the target Python file
                                file_path = os.path.join(current_dir, button["file"])

                                # Run the Python file
                                subprocess.Popen([sys.executable, file_path])
                                running = False  # Close the launcher
                            except Exception as e:
                                print(f"Error launching {button['file']}: {e}")

            # Draw buttons
            for button in self.buttons:
                hover = button["rect"].collidepoint(mx, my)
                self.draw_button(button, hover)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    launcher = ChessLauncher()
    launcher.run()
