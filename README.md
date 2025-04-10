# YWCA Rent Reminder Generator

## NOT OFFICIAL OR AFFILIATED WITH YWCA....I JUST USED THEIR NAME SINCE I'M A RESIDENT AND I'M WORKING ON A SCHOOL PROJECT

## Overview
The YWCA Rent Reminder Generator is a simple Flask web application that creates professional rent reminder notices in the form of downloadable image files. This tool was created to help streamline the rent reminder process for hostel management.

## Acknowledgment
This project uses the YWCA Kenya name and logo for demonstration purposes only. I would like to express my gratitude to the YWCA Hostels in Nairobi where I stayed during my time in Kenya. The supportive environment and services provided by YWCA inspired this project. This application is not officially affiliated with or endorsed by YWCA Kenya or YWCA Hostels.

## Features
- Generates formal rent reminder notices as high-quality PNG images
- Customizable fields: resident name, room number, amount due, and payment due date
- Preview functionality before downloading
- Professional letterhead design with YWCA branding elements
- Responsive web interface

## Installation

### Prerequisites
- Python 3.6 or higher
- Flask
- Pillow (PIL Fork)

### Setup
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ywca-rent-reminder.git
   cd ywca-rent-reminder
   ```

2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```
   pip install flask pillow
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage
1. Fill in the form with relevant details:
   - Resident Name
   - Room/Unit Number
   - Amount Due (in KES)
   - Due Date

2. Click "Preview Notice" to see how the reminder will look

3. Click "Download Notice" to download the notice as a PNG file

## Technical Details
- Built with Flask web framework
- Uses Pillow (PIL) for image generation
- Auto-creates necessary directories and templates on first run
- Implements responsive web design
- Generates high-resolution (300 DPI) notices suitable for printing

## Project Structure
```
ywca-rent-reminder/
│
├── app.py              # Main application file
├── static/             # Static files directory
│   └── ywca_logo.png   # Logo file (downloaded if not present)
├── templates/          # Templates directory
│   └── index.html      # Main HTML form template
└── README.md           # This file
```

## License
This project is for educational and personal use only. Any commercial use or redistribution requires permission from the developer and should respect YWCA Kenya's branding rights.

## Disclaimer
This software is provided "as is", without warranty of any kind. The YWCA name and logo are used with respect and admiration for the organization's work in empowering women and providing quality accommodation services.