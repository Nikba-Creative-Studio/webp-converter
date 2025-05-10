from PIL import Image, ImageDraw
import os

def create_app_icon():
    # Create a 512x512 image with a transparent background
    size = 512
    icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Draw the background circle
    circle_color = (114, 99, 242)  # #7263f2
    draw.ellipse([(50, 50), (size-50, size-50)], fill=circle_color)
    
    # Draw the "W" letter
    text_color = (255, 255, 255)  # White
    # Create a temporary image for the text
    text_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    
    # Draw a stylized "W"
    points = [
        (size//4, size//3),  # Start of first line
        (size//2, size*2//3),  # Middle point
        (size*3//4, size//3),  # End of first line
        (size*2//3, size*2//3),  # Middle of second line
        (size//2, size//3),  # Middle point
        (size//3, size*2//3),  # Middle of first line
    ]
    text_draw.line(points, fill=text_color, width=30)
    
    # Composite the text onto the main image
    icon = Image.alpha_composite(icon, text_img)
    
    # Save in different sizes
    sizes = [16, 32, 64, 128, 256, 512]
    for s in sizes:
        resized = icon.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f'icon_{s}.png')
    
    # Save as ICO file
    icon.save('app_icon.ico', format='ICO', sizes=[(s, s) for s in sizes])
    
    return 'app_icon.ico'

if __name__ == '__main__':
    create_app_icon() 