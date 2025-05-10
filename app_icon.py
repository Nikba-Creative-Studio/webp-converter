from PIL import Image, ImageDraw
import os
import subprocess

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
    
    # Create iconset directory
    iconset_dir = 'icon.iconset'
    if not os.path.exists(iconset_dir):
        os.makedirs(iconset_dir)
    
    # Save in different sizes for macOS
    sizes = {
        16: '16x16',
        32: '16x16@2x',
        32: '32x32',
        64: '32x32@2x',
        128: '128x128',
        256: '128x128@2x',
        256: '256x256',
        512: '256x256@2x',
        512: '512x512',
        1024: '512x512@2x'
    }
    
    for size, name in sizes.items():
        resized = icon.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f'{iconset_dir}/icon_{name}.png')
    
    # Convert to icns using iconutil
    try:
        subprocess.run(['iconutil', '-c', 'icns', iconset_dir], check=True)
        # Clean up iconset directory
        subprocess.run(['rm', '-rf', iconset_dir])
        return 'icon.icns'
    except subprocess.CalledProcessError:
        print("Warning: Failed to create .icns file")
        return None

if __name__ == '__main__':
    create_app_icon() 