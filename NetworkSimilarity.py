# from DeepImageSearch import Index,LoadData,SearchImage
import cv2
import numpy as np
import skimage
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import glob
import matplotlib.pyplot as plt
import os


class NetworkSimilarity:
    num_instances: int = 0

    def __init__(self, query_image_path: str, scraped_images_path: list[str]):
        self.query_image_path = query_image_path
        self.scraped_image_path = scraped_images_path

    def cosine_formula(self, query_image, image):
        return np.dot(query_image, image) / (np.linalg.norm(query_image) * np.linalg.norm(image))

    def cosine_similarities(self) -> list[float]:
        model = SentenceTransformer('clip-ViT-B-32')

        # Next we compute the embeddings
        # To encode an image, you can use the following code:
        # from PIL import Image
        # encoded_image = model.encode(Image.open(filepath))
        # image_names = list(glob.glob('images/*.png'))
        # print("Images:", len(image_names))
        images = [Image.open(filepath) for filepath in self.scraped_image_path]
        # image = Image.open(self.scraped_image_path)

        encoded_images = model.encode(images, batch_size=128, show_progress_bar=True)
        # encoded_image_scraped_image = model.encode(image, batch_size=128, show_progress_bar=True)
        print("Länge encoded image", len(encoded_images))

        query_image = model.encode(Image.open(self.query_image_path))


        cosine_similarities = [np.round(self.cosine_formula(query_image, image), 2) for image in encoded_images]

        return query_image, encoded_images
