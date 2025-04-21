import os
import sys
from PIL import Image, ImageDraw, ImageFont

def create_icon():
    """Create a simple icon for the Ollama History Cleaner app"""
    try:
        # Create the icon directory if it doesn't exist
        icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.iconset')
        os.makedirs(icon_dir, exist_ok=True)
        
        # Icon sizes needed for macOS
        sizes = [16, 32, 64, 128, 256, 512, 1024]
        
        for size in sizes:
            # Create a new transparent image
            icon = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(icon)
            
            # Draw a blue circle as background
            circle_color = (41, 128, 185)  # Blue color
            margin = int(size * 0.1)
            draw.ellipse([margin, margin, size - margin, size - margin], fill=circle_color)
            
            # Draw a white "X" in the middle to symbolize cleaning
            line_width = max(int(size * 0.06), 1)
            line_margin = int(size * 0.3)
            draw.line(
                [(line_margin, line_margin), (size - line_margin, size - line_margin)], 
                fill="white", 
                width=line_width
            )
            draw.line(
                [(size - line_margin, line_margin), (line_margin, size - line_margin)], 
                fill="white", 
                width=line_width
            )
            
            # Save the icon with the appropriate name
            icon_path = os.path.join(icon_dir, f'icon_{size}x{size}.png')
            icon.save(icon_path)
            
            # For macOS, we also need @2x versions for Retina displays
            if size <= 512:
                icon_path_2x = os.path.join(icon_dir, f'icon_{size}x{size}@2x.png')
                # Just save the next size up as the 2x version (or the same if we're at the max)
                next_size_idx = min(sizes.index(size) + 1, len(sizes) - 1)
                icon_2x_path = os.path.join(icon_dir, f'icon_{sizes[next_size_idx]}x{sizes[next_size_idx]}.png')
                if os.path.exists(icon_2x_path):
                    import shutil
                    shutil.copy2(icon_2x_path, icon_path_2x)
        
        print(f"Icon files created in {icon_dir}")
        print("Use the following command to create the .icns file:")
        print(f"iconutil -c icns {icon_dir}")
        
        return icon_dir
    except Exception as e:
        print(f"Error creating icons: {e}")
        return None

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed. Installing...")
        import subprocess
        subprocess.call([sys.executable, "-m", "pip", "install", "Pillow"])
        from PIL import Image, ImageDraw, ImageFont
    
    create_icon()
