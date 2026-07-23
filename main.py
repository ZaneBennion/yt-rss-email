import os
from dotenv import load_dotenv
import state
import youtube
import email_sender

# Load local .env variables if running locally (ignored by GitHub Actions)
load_dotenv('.env.local')

def main():
    handles = state.get_handles()
    cache = state.load_cache()
    history = state.load_history()
    
    all_videos = []
    
    # 1. Resolve handles to Channel IDs and cache them
    cache_updated = False
    for handle in handles:
        if handle not in cache:
            print(f"Resolving new handle: {handle}")
            channel_id = youtube.resolve_handle(handle)
            if channel_id:
                cache[handle] = channel_id
                cache_updated = True
            else:
                print(f"Could not resolve handle: {handle}")
                
    if cache_updated:
        state.save_cache(cache)

    # 2. Fetch RSS feeds for all cached channels
    for handle, channel_id in cache.items():
        # Clean up cache if handle was removed from handles.txt
        if handle not in handles:
            continue
            
        print(f"Fetching RSS for: {handle}")
        all_videos.extend(youtube.fetch_videos(channel_id))

    # 3. Sort globally by publish date (newest first)
    all_videos.sort(key=lambda x: x['published_dt'], reverse=True)

    # 4. Take the absolute top 10 freshest videos, THEN filter out the ones we've sent
    top_10_overall = all_videos[:10]
    new_videos = [v for v in top_10_overall if v['id'] not in history]

    # 5. Send Email
    print(f"Sending {len(new_videos)} videos...")
    email_sender.send_email(new_videos)

    # 6. Update History
    # We now just save the IDs of the top 10 overall videos so we don't send them tomorrow
    new_history = [v['id'] for v in top_10_overall]
    state.save_history(new_history)
    print("History updated.")

if __name__ == "__main__":
    main()
