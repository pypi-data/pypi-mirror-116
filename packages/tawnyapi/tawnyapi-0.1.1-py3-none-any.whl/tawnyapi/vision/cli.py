
from typing import List
from pprint import pprint

import typer

from .client import TawnyVisionApiClient


app = typer.Typer()


@app.command()
def hello():
    print('Hello from TAWNY!')


@app.command()
def analyze(
        image: List[str] = [],
        maxresults: int = 1,
        resize: int = 720,
        apiurl: str = None,
        apikey: str = None):
    """
    Sends a request to the TAWNY Vision API. You can provide --image more than
    once to send several images in one request.
    """

    if apiurl is None:
        print('ERROR: You have to provide the --apiurl argument.')
        return

    if apikey is None:
        print('ERROR: You have to provide the --apikey argument.')
        return

    client = TawnyVisionApiClient(
        api_url=apiurl,
        api_key=apikey
    )
    result = client.analyze_images_from_paths(
        image_paths=image,
        max_results=maxresults,
        resize=resize
    )
    pprint(result)


if __name__ == "__main__":
    app()
