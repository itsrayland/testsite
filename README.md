# Airtable Manager

A modern web interface for managing Airtable bases. This interface provides a user-friendly way to view, add, edit, and delete records across all tables in your Airtable base.

## Features

- Tabbed interface for easy navigation between tables
- View all records in each table
- Add new records with form validation
- Edit existing records
- Delete records with confirmation
- Support for all Airtable field types
- Responsive design that works on all screen sizes
- Modern UI with Bootstrap 5

## Setup

1. Clone this repository
2. Copy `airtable-config.template.js` to `airtable-config.js`
3. Edit `airtable-config.js` and add your Airtable credentials:
   ```javascript
   const AIRTABLE_CONFIG = {
       PAT: "your_personal_access_token_here",
       BASE_ID: "your_base_id_here"
   };
   ```
4. Open `airtable-manager.html` in a web browser
5. The interface will automatically connect to your Airtable base using your configured credentials

## Security Note

The `airtable-config.js` file contains sensitive credentials and is excluded from Git via `.gitignore`. Never commit this file to version control.

## Usage

1. Click on a table tab to view its records
2. Use the "Add Record" button to create new records
3. Use the edit and delete buttons on each row to modify or remove records
4. All changes are saved directly to your Airtable base

## Dependencies

- Bootstrap 5.3.0
- Bootstrap Icons 1.7.2

## License

MIT License 