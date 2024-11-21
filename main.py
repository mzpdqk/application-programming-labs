import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys

def load_image(file_path):
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError(f"Unable to load image from {file_path}")
    return image

def display_image_size(image, name):
    height, width, _ = image.shape
    print(f"Size of {name}: {width}x{height}")

def plot_histogram(image, title):
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([0, 256])
    plt.title(title)
    plt.xlabel('Intensity')
    plt.ylabel('Count')
    plt.show()

def blend_images(base_image, overlay_image, alpha):
    overlay_image = cv2.resize(overlay_image, (base_image.shape[1], base_image.shape[0]))
    blended = cv2.addWeighted(base_image, 1 - alpha, overlay_image, alpha, 0)
    return blended

def main(base_image_path, overlay_image_path, output_path, alpha):
    base_image = load_image(base_image_path)
    overlay_image = load_image(overlay_image_path)

    display_image_size(base_image, "Base Image")
    display_image_size(overlay_image, "Overlay Image")

    plot_histogram(base_image, "Histogram of Base Image")
    plot_histogram(overlay_image, "Histogram of Overlay Image")

    blended_image = blend_images(base_image, overlay_image, alpha)

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 3, 1)
    plt.title('Base Image')
    plt.imshow(cv2.cvtColor(base_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title('Overlay Image')
    plt.imshow(cv2.cvtColor(overlay_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title('Blended Image')
    plt.imshow(cv2.cvtColor(blended_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.show()

    cv2.imwrite(output_path, blended_image)
    print(f"Blended image saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <base_image_path> <overlay_image_path> <output_path> <alpha>")
        sys.exit(1)

    base_image_path = r'C:\Users\User\PycharmProjects\Lab3\base_image.jpg'  # Use raw string
    overlay_image_path = r'C:\Users\User\PycharmProjects\Lab3\overlay_image.jpg'  # Adjust this path
    output_path = r'C:\Users\User\PycharmProjects\Lab3\output_image.jpg'  # Adjust this path
    alpha = float(sys.argv[4])  # Ensure alpha is passed correctly

    main(base_image_path, overlay_image_path, output_path, alpha)

