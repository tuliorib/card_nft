import random
from PIL import Image
from colorsys import rgb_to_hls, hls_to_rgb

def fisher_yates_shuffle(deck):
    """Shuffle the deck using the Fisher-Yates algorithm."""
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def hex_to_rgb(hex_color):
    """Convert HEX to RGB."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB to HEX."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def generate_tones(base_color, num_tones=13, brightness_limit=80):
    """Generate 13 tones for a base color, restricting brightness as a percentage."""
    rgb = hex_to_rgb(base_color)
    h, l, s = rgb_to_hls(*[x / 255.0 for x in rgb])

    # Calculate brightness range
    min_brightness = (100 - brightness_limit) / 100.0
    max_brightness = brightness_limit / 100.0

    # Generate tones
    tones = []
    for i in range(num_tones):
        # Spread lightness values between min and max brightness
        lightness = min_brightness + (max_brightness - min_brightness) * (i / (num_tones - 1))
        r, g, b = hls_to_rgb(h, lightness, s)
        tones.append((int(r * 255), int(g * 255), int(b * 255)))
    return tones

def create_deck(base_colors, brightness_limit=80):
    """Create a deck of 52 cards using base colors and tone variations."""
    deck = []
    for base_color in base_colors:
        tones = generate_tones(base_color, brightness_limit=brightness_limit)
        deck.extend(tones)  # Add the 13 tones for each suit
    return deck

def create_image(deck, output_file):
    """Create an 8x8 image with shuffled deck representation."""
    image_size = 240  # 240x240 pixels
    block_size = 30  # Each block is 30x30 pixels
    img = Image.new('RGB', (image_size, image_size), 'black')

    # Get shuffled deck
    fisher_yates_shuffle(deck)

    # Define blocks to skip (L-shaped corners)
    skip_blocks = {
        (0, 0), (0, 1), (1, 0),  # Top-left corner
        (0, 6), (0, 7), (1, 7),  # Top-right corner
        (6, 0), (7, 0), (7, 1),  # Bottom-left corner
        (6, 7), (7, 6), (7, 7),  # Bottom-right corner
    }

    # Draw the 52 cards in the remaining blocks
    pixels = img.load()
    index = 0

    for y in range(8):
        for x in range(8):
            if (y, x) in skip_blocks:
                continue
            if index < len(deck):
                card_color = deck[index]
                for dy in range(block_size):
                    for dx in range(block_size):
                        pixels[x * block_size + dx, y * block_size + dy] = card_color
                index += 1

    # Save the image
    img.save(output_file)

def generate_images(base_colors, num_images, brightness_limit=80):
    """Generate a specified number of random deck images."""
    for i in range(num_images):
        deck = create_deck(base_colors, brightness_limit=brightness_limit)
        output_file = f'deck_image_{i + 1}.png'
        create_image(deck, output_file)
        print(f"Image {i + 1} saved as {output_file}")

if __name__ == '__main__':
    # Base colors for the suits (center tones for card 7)
    #base_colors = ["CFFCFF", "AAEFDF", "9EE37D", "63C132"]
    base_colors = ["EEE82C", "91CB3E", "53A548", "4C934C"]

    # Generate 1000 random deck images with brightness limit of 80%
    generate_images(base_colors, num_images=1000, brightness_limit=80)

