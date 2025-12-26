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
PADDING = 60  # Reduced padding for larger screenshots
ANNOTATION_WIDTH = 340  # Annotation width for large text
GAP = 40  # Gap between screenshot and annotation

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

def draw_annotation(draw, text, x, y, font, align='left'):
    """Draw text annotation with background box"""
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 15
    box_width = text_width + padding * 2
    box_height = text_height + padding * 2

    if align == 'right':
        box_x = x - box_width
    else:
        box_x = x

    box_y = y - padding

    # Draw semi-transparent background box with rounded corners
    box = Image.new('RGBA', (box_width, box_height), (0, 0, 0, 0))
    box_draw = ImageDraw.Draw(box)
    box_draw.rounded_rectangle(
        [(0, 0), (box_width, box_height)],
        radius=8,
        fill=(0, 0, 0, 200)
    )

    return box, box_x, box_y, text_width, text_height, padding

def create_store_image(screenshot_path, output_path, annotation=None, annotation_position='right'):
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

    # Calculate available space for screenshot
    reserved_space = ANNOTATION_WIDTH + GAP if annotation else 0
    max_width = OUTPUT_WIDTH - PADDING * 2 - reserved_space
    max_height = OUTPUT_HEIGHT - PADDING * 2

    # Scale screenshot to be as large as possible while fitting
    scale = min(max_width / screenshot.width, max_height / screenshot.height)
    # Use 98% of available space for minimal breathing room
    scale *= 0.98

    screenshot_with_shadow = screenshot_with_shadow.resize(
        (int(screenshot_with_shadow.width * scale),
         int(screenshot_with_shadow.height * scale)),
        Image.Resampling.LANCZOS
    )

    # Center the entire screenshot+annotation combo
    total_width = screenshot_with_shadow.width + (reserved_space if annotation else 0)
    combo_start_x = (OUTPUT_WIDTH - total_width) // 2

    # Position screenshot
    if annotation_position == 'right':
        x = combo_start_x
    else:
        x = combo_start_x + ANNOTATION_WIDTH + GAP

    y = (OUTPUT_HEIGHT - screenshot_with_shadow.height) // 2

    # Composite screenshot onto background
    background.paste(screenshot_with_shadow, (x, y), screenshot_with_shadow)

    # Add annotation if provided
    if annotation:
        draw = ImageDraw.Draw(background)

        # Load fonts - Bahnschrift for title, Cambria for subtitle
        try:
            title_font = ImageFont.truetype("bahnschrift.ttf", 72)
        except:
            try:
                title_font = ImageFont.truetype("segoeui.ttf", 72)
            except:
                try:
                    title_font = ImageFont.truetype("arial.ttf", 72)
                except:
                    title_font = ImageFont.load_default()

        try:
            subtitle_font = ImageFont.truetype("seguili.ttf", 42)  # Segoe UI Light Italic
        except:
            try:
                subtitle_font = ImageFont.truetype("segoeuii.ttf", 42)  # Segoe UI Italic
            except:
                try:
                    subtitle_font = ImageFont.truetype("ariali.ttf", 42)
                except:
                    subtitle_font = ImageFont.load_default()

        # Parse annotation (title and optional subtitle)
        if isinstance(annotation, dict):
            title = annotation.get('title', '')
            subtitle = annotation.get('subtitle', '')
        else:
            title = annotation
            subtitle = ''

        # Calculate annotation x position
        if annotation_position == 'right':
            ann_x = x + screenshot_with_shadow.width + GAP
        else:
            ann_x = combo_start_x

        # Line height settings
        title_line_height = 85
        subtitle_line_height = 55
        title_subtitle_gap = 10

        # Word wrap title (calculate lines first)
        title_words = title.split()
        title_lines = []
        current_line = []
        title_max_width = ANNOTATION_WIDTH - 20

        for word in title_words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] - bbox[0] > title_max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    title_lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    title_lines.append(word)
                    current_line = []

        if current_line:
            title_lines.append(' '.join(current_line))

        # Word wrap subtitle (calculate lines first)
        subtitle_lines = []
        if subtitle:
            words = subtitle.split()
            current_line = []
            max_width = ANNOTATION_WIDTH - 20

            for word in words:
                current_line.append(word)
                test_line = ' '.join(current_line)
                bbox = draw.textbbox((0, 0), test_line, font=subtitle_font)
                if bbox[2] - bbox[0] > max_width:
                    if len(current_line) > 1:
                        current_line.pop()
                        subtitle_lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        subtitle_lines.append(word)
                        current_line = []

            if current_line:
                subtitle_lines.append(' '.join(current_line))

        # Calculate total height and center vertically
        title_height = len(title_lines) * title_line_height
        subtitle_height = len(subtitle_lines) * subtitle_line_height if subtitle_lines else 0
        gap_height = title_subtitle_gap if subtitle_lines else 0
        total_height = title_height + gap_height + subtitle_height
        ann_y = (OUTPUT_HEIGHT - total_height) // 2

        # Draw title lines with shadow
        for i, line in enumerate(title_lines):
            line_y = ann_y + i * title_line_height
            draw.text((ann_x + 2, line_y + 2), line, fill=(0, 0, 0, 150), font=title_font)
            draw.text((ann_x, line_y), line, fill=(255, 255, 255, 255), font=title_font)

        # Draw subtitle lines
        if subtitle_lines:
            sub_y = ann_y + title_height + title_subtitle_gap
            for i, line in enumerate(subtitle_lines):
                line_y = sub_y + i * subtitle_line_height
                draw.text((ann_x + 2, line_y + 2), line, fill=(0, 0, 0, 100), font=subtitle_font)
                draw.text((ann_x, line_y), line, fill=(200, 200, 200, 255), font=subtitle_font)

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

    # Define screenshots with annotations
    images = [
        (
            "Screenshot 2025-12-25 215031.png",
            "1-popup-dark.png",
            {
                'title': 'Dark Theme',
                'subtitle': 'Manage search engines with a sleek dark interface'
            },
            'right'
        ),
        (
            "Screenshot 2025-12-25 215243.png",
            "2-popup-light.png",
            {
                'title': 'Light Theme',
                'subtitle': 'Automatic theme switching to match your preferences'
            },
            'right'
        ),
        (
            "Screenshot 2025-12-25 220054.png",
            "3-context-menu-single.png",
            {
                'title': 'Quick Search',
                'subtitle': 'Right-click selected text to search instantly'
            },
            'right'
        ),
        (
            "Screenshot 2025-12-25 220209.png",
            "4-context-menu-multiple.png",
            {
                'title': 'Multiple Engines',
                'subtitle': 'Choose from all your enabled search engines'
            },
            'right'
        ),
    ]

    for screenshot_name, output_name, annotation, position in images:
        screenshot_path = os.path.join(screenshots_dir, screenshot_name)
        output_path = os.path.join(output_dir, output_name)

        if os.path.exists(screenshot_path):
            create_store_image(screenshot_path, output_path, annotation, position)
        else:
            print(f"Warning: {screenshot_path} not found")

    print(f"\nAll store listing images created in {output_dir}/")
    print(f"  Dimensions: {OUTPUT_WIDTH}x{OUTPUT_HEIGHT} (Chrome Web Store recommended)")

if __name__ == "__main__":
    main()
