#!/usr/bin/env python3
"""
Create professional Chrome Web Store listing images from screenshots.
Adds padding, backgrounds, shadows, and captions.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

# Chrome Web Store recommended dimensions
OUTPUT_WIDTH = 1280
OUTPUT_HEIGHT = 800

# Design settings
BACKGROUND_COLOR = (45, 55, 72)  # Slate blue-gray
ACCENT_COLOR = (59, 130, 246)    # Blue accent
SHADOW_OFFSET = 15
SHADOW_BLUR = 30
PADDING = 80

def create_gradient_background(width, height):
    """Create a subtle gradient background"""
    img = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(img)

    # Create vertical gradient from dark to slightly lighter
    for y in range(height):
        # Gradient from BACKGROUND_COLOR to slightly lighter
        ratio = y / height
        r = int(BACKGROUND_COLOR[0] + (BACKGROUND_COLOR[0] * 0.2 * ratio))
        g = int(BACKGROUND_COLOR[1] + (BACKGROUND_COLOR[1] * 0.2 * ratio))
        b = int(BACKGROUND_COLOR[2] + (BACKGROUND_COLOR[2] * 0.2 * ratio))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    return img

def add_shadow(img, offset=SHADOW_OFFSET, blur=SHADOW_BLUR):
    """Add drop shadow to image"""
    # Create shadow layer
    shadow = Image.new('RGBA',
                      (img.width + offset * 2, img.height + offset * 2),
                      (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle(
        [(offset, offset), (img.width + offset, img.height + offset)],
        fill=(0, 0, 0, 180)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))

    # Paste original image on top of shadow
    result = Image.new('RGBA', shadow.size, (0, 0, 0, 0))
    result.paste(shadow, (0, 0))
    result.paste(img, (offset, offset), img if img.mode == 'RGBA' else None)

    return result

def add_rounded_corners(img, radius=20):
    """Add rounded corners to image"""
    # Create mask
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)

    # Apply mask
    output = Image.new('RGBA', img.size, (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)

    return output

def create_store_image(screenshot_path, output_path, title=None):
    """Create a professional store listing image from a screenshot"""
    print(f"Processing: {screenshot_path}")

    # Load screenshot
    screenshot = Image.open(screenshot_path)
    if screenshot.mode != 'RGBA':
        screenshot = screenshot.convert('RGBA')

    # Add rounded corners to screenshot
    screenshot = add_rounded_corners(screenshot, radius=12)

    # Add shadow
    screenshot_with_shadow = add_shadow(screenshot)

    # Create background
    background = create_gradient_background(OUTPUT_WIDTH, OUTPUT_HEIGHT)
    background = background.convert('RGBA')

    # Calculate position to center screenshot (accounting for shadow)
    title_height = 60 if title else 0
    available_height = OUTPUT_HEIGHT - PADDING * 2 - title_height

    # Scale screenshot to fit while maintaining aspect ratio
    screenshot_aspect = screenshot.width / screenshot.height
    max_width = OUTPUT_WIDTH - PADDING * 2
    max_height = available_height

    if screenshot.width > max_width or screenshot.height > max_height:
        # Scale down to fit
        scale = min(max_width / screenshot.width, max_height / screenshot.height)
        # Add some extra scaling to make it look nice (not too big)
        scale *= 0.8
        new_width = int(screenshot.width * scale)
        new_height = int(screenshot.height * scale)
        screenshot_with_shadow = screenshot_with_shadow.resize(
            (int(screenshot_with_shadow.width * scale),
             int(screenshot_with_shadow.height * scale)),
            Image.Resampling.LANCZOS
        )

    # Center the screenshot with shadow
    x = (OUTPUT_WIDTH - screenshot_with_shadow.width) // 2
    y = (OUTPUT_HEIGHT - screenshot_with_shadow.height - title_height) // 2 + title_height // 2

    # Composite screenshot onto background
    background.paste(screenshot_with_shadow, (x, y), screenshot_with_shadow)

    # Add title if provided
    if title:
        draw = ImageDraw.Draw(background)
        try:
            font = ImageFont.truetype("segoeui.ttf", 36)
        except:
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()

        # Get text bounding box
        bbox = draw.textbbox((0, 0), title, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = (OUTPUT_WIDTH - text_width) // 2
        text_y = PADDING // 2

        # Draw text with subtle shadow
        draw.text((text_x + 2, text_y + 2), title, fill=(0, 0, 0, 100), font=font)
        draw.text((text_x, text_y), title, fill=(255, 255, 255, 255), font=font)

    # Convert back to RGB for saving
    final = Image.new('RGB', background.size, BACKGROUND_COLOR)
    final.paste(background, (0, 0), background)

    # Save
    final.save(output_path, 'PNG', quality=95)
    print(f"Created: {output_path}")

def main():
    """Process all screenshots"""
    screenshots_dir = "screenshots"
    output_dir = "screenshots/store-listing"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Define screenshots and their titles
    images = [
        ("Screenshot 2025-12-25 215031.png", "1-popup-dark.png", "Manage Your Search Engines"),
        ("Screenshot 2025-12-25 215243.png", "2-popup-light.png", "Light Theme Support"),
        ("Screenshot 2025-12-25 220054.png", "3-context-menu-single.png", "Right-Click to Search"),
        ("Screenshot 2025-12-25 220209.png", "4-context-menu-multiple.png", "Multiple Search Options"),
    ]

    for screenshot_name, output_name, title in images:
        screenshot_path = os.path.join(screenshots_dir, screenshot_name)
        output_path = os.path.join(output_dir, output_name)

        if os.path.exists(screenshot_path):
            create_store_image(screenshot_path, output_path, title)
        else:
            print(f"Warning: {screenshot_path} not found")

    print(f"\nAll store listing images created in {output_dir}/")
    print(f"  Dimensions: {OUTPUT_WIDTH}x{OUTPUT_HEIGHT} (Chrome Web Store recommended)")

if __name__ == "__main__":
    main()
