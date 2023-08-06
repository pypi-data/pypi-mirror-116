
from typing import List
import asyncio

import aiohttp

from . import apitypes
from .util import get_base64_images


class TawnyVisionApiClient():

    def __init__(self, api_url: str, api_key: str):
        self.async_client = TawnyVisionApiAsyncClient(
            api_url=api_url,
            api_key=api_key
        )

    def analyze_image_from_path(
            self,
            image_path: str,
            max_results: int = 1,
            resize: int = 720):
        return asyncio.run(self.async_client.analyze_image_from_path(
            image_path=image_path,
            max_results=max_results,
            resize=resize
        ))

    def analyze_images_from_paths(
            self,
            image_paths: List[str] = [],
            max_results: int = 1,
            resize: int = 720):
        return asyncio.run(self.async_client.analyze_images_from_paths(
            image_paths=image_paths,
            max_results=max_results,
            resize=resize
        ))


class TawnyVisionApiAsyncClient():

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    async def analyze_image_from_path(
            self,
            image_path: str,
            max_results: int = 1,
            resize: int = 720):
        return await self.analyze_images_from_paths(
            image_paths=[image_path],
            max_results=max_results,
            resize=resize
        )

    async def analyze_images_from_paths(
            self,
            image_paths: List[str] = [],
            max_results: int = 1,
            resize: int = 720):

        images = get_base64_images(image_paths, resize=resize)
        request_data = {
            'requests': []
        }
        for img in images:
            request_data['requests'].append({
                'image': img,
                'imageInputType': apitypes.ImageInputType.RAW,
                'features': [
                    apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                    apitypes.ImageAnnotationFeatures.FACE_EMOTION
                ],
                'emotionModelVersion': apitypes.ImageEmotionModelVersion.V_1_4,
                'maxResults': max_results
            })

        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        async with aiohttp.ClientSession() as session:
            resp = await session.post(
                self.api_url,
                headers=headers,
                json=request_data
            )
            result = await resp.json()
            return result
