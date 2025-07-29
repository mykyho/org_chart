from PIL import Image, ImageDraw, ImageFont
import os

def create_symetra_logo():
    # Create a black background image
    img = Image.new('RGB', (400, 200), color='black')
    draw = ImageDraw.Draw(img)
    
    # Draw the blue wing-like graphic elements
    # Upper curved form
    points_upper = [(50, 60), (100, 40), (150, 50), (200, 45), (250, 55), (300, 50), (350, 60)]
    draw.line(points_upper, fill='#0072cc', width=8)
    
    # Lower curved form (larger)
    points_lower = [(30, 80), (80, 60), (130, 70), (180, 65), (230, 75), (280, 70), (330, 80), (370, 75)]
    draw.line(points_lower, fill='#0072cc', width=10)
    
    # Add SYMETRA text in white
    try:
        font = ImageFont.truetype("Arial", 36)
    except:
        font = ImageFont.load_default()
    
    draw.text((200, 100), "SYMETRA", fill='white', font=font, anchor="mm")
    
    # Add registered trademark symbol
    draw.text((320, 85), "®", fill='white', font=ImageFont.load_default())
    
    # Add tagline
    try:
        small_font = ImageFont.truetype("Arial", 16)
    except:
        small_font = ImageFont.load_default()
    
    draw.text((200, 140), "RETIREMENT | BENEFITS | LIFE", fill='white', font=small_font, anchor="mm")
    
    img.save('symetra_logo.png')
    print("Symetra logo created successfully!")

def create_salesforce_logo():
    # Create a light gray background with grid pattern
    img = Image.new('RGB', (400, 200), color='#f0f0f0')
    draw = ImageDraw.Draw(img)
    
    # Draw grid pattern
    for i in range(0, 400, 20):
        draw.line([(i, 0), (i, 200)], fill='#e0e0e0', width=1)
    for i in range(0, 200, 20):
        draw.line([(0, i), (400, i)], fill='#e0e0e0', width=1)
    
    # Draw the blue cloud shape
    # Main cloud body
    draw.ellipse([100, 60, 300, 120], fill='#00a1e0')
    
    # Cloud bumps
    draw.ellipse([80, 70, 120, 100], fill='#00a1e0')
    draw.ellipse([280, 70, 320, 100], fill='#00a1e0')
    draw.ellipse([120, 50, 180, 90], fill='#00a1e0')
    draw.ellipse([220, 50, 280, 90], fill='#00a1e0')
    
    # Add "salesforce" text in white
    try:
        font = ImageFont.truetype("Arial", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((200, 90), "salesforce", fill='white', font=font, anchor="mm")
    
    img.save('salesforce_logo.png')
    print("Salesforce logo created successfully!")

if __name__ == "__main__":
    create_symetra_logo()
    create_salesforce_logo()
    print("Both logos created successfully!") 