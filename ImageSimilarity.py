# from DeepImageSearch import Index,LoadData,SearchImage
import cv2
import numpy as np
import skimage
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import glob
import matplotlib.pyplot as plt
import os


# Network similarity
# Load the OpenAI CLIP Model

class SimilarityVector:

    def __init__(self, image_path_with_color_tag, query_image):
        self.image_path_with_color_tag = image_path_with_color_tag
        self.query_image = query_image


    def network_similarity(self, image_path):
        model = SentenceTransformer('clip-ViT-B-32')

        # Next we compute the embeddings
        # To encode an image, you can use the following code:
        # from PIL import Image
        # encoded_image = model.encode(Image.open(filepath))
        image_names = list(glob.glob('images/*.png'))
        print("Images:", len(image_names))
        images = [Image.open(filepath) for filepath in image_names]
        encoded_images = model.encode(images, batch_size=128, show_progress_bar=True)
        print("Länge encoded image", len(encoded_images))
        query_image = model.encode(Image.open(image_names[3]))

        cosine_similarities: list = [np.dot(query_image, image) / (np.linalg.norm(query_image) * np.linalg.norm(image))
                                     for image in encoded_images]
        print(cosine_similarities)
        sorting = np.argsort(np.asarray(cosine_similarities))[::-1]
        images = np.asarray(images)
        cosine_similarities = np.asarray(cosine_similarities)
        fig, axes = plt.subplots(ncols=len(image_names))
        for img, a, sim in zip(images[sorting], axes, cosine_similarities[sorting]):
            a.imshow(img)
            a.set_title(sim)
        plt.show()
        return cosine_similarities

    def color_distance(self, query_color: str, image_color: str):
        img = cv2.imread('images/orange.png')  # image in grayscale

        color_mapping = {
            "red": np.asarray([53.23288178584245, 80.10930952982204, 67.22006831026425]),
            "green": np.asarray([73.1779906964669, -41.63999994303724, 36.55930009725496]),
            "dark green": np.asarray([17.4226996, -21.096043786174718, 7.117413245366821]),
            "khaki": np.asarray([82.63999833659311, -4.450728842501195, 19.543062710870608]),
            "brown": np.asarray([27.87325768195545, 12.464239465294874, 16.512943084931198]),
            "blue": np.asarray([32.302586667249486, 79.19666178930935, -107.86368104495168]),
            "yellow": np.asarray([92.86438859923291, -13.023145570386474, 58, 133668935258996]),
            "orange": np.asarray([74.0476701963864, 23.581201404374475, 74.34311720316882]),
            "black": np.asarray([0, 0, 0]),
            "white": np.asarray([100, 0.00526049995830391, -0.010408184525267927]),
            "creme": np.asarray([97.76767980018643, -3.38976351049064, 8.50673920252416]),
            "bordeaux": np.asarray([26.214160584684244, 49.9027889615648, 9.505990608977976]),
            "pink": np.asarray([55.95428053659428, 84.55626603780291, -5.71470820760005]),
            "purple": np.asarray([35.699358741104454, 25.067934873951092, -20.48206150243018]),
            "light blue": np.asarray([83.13398976372372, -13.12999531860437, -20.047629870200325])
        }

        color_distance = np.round(np.linalg.norm(color_mapping[user_color] - color_mapping[image_color]), 2)

        return color_distance

    def get_similarity_vector(self, image_with_color_tag, query_image_color: str):
        all_similarity_vec = []

        image_path, color = image_with_color_tag
        similarity_vec = np.array(
            (self.color_distance(query_image_color, image_path), self.network_similarity(image_path)))

        return similarity_vec


class AllSimilarityVectors:

    def get_similarity_vector_list(self, images_with_color_tag, query_image_color: str):
        for im in images_with_color_tag:
            image_path, color = im
            sim_vec = SimilarityVector().get_similarity_vector()

        return similarity_vec
