# -*- coding: utf-8 -*-
from src.pricetag import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
