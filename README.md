# YouTube RSS Email Script

This script runs on a github action once a day and sends you an email with the latest videos from the channels you want.
It pulls the RSS feeds for each channel listed in `handels.txt`, sorts each video by date/time published, and sends you
the latest 10 videos. It stores the 10 videos it sends you so you wont get repeat entries.

I made this script because there's a lot of YouTube channels I enjoy, but I find myself wasting a lot of time
on recommended videos when I only went to YouTube to check up on my subscriptions. With this script, you'll
stay up to date on the videos from the channels you care about but don't have to risk getting sucked into
YouTube rabbit holes.

## Credentials

You're going to need 2 things to set this up for yourself
1. A Google Cloud API key that has access to the YouTube Data API
(to take the list of handles and return the channel IDs which can be used to get the RSS feed for a channel)
2. Get SMTP credentials with whoever you use as your email provider

## Setup

- Fork this repository
- Customize the CRON schedule in the Github Action to run the script when you want
- Delete `history.json` and `channel_cache.json`, these files are used as caches and are automatically created when the script runs
- Change `handles.txt` to the channels you'd like to see
- Change `Settings -> Actions -> General -> Workflow permissions` to Read and write permissions, so your action can commit the JSON files it generates
- Check `.env.example` to see the names of the credentials you need
- Add those credentials here: `Settings -> Secrets and variables -> Actions -> New repository secret`
