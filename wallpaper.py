#!/usr/bin/python3

import os
import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime

# URL of the NOAA directory page
PAGE_URL = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/"
DESTINATION_FOLDER = os.path.expanduser("~/scripts/FullDisk")


def get_latest_high_res_image_url():
    """Scrape the NOAA page to find the latest high-resolution image URL."""
    try:
        response = requests.get(PAGE_URL)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        # Filter for the 21696x21696 images
        high_res_images = [
            link['href'] for link in links
            if link['href'].endswith("21696x21696.jpg")
        ]

        if not high_res_images:
            print("No high-resolution images found.")
            return None

        # Get the latest image (last in the list, assuming sorted order)
        latest_image = sorted(high_res_images)[-1]
        full_url = PAGE_URL + latest_image
        print(f"Latest high-res image URL: {full_url}")
        return full_url
    except Exception as e:
        print(f"Error fetching latest image URL: {e}")
        return None


def download_image(image_url):
    """Download the image from the given URL with a timestamped filename."""
    try:
        if not os.path.exists(DESTINATION_FOLDER):
            os.makedirs(DESTINATION_FOLDER)

        # Generate a timestamped filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        image_filename = f"NOAA_FullDisk_{timestamp}.jpg"
        image_path = os.path.join(DESTINATION_FOLDER, image_filename)

        # Download the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Downloaded the latest image to {image_path}.")
        return image_path
    except Exception as e:
        print(f"Error downloading the image: {e}")
        return None


def set_wallpaper(image_path):
    """Set the downloaded image as the wallpaper."""
    try:
        # AppleScript to set the wallpaper
        script = f"""
        tell application "System Events"
            set theDesktops to a reference to every desktop
            repeat with aDesktop in theDesktops
                set picture of aDesktop to "{image_path}"
            end repeat
        end tell
        """
        process = subprocess.Popen(["osascript", "-e", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            print("Wallpaper updated successfully.")
            return True
        else:
            print(f"Error setting wallpaper: {stderr.decode()}")
            return False
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return False


def cleanup_folder(exclude_path):
    """Delete all files in the destination folder except the specified file."""
    try:
        files = [os.path.join(DESTINATION_FOLDER, f) for f in os.listdir(DESTINATION_FOLDER)]
        for file in files:
            if file != exclude_path and os.path.isfile(file):
                os.remove(file)
                print(f"Deleted: {file}")
    except Exception as e:
        print(f"Error during cleanup: {e}")


def main():
    # Get the latest image URL and download the new image
    image_url = get_latest_high_res_image_url()
    if image_url:
        image_path = download_image(image_url)
        if image_path:
            # Set the wallpaper and clean up old files
            if set_wallpaper(image_path):
                cleanup_folder(image_path)


if __name__ == "__main__":
    main()

