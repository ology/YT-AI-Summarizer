from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.summarize_yt import YTSummarizer

def sanitize(text):
    text = text.replace('\n', '<p></p>')
    text = text.replace('### ', '')
    text = text.replace('**', '')
    return text

def summarize(video_url):
    summ = YTSummarizer()
    video_id = summ.extract_video_id(video_url)
    transcript_text = summ.get_transcript_text(video_id)
    transcript_summary = None
    if transcript_text:
        transcript_summary = summ.summarize_text(transcript_text[:summ.MAX])
        transcript_summary = sanitize(transcript_summary)
    comments_summary = None
    comments = summ.get_video_comments(video_id)
    if comments:
        comment_text = " ".join(comments)
        if comment_text:
            comments_summary = summ.summarize_text(comment_text[:summ.MAX])
            comments_summary = sanitize(comments_summary)
    return transcript_summary, comments_summary

app = FastAPI(openapi_url=None, docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory="templates")

# allow the browser extension to send data to localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlData(BaseModel):
    url: str

FAVICON_PATH = "favicon.ico"
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(FAVICON_PATH)

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/submit_form/")
def submit_form(request: Request, url: Annotated[str, Form()]):
    print(f"Received form input: {url}")
    transcript, comments = summarize(url)
    return templates.TemplateResponse(request, "summary.html",
        { "transcript": transcript, "comments": comments }
    )

@app.post("/api/url")
async def receive_url(data: UrlData):
    print(f"Received URL: {data.url}")
    transcript, comments = summarize(data.url)
    return { "message": "URL summarized successfully", "transcript": transcript, "comments": comments }
