![images/overall_flow.png](images/overall_flow.png)

# MalaysianPayGap LLM using LocalGPT
A sandbox approach to create an end-to-end flow using cutting edge tools & techs. For demo purpose, I've crawled data from Jan 2018 -  Jan 2024 from `malaysianpaygap` Instagram profile.


## Prerequisites
- Python 3.10
- Metaflow (https://docs.metaflow.org/getting-started/install)
- Instaloader (https://github.com/instaloader/instaloader)
- EasyOCR (https://github.com/JaidedAI/EasyOCR)
- LocalGPT (https://github.com/PromtEngineer/localGPT)

## To Reproduce
- STEP 1: Install all dependencies
- STEP 2: Run `python process_flow.py run --profile <TARGET_PROFILE_NAME> --start_date "2018-01-01" --end_date "2024-01-01"`
- STEP 3: Copy `data.txt` to LocalGPT's `SOURCE_DOCUMENTS` directory
- STEP 4: Setup (follow github guidelines), Ingest & Run LocalGPT!

## Demo Screenshot
![images/localgpt-demo.png](images/localgpt-demo.png)

## Others
- Metaflow Sandbox: https://outerbounds.com/sandbox/