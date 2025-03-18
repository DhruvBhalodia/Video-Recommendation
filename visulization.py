import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set plot style
sns.set(style="whitegrid", palette="muted", font_scale=1.1)

# -------------------------------
# 1. Load Data
# -------------------------------
users_df = pd.read_csv("users.csv")
channels_df = pd.read_csv("channels.csv")
videos_df = pd.read_csv("videos.csv")
interactions_df = pd.read_csv("interactions.csv")

# Convert dates to datetime objects
videos_df['upload_date'] = pd.to_datetime(videos_df['upload_date'])
interactions_df['timestamp'] = pd.to_datetime(interactions_df['timestamp'])

# -------------------------------
# 2. Users Data Visualizations
# -------------------------------

# Split the followed_categories into separate rows for analysis
users_categories = users_df['followed_categories'].str.split(',', expand=True).stack().reset_index(drop=True)
users_categories_df = pd.DataFrame(users_categories, columns=['category'])

plt.figure(figsize=(10, 4))
sns.countplot(data=users_categories_df, x='category', 
              order=users_categories_df['category'].value_counts().index)
plt.title("Distribution of Followed Categories (Users)")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Distribution of preferred video lengths
plt.figure(figsize=(6, 4))
sns.countplot(data=users_df, x='preferred_length', order=["short", "medium", "long"])
plt.title("Distribution of Preferred Video Lengths (Users)")
plt.xlabel("Preferred Length")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Distribution of users' attention spans
plt.figure(figsize=(8, 4))
sns.histplot(users_df['attention_span'], bins=30, kde=True)
plt.title("Distribution of User Attention Span")
plt.xlabel("Attention Span")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# -------------------------------
# 3. Channels Data Visualizations
# -------------------------------

# Distribution of primary categories among channels
plt.figure(figsize=(10, 4))
sns.countplot(data=channels_df, x='primary_category',
              order=channels_df['primary_category'].value_counts().index)
plt.title("Distribution of Primary Categories (Channels)")
plt.xlabel("Primary Category")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Distribution of channel consistency (Beta distribution)
plt.figure(figsize=(8, 4))
sns.histplot(channels_df['consistency'], bins=30, kde=True)
plt.title("Distribution of Channel Consistency")
plt.xlabel("Consistency")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Distribution of upload frequencies for channels (Poisson)
plt.figure(figsize=(8, 4))
sns.histplot(channels_df['upload_frequency'], bins=range(0, channels_df['upload_frequency'].max() + 2), kde=False)
plt.title("Distribution of Channel Upload Frequencies")
plt.xlabel("Upload Frequency")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# -------------------------------
# 4. Videos Data Visualizations
# -------------------------------

# Distribution of video categories
plt.figure(figsize=(10, 4))
sns.countplot(data=videos_df, x='category',
              order=videos_df['category'].value_counts().index)
plt.title("Distribution of Video Categories")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Distribution of video lengths
plt.figure(figsize=(6, 4))
sns.countplot(data=videos_df, x='length', order=["short", "medium", "long"])
plt.title("Distribution of Video Lengths")
plt.xlabel("Video Length")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Histogram of video views (use log scale due to large range)
plt.figure(figsize=(10, 5))
sns.histplot(videos_df['views'], bins=50, log_scale=True)
plt.title("Distribution of Video Views (Log Scale)")
plt.xlabel("Views")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Count of trending vs. non-trending videos
plt.figure(figsize=(6, 4))
sns.countplot(data=videos_df, x='is_trending')
plt.title("Trending vs. Non-Trending Videos")
plt.xlabel("Is Trending (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Time-series: Videos uploaded per week (last 180 days)
videos_df['upload_week'] = videos_df['upload_date'].dt.to_period('W').astype(str)
videos_per_week = videos_df.groupby('upload_week').size().reset_index(name='count')
plt.figure(figsize=(12, 6))
sns.lineplot(x='upload_week', y='count', data=videos_per_week, marker="o")
plt.title("Number of Videos Uploaded per Week")
plt.xlabel("Upload Week")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------------
# 5. Interactions Data Visualizations
# -------------------------------

# Distribution of watch percentages
plt.figure(figsize=(8, 4))
sns.histplot(interactions_df['watch_percentage'], bins=50, kde=True)
plt.title("Distribution of Watch Percentage")
plt.xlabel("Watch Percentage")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Distribution of liked interactions
plt.figure(figsize=(6, 4))
sns.countplot(data=interactions_df, x='liked')
plt.title("Distribution of Liked Interactions")
plt.xlabel("Liked (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Distribution of disliked interactions
plt.figure(figsize=(6, 4))
sns.countplot(data=interactions_df, x='disliked')
plt.title("Distribution of Disliked Interactions")
plt.xlabel("Disliked (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Interactions per user (to see potential outliers or sparsity)
interactions_per_user = interactions_df['user_id'].value_counts()
plt.figure(figsize=(10, 4))
sns.histplot(interactions_per_user, bins=50, kde=True)
plt.title("Distribution of Interactions per User")
plt.xlabel("Number of Interactions")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Time-series: Interactions per week
interactions_df['interaction_week'] = interactions_df['timestamp'].dt.to_period('W').astype(str)
interactions_per_week = interactions_df.groupby('interaction_week').size().reset_index(name='count')
plt.figure(figsize=(12, 6))
sns.lineplot(x='interaction_week', y='count', data=interactions_per_week, marker="o")
plt.title("Number of Interactions per Week")
plt.xlabel("Interaction Week")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# -------------------------------
# 6. Merged Analysis & Correlations
# -------------------------------

# Merge interactions with users for additional insights
merged_df = interactions_df.merge(users_df[['user_id', 'attention_span']], on='user_id', how='left')

# Scatter plot: Watch percentage vs. User Attention Span
plt.figure(figsize=(8, 6))
sns.scatterplot(x='attention_span', y='watch_percentage', data=merged_df, alpha=0.3)
plt.title("Watch Percentage vs. User Attention Span")
plt.xlabel("User Attention Span")
plt.ylabel("Watch Percentage")
plt.tight_layout()
plt.show()

# Correlation heatmap for key interaction metrics
plt.figure(figsize=(6, 4))
numeric_cols = ['watch_percentage', 'liked', 'disliked']
corr = interactions_df[numeric_cols].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Correlation Heatmap: Interaction Features")
plt.tight_layout()
plt.show()

# -------------------------------
# 7. Edge Case Checks
# -------------------------------
# Check for users with very few interactions (could be cold-start issues)
few_interactions = interactions_per_user[interactions_per_user < 10]
print("Users with fewer than 10 interactions:")
print(few_interactions)

# Check for videos with zero interactions (could indicate isolated items)
videos_with_interactions = interactions_df['video_id'].value_counts()
videos_no_interaction = videos_df[~videos_df['video_id'].isin(videos_with_interactions.index)]
print(f"Number of videos with zero interactions: {len(videos_no_interaction)}")

# -------------------------------
# End of Visualizations
# -------------------------------
print("Visualization complete!")