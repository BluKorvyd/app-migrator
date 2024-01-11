import json
import os
import subprocess
import sys
import requests

from typing import List, Dict, Any

def validate_url(url: str) -> bool:
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def download_apk(apk_url: str, apk_file: str) -> None:
    response = requests.get(apk_url)
    with open(apk_file, "wb") as f:
        f.write(response.content)

def run_shell_command(params: List[str]) -> None:
  result = subprocess.run(params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  if result.returncode == 0:
    print(result.stdout.decode().strip())
  else:
    print(result.stderr.decode().strip())


def migrate_apps(url: str) -> None:
  # Download JSON file from URL
  response = requests.get(url)
  data = json.loads(response.text)

  # Get list of installed package names and find common packages
  adb_output = subprocess.check_output(["adb", "shell", "pm", "list", "packages"]).decode("utf-8")
  installed_packages = [line.replace("package:", "").strip() for line in adb_output.split("\n") if line]
  common_packages = [item for item in data if item["pkg"] in installed_packages]

  successes: List[str] = []
  failures: List[str] = []
  total: int = len(common_packages)
  print(f"Found a total of {total} matching apps.")
  print()

  # Download APK files, and replace the apps
  for index in range(len(common_packages)):
      try:
        item: Dict[str, Any] = common_packages[index]
        app_name: str = item["name"]
        package_name: str = item["pkg"]
        apk_filename: str = item["apk"]
        count: int = index + 1

        print(f"[{count}/{total}] Downloading APK for {app_name}...")
        apk_url = os.path.join(url.rstrip("index.min.json"), "apk", apk_filename)
        apk_file = os.path.join(os.getcwd(), apk_filename)
        download_apk(apk_url, apk_file)
            
        print(f"[{count}/{total}] Uninstalling {app_name}...")
        run_shell_command(["adb", "uninstall", package_name])

        print(f"[{count}/{total}] Installing {app_name}...")
        run_shell_command(["adb", "install", apk_file])

        print(f"[{count}/{total}] Removing APK for {app_name}...")
        os.remove(apk_file)
        print(f"[{count}/{total}] Successfully replaced {app_name}.")
        print()

        successes.append(app_name)
      except Exception as ex:
        failures.append(app_name)
        print(f"[{count}/{total}] Error replacing {app_name}: {ex}", file=sys.stderr)
        print()

  print(f"Finished.")
  print(f"Successes: {len(successes)}/{total}.")
  print(f"Failures: {len(failures)}/{total}.{' Please check the error log.' if len(failures) > 0 else ''}")


if __name__ == "__main__":
    url = input("Enter the direct URL to the index.min.js/index.json of the APK repository: ")
    while not validate_url(url):
      url = input("Enter the direct URL to the index.min.js/index.json of the APK repository: ")
    migrate_apps(url)
