from fastapi import FastAPI, HTTPException, Header, Request
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"),
          name="static")  # Assuming your CSS and JS are in a 'static' folder

templates = Jinja2Templates(
    directory="templates")  # Assuming your HTML is in a 'templates' folder

temps = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


@app.get("/temp")
def get_temp(api_key: Annotated[str | None, Header()] = None):
  if api_key is None:
    raise HTTPException(status_code=401, detail="API key is required")
  if api_key not in temps:
    raise HTTPException(status_code=404, detail="API key not found")
  return temps[api_key]


@app.put("/temp")
async def set_temp(request: Request,
                   api_key: Annotated[str | None, Header()] = None):
  if api_key is None:
    raise HTTPException(status_code=401, detail="API key is required")
  temp = (await request.json())
  temps[api_key] = temp
  return {"message": "Temperature set successfully"}


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=10000)
