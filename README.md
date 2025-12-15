# YT-AI-Summarizer
Summarize a YouTube Video Transcript and Comments

```
git clone https://github.com/ology/YT-AI-Summarizer.git
cd YT-AI-Summarizer
export OPENAI_API_KEY=xyz667ghfiwuefhiwuefkjsdjbvkzhsgfiwyegf
export YOUTUBE_API_KEY=abc123iufh897342yriwuefbwkefiw37yrf3i
python -m venv .
source ./bin/activate
pip install "fastapi[standard]" google-api-python-client google-auth-oauthlib google-auth-httplib2 youtube_transcript_api openai
uvicorn main:app --host 127.0.0.1 --port 8000
# then browse to http://127.0.0.1:8000/
```
