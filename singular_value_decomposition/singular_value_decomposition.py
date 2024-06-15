import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

image_path = './data/thoune_5.jpg'
image = Image.open(image_path)
image_gray = image.convert('L')
image_array = np.array(image_gray)

U, S, V = np.linalg.svd(image_array)

num_eigenvalues = 100

# Truncate the singular value matrices
U_truncated = U[:, :num_eigenvalues]
S_truncated = np.diag(S[:num_eigenvalues])
V_truncated = V[:num_eigenvalues, :]

# Reconstruct the image using the truncated matrices
image_reconstructed = U_truncated @ S_truncated @ V_truncated

# Display the original and reconstructed images
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].imshow(image_array, cmap='gray')
axs[0].set_title('Original Image')
axs[0].axis('off')
axs[1].imshow(image_reconstructed, cmap='gray')
axs[1].set_title(f'Reconstructed Image ({num_eigenvalues} eigenvalues)')
axs[1].axis('off')

# Show the plot
plt.show()


