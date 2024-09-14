import pygame
import random
import time
import controls  # Import gesture controls

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Balls")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game clock and font
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Game variables
cart_width = 100
cart_height = 20
cart_x = WIDTH // 2 - cart_width // 2
cart_y = HEIGHT - 60
ball_radius = 20
ball_speed = 5
balls = []
score = 0
game_time = 120  # 2 minutes = 120 seconds

# Function to create new ball
def create_ball():
    x = random.randint(0, WIDTH - ball_radius * 2)
    return {"x": x, "y": -ball_radius}

# Function to check if the ball is caught by the cart
def is_ball_caught(ball_x, ball_y, cart_x, cart_y, cart_width):
    return cart_x < ball_x < cart_x + cart_width and cart_y < ball_y < cart_y + cart_height

# Function to reset the game
def reset_game():
    global balls, score, cart_x, start_time
    balls = []
    score = 0
    cart_x = WIDTH // 2 - cart_width // 2
    start_time = time.time()

# Main game loop
def game_loop():
    global cart_x, score  # Declare score and cart_x as global
    running = True
    start_time = time.time()

    while running:
        screen.fill(WHITE)  # Fill the screen with white color

        # Calculate remaining time
        elapsed_time = time.time() - start_time
        remaining_time = game_time - int(elapsed_time)
        
        if remaining_time <= 0:
            remaining_time = 0
            running = False  # Stop the game when time is up
        
        # Draw the cart as a rectangle
        gesture_direction = controls.get_gesture_direction()  # Get gesture direction from controls.py
        
        move_speed = 60  # Default movement speed
        if gesture_direction == "left" and cart_x > 0:
            cart_x -= move_speed
        if gesture_direction == "right" and cart_x < WIDTH - cart_width:
            cart_x += move_speed

        pygame.draw.rect(screen, BLUE, (cart_x, cart_y, cart_width, cart_height))  # Draw the rectangle
        
        # Create and update falling balls
        if random.random() < 0.02:  # Probability of a new ball appearing
            balls.append(create_ball())
        
        for ball in balls[:]:
            ball["y"] += ball_speed
            pygame.draw.circle(screen, RED, (ball["x"], ball["y"]), ball_radius)
            
            # Check if ball is caught
            if is_ball_caught(ball["x"], ball["y"], cart_x, cart_y, cart_width):
                score += 1
                balls.remove(ball)
            
            # Remove the ball if it goes off the screen
            elif ball["y"] > HEIGHT:
                balls.remove(ball)

        # Display score and timer
        score_text = font.render(f"Score: {score}", True, BLACK)
        timer_text = font.render(f"Time: {remaining_time}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (WIDTH - 150, 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                controls.release_camera()  # Release the camera before quitting
                pygame.quit()
                quit()

        pygame.display.flip()
        clock.tick(60)

    return game_over_screen()

# Game over screen with restart option
def game_over_screen():
    screen.fill(WHITE)
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - 200, HEIGHT // 2))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                controls.release_camera()  # Release the camera before quitting
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    return True
                elif event.key == pygame.K_q:
                    controls.release_camera()  # Release the camera before quitting
                    pygame.quit()
                    quit()

# Start the game
reset_game()
while True:
    game_loop()
