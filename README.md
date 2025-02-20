# RSS to Nostr Crossposter (site2nostr)

This script automatically crossposts new items from an RSS feed to the Nostr decentralized social network. It monitors an RSS feed for new content and publishes the title and link of each new item as a note on Nostr.

## Features

*   Automatically posts new RSS feed items to Nostr.
*   Easy configuration via environment variables.
*   Simple and straightforward code.

## Prerequisites

Before you can use this script, you'll need to:

1.  **Install Python:** Make sure you have Python 3.6 or higher installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2.  **Install pip:** Pip is a package installer for Python. It usually comes with Python, but if you don't have it, you can install it following the instructions [here](https://pip.pypa.io/en/stable/installing/).

3.  **Create a Nostr Key:** You'll need a Nostr private key to sign and publish events. If you don't have one, you can generate one using a Nostr client or library. Keep this key safe and secure!

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/j4ckxyz/site2nostr
    cd site2nostr
    ```

    Replace `your-username` and `your-repository-name` with your actual GitHub username and repository name.

2.  **Create a virtual environment:** It's recommended to use a virtual environment to isolate the project dependencies.

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**

    *   On Linux/macOS:

        ```bash
        source venv/bin/activate
        ```

    *   On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file, create one with the following content:

    ```
    feedparser
    pynostr
    ```

    Then run the `pip install -r requirements.txt` command.

## Configuration

You need to set the following environment variables:

*   `FEED_URL`: The URL of the RSS feed you want to crosspost.
*   `NOSTR_PRIVATE_KEY`: Your Nostr private key in `nsec` format.

You can set these variables in your terminal before running the script:

```bash
export FEED_URL="your_rss_feed_url"
export NOSTR_PRIVATE_KEY="your_nostr_private_key"
