# ResidenceReminder

## Overview
ResidenceReminder is a Flask-based web application that creates professional rent reminder notices for property managers and landlords. The application generates high-quality, downloadable PNG images that can be printed or emailed to residents.

## Features
- Creates formal rent reminder notices with professional letterhead design
- Customizable fields: resident name, unit number, amount due, and payment due date
- Preview functionality before downloading
- High-resolution output (300 DPI) suitable for printing
- Responsive web interface for use on various devices
- Automatic logo handling with placeholder fallback

## Installation

### Prerequisites
- Python 3.6 or higher
- Flask
- Pillow (PIL Fork)

### Setup
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/residence-reminder.git
   cd residence-reminder
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
   - Unit Number
   - Amount Due (in $)
   - Due Date

2. Click "Preview Notice" to see how the reminder will look

3. Click "Download Notice" to download the notice as a PNG file

## Customization
- To change the default property name, edit the variables in the script:
  - `org_text` variable in the `create_rent_reminder` function
  - `address_lines` list in the same function
- To use your own logo, place it in the `static` directory as `parkview_logo.png`
- Font and color schemes can be modified in the respective variables

## Technical Details
- Built with Flask web framework
- Uses Pillow (PIL) for image generation
- Auto-creates necessary directories and templates on first run
- Uses responsive design for better user experience across devices
- Generates professional-looking documents with subtle design details like watermarks and texture

## Project Structure
```
residence-reminder/
│
├── app.py              # Main application file
├── static/             # Static files directory
│   └── parkview_logo.png   # Logo file (downloaded if not present)
├── templates/          # Templates directory
│   └── index.html      # Main HTML form template
└── README.md           # This file
```

## Use Case: Parkview Apartments
The default configuration uses "Parkview Apartments" as an example implementation. The system can be easily customized for any residential property by modifying the property name, logo, and contact information.

## License
This project is open source and available under the MIT License.

## Credits
- Created by [Your Name]
- Inspired by the need for streamlined property management communications
- Uses Flask, PIL, and other open-source libraries

## Future Enhancements
- Multiple notice templates (payment confirmation, maintenance alerts)
- Email integration for direct sending
- User accounts for property managers
- Resident database integration
- Multilingual support