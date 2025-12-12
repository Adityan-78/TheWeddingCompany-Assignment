# app/main.py
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import RedirectResponse

# import routers AFTER creating app
from app.api.v1 import orgs, admin

app = FastAPI(
    title="Organization Management Service",
    version="0.1.0",
    docs_url=None,   # disable default docs
    redoc_url=None,  # disable default redoc
    openapi_url="/openapi.json"
)

# include routers BEFORE exposing custom docs so openapi.json contains paths
app.include_router(orgs.router)
app.include_router(admin.router)

# mount static directory for custom css and ui.html
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# custom docs route using our minimal CSS (keeps default Swagger UI look)
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    """
    Serve the default Swagger UI but allow injecting a small CSS file
    (app/static/swagger.css) to increase readability without changing layout.
    """
    return get_swagger_ui_html(
        title=f"{app.title} - docs",
        swagger_css_url="/static/swagger.css",
    )


# convenient route to open the custom UI (static ui.html)
@app.get("/ui", include_in_schema=False)
async def ui_redirect():
    return RedirectResponse(url="/static/ui.html")


# root -> redirect to UI
@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/ui")


# simple health check
@app.get("/health", include_in_schema=True)
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
