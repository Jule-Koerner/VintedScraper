#from DeepImageSearch import Index,LoadData,SearchImage
import cv2
import numpy as np
import skimage




from sentence_transformers import SentenceTransformer, util
from PIL import Image
import glob
import matplotlib.pyplot as plt
import os

# Load the OpenAI CLIP Model
print('Loading CLIP Model...')
model = SentenceTransformer('clip-ViT-B-32')

# Next we compute the embeddings
# To encode an image, you can use the following code:
# from PIL import Image
# encoded_image = model.encode(Image.open(filepath))
image_names = list(glob.glob('images/*.png'))
print("Images:", len(image_names))
images = [Image.open(filepath) for filepath in image_names]
encoded_images = model.encode(images, batch_size=128, show_progress_bar=True)
print("Länge encoded image" ,len(encoded_images))
query_image = model.encode(Image.open(image_names[3]))

cosine_similarities: list = [np.dot(query_image, image)/ (np.linalg.norm(query_image) * np.linalg.norm(image)) for image in encoded_images]
print(cosine_similarities)

sorting = np.argsort(np.asarray(cosine_similarities))[::-1]
images = np.asarray(images)
cosine_similarities = np.asarray(cosine_similarities)
fig, axes = plt.subplots(ncols=len(image_names))
for img, a, sim in zip(images[sorting], axes, cosine_similarities[sorting]):
    a.imshow(img)
    a.set_title(sim)
plt.show()

#Now we run the clustering algorithm. This function compares images aganist
# all other images and returns a list with the pairs that have the highest
# cosine similarity score
#processed_images = util.paraphrase_mining_embeddings(encoded_image)


