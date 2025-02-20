#!/usr/bin/env python3
import time
import feedparser
import re
import os
from html import unescape

from pynostr.event import Event
from pynostr.relay_manager import RelayManager
from pynostr.key import PrivateKey

# ---------------- Configurations ----------------

# Configure these environment variables:
# - FEED_URL: The URL of the RSS feed to crosspost.
# - NOSTR_PRIVATE_KEY: Your Nostr private key in nsec format.

FEED_URL = os.environ.get("FEED_URL")
NOSTR_PRIVATE_KEY = os.environ.get("NOSTR_PRIVATE_KEY")

# List of Nostr relays to publish to.  You can add or remove relays as desired.
NOSTR_RELAYS = [
    "wss://relay.damus.io/",
    "wss://relay.snort.social/",
    "wss://relay.nostr.band/",
    "wss://relay.primal.net/",
    "wss://relay.highlighter.foundation/",
    "wss://relay.nsecbunker.com/",
    "wss://relay.snort.social/",
    "wss://relay.nsecbunker.com/"
]

CHECK_INTERVAL = 30  # Check every 30 seconds

# ---------------- Helper Functions ----------------

def strip_html_tags(text):
    """Remove HTML tags and decode HTML entities from text"""
    text = unescape(text)
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def build_nostr_entry(entry):
    """
    Build a string from the feed entry that includes the title and link.
    """
    title = entry.get('title', 'New Post')
    link = entry.get('link', '')
    content = f"{title}\n\n{link}"

    # If you want to post the content instead of the title and link,
    # uncomment the following lines and comment out the lines above.
    # content = entry.get("content", [{}])[0].get("value", "").strip() or \
    #           entry.get("summary", "").strip() or \
    #           entry.get("description", "").strip()
    # content = strip_html_tags(content)

    return content.strip()

def create_nostr_event(message_content, relay_manager, priv_key):
    """
    Build, sign, and publish the event to the configured Nostr relays.
    """
    try:
        if not message_content:
            print("No content found for this entry. Skipping...")
            return False

        # Create the event with kind=1 (a standard text note)
        event = Event(message_content, kind=1)

        # Sign with the private key
        event.sign(priv_key.hex())

        # Publish the event through the relay manager
        relay_manager.publish_event(event)
        relay_manager.run_sync()

        print("Published to Nostr with content:")
        print(message_content)
        return True
    except Exception as e:
        print(f"Submitting to Nostr failed: {e}")
        return False

def fetch_latest_feed_entry(feed_url):
    """
    Fetch and return the most recent entry from the feed
    """
    feed = feedparser.parse(feed_url)
    if not feed.entries:
        return None
    return feed.entries[0]

# ---------------- Main Function ----------------

def main():
    # Check if required environment variables are set
    if not FEED_URL:
        print("Error: FEED_URL environment variable not set.")
        return
    if not NOSTR_PRIVATE_KEY:
        print("Error: NOSTR_PRIVATE_KEY environment variable not set.")
        return

    # Initialize Nostr
    priv_key = PrivateKey.from_nsec(NOSTR_PRIVATE_KEY)
    relay_manager = RelayManager()
    for relay in NOSTR_RELAYS:
        relay_manager.add_relay(relay)
    time.sleep(1.5)

    # Main loop
    last_published_link = None
    while True:
        try:
            latest_entry = fetch_latest_feed_entry(FEED_URL)
            if not latest_entry:
                print("No entries found in the feed.")
            else:
                # Check if the post is new
                if latest_entry.get("link") != last_published_link:
                    message_content = build_nostr_entry(latest_entry)
                    success = create_nostr_event(message_content, relay_manager, priv_key)
                    if success:
                        last_published_link = latest_entry.get("link")
                        print("Event published successfully!")
                else:
                    print("No new posts to publish.")

        except Exception as e:
            print(f"Error in main loop: {e}")

        # Wait before checking again
        time.sleep(CHECK_INTERVAL)

    relay_manager.close_connections()

if __name__ == "__main__":
    main()
