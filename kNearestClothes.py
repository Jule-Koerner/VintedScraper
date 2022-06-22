import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from sklearn.decomposition import PCA


def get_image(path, zoom=0.3):
    return OffsetImage(plt.imread(path), zoom=zoom)


class KNearestClothes:


    def __init__(self, query_e, scrape_e, k=25):
       # self.cosine_similarities = cosine_similarities
        self.k = k
        self.target_indices = None
        self.distances = None
        self.query_e = query_e
        self.scrape_e = scrape_e

    def reduce_dimension(self):
        whole_data = np.concatenate((self.query_e.reshape(1,-1), self.scrape_e))
        pca_s = PCA(n_components=2)
        pca_s.fit(whole_data)
        whole_data = pca_s.fit_transform(whole_data)

        self.query_e = whole_data[0]
        self.scrape_e = whole_data[1:]




       # pca_q = PCA(n_components=10)
       # pca_q.fit(self.query_e.reshape(1,-1))
       # self.query_e = pca_q.fit_transform(self.query_e.reshape(1,-1))

    def __call__(self ):
        self.reduce_dimension()
        print("IM INNNNNNNNNNNNNNNNNNNN")
       # cosine_similarities = self.cosine_similarities.reshape(1,-1)
        knn = NearestNeighbors(n_neighbors=self.k, p=2)
        knn.fit(self.scrape_e)  # storing dataset

        distances, target_indices = knn.kneighbors(self.query_e.reshape(1,-1), return_distance=True)
        self.target_indices = target_indices
        self.distances = distances #normalize
        print("DISTANCESSSSSS", self.distances)

        return target_indices, distances

    def plot_k_nearest_clothes(self, scraped_image_paths: list[str], query_image_path: str):

        nearest_scrapes_arr = np.take(np.array(scraped_image_paths), self.target_indices)
       # nearest_distances_arr = np.take(self.distances.T, self.target_indices)
        query_image = np.array([[0, 0]])
        q_x, q_y = query_image.T

        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.set(
            xlim=[0, self.k + 1],
            ylim=[0, np.max(self.distances)],
            xlabel='Images',
            ylabel='distance',
        )

        k_images = np.arange(1, self.k+1, 1)

        ax.scatter(q_x, q_y)
        ax.scatter(k_images, self.distances)

#        query image
        q_ab = AnnotationBbox(get_image(query_image_path), (q_x, q_y), frameon=False)
        ax.add_artist(q_ab)
        #

        #k_im = k_images.reshape(1,-1)
       # dis = self.distances.reshape(1,-1)
        #
        # # # Scraped images
        for k_image, y, path in zip(list(k_images), list(self.distances[0]), scraped_image_paths):
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
