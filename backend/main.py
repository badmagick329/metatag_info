from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from meta_info import MetaTagInfo
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SiteData(BaseModel):
    url: str
    selected_tags: list[str] | None = None


@app.post("/url")
def parse_url(site_data: SiteData):
    if site_data.selected_tags:
        site_data.selected_tags = [t for t in site_data.selected_tags if t.strip()]
    meta_info = MetaTagInfo(
        url=site_data.url,
        selected_tags=site_data.selected_tags,
    )
    try:
        meta_info.fetch()
    except Exception as e:
        return {"error": str(e), "data": None}
    return {"error": None, "data": meta_info.to_markdown()}
