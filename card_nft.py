import random
from PIL import Image

def fisher_yates_shuffle(deck):
    """Shuffle the deck using the Fisher-Yates algorithm."""
    for i in range(len(deck) - 1, 0, -1):
        j = random.randint(0, i)
        deck[i], deck[j] = deck[j], deck[i]

def create_deck():
    """Create a standard 52-card deck."""
    suits = ['red', 'green', 'blue', 'yellow']  # Red: Hearts, Green: Diamonds, Blue: Clubs, Yellow: Spades
    deck = []
    for suit in suits:
        for value in range(13):  # 13 cards per suit
            tone = (value + 1) * 16  # Increment tone for each card
            deck.append((suit, tone))
    return deck

def color_for_card(card):
    """Return an RGB color for the given card."""
    suit, tone = card
    if suit == 'red':
        return (tone, 0, 0)
    elif suit == 'green':
        return (0, tone, 0)
    elif suit == 'blue':
        return (0, 0, tone)
    elif suit == 'yellow':
        return (tone, tone, 0)

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
                card_color = color_for_card(deck[index])
                for dy in range(block_size):
                    for dx in range(block_size):
                        pixels[x * block_size + dx, y * block_size + dy] = card_color
                index += 1

    # Save the image
    img.save(output_file)

def generate_images(num_images):
    """Generate a specified number of random deck images."""
    for i in range(num_images):
        deck = create_deck()
        output_file = f'deck_image_{i + 1}.png'
        create_image(deck, output_file)
        print(f"Image {i + 1} saved as {output_file}")

if __name__ == '__main__':
    # Generate 1000 random deck images
    generate_images(1000)

