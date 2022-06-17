import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def get_image(path, zoom=0.3):
    return OffsetImage(plt.imread(path), zoom=zoom)


class KNearestClothes:

    def __init__(self, cosine_similarities, k=10):
        self.cosine_similarities = cosine_similarities
        self.k = k
        self.target_indices = None
        self.distances = None

    def __call__(self ):
       # cosine_similarities = self.cosine_similarities.reshape(1,-1)
        knn = NearestNeighbors(n_neighbors=self.k, p=2)
        knn.fit(self.cosine_similarities.reshape(-1,1))  # storing dataset

        target_indices, distances = knn.kneighbors(np.array([[0]]), return_distance=True)
        self.target_indices = target_indices
        self.distances = distances

        return target_indices, distances

    def plot_k_nearest_clothes(self, scraped_image_paths: list[str], query_image_path: str):
        query_image = np.array([[0, 0]])
        q_x, q_y = query_image.T

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.set(
            xlim=[0, self.k + 1],
            ylim=[0, np.max(self.distances) + 2],
            xlabel='Images',
            ylabel='1 - Cosine similarity',
        )

        k_images = np.arange(1, self.k+1, 1)

        ax.scatter(q_x, q_y)
        ax.scatter(k_images, self.distances)

#        query image
        q_ab = AnnotationBbox(get_image(query_image_path), (q_x, q_y), frameon=False)
        ax.add_artist(q_ab)
        #

        k_im = k_images.reshape(1,-1)
        dis = self.distances.reshape(1,-1)

        # # Scraped images
        for k_image, y, path in zip(k_im[0].tolist(), dis[0].tolist(), scraped_image_paths):
            print("Im innnn")
            ab = AnnotationBbox(get_image(path), (k_image, y), frameon=False)
            ax.add_artist(ab)
        plt.show()

# knearest neighbors

# def k_nearest_neighbors(image_vectors, k=10):
#     print(image_vectors)
#
#     knn = NearestNeighbors(n_neighbors=k, p=2)
#     knn.fit(image_vectors)  # storing dataset
#
#     target_indices = knn.kneighbors(np.array([[0, 0]]), return_distance=False)
#
#     print("target indices", target_indices)
#     # print("first", np.reshape(target_indices, (,1)))
#
#     target_elements = np.take(image_vectors, indices=target_indices)
#
#     return target_indices
#
#
# def plot_k_nearest_neighbors(scraped_images_distances, scraped_image_paths, query_image_path):
#     print("distances", scraped_images_distances)
#     query_image = np.array([[0, 0]])
#     q_x, q_y = query_image.T
#
#     scraped_image_paths = [path for (path, _) in scraped_image_paths]
#     print(scraped_image_paths)
#
#     max_color_distances = np.max(scraped_images_distances[:, 0])
#     s_x, s_y = scraped_images_distances.T
#
#     fig, ax = plt.subplots(nrows=1, ncols=1)
#     ax.set(
#         # xlim = [-1,max_color_distances+1],
#         # ylim = [-1,4],
#         xlabel='Color  distance',
#         ylabel='Cosine similarity',
#     )
#
#     ax.scatter(q_x, q_y, color="green")
#     ax.scatter(s_x, s_y)
#
#     # Query Image
#     q_ab = AnnotationBbox(get_image(query_image_path), (q_x, q_y), frameon=False)
#     ax.add_artist(q_ab)
#
#     # Scraped images
#     for x0, y0, path in zip(s_x, s_y, scraped_image_paths):
#         ab = AnnotationBbox(get_image(path), (x0, y0), frameon=False)
#         ax.add_artist(ab)
#     plt.show()

# plot_k_nearest_neighbors()

# fig, ax = plt.subplots(nrows=1, ncols=1)
# ax.set(
#     ylim=[0, 1],
#     xlabel='Color  distance',
#     ylabel='Cosine similarity',
# )
# plt.show()
