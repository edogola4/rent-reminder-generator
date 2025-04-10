from PIL import Image, ImageDraw, ImageFont
import os
import urllib.request
from io import BytesIO
from datetime import datetime
import random

def get_logo(local_path="ywca_logo.png", 
             download_url="https://ywcanairobi.org/wp-content/uploads/2022/05/YWCA-logo.png"):
    """
    Attempts to load the logo from a local file.
    If the file doesn't exist, tries to download it from the provided URL.
    """
    if os.path.exists(local_path):
        try:
            return Image.open(local_path).convert("RGBA")
        except Exception as e:
            print(f"Error opening local logo file '{local_path}': {e}")
    
    try:
        with urllib.request.urlopen(download_url) as response:
            logo_data = response.read()
        logo = Image.open(BytesIO(logo_data)).convert('RGBA')
        logo.save(local_path)
        return logo
    except Exception as e:
        print(f"Could not download logo from URL: {e}")
        return None

def create_rent_reminder(resident_name="Resident", room_number="", amount_due="", due_date="10th"):
    """
    Creates a formal rent reminder notice styled like an A4 letter.
    
    Parameters:
    - resident_name: Name of the resident
    - room_number: Room or apartment number
    - amount_due: Amount of rent due
    - due_date: Date when rent is due (default: 10th)
    """
    # Approximate A4 size at 300 dpi for higher quality: 2480 x 3508 pixels
    a4_width, a4_height = 2480, 3508
    image = Image.new('RGB', (a4_width, a4_height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Scale all dimensions for higher resolution
    scale_factor = 4  # Since we went from ~72dpi to 300dpi
    
    # Margins and Layout
    margin_left   = 200 * scale_factor // 4
    margin_right  = 200 * scale_factor // 4
    margin_top    = 240 * scale_factor // 4
    margin_bottom = 240 * scale_factor // 4
    
    # Colors
    accent_color = (0, 85, 164)       # YWCA blue
    light_gray   = (230, 230, 230)    # Divider lines
    black        = (0, 0, 0)
    
    # Try to use professional serif fonts
    try:
        # For Windows/Mac common fonts
        header_font = ImageFont.truetype("Times New Roman.ttf", 24 * scale_factor // 3)
        subheader_font = ImageFont.truetype("Times New Roman.ttf", 16 * scale_factor // 3)
        text_font = ImageFont.truetype("Times New Roman.ttf", 16 * scale_factor // 3)
        footer_font = ImageFont.truetype("Times New Roman.ttf", 14 * scale_factor // 3)
        small_font = ImageFont.truetype("Times New Roman.ttf", 12 * scale_factor // 3)
    except IOError:
        try:
            # Try common Linux fonts
            header_font = ImageFont.truetype("DejaVuSerif.ttf", 24 * scale_factor // 3)
            subheader_font = ImageFont.truetype("DejaVuSerif.ttf", 16 * scale_factor // 3)
            text_font = ImageFont.truetype("DejaVuSerif.ttf", 16 * scale_factor // 3)
            footer_font = ImageFont.truetype("DejaVuSerif.ttf", 14 * scale_factor // 3)
            small_font = ImageFont.truetype("DejaVuSerif.ttf", 12 * scale_factor // 3)
        except IOError:
            # Fallback to default
            print("Warning: Preferred fonts not found, using default fonts")
            header_font = ImageFont.load_default()
            subheader_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            footer_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
    
    # ----------------------------
    # 1) HEADER SECTION
    # ----------------------------
    header_height = 100 * scale_factor // 3
    
    # Create subtle letterhead with very light gray
    draw.rectangle(
        [(0, 0), (a4_width, header_height)],
        fill=(248, 248, 248)  # very light gray for the header bar
    )
    
    # Load/Insert Logo
    logo = get_logo()
    if logo:
        # Resize logo to fit nicely in the header
        max_logo_width, max_logo_height = 120 * scale_factor // 3, 50 * scale_factor // 3
        logo.thumbnail((max_logo_width, max_logo_height), resample=Image.LANCZOS)
        # Place the logo near the left margin, vertically centered in the header
        logo_x = margin_left
        logo_y = (header_height - logo.height) // 2
        # Composite for handling transparency
        logo_bg = Image.new('RGBA', logo.size, (255, 255, 255, 0))  # Transparent background
        logo_composite = Image.alpha_composite(logo_bg, logo)
        image.paste(logo_composite.convert('RGB'), (logo_x, logo_y), logo_composite.getchannel('A'))
    else:
        # Fallback if no logo
        fallback_width, fallback_height = 120 * scale_factor // 3, 50 * scale_factor // 3
        fallback_x = margin_left
        fallback_y = (header_height - fallback_height) // 2
        draw.rectangle(
            [(fallback_x, fallback_y), (fallback_x + fallback_width, fallback_y + fallback_height)],
            fill=accent_color
        )
        draw.text(
            (fallback_x + 10, fallback_y + 10),
            "YWCA",
            fill='white',
            font=subheader_font
        )
    
    # Draw the main header text on the right
    org_text = "YWCA Kenya\nEmpowering Women, Transforming Communities"
    org_lines = org_text.split("\n")
    line_y = margin_top - 30 * scale_factor // 3
    for line in org_lines:
        bbox = draw.textbbox((0, 0), line, font=subheader_font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            (a4_width - margin_right - w, line_y),
            line,
            fill=black,
            font=subheader_font
        )
        line_y += h + 5
    
    # Add a dividing line after the header
    draw.line(
        [(margin_left, header_height + 10 * scale_factor // 3), 
         (a4_width - margin_right, header_height + 10 * scale_factor // 3)],
        fill=light_gray, 
        width=1
    )
    
    # Add a large centered header text just below
    header_str = "RENT REMINDER NOTICE"
    bbox = draw.textbbox((0, 0), header_str, font=header_font)
    w_header, h_header = bbox[2] - bbox[0], bbox[3] - bbox[1]
    header_x = (a4_width - w_header) // 2
    header_y = header_height + 60 * scale_factor // 3
    draw.text((header_x, header_y), header_str, fill=black, font=header_font)
    
    # ----------------------------
    # 2) MAIN CONTENT
    # ----------------------------
    # Start main content below header
    content_start_y = header_y + h_header + 30 * scale_factor // 3
    
    # Add a reference number and date at the top right of content area
    current_date = datetime.now().strftime("%d/%m/%Y")
    ref_num = f"RMR/{random.randint(1000, 9999)}/{datetime.now().year}"
    
    date_text = f"Date: {current_date}"
    ref_text = f"Reference: {ref_num}"
    
    # Position these elements on the right side
    bbox = draw.textbbox((0, 0), date_text, font=text_font)
    date_w = bbox[2] - bbox[0]
    draw.text(
        (a4_width - margin_right - date_w, content_start_y),
        date_text,
        fill=black,
        font=text_font
    )
    
    bbox = draw.textbbox((0, 0), ref_text, font=text_font)
    ref_w = bbox[2] - bbox[0]
    ref_h = bbox[3] - bbox[1]
    draw.text(
        (a4_width - margin_right - ref_w, content_start_y + ref_h + 10),
        ref_text,
        fill=black,
        font=text_font
    )
    
    # Address block on left
    address_start_y = content_start_y + 40 * scale_factor // 3
    
    address_lines = [
        "YWCA Hostels",
        "Mamlaka Road, Nairobi",
        "P.O. Box 40112-00100, Nairobi, Kenya",
        "Tel: +254 (0) 20 2724789",
        "Email: info@ywcahostels.co.ke"
    ]
    
    for line in address_lines:
        bbox = draw.textbbox((0, 0), line, font=text_font)
        h_line = bbox[3] - bbox[1]
        draw.text((margin_left, address_start_y), line, fill=black, font=text_font)
        address_start_y += h_line + 5
    
    # Add some space
    content_start_y = address_start_y + 60 * scale_factor // 3
    
    # Resident information in a subtle box
    if room_number:
        resident_info = f"Room/Unit: {room_number}"
        if resident_name and resident_name.lower() != "resident":
            resident_info = f"Resident: {resident_name}\n{resident_info}"
        
        # Draw a light box around resident info
        bbox = draw.multiline_textbbox((0, 0), resident_info, font=text_font)
        info_height = bbox[3] - bbox[1] + 20 * scale_factor // 3
        info_width = a4_width - margin_left - margin_right
        
        draw.rectangle(
            [(margin_left, content_start_y), 
             (margin_left + info_width, content_start_y + info_height)],
            fill=(248, 248, 248),  # Very light gray
            outline=(220, 220, 220)  # Slightly darker for border
        )
        
        # Draw the resident info text
        draw.multiline_text(
            (margin_left + 10 * scale_factor // 3, content_start_y + 10 * scale_factor // 3),
            resident_info,
            fill=black,
            font=text_font
        )
        
        content_start_y += info_height + 20 * scale_factor // 3
    
    # Greeting
    greeting_text = f"Dear {resident_name},"
    draw.text((margin_left, content_start_y), greeting_text, fill=black, font=text_font)
    bbox = draw.textbbox((0, 0), greeting_text, font=text_font)
    g_h = bbox[3] - bbox[1]
    content_start_y += g_h + 15 * scale_factor // 3
    
    # Body text - create more professional and detailed message
    body_text = f"""This is a formal reminder that your rent payment for the current month is due by the {due_date} of this month."""
    
    if amount_due:
        body_text += f" The amount due is KES {amount_due}."
    
    body_text += """

Please ensure your payment is submitted on time to avoid any late fee charges that may be applicable according to your tenancy agreement.

Payment can be made through the following methods:
• M-Pesa Paybill: 123456, Account: Your Room Number
• Direct deposit to our bank account
• Cash payment at the management office during office hours

If you have already made your payment, kindly disregard this notice and provide proof of payment to the management office for our records.
"""
    
    # Draw body text with proper line spacing
    lines = body_text.split('\n')
    for line in lines:
        if not line:  # Empty line for paragraph break
            content_start_y += 15 * scale_factor // 3
            continue
            
        # Handle text wrapping for long lines
        words = line.split()
        if words:
            current_line = words[0]
            for word in words[1:]:
                test_line = current_line + " " + word
                bbox = draw.textbbox((0, 0), test_line, font=text_font)
                test_width = bbox[2] - bbox[0]
                
                if test_width <= a4_width - margin_left - margin_right:
                    current_line = test_line
                else:
                    # Draw current line and start a new one
                    draw.text((margin_left, content_start_y), current_line, fill=black, font=text_font)
                    bbox = draw.textbbox((0, 0), current_line, font=text_font)
                    line_height = bbox[3] - bbox[1]
                    content_start_y += line_height + 5
                    current_line = word
                    
            # Draw the last line
            draw.text((margin_left, content_start_y), current_line, fill=black, font=text_font)
            bbox = draw.textbbox((0, 0), current_line, font=text_font)
            line_height = bbox[3] - bbox[1]
            content_start_y += line_height + 5
    
    # Closing and signature
    content_start_y += 30 * scale_factor // 3
    closing_text = "Thank you for your prompt attention to this matter."
    draw.text((margin_left, content_start_y), closing_text, fill=black, font=text_font)
    
    # Add signature space
    content_start_y += 80 * scale_factor // 3
    signature_text = "YWCA Hostels Management"
    draw.text((margin_left, content_start_y), signature_text, fill=black, font=text_font)
    
    # Add a manager name and title
    content_start_y += 25 * scale_factor // 3
    manager_text = "Mary Wanjiku\nHostel Manager"
    draw.text((margin_left, content_start_y), manager_text, fill=black, font=small_font)
    
    # ----------------------------
    # 3) FOOTER SECTION
    # ----------------------------
    footer_height = 50 * scale_factor // 3
    footer_y = a4_height - footer_height - margin_bottom
    
    # Light gray line to separate content from footer
    draw.line([(margin_left, footer_y), (a4_width - margin_right, footer_y)], fill=light_gray, width=1)
    
    # Footer text with disclaimer and reference number
    footer_text = "This is an automated notice generated by our system. If you have questions, please contact the management office."
    ref_str = f"Ref: YWCA-RR-{datetime.now().year}-{random.randint(100, 999)}"
    
    # Print date at bottom-left
    bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_text_h = bbox[3] - bbox[1]
    draw.text(
        (margin_left, footer_y + (footer_height - footer_text_h) // 2),
        footer_text,
        fill=(100, 100, 100),  # Darker gray for footer text
        font=footer_font
    )
    
    # Print reference at bottom-right
    bbox = draw.textbbox((0, 0), ref_str, font=footer_font)
    ref_w, ref_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        (a4_width - margin_right - ref_w, footer_y + footer_height + 10),
        ref_str,
        fill=(100, 100, 100),  # Darker gray
        font=footer_font
    )
    
    # Add a subtle watermark or background element for authenticity
    watermark_text = "OFFICIAL NOTICE"
    watermark_font = subheader_font
    bbox = draw.textbbox((0, 0), watermark_text, font=watermark_font)
    w_mark, h_mark = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Position at an angle in the background
    # We'll just put it in the center, very light
    draw.text(
        ((a4_width - w_mark) // 2, (a4_height - h_mark) // 2),
        watermark_text,
        fill=(245, 245, 245),  # Very light gray
        font=watermark_font
    )
    
    # Optional: Add subtle texture or noise for a more printed look
    if random.random() > 0.5:  # 50% chance to add noise
        # Add very slight noise to simulate paper texture
        for _ in range(5000):
            x = random.randint(0, a4_width - 1)
            y = random.randint(0, a4_height - 1)
            # Very subtle light gray dots
            image.putpixel((x, y), (240, 240, 240))
    
    # ----------------------------
    # 4) SAVE THE FINAL IMAGE
    # ----------------------------
    output_filename = "rent_reminder_notice.png"
    image.save(output_filename, dpi=(300, 300))
    print(f"Official rent reminder notice created successfully! Saved as {output_filename}")
    
    # Return the image for potential further processing
    return image

if __name__ == "__main__":
    # Example usage with customization options
    create_rent_reminder(
        resident_name="Bran Don",  # Change to specific name or leave as "Resident"
        room_number="B-204",       # Optional room number
        amount_due="15,000",       # Optional amount due
        due_date="10th"            # Default is 10th
    )