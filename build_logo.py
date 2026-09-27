import math
import os
from PIL import Image, ImageDraw, ImageFilter

def create_logo_variants():
    # Colors
    bg_color = (30, 41, 59, 255) # Slate 800
    cyan_color = (34, 211, 238, 255) # Cyan 400
    transparent = (0, 0, 0, 0)
    
    # Sizes needed for ICO
    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # Create the high-res base image
    base_size = 1024
    
    def draw_symbol(draw, cx, cy, R, T, gap, color):
        # Calculate chevron parameters
        # L is the length of the arm along the outer edge
        L = R / 2.0 - gap / 2.0
        
        for i in range(6):
            angle = math.radians(i * 60)
            
            # Rotation helper
            def rot(x, y):
                rx = x * math.cos(angle) - y * math.sin(angle)
                ry = x * math.sin(angle) + y * math.cos(angle)
                return (cx + rx, cy + ry)
                
            # Base chevron at 0 degrees
            # D1 = 120 deg
            d1_x = -0.5
            d1_y = math.sqrt(3) / 2.0
            
            # D5 = 240 deg
            d5_x = -0.5
            d5_y = -math.sqrt(3) / 2.0
            
            # N1 = 210 deg
            n1_x = -math.sqrt(3) / 2.0
            n1_y = -0.5
            
            # N5 = 150 deg
            n5_x = -math.sqrt(3) / 2.0
            n5_y = 0.5
            
            p1 = (R, 0)
            p2 = (R + L * d1_x, L * d1_y)
            p3 = (R + L * d1_x + T * n1_x, L * d1_y + T * n1_y)
            p4 = (R - T * 2.0 / math.sqrt(3), 0)
            p5 = (R + L * d5_x + T * n5_x, L * d5_y + T * n5_y)
            p6 = (R + L * d5_x, L * d5_y)
            
            # Rotate and shift points
            poly = [rot(*p) for p in (p1, p2, p3, p4, p5, p6)]
            
            # Draw polygon
            draw.polygon(poly, fill=color)

    # 1. Primary Application Icon (1024x1024)
    img_primary = Image.new('RGBA', (base_size, base_size), transparent)
    draw_primary = ImageDraw.Draw(img_primary)
    
    # Draw rounded square background
    bg_radius = 220
    draw_primary.rounded_rectangle([0, 0, base_size, base_size], radius=bg_radius, fill=bg_color)
    
    # Draw symbol
    # Super-sampling for anti-aliasing
    ss = 4
    img_ss = Image.new('RGBA', (base_size * ss, base_size * ss), transparent)
    draw_ss = ImageDraw.Draw(img_ss)
    
    # Background in SS
    draw_ss.rounded_rectangle([0, 0, base_size * ss, base_size * ss], radius=bg_radius * ss, fill=bg_color)
    
    # Symbol parameters
    R = 360 * ss
    T = 110 * ss
    gap = 24 * ss
    draw_symbol(draw_ss, base_size * ss / 2, base_size * ss / 2, R, T, gap, cyan_color)
    
    img_primary = img_ss.resize((base_size, base_size), Image.Resampling.LANCZOS)
    
    # Save variants
    os.makedirs('app/public', exist_ok=True)
    img_primary.save('app/public/icon_primary.png')
    
    # 2. Transparent Brand Mark
    img_mark_ss = Image.new('RGBA', (base_size * ss, base_size * ss), transparent)
    draw_mark_ss = ImageDraw.Draw(img_mark_ss)
    draw_symbol(draw_mark_ss, base_size * ss / 2, base_size * ss / 2, R, T, gap, cyan_color)
    img_mark = img_mark_ss.resize((base_size, base_size), Image.Resampling.LANCZOS)
    img_mark.save('app/public/icon_transparent.png')
    
    # 3. Small Icon Variant (optimized for 16-32px)
    # For small icons, we thicken the lines and increase the gap to maintain readability
    img_small_ss = Image.new('RGBA', (base_size * ss, base_size * ss), transparent)
    draw_small_ss = ImageDraw.Draw(img_small_ss)
    draw_small_ss.rounded_rectangle([0, 0, base_size * ss, base_size * ss], radius=bg_radius * ss, fill=bg_color)
    draw_symbol(draw_small_ss, base_size * ss / 2, base_size * ss / 2, R * 0.95, T * 1.3, gap * 2.5, cyan_color)
    img_small = img_small_ss.resize((base_size, base_size), Image.Resampling.LANCZOS)
    
    # Generate ICO file
    ico_images = []
    for size in ico_sizes:
        if size <= 48:
            # Use small optimized variant
            ico_images.append(img_small.resize((size, size), Image.Resampling.LANCZOS))
        else:
            # Use primary variant
            ico_images.append(img_primary.resize((size, size), Image.Resampling.LANCZOS))
            
    # Save without the sizes argument so Pillow just uses the exact images we pass
    ico_images[0].save('app/public/icon.ico', format='ICO', append_images=ico_images[1:])
    print("Logo variants and icon.ico generated successfully.")

if __name__ == "__main__":
    create_logo_variants()
