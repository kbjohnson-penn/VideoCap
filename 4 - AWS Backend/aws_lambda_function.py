import boto3
import csv
import json
import re
import random
from io import StringIO
from collections import defaultdict

# Survey URL variable
SURVEY_URL = "" # Enter your base survey URL here

def generate_random_number(length=8):
    digits = [str(x) for x in range(10)]
    random_number = ''.join(random.choice(digits) for _ in range(length))
    return random_number

def extract_part_number(filename):
    match = re.match(r"^(.*_Part_)(\d+)(\.mp4)$", filename)
    return int(match.group(2)) if match else 0

def read_state(s3_client, bucket, state_key):
    try:
        response = s3_client.get_object(Bucket=bucket, Key=state_key)
        state_data = response['Body'].read().decode('utf-8').strip()
        if state_data:
            return list(map(int, state_data.split()))
        else:
            # Return default values if the file is empty
            return [0, 0, 0]
    except Exception as e:
        print(f"Error reading state: {e}")
        # Return default values if there's an error reading the file
        return [0, 0, 0]

def write_state(s3_client, bucket, state_key, video_index, round_index, batch_index):
    state_data = f"{video_index} {round_index} {batch_index}"
    s3_client.put_object(Bucket=bucket, Key=state_key, Body=state_data)

def lambda_handler(event, context):
    s3_bucket = "clipsdata"
    s3_key = "all_videos.csv"
    state_key = "all_videos_state.txt"
    s3_client = boto3.client('s3')

    # Read CSV data from S3
    try:
        response = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
        csv_data = response['Body'].read().decode('utf-8')
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(f"Failed to read CSV: {str(e)}")}

    data = StringIO(csv_data)
    reader = csv.DictReader(data)
    
    # Handle BOM in the header if present
    if reader.fieldnames and reader.fieldnames[0].startswith('\ufeff'):
        reader.fieldnames[0] = reader.fieldnames[0][1:]  # Remove BOM from the first column name
    
    rows = list(reader)
    header = reader.fieldnames

    watched_columns = ['watched_1', 'watched_2', 'watched_3', 'watched_4', 'watched_5']

    video_groups = defaultdict(list)
    for row in rows:
        try:
            base_name = "_".join(row['name'].split("_")[:-1])
            video_groups[base_name].append(row)
        except KeyError as e:
            print(f"KeyError: {e} in row {row}")

    # Flatten all video parts into a single list, sorted by group and part number
    all_videos = []
    for group_name in sorted(video_groups.keys()):
        sorted_group = sorted(video_groups[group_name], key=lambda x: extract_part_number(x['name']))
        all_videos.extend(sorted_group)

    # Read current state (current position in the global video list)
    current_video_index, current_round_index, _ = read_state(s3_client, s3_bucket, state_key)

    # Determine batch size (always 4 videos per batch)
    batch_size = 4
    total_videos = len(all_videos)
    videos_to_return = []

    # Collect exactly 4 videos, wrapping around if necessary
    for i in range(batch_size):
        index = (current_video_index + i) % total_videos
        videos_to_return.append(all_videos[index])

    # Update the 'watched' column for the current round
    for row in videos_to_return:
        row[watched_columns[current_round_index]] = 'x'

    # Update the state
    current_video_index = (current_video_index + batch_size) % total_videos
    if current_video_index == 0:
        current_round_index = (current_round_index + 1) % len(watched_columns)

    write_state(s3_client, s3_bucket, state_key, current_video_index, current_round_index, 0)

    # Write the updated CSV data back to S3
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=header)
    writer.writeheader()
    writer.writerows(rows)
    s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=output.getvalue())

    # Build the video list for the URL
    all_videos_str = ""
    for i, row in enumerate(videos_to_return, 1):
        video_name = f"video_{i}={row['link']}"
        all_videos_str += "&" + video_name if i > 1 else video_name

    # Use SURVEY_URL variable here
    target_url = f"{SURVEY_URL}&{all_videos_str}&sp={generate_random_number()}"
    html_content = f"<html><head><title>Redirecting...</title><script type='text/javascript'>window.location.href = '{target_url}';</script></head><body><p>If you are not redirected, <a href='{target_url}'>click here to continue</a>.</p></body></html>"

    return {'statusCode': 200, 'headers': {'Content-Type': 'text/html'}, 'body': html_content}
