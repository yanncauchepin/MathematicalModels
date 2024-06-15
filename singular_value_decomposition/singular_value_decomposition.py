import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def read_image(image_path):
    image = Image.open(image_path)
    image_gray = image.convert('L')
    image_array = np.array(image_gray)
    return image_array

def compute_svd(image_array):
    U, S, V = np.linalg.svd(image_array)
    return U, S, V

def define_truncated_matrices(U, S, V, num_eigenvalues):
    U_truncated = U[:, :num_eigenvalues]
    S_truncated = np.diag(S[:num_eigenvalues])
    V_truncated = V[:num_eigenvalues, :]
    return U_truncated, S_truncated, V_truncated

def plot_eigenvalues_evolution(S):
    plt.figure(figsize=(6, 4))
    plt.plot(np.arange(len(S)), S, 'o-')
    plt.yscale('log')
    plt.title('Eigenvalues')
    plt.xlabel('Index')
    plt.ylabel('Magnitude (log scale)')
    plt.show()

def plot_cumulative_energy(S):
    cumulative_energy = np.cumsum(S) / np.sum(S)
    plt.figure(figsize=(6, 4))
    plt.plot(np.arange(len(S)), cumulative_energy, 'o-')
    plt.title('Cumulative Energy')
    plt.xlabel('Index')
    plt.ylabel('Cumulative Energy')
    plt.show()


def reconstruct_image(U_truncated, S_truncated, V_truncated):
    image_reconstructed = U_truncated @ S_truncated @ V_truncated
    return image_reconstructed


def display_comparison_images(image_array, image_reconstructed):
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    
    original_size_kb = image_array.nbytes / 1024
    reconstructed_size_kb = image_reconstructed.nbytes / 1024
    
    axs[0].imshow(image_array, cmap='gray')
    axs[0].set_title(f'Original Image (size: {original_size_kb:.2f} kB)')
    axs[0].axis('off')
    
    axs[1].imshow(image_reconstructed, cmap='gray')
    axs[1].set_title(f'Reconstructed Image (size: {reconstructed_size_kb:.2f} kB, {num_eigenvalues} eigenvalues)')
    axs[1].axis('off')
    
    plt.show()


if __name__=='__main__':
    image_path = './dataset/tiger_forest.jpg'
    image_array = read_image(image_path)
    U, S, V = compute_svd(image_array)
    plot_eigenvalues_evolution(S)
    plot_cumulative_energy(S)
    num_eigenvalues = 50
    U_truncated, S_truncated, V_truncated = define_truncated_matrices(U, S, V, num_eigenvalues)
    image_reconstructed = reconstruct_image(U_truncated, S_truncated, V_truncated)
    # image_reconstructed = np.rint(image_reconstructed).astype(int)
    display_comparison_images(image_array, image_reconstructed)

