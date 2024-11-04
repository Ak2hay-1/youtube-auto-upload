import time, os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_argument("user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome Beta\\User Data\\")
options.binary_location = "C:\\Program Files\\Google\\Chrome Beta\\Application\\chrome.exe"
service = Service("chromedriver.exe")

# Load your hashtags from a file or define them directly in a list
with open('hashtags.txt', 'r') as file:
    hashtags = [line.strip() for line in file if line.strip()]  # Load and strip new lines


def natural_sort_key(s):
    """ Key function to sort filenames in natural order (e.g., vid1, vid2, vid10) """
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]


def get_random_hashtags():
    """ Select 5 random hashtags from the list """
    return random.sample(hashtags, 5)  # Get exactly 5 random hashtags


def upload_video(video_path):
    bot = webdriver.Chrome(service=service, options=options)
    bot.get("https://studio.youtube.com")

    try:
        # Wait for the upload button to be clickable and click it
        upload_button = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="upload-icon"]')))
        upload_button.click()

        # Wait for file input and send the video file path
        file_input = WebDriverWait(bot, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/input')))
        file_input.send_keys(video_path)

        time.sleep(7)  # Wait for the video to upload

        # Get the filename without the extension for the title
        video_title = os.path.splitext(os.path.basename(video_path))[0]
        random_hashtags = ' '.join(get_random_hashtags())

        # Set the title to the video filename and append random hashtags
        full_title = f"{video_title} {random_hashtags}"

        # Add video title and hashtags
        title_input = WebDriverWait(bot, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="textbox"]')))
        title_input.clear()  # Clear the input box first
        title_input.send_keys(full_title)  # Set title

        # Handle "Made for Kids" option (No, it's not made for kids)
        not_made_for_kids_button = WebDriverWait(bot, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//tp-yt-paper-radio-button[@name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]')))
        not_made_for_kids_button.click()

        # Click "Next" three times
        for _ in range(3):
            next_button = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="next-button"]')))
            next_button.click()
            time.sleep(1)

        # Wait for the public publish button and click it to make the video public
        public_button = WebDriverWait(bot, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="privacy-radios"]/tp-yt-paper-radio-button[3]')))
        public_button.click()

        # Confirm publishing by clicking the done button
        done_button = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="done-button"]')))
        done_button.click()

        time.sleep(5)  # Give time to finish the upload
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        bot.quit()


print(
    "\033[1;31;40m IMPORTANT: Put one or more videos in the *videos* folder in the bot directory. Please make sure to name the video files like this --> Ex: vid1.mp4 vid2.mp4 vid3.mp4 etc..")
time.sleep(6)

answer = input(
    "\033[1;32;40m Press 1 if you want to spam the same video or Press 2 if you want to upload multiple videos: ")

if answer == '1':
    nameofvid = input(
        "\033[1;33;40m Put the name of the video you want to upload (Ex: vid.mp4 or myshort.mp4 etc..) ---> ")
    howmany = input("\033[1;33;40m How many times you want to upload this video ---> ")

    for i in range(int(howmany)):
        video_path = os.path.abspath(f'videos/{nameofvid}')
        upload_video(video_path)

elif answer == '2':
    print(
        "\033[1;31;40m IMPORTANT: Please make sure the name of the videos are like this: vid1.mp4, vid2.mp4, vid3.mp4 ... etc")
    dir_path = './videos'
    video_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]

    # Sort video files in natural order (vid1, vid2, vid10 instead of vid1, vid10, vid2)
    video_files.sort(key=natural_sort_key)

    # Ask the user from which video number to start
    start_num = int(input("\033[1;33;40m Enter the video number to start from (e.g., 62 to start from vid62.mp4): "))

    print(f"   {len(video_files)} Videos found in the videos folder, starting from vid{start_num}.mp4...")
    time.sleep(6)

    for i in range(start_num - 1, len(video_files)):
        video_path = os.path.abspath(f'videos/vid{i + 1}.mp4')
        upload_video(video_path)
