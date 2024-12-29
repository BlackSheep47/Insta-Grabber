import instaloader

def scrape_instagram_data(profile_name, post_count=10, username=None, password=None, download_stories=False, download_highlights=False, download_comments=False):
    """
    Scrapes posts, stories, highlights, and comments from an Instagram profile, including private profiles if logged in.

    Args:
        profile_name (str): Instagram username to scrape.
        post_count (int): Number of posts to scrape. Defaults to 10.
        username (str): Your Instagram username (for private profiles).
        password (str): Your Instagram password (for private profiles).
        download_stories (bool): Whether to download stories.
        download_highlights (bool): Whether to download highlights.
        download_comments (bool): Whether to download comments for posts.
    """
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Log in if credentials are provided
        if username and password:
            loader.login(username, password)
            print(f"Logged in as {username}")

        # Load the profile
        profile = instaloader.Profile.from_username(loader.context, profile_name)
        
        # Check access to private profiles
        if profile.is_private and not profile.followed_by_viewer:
            print(f"Error: Cannot access private profile '{profile_name}'. You must follow this account.")
            return

        print(f"Scraping {post_count} posts from {profile_name}...")

        # Download posts
        for i, post in enumerate(profile.get_posts()):
            if i >= post_count:
                break

            # Download each post
            loader.download_post(post, target=f"{profile_name}_posts")
            print(f"Downloaded post {i+1}")

            # Download comments if specified
            if download_comments:
                print(f"Downloading comments for post {i+1}...")
                comments = post.get_comments()
                with open(f"{profile_name}_posts/post_{post.shortcode}_comments.txt", "w", encoding="utf-8") as file:
                    for comment in comments:
                        file.write(f"{comment.owner.username}: {comment.text}\n")
                print(f"Comments saved for post {i+1}")

        # Download stories if specified
        if download_stories:
            print(f"Downloading stories from {profile_name}...")
            for story in loader.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    loader.download_storyitem(item, target=f"{profile_name}_stories")
                    print(f"Downloaded story {item.media_id}")

        # Download highlights if specified
        if download_highlights:
            print(f"Downloading highlights from {profile_name}...")
            for highlight in profile.get_highlights():
                for item in highlight.get_items():
                    loader.download_storyitem(item, target=f"{profile_name}_highlights")
                    print(f"Downloaded highlight {item.media_id}")

        print("Scraping completed!")

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: The profile '{profile_name}' does not exist.")
    except instaloader.exceptions.LoginRequiredException:
        print("Error: Login required to access this profile.")
    except instaloader.exceptions.ConnectionException as ce:
        print(f"Error: Connection issue occurred: {ce}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
if __name__ == "__main__":
    profile = input("Enter the Instagram username to scrape: ")
    posts = int(input("Enter the number of posts to scrape: "))
    download_stories = input("Do you want to download stories? (yes/no): ").strip().lower() == "yes"
    download_highlights = input("Do you want to download highlights? (yes/no): ").strip().lower() == "yes"
    download_comments = input("Do you want to download comments? (yes/no): ").strip().lower() == "yes"
    need_login = input("Do you need to log in to access private profiles? (yes/no): ").strip().lower()

    if need_login == "yes":
        user = input("Enter your Instagram username: ")
        passwd = input("Enter your Instagram password: ")
        scrape_instagram_data(profile, posts, user, passwd, download_stories, download_highlights, download_comments)
    else:
        scrape_instagram_data(profile, posts, download_stories=download_stories, download_highlights=download_highlights, download_comments=download_comments)
