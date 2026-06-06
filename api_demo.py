import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url)

posts = response.json()

df = pd.DataFrame(posts)

df.to_csv(
    "data/api_posts.csv",
    index=False
)

print("API Dataset Saved")
print(df.head())

