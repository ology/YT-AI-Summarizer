# YT-AI-Summarizer
Summarize a YouTube Video Transcript and Comments

```
git clone https://github.com/ology/YT-AI-Summarizer.git
cd YT-AI-Summarizer
python -m venv .
source ./bin/activate
pip install "fastapi[standard]" google-api-python-client google-auth-oauthlib google-auth-httplib2 openai
uvicorn main:app --host 192.168.99.50 --port 8000
```
