import re
from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.summarize_yt import YTSummarizer

def summarize(video_url):
    summ = YTSummarizer()
    video_id = summ.extract_video_id(video_url)
    transcript_text = summ.get_transcript_text(video_id)
    transcript_summary = None
    if transcript_text:
        transcript_summary = summ.summarize_text(transcript_text[:summ.MAX])
    comments_summary = None
    comments = summ.get_video_comments(video_id)
    comment_text = " ".join(comments)
    if comment_text:
        comments_summary = summ.summarize_text(comment_text[:summ.MAX])
    return transcript_summary, comments_summary

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/submit_form/")
def submit_form(request: Request, url: Annotated[str, Form()]):
    print(f"Received form input: {url}")
    t, c = summarize(url)
    transcript = re.sub(r'\n', '<p></p>', t)
    comments = re.sub(r'\n', '<p></p>', c)
    return templates.TemplateResponse(request, "summary.html",
        { "transcript": transcript, "comments": comments }
    )
