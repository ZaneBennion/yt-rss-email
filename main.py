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

    # 4. Filter out videos we've already sent, then take top 10
    new_videos = [v for v in all_videos if v['id'] not in history][:10]

    # 5. Send Email
    print(f"Sending {len(new_videos)} videos...")
    email_sender.send_email(new_videos)

    # 6. Update History
    if new_videos:
        new_history = [v['id'] for v in new_videos] + history
        state.save_history(new_history)
        print("History updated.")

if __name__ == "__main__":
    main()
