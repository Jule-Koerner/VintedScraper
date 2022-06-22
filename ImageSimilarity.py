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
    num_instances: int = 0

    def __init__(self, scraped_image_path_with_color_tag, query_image, query_color):
        SimilarityVector.num_instances += 1
        image_path, color = scraped_image_path_with_color_tag
        self.scraped_image_path = image_path
        self.scraped_image_color = color

        self.query_image_path = query_image
        self.query_color = query_color

    def network_similarity(self):
        model = SentenceTransformer('clip-ViT-B-32')

        # Next we compute the embeddings
        # To encode an image, you can use the following code:
        # from PIL import Image
        # encoded_image = model.encode(Image.open(filepath))
        image_names = list(glob.glob('images/*.png'))
        print("Images:", len(image_names))
        images = [Image.open(filepath) for filepath in image_names]
        image = Image.open(self.scraped_image_path)

        encoded_images = model.encode(images, batch_size=128, show_progress_bar=True)
        encoded_image_scraped_image = model.encode(image, batch_size=128, show_progress_bar=True)
        print("Länge encoded image", len(encoded_images))

        query_image = model.encode(Image.open(image_names[3]))
        query_image = model.encode(Image.open(self.query_image_path))

        # cosine_similarities: list = [np.dot(query_image, image) / (np.linalg.norm(query_image) * np.linalg.norm(image))
        #                              for image in encoded_images]
        cosine_similarity = np.dot(query_image, encoded_image_scraped_image) / (np.linalg.norm(query_image) * np.linalg.norm(encoded_image_scraped_image))

        #
        # sorting = np.argsort(np.asarray(cosine_similarities))[::-1]
        # images = np.asarray(images)
        # cosine_similarities = np.asarray(cosine_similarities)
        # fig, axes = plt.subplots(ncols=len(image_names))
        # for img, a, sim in zip(images[sorting], axes, cosine_similarities[sorting]):
        #     a.imshow(img)
        #     a.set_title(sim)
        # plt.show()
        return np.round(1 - cosine_similarity, 2)

    def color_distance(self):
       # img = cv2.imread('images/orange.png')  # image in grayscale

        color_mapping = {
            "rot": np.array([53.23288178584245, 80.10930952982204, 67.22006831026425]),
            "burgunderrot": np.array([23.245319456184895, 38.92594200715973, -0.2174795299689558]),
            "grün": np.array([73.1779906964669, -41.63999994303724, 36.55930009725496]),
            "dunkelgrün": np.array([17.4226996, -21.096043786174718, 7.117413245366821]),
            "khaki": np.array([82.63999833659311, -4.450728842501195, 19.543062710870608]),
            "braun": np.array([27.87325768195545, 12.464239465294874, 16.512943084931198]),
            "blau": np.array([32.302586667249486, 79.19666178930935, -107.86368104495168]),
            "gelb": np.array([92.86438859923291, -13.023145570386474, 58, 133668935258996]),
            "orange": np.array([74.0476701963864, 23.581201404374475, 74.34311720316882]),
            "schwarz": np.array([0, 0, 0]),
            "weiß": np.array([100, 0.00526049995830391, -0.010408184525267927]),
            "creme": np.array([97.76767980018643, -3.38976351049064, 8.50673920252416]),
            "bordeaux": np.array([26.214160584684244, 49.9027889615648, 9.505990608977976]),
            "pink": np.array([55.95428053659428, 84.55626603780291, -5.71470820760005]),
            "lila": np.array([35.699358741104454, 25.067934873951092, -20.48206150243018]),
            "hellblau": np.array([83.13398976372372, -13.12999531860437, -20.047629870200325]),
            "grau": np.array([56.7034107567544, 0.0032970369763796, -0.0065233665066833]),
            "silber": np.array([56.7034107567544, 0.0032970369763796, -0.0065233665066833]),
            "marineblau": np.array([39.84748054713849, -4.895828262263924, -22.384858594081113]),
            "türkis": np.array([81.26705459794431, -44.07625420413397, -4.034478714864265]),

        }

        try:
            print("Im in color")
            #If more than one color in scraped image -> take mean
            if len(self.scraped_image_color) != 1:
                arr_scraped_image_color = np.array(self.scraped_image_color)

                if any(arr_scraped_image_color) == "bunt":
                    print("im in bunt")
                    all_dist = []
                    indices = np.where(arr_scraped_image_color != "bunt")
                    print("indices", indices)
                    for i in indices:
                        color_distance = np.linalg.norm(color_mapping[self.query_color] - color_mapping[self.scraped_image_color[i]])
                        all_dist.append(color_distance)

                    mean_dist = np.mean(all_dist)
                    return np.round(mean_dist,2)

                else:
                    print("not in bunt")
                    all_dist = []
                    for im in self.scraped_image_color:
                        color_distance = np.linalg.norm(
                            color_mapping[self.query_color] - color_mapping[im])
                        all_dist.append(color_distance)
                    mean_dist = np.mean(all_dist)
                    return np.round(mean_dist, 2)
            #If only one color in scraped image
            else:
                dist = np.linalg.norm(color_mapping[self.query_color] - color_mapping[self.scraped_image_color[0]])
                color_distance = np.round(dist, 2)
                return color_distance

         #return color_distance
        except Exception as e:
            print("Exception", e)
            return 800
            #color_distance = 300
            #return color_distance

    def __call__(self):
        all_similarity_vec = []

       # similarity_vec = np.array((self.color_distance(), self.network_similarity()))
        similarity_vec = [self.color_distance(), self.network_similarity()]
        return similarity_vec

    @staticmethod
    def get_multiple_similarities(scraped_image_paths_with_color_tag: list, query_image= 'scraped_imgs/img1.png', query_color="blau"):
        all_similarity_vectors = []
        for im in scraped_image_paths_with_color_tag:
            sim_vec = SimilarityVector(im, query_image, query_color)
            all_similarity_vectors.append(sim_vec())

        return np.array(all_similarity_vectors)


class AllSimilarityVectors:
    def __init__(self, scraped_image_paths_with_color_tag: list, query_image= 'scraped_imgs/img0.png', query_color="blau" ):
        self.scraped_image_paths_with_color_tag = scraped_image_paths_with_color_tag
        self.query_image = query_image
        self.query_color = query_color

    def __call__(self):
        all_similarity_vectors = []
        for im in self.scraped_image_paths_with_color_tag:
            sim_vec = SimilarityVector(im, self.query_image, self.query_color)
            all_similarity_vectors.append(sim_vec())

        return np.array(all_similarity_vectors)


if __name__ == '__main__':

    SimilarityVector.get_multiple_similarities()


