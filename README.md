# VideoCap

## Live Example
> Explore a live example of the survey featured in this repository [here](https://redcap.med.upenn.edu/surveys/?s=73N9R8PH4N3MEW4H&video_1=https://upenn.box.com/s/ninyxkukphe79m2urbwmw4wtzzsa3h4z&video_2=https://upenn.box.com/s/4z0b3r7g3yja1z8eg8rs2vkza60ztsqi&video_3=https://upenn.box.com/s/5chq6x32kp4i9fyhjbqxhfe55bp3edia&sp=7248391052).

## Introduction
VideoCap is a workflow for crowdsourcing insights from clinical encounter videos. It focuses on preparing, delivering, and collecting annotations on segmented video content via REDCap and a lightweight AWS backend. VideoCap is a component within CLIPS, which is part of the broader REDUCE (Reimagining Documentation Using Computation from Clinical Encounters) initiative.

Note: The included REDCap survey export is named "CLIPS Survey" (as released). VideoCap is the tool/workflow that powers it.

## VideoCap Objectives
1. **Primary Objective:** Collect qualitative and quantitative data on diverse perspectives regarding clinical encounter videos.
2. **Primary Outcome:** Comprehensive set of annotations per video segment, categorized into both categorical labels and free-form text descriptions.
3. **Secondary Outcomes:** Demographic and mediator data such as medical experience, age, language preference, race, ethnicity, occupation, and current state of residence.

## Integration and Tools
VideoCap integrates REDCap with Amazon AWS and an embeddable content delivery network for efficient video handling and scalable data collection. This integration addresses the challenge of embedding a library of video segments of varied lengths for crowdsourced ground truth labeling in REDCap.

## Key Features
- **Efficient Video Management:** Handles varied segmented video libraries using a content delivery network (CDN).
- **Metadata- driven survey URL generation:** Dynamically generates survey URLs based on video metadata.
- **Single URL access point:** Distributes unique video sets within a single REDCap survey using dynamic URL parameters.

## Repository Structure
This repository contains all the necessary components to replicate and extend the VideoCap project. The structure is as follows:
```
.
├── 1 - REDCap Survey
│   ├── README.md
│   ├── CLIPSSurveyREDCap.xml
├── 2 - Video Preprocessing
│   ├── README.md
│   ├── split_videos.sh
├── 3 - Accessible Video URLs CSV Generation
│   ├── Box, Inc.
│   │   ├── README.md
│   │   ├── generate_videos_csv.py
├── 4 - AWS Backend
│   ├── README.md
│   ├── aws_lambda_function.py
```

## Getting Started
### Prerequisites
- Python
- REDCap access
- AWS account
- A content delivery network
- An Amazon Mechanical Turk Requester account with increased payment limits

### Installation
1. Clone the repository:
```
git clone https://github.com/kbjohnson-penn/CLIPS.git
cd CLIPS
```
2. Configure your survey variables for REDCap, your AWS account, your content delivery network (Box was used for our purposes), and your Amazon Mechanical Turk Requester account.

### Hosting the Project

1. Follow the instructions in [1 - REDCap Survey](https://github.com/kbjohnson-penn/CLIPS/tree/main/1%20-%20REDCap%20Survey) to host our template survey.

2. Preprocessing Videos:
    - Place your videos in the same directory as [split_videos.sh](https://github.com/kbjohnson-penn/CLIPS/blob/main/2%20-%20Video%20Preprocessing/split_videos.sh)
    - Ensure the script has execution, read, and write permissions:
        ```
        chmod +rwx split_videos.sh
        ```
    - Run the script to split your videos into one-minute segments:
        ```
        ./split_videos.sh
        ```

3. Generate a CSV file with all your video names and URLs (this step is [CDN-specific](https://github.com/kbjohnson-penn/CLIPS/tree/main/3%20-%20Accessible%20Video%20URLs%20CSV%20Generation)).

4. Host the CSV file in an AWS S3 bucket with accessible permissions from your Lambda function.

5. Deploy AWS Lambda Functions for URL Redirect: [aws_lambda_function.py](https://github.com/kbjohnson-penn/CLIPS/blob/main/4%20-%20AWS%20Backend/aws_lambda_function.py)

## Cite as

Alasaly B, Jang KJ, Mopidevi S, Johnson KB. CLIPS - Crowdsourcing Likely Insights from Patient Encounter Snippets. Poster presented at: REDCapCon; September 9, 2024; St. Petersburg, Florida. DOI: [10.13140/RG.2.2.10338.54723](https://doi.org/10.13140/RG.2.2.10338.54723).

## Contributing

We welcome contributions from the community, especially for expanding the list of supported CDNs that embed in REDCap.

## License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. You must give appropriate credit, provide a link to the license, and indicate if changes were made. See the [LICENSE](https://github.com/kbjohnson-penn/CLIPS/blob/main/LICENSE) file for details.

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

## Acknowledgements

We would like to thank the team at the University of Pennsylvania, contributors, and supporting staff who have made this project possible.
