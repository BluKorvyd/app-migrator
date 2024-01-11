# app-migrator

This script migrates Android apps using a repository with a JSON file. It downloads the JSON file with the information, downloads APK files for the apps that are installed on the mobile device and available in the repository, and uninstalls the apps in the device. replacing them by installing the APK from repository. 

Note: The repository and the JSON file must have a structure that is compatible with the script for it to work.

## Potential use cases

- Apps remaining the same but changing signature
- Bulk updates where for some reason the apps need to be removed first

## Requirements

- Python 3.x
- `requests` library
- adb

## Usage

1. Download the script and save it to your local machine.
2. Open a terminal window and navigate to the directory where the script is saved.
3. Connect your device to your computer via USB.
4. Enable USB debugging on your device.
5. Run the following command to start the app migration process:

```bash
python app_migration.py
```

6. Enter the direct URL to the index.min.js/index.json of the APK repository when prompted.
7. Wait for the script to complete.
