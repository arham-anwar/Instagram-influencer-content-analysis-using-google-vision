import os
import json
import pandas as pd

# Path to the 'Data' directory
data_dir = 'Data'  # Change this to the path of your 'Data' directory

# Prepare a list to store each row's data
data = []

# Traverse through each post's folder inside the 'Data' directory
for post_id in os.listdir(data_dir):
    post_dir = os.path.join(data_dir, post_id)
    
    # Check if it's a directory
    if os.path.isdir(post_dir):
        # List all files and sort them to ensure consistency
        files = sorted(os.listdir(post_dir))
        
        # Initialize variables for post-level data
        comments_count = 0
        likes_count = 0
        followers = 0
        author_name = None
        caption = None  # Initialize post-level caption
        
        # Look for JSON files related to the post
        for file in files:
            if file.endswith('.json'):
                # Read the JSON file
                with open(os.path.join(post_dir, file), 'r') as f:
                    json_data = json.load(f)
                    # Extract post-level data
                    comments_count += json_data["node"]["edge_media_to_comment"]["count"]
                    likes_count += json_data["node"]["edge_media_preview_like"]["count"]
                    author_name = json_data["node"]["owner"]["username"]
                    # Extract caption from the JSON data if available
                    edges = json_data["node"]["edge_media_to_caption"]["edges"]
                    if edges:
                        caption = edges[0]["node"]["text"]
        
        # Count followers from a separate file if available
        followers_file_path = os.path.join(post_dir, 'followers.json')
        if os.path.exists(followers_file_path):
            with open(followers_file_path, 'r') as f:
                followers_data = json.load(f)
                followers = followers_data['followers']
        
        # Iterate through all images found in the post directory
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                image_name = file
                
                # Append the data for the current image to the list
                data.append({'post_id': post_id, 'image_ID': image_name, 'comments_count': comments_count, 'likes_count': likes_count, 'followers': followers, 'author_name': author_name, 'caption': caption})

# Convert the list to a DataFrame
df = pd.DataFrame(data)

# Extract date from image_ID
df['date'] = df['image_ID'].str[:9]
df['year'] = df['date'].str[:4]
df['month'] = df['date'].str[5:7]
df['day'] = df['date'].str[8:]

# Reorder columns
df = df[['post_id', 'image_ID', 'comments_count', 'likes_count', 'followers', 'author_name', 'caption', 'date', 'year', 'month', 'day']]

# Display the DataFrame
from IPython.display import display
pd.set_option('display.max_columns', None)
display(df.head())

# Save output to a CSV file
df.to_csv('tabular_data.csv', index=False)
