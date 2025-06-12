from fastapi import FastAPI, HTTPException, Body, status, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates   
from starlette.requests import Request       
from pydantic import HttpUrl
import mongo, utils

app = FastAPI(title="Url shorten")
templates = Jinja2Templates(directory="templates")


@app.post("/", response_class=HTMLResponse)
def create_from_form(url: str = Form(...)):
    if not utils.is_valid_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    doc = mongo.save(url)
    return RedirectResponse(f"/{doc['short']}", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/all", response_class=HTMLResponse)
def list_all(request: Request):
    vals = list(mongo.col.find())              
    return templates.TemplateResponse(
        "all_urls.html",
        {"request": request, "vals": vals}
    )
@app.post("/api/shorten", status_code=status.HTTP_201_CREATED)
def create(url: str = Form(...)):        
    if not utils.is_valid_url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    doc = mongo.save(url)
    return RedirectResponse(url=f"/display/{doc['short']}", status_code=303)

@app.get("/api/shorten/{code}")
def read(code: str):
    doc = mongo.find(code)
    if doc is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return doc

@app.put("/api/shorten/{code}")
def update(code: str, url: HttpUrl = Body(..., embed=True)):    
    doc = mongo.update(code, str(url))
    if doc is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return doc

@app.delete("/api/shorten/{code}", status_code=status.HTTP_204_NO_CONTENT)
def remove(code: str):
    if not mongo.delete(code):
        raise HTTPException(status_code=404, detail="Code not found")

@app.get("/api/shorten/{code}/stats")
def stats(code: str):
    doc = mongo.find(code)
    if doc is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return {"short_link": code, "accessCount": doc["accessCount"]}

@app.get("/{code}")
def redirect(code: str):
    doc = mongo.find(code)
    if doc is None:
        raise HTTPException(status_code=404, detail="Code not found")
    mongo.inc_counter(code)
    return RedirectResponse(doc["long"], status_code=301)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "url_page.html",       
        {"request": request}   
    )
@app.get("/display/{code}", response_class=HTMLResponse)
def display(request: Request, code: str):
    return templates.TemplateResponse(
        "display_url.html",
        {"request": request, "short_url_display": code}
    )
