from skimage import feature
from skimage import data
from matplotlib import pyplot as plt
#
# def loadImages(fileList):
#     for i in range(len(fileList)):
#         fileList[i] =s


if __name__ == '__main__':
    image = data.lena()  # Albo: coins(), page(), moon()
    # image = filter.sobel(image)
    feature.canny(image)
    plt.imshow(image)
    plt.show()  # Niepotrzebne, jesli ipython notebook --matplotlib=inline