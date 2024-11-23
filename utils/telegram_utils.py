import os
import requests


def api_url(token, method):
    return f"https://api.telegram.org/bot{token}/{method}"


def telegram_command(name, data=None, files=None):
    """
    Makes a POST request to the Telegram Bot API.

    Args:
        name (str): The method name (e.g., 'sendMessage' or 'sendVideo').
        data (dict): The payload for the API request.
        files (dict): Files to be sent with the request (e.g., video file).

    Returns:
        Response object from the requests.post call.
    """
    TELEGRAM_ACCESS_TOKEN = os.environ['TELEGRAM_ACCESS_TOKEN']
    url = api_url(token=TELEGRAM_ACCESS_TOKEN, method=name)

    if files:
        response = requests.post(url, data=data, files=files)
    else:
        response = requests.post(url, json=data)

    # Error handling: check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to send request: {response.status_code}, {response.text}")

    return response.json()


def telegram_sendMessage(text: str, chat_id: str, notify=False):
    """
    Sends a message to a Telegram chat.

    Args:
        text (str): The message text.
        chat_id (str): The chat ID or username (e.g., '@channel_name').
        notify (bool): Whether or not to send a notification.

    Returns:
        Response object from the API.
    """
    if not text:
        # Do nothing if text is missing
        print("No text provided. Skipping message post.")
        return

    return telegram_command('sendMessage', {
        'text': text,
        'chat_id': chat_id,
        'parse_mode': 'markdown',  # Optional: Can be 'html' or 'markdown'
        'disable_notification': not notify  # Send without notification if False
    })


def telegram_sendVideo(video_path: str, chat_id: str, caption: str = None, notify=False):
    """
    Sends a video to a Telegram chat.

    Args:
        video_path (str): Path to the video file.
        chat_id (str): The chat ID or username (e.g., '@channel_name').
        caption (str): Optional caption for the video.
        notify (bool): Whether or not to send a notification.

    Returns:
        Response object from the API.
    """
    if not os.path.exists(video_path):
        # Do nothing if the video file is missing
        print(f"No video file found at: {video_path}. Skipping video post.")
        return

    if not caption:
        # Do nothing if the caption is missing
        print("No caption provided. Skipping video post.")
        return

    with open(video_path, 'rb') as video_file:
        return telegram_command(
            'sendVideo',
            data={
                'chat_id': chat_id,
                'caption': caption,
                'disable_notification': not notify
            },
            files={'video': video_file}
        )

