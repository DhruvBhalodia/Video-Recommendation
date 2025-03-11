import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize Faker and set seeds for reproducibility
fake = Faker()

# Constants
NUM_USERS = 1000
NUM_CHANNELS = 50
VIDEOS_PER_CHANNEL = 100
MAX_INTERACTIONS_PER_USER = 200

# Updated categories and tags
CATEGORIES = ["Anime", "Tech", "Gaming", "Music", "Education", "Sports", "Comedy", "Cooking", "Fitness", "News"]
probabilities = [0.4, 0.2, 0.3, 0.06, 0.02, 0.01, 0.01, 0, 0, 0]
p2 = [0.1, 0.1, 0.15, 0.15, 0.2, 0.1, 0.1, 0.05, 0.05, 0]
TAGS = {
    "Anime": [
        "Shonen", "Shojo", "Seinen", "Isekai", "Mecha", "Fantasy", "Slice of Life",
        "One Piece", "Attack on Titan", "Naruto", "Demon Slayer", "Jujutsu Kaisen",
        "Studio Ghibli", "My Hero Academia", "Cosplay", "AMV", "Anime Convention",
        "Voice Actors", "Manga Adaptation", "OVA", "Anime Review"
    ],
    "Tech": [
        "Python", "JavaScript", "Machine Learning", "Cloud Computing", "IoT",
        "Cybersecurity", "Blockchain", "Quantum Computing", "AR/VR", "Robotics",
        "Data Science", "Linux", "Open Source", "Startups", "Tech Reviews",
        "DevOps", "API Development", "Computer Vision", "Edge Computing", "5G"
    ],
    "Gaming": [
        "FPS", "RPG", "MMORPG", "Battle Royale", "Speedrunning", "Esports",
        "Game Development", "Retro Gaming", "Indie Games", "VR Gaming",
        "PC Gaming", "Console Wars", "Game Mods", "Walkthrough", "Let's Play",
        "Speedrun", "Game Analysis", "Mobile Gaming", "Simulation", "Survival"
    ],
    "Music": [
        "Pop", "Rock", "Hip-Hop", "EDM", "Classical", "Jazz", "K-Pop",
        "Music Production", "Guitar Covers", "Piano Tutorials", "Live Concerts",
        "Album Reviews", "Music Theory", "Songwriting", "Vinyl Collection",
        "Music Videos", "Lyrics Analysis", "DJ Sets", "Acoustic Sessions",
        "Music History"
    ],
    "Education": [
        "STEM", "Online Courses", "Coding Bootcamps", "Language Learning",
        "University Lectures", "Skill Development", "Career Advice",
        "Documentaries", "Science Experiments", "Book Summaries",
        "Critical Thinking", "Research Papers", "MOOCs", "Khan Academy",
        "Coursera", "TED Talks", "Educational Animation", "History Lessons",
        "Philosophy", "Financial Literacy"
    ],
    "Sports": [
        "Football", "Cricket", "Basketball", "Tennis", "Olympics",
        "Athletics", "Swimming", "Extreme Sports", "Sports Science",
        "Player Interviews", "Match Analysis", "Fantasy Leagues",
        "Sports Medicine", "Training Routines", "Esports",
        "Winter Sports", "Martial Arts", "Cycling", "Gymnastics",
        "Sports Nutrition"
    ],
    "Comedy": [
        "Standup Specials", "Sketch Comedy", "Improv", "Satire",
        "Dark Comedy", "Prank Videos", "Roast Battles", "Parody",
        "Comedy Podcasts", "Sitcom Clips", "Dad Jokes", "Memes",
        "Viral Challenges", "Comedy Roasts", "Wholesome Humor",
        "Political Satire", "Comedy Music", "Pun Compilations",
        "Fail Compilations", "Cringe Comedy"
    ],
    "Cooking": [
        "Gourmet", "Meal Prep", "Street Food", "Baking", "Vegan Recipes",
        "Keto Diet", "Food Challenges", "Culinary Travel", "Kitchen Hacks",
        "Food Science", "MasterChef", "Fermentation", "Mixology",
        "Food Photography", "Restaurant Reviews", "Historical Recipes",
        "Molecular Gastronomy", "Food Trucks", "Zero Waste Cooking",
        "Food Festivals"
    ],
    "Fitness": [
        "Calisthenics", "CrossFit", "Pilates", "Marathon Training",
        "Home Workouts", "Weight Loss Journey", "Physical Therapy",
        "Sports Nutrition", "Yoga Flow", "Powerlifting",
        "Mobility Training", "Athlete Training", "Gym Vlogs",
        "Fitness Challenges", "Bodybuilding", "HIIT Workouts",
        "Mind-Body Connection", "Recovery Techniques", "Fitness Gear",
        "Macro Counting"
    ],
    "News": [
        "Breaking News", "Political Analysis", "Tech News",
        "Environmental Issues", "Global Economy", "Health Updates",
        "Science News", "Entertainment News", "Investigative Journalism",
        "War Reporting", "Financial Markets", "Social Media Trends",
        "Cybersecurity Alerts", "Space Exploration", "Cultural Shifts",
        "Education Reform", "Sports Updates", "Celebrity News",
        "Local Events", "Human Interest"
    ]
}

# Parameterized probabilities and thresholds
PREFERRED_CHANNEL_PROB = 0.8   # 80% interactions come from followed channels
TRENDING_PROB = 0.05           # 5% of videos are trending
LIKE_THRESHOLD = 0.95          # Fully watched videos (>=95%) are liked
MIN_WATCH_FOR_DISLIKE = 0.1    # <10% watch indicates likely dislike

# Helper function: Generate a timestamp with recent bias
def get_weighted_ts(days=365):
    """
    Generate a datetime object between now and 'days' ago.
    """
    return fake.date_time_between(start_date=f'-{days}d', end_date='now')

###############################
# 1. Generate Users
###############################
users = []
for _ in range(NUM_USERS):
    user = {
        "user_id": fake.uuid4(),
        "preferred_category": np.random.choice(
            CATEGORIES, 
            p=np.random.permutation(probabilities)
        ),
        "preferred_length": np.random.choice(["short", "medium", "long"], p=[0.4, 0.5, 0.1]),
        "disliked_category": np.random.choice(
            CATEGORIES, 
            p=np.random.permutation(p2)
        ),
        "attention_span": np.clip(np.random.normal(loc=0.7, scale=0.2), 0, 1)
    }
    users.append(user)
users_df = pd.DataFrame(users)
print("Users generated.")

###############################
# 2. Generate Channels
###############################
channels = []
for _ in range(NUM_CHANNELS):
    channel = {
        "channel_id": fake.uuid4(),
        "primary_category": np.random.choice(CATEGORIES),
        "consistency": np.random.beta(2, 2),  # Likelihood to stick to primary category
        "upload_frequency": np.random.poisson(3)
    }
    channels.append(channel)
channels_df = pd.DataFrame(channels)
print("Channels generated.")

###############################
# 3. Generate Videos
###############################
videos = []
current_date = datetime.now()

for channel in channels:
    for _ in range(VIDEOS_PER_CHANNEL):
        # Determine video category: based on channel's consistency
        if random.random() < channel["consistency"]:
            category = channel["primary_category"]
        else:
            category = np.random.choice(CATEGORIES)
        
        # Generate tags as a comma-separated string
        tags = ",".join(np.random.choice(TAGS[category], size=2, replace=False))
        
        video = {
            "video_id": fake.uuid4(),
            "channel_id": channel["channel_id"],
            "category": category,
            "tags": tags,
            "length": np.random.choice(["short", "medium", "long"], p=[0.4, 0.5, 0.1]),
            "upload_date": get_weighted_ts(180),
            "views": 0,
            "is_trending": False
        }
        
        # Set trending videos based on TRENDING_PROB
        if random.random() < TRENDING_PROB:
            video["views"] = np.random.randint(50000, 100000)
            video["is_trending"] = True
        else:
            video["views"] = np.random.randint(100, 10000)
        
        videos.append(video)
videos_df = pd.DataFrame(videos)
print("Videos generated.")

###############################
# 4. Generate Interactions
###############################
interactions = []

for user in users:
    preferred_category = user["preferred_category"]
    preferred_length = user["preferred_length"]
    disliked_category = user["disliked_category"]
    
    # Sample followed channels based on user's preferred category
    matched_channels = channels_df[channels_df["primary_category"] == preferred_category]
    sample_size = min(3, len(matched_channels))
    followed_channels = (
        matched_channels.sample(sample_size)["channel_id"].tolist()
        if sample_size > 0 else []
    )
    
    num_interactions = np.random.randint(50, MAX_INTERACTIONS_PER_USER)
    
    for _ in range(num_interactions):
        if random.random() < PREFERRED_CHANNEL_PROB and followed_channels:
            candidate_videos = videos_df[
                (videos_df["channel_id"].isin(followed_channels)) &
                (videos_df["category"] != disliked_category)
            ]
            if candidate_videos.empty:
                video = videos_df.sample(1).iloc[0]
            else:
                video = candidate_videos.sample(1).iloc[0]
        else:
            if random.random() < 0.95:
                candidate_videos = videos_df[videos_df["category"] != disliked_category]
            else:
                candidate_videos = videos_df[
                    (videos_df["category"] == disliked_category) &
                    (videos_df["upload_date"] < (current_date - timedelta(days=30)))
                ]
            if candidate_videos.empty:
                video = videos_df.sample(1).iloc[0]
            else:
                video = candidate_videos.sample(1).iloc[0]
        
        # Calculate watch percentage based on user's attention span and video length
        base_watch = user["attention_span"]
        if video["length"] == preferred_length:
            raw_watch_pct = base_watch + np.random.normal(0.2, 0.1)
        else:
            raw_watch_pct = base_watch - np.random.normal(0.3, 0.15)
        
        # Ensure watch percentage is always between 0 and 1
        watch_pct = np.clip(raw_watch_pct, 0, 1)
        
        # Generate interaction record
        interaction = {
            "user_id": user["user_id"],
            "video_id": video["video_id"],
            "watch_percentage": watch_pct,
            "liked": 1 if watch_pct >= LIKE_THRESHOLD else (1 if watch_pct > 0.8 and random.random() < 0.3 else 0),
            "disliked": 1 if watch_pct < MIN_WATCH_FOR_DISLIKE and random.random() < 0.7 else 0,
            "timestamp": get_weighted_ts(90 if video["category"] != disliked_category else 180)
        }
        
        # Fully watched videos are marked as liked and not disliked.
        if watch_pct >= LIKE_THRESHOLD:
            interaction["liked"] = 1
            interaction["disliked"] = 0
        
        interactions.append(interaction)
interactions_df = pd.DataFrame(interactions)
print("Interactions generated.")

###############################
# 5. Save Datasets
###############################
users_df.to_csv("users.csv", index=False)
channels_df.to_csv("channels.csv", index=False)
videos_df.to_csv("videos.csv", index=False)
interactions_df.to_csv("interactions.csv", index=False)

print("Synthetic dataset created successfully!")