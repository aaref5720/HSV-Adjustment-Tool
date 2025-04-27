# @file StaticProgram.py
# @brief Static image processing library for HSV color space manipulation.
# @details This library provides functionality for:
#          - Loading and manipulating images in HSV color space
#          - Converting between RGB and HSV color spaces
#          - Performance comparison between matrix and loop-based implementations
#          - Visualization of HSV channel transformations
# @author Abdelrahman Aref & Ahmed Hassan
# @date 2025
# @version 0.1
# @copyright 2025 Abdelrahman Aref & Ahmed Hassan
# @license MIT
#
# @section DESCRIPTION
# This library implements various image processing functions using the HSV color space.
# It provides both matrix-based and loop-based implementations for color space
# conversion, allowing performance comparison between the two approaches.
#
# @section INSTALLATION
# Requirements:
#   - Python 3.8 or higher
#   - OpenCV (>=4.0.0)
#   - NumPy (>=1.19.0)
#   - Matplotlib (>=3.3.0)
#
# Installation steps:
#   1. pip install opencv-python>=4.0.0
#   2. pip install numpy>=1.19.0
#   3. pip install matplotlib>=3.3.0
#
# @section USAGE
# Basic usage:
#   ```python
#   from StaticProgram import modify_hsv_image
#   
#   # Load and modify an image
#   original, modified_loops, modified_numpy = modify_hsv_image(
#       "input.jpg",
#       hue_shift=120,
#       value_exp=1.5,
#       save_path="output.jpg",
#       print_values=True
#   )
#   ```
#
# @section EXAMPLES
# Performance comparison:
#   ```python
#   from StaticProgram import compare_performance
#   
#   # Compare performance with different image sizes
#   compare_performance(["small.jpg", "medium.jpg", "large.jpg"])
#   ```
#
# Visualization:
#   ```python
#   from StaticProgram import visualize_hsv_changes
#   
#   # Visualize HSV transformations
#   visualize_hsv_changes("input.jpg", hue_shift=120, value_exp=1.5)
#   ```
#
# @bug
#    - Memory usage may be high for large images
#    - Performance degrades with image size
#    - Some color artifacts may appear at extreme HSV values
#
# @note
#    - Matrix operations are significantly faster than loop-based operations
#    - Memory usage increases with image size
#    - HSV color space may produce artifacts at extreme values

import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

class ColorConverter:
    """
    @brief A class for handling color space conversions between HSV and RGB.
    
    @details This class provides two methods for HSV to RGB conversion:
             1. Matrix-based conversion (fast, vectorized)
             2. Loop-based conversion (slower, but memory efficient)
    """
    
    def hsv_to_rgb_matrix(self, hsv_img):
        """Convert HSV to RGB using vectorized matrix operations."""
        hsv_img = hsv_img.astype(np.float32)
        h, s, v = hsv_img[:, :, 0] * 2.0, hsv_img[:, :, 1], hsv_img[:, :, 2]
        h = h / 60.0
        s = s / 255.0
        v = v / 255.0
        c = v * s
        x = c * (1 - np.abs((h % 2) - 1))
        m = v - c
            
        rgb = np.zeros_like(hsv_img)
        zeros = np.zeros_like(c)
            
        mask = (h >= 0) & (h < 1)
        r, g, b = c[mask], x[mask], zeros[mask]
        rgb[mask, 0], rgb[mask, 1], rgb[mask, 2] = r, g, b
            
        mask = (h >= 1) & (h < 2)
        r, g, b = x[mask], c[mask], zeros[mask]
        rgb[mask, 0], rgb[mask, 1], rgb[mask, 2] = r, g, b
            
        mask = (h >= 2) & (h < 3)
        r, g, b = zeros[mask], c[mask], x[mask]
        rgb[mask, 0], rgb[mask, 1], rgb[mask, 2] = r, g, b
            
        mask = (h >= 3) & (h < 4)
        r, g, b = zeros[mask], x[mask], c[mask]
        rgb[mask, 0], rgb[mask, 1], rgb[mask, 2] = r, g, b
            
        mask = (h >= 4) & (h < 5)
        r, g, b = x[mask], zeros[mask], c[mask]
        rgb[mask, 0], rgb[mask, 1], rgb[mask, 2] = r, g, b
            
        mask = (h >= 5)
        r, g, b = c[mask], zeros[mask], x[mask]
        rgb[mask, 0], rgb[mask, 1], rgb[mask, 2] = r, g, b
            
        rgb[:, :, 0] += m
        rgb[:, :, 1] += m
        rgb[:, :, 2] += m
            
        return (rgb * 255).clip(0, 255).astype(np.uint8)
    
    def hsv_to_rgb_loop(self, hsv_img):
        """Convert HSV to RGB using pixel-by-pixel loop processing."""
        hsv_img = hsv_img.astype(np.float32)
        height, width = hsv_img.shape[:2]
        rgb_img = np.zeros((height, width, 3), dtype=np.uint8)
        
        for i in range(height):
            for j in range(width):
                h, s, v = hsv_img[i, j]
                h = (h * 2.0) / 60.0
                s = s / 255.0
                v = v / 255.0
                c = v * s
                x = c * (1 - abs((h % 2) - 1))
                m = v - c
                
                if 0 <= h < 1:
                    r, g, b = c, x, 0
                elif 1 <= h < 2:
                    r, g, b = x, c, 0
                elif 2 <= h < 3:
                    r, g, b = 0, c, x
                elif 3 <= h < 4:
                    r, g, b = 0, x, c
                elif 4 <= h < 5:
                    r, g, b = x, 0, c
                else:
                    r, g, b = c, 0, x
                
                rgb_img[i, j] = [(r + m) * 255, (g + m) * 255, (b + m) * 255]
        
        return rgb_img

def modify_hsv_image(image_path, hue_shift, value_exp, save_path=None, print_values=False):
    """
    @brief Load an image and modify its HSV color space values.
    
    @details This function performs the following operations:
             1. Loads an image from the specified path
             2. Converts it from BGR to RGB to HSV color space
             3. Modifies the Hue and Value channels based on input parameters
             4. Converts back to RGB using both loop and matrix-based methods
             5. Optionally saves the result and prints transformation details
    
    @param image_path Path to the input image file
    @type image_path str
    @param hue_shift Amount to shift the hue channel in degrees (0-360)
    @type hue_shift float
    @param value_exp Exponential value for value channel modification (0.5-4)
    @type value_exp float
    @param save_path Optional path to save the modified image
    @type save_path str or None
    @param print_values Whether to print detailed transformation values
    @type print_values bool
    
    @return Tuple containing (original_image, modified_loops, modified_numpy)
    @rtype tuple(numpy.ndarray, numpy.ndarray, numpy.ndarray)
    
    @exception ValueError If the image cannot be loaded or parameters are invalid
    @exception IOError If the save path is invalid
    @exception cv2.error If OpenCV operations fail
    
    @see hsv_to_rgb_loop For loop-based HSV to RGB conversion
    @see hsv_to_rgb_matrix For matrix-based HSV to RGB conversion
    """
    # Create an instance of ColorConverter
    converter = ColorConverter()
    
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    # Convert BGR to RGB (OpenCV loads as BGR)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert RGB to HSV using OpenCV
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    
    # Create a copy of the HSV image for modification
    modified_hsv = img_hsv.copy()
    
    # Modify the Hue channel
    hue_shift_normalized = hue_shift / 2
    original_hue = modified_hsv[:, :, 0].copy()
    modified_hsv[:, :, 0] = (modified_hsv[:, :, 0] + hue_shift_normalized) % 180
    modified_hue = modified_hsv[:, :, 0]
    
    # Modify the Value channel
    original_value = modified_hsv[:, :, 2].copy()
    normalized_value = original_value / 255.0
    modified_value = np.power(normalized_value, value_exp) * 255.0
    modified_hsv[:, :, 2] = np.clip(modified_value, 0, 255).astype(np.uint8)
    
    if print_values:
        print("\nHue Channel Transformation:")
        print(f"  - Original Hue Range: [{np.min(original_hue)}, {np.max(original_hue)}] (OpenCV scale: 0-180)")
        print(f"  - Modified Hue Range: [{np.min(modified_hue)}, {np.max(modified_hue)}] (OpenCV scale: 0-180)")
        print(f"  - Original Hue Range in Degrees: [{float(np.min(original_hue))*2:.1f}, {float(np.max(original_hue))*2:.1f}]°")
        print(f"  - Modified Hue Range in Degrees: [{float(np.min(modified_hue))*2:.1f}, {float(np.max(modified_hue))*2:.1f}]°")
        print(f"  - Applied Hue Shift: {hue_shift}°")
        
        print("\nValue Channel Transformation:")
        print(f"  - Original Value Range: [{np.min(original_value)}, {np.max(original_value)}] (0-255)")
        print(f"  - Modified Value Range: [{np.min(modified_hsv[:, :, 2])}, {np.max(modified_hsv[:, :, 2])}] (0-255)")
        print(f"  - Applied Exponential Value: {value_exp}")

        # Print a sample of pixel transformations (5 random pixels)
        height, width = img_hsv.shape[:2]
        sample_points = []
        for _ in range(5):
            y = np.random.randint(0, height)
            x = np.random.randint(0, width)
            sample_points.append((y, x))
        
        print("\nSample Pixel Transformations (5 random pixels):")
        for i, (y, x) in enumerate(sample_points):
            print(f"\nPixel {i+1} at position ({x}, {y}):")
            print(f"  - Original Hue: {original_hue[y, x]} ({float(original_hue[y, x])*2:.1f}°)")
            print(f"  - Modified Hue: {modified_hue[y, x]} ({float(modified_hue[y, x])*2:.1f}°)")
            print(f"  - Original Value: {original_value[y, x]}")
            print(f"  - Modified Value: {modified_hsv[y, x, 2]}")
            print(f"  - Normalized Original Value: {original_value[y, x]/255:.4f}")
            print(f"  - After Value Exp Transformation: {(original_value[y, x]/255)**value_exp:.4f}")
    
    # Convert modified HSV back to RGB using different methods
    start_time_loops = time.time()
    modified_rgb_loops = converter.hsv_to_rgb_loop(modified_hsv)
    time_loops = time.time() - start_time_loops
    
    start_time_matrix = time.time()
    modified_rgb_matrix = converter.hsv_to_rgb_matrix(modified_hsv)
    time_matrix = time.time() - start_time_matrix
    
    print(f"\nMethod comparison for image shape {img.shape}:")
    print(f"  - Traditional loops: {time_loops:.6f} seconds")
    print(f"  - Matrix operations: {time_matrix:.6f} seconds")
    print(f"  - Speed improvement: {time_loops / time_matrix:.2f}x")
    
    if save_path:
        modified_rgb_bgr = cv2.cvtColor(modified_rgb_matrix, cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, modified_rgb_bgr)
        print(f"Modified image saved to {save_path}")
    
    return img_rgb, modified_rgb_loops, modified_rgb_matrix

def compare_performance(image_paths):
    """
    @brief Compare performance between loop and matrix-based conversion methods.
    
    @details This function:
             1. Loads each image from the provided paths
             2. Times both conversion methods on each image
             3. Creates performance comparison plots
             4. Saves results as 'performance_comparison.png'
    
    @param image_paths List of paths to test images of different sizes
    @type image_paths list[str]
    
    @exception FileNotFoundError If any image file cannot be found
    @exception ValueError If images cannot be loaded
    @exception IOError If saving the plot fails
    
    @see hsv_to_rgb_loop For the loop-based implementation
    @see hsv_to_rgb_matrix For the matrix-based implementation
    """
    # Create an instance of ColorConverter
    converter = ColorConverter()
    
    loop_times = []
    matrix_times = []
    image_sizes = []
    
    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"Could not load image from {path}")
            continue
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
        
        # Measure time for loop-based conversion
        start_time = time.time()
        converter.hsv_to_rgb_loop(img_hsv)
        loop_time = time.time() - start_time
        
        # Measure time for matrix-based conversion
        start_time = time.time()
        converter.hsv_to_rgb_matrix(img_hsv)
        matrix_time = time.time() - start_time
        
        # Record times and image size
        loop_times.append(loop_time)
        matrix_times.append(matrix_time)
        image_sizes.append(img.shape[0] * img.shape[1])
        
        print(f"Image: {path}")
        print(f"  - Size: {img.shape[0]}x{img.shape[1]} ({img.shape[0] * img.shape[1]} pixels)")
        print(f"  - Loop time: {loop_time:.6f} seconds")
        print(f"  - Matrix time: {matrix_time:.6f} seconds")
        print(f"  - Speed improvement: {loop_time / matrix_time:.2f}x")
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(image_sizes, loop_times, 'o-', label='Traditional loops')
    plt.plot(image_sizes, matrix_times, 'o-', label='Matrix operations')
    plt.xlabel('Image Size (pixels)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Performance Comparison: HSV to RGB Conversion')
    plt.legend()
    plt.grid(True)
    plt.savefig('performance_comparison.png')
    plt.show()

def show_results(original, modified_loops, modified_matrix):
    """
    @brief Display comparison of original and modified images.
    
    @details Creates a figure with three subplots showing:
             1. The original image
             2. The modified image using loop-based conversion
             3. The modified image using matrix-based conversion
    
    @param original Original RGB image
    @type original numpy.ndarray
    @param modified_loops Modified image using loop-based conversion
    @type modified_loops numpy.ndarray
    @param modified_matrix Modified image using matrix-based conversion
    @type modified_matrix numpy.ndarray
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(original)
    axes[0].set_title('Original Image')
    axes[0].axis('off')
    
    axes[1].imshow(modified_loops)
    axes[1].set_title('Modified (Loop-based)')
    axes[1].axis('off')
    
    axes[2].imshow(modified_matrix)
    axes[2].set_title('Modified (Matrix-based)')
    axes[2].axis('off')
    
    plt.tight_layout()
    plt.savefig('comparison.png')
    plt.show()


def main():
    """
    @brief Application entry point demonstrating library functionality.
    
    @details This function demonstrates the core functionality of the library:
             1. Image loading and HSV modification
             2. Visualization of transformations
             3. Performance comparison between methods
             4. Saving results to files
    
    The function uses example values:
    - Hue shift: 120 degrees
    - Value exponential: 1.5
    
    @exception FileNotFoundError If the input image cannot be found
    @exception RuntimeError If processing fails
    @exception IOError If saving output files fails
    
    @see modify_hsv_image For the core transformation function
    @see visualize_hsv_changes For HSV visualization
    @see compare_performance For method comparison
    """
    # Example usage
    image_path = "input_image.jpg"  # Replace with your image path
    
    # Parameters for modification
    hue_shift = 120  # Shift hue by 120 degrees
    value_exp = 1.5  # Apply exponential value of 1.5 to value channel
    
    # Process the image with value printing enabled
    try:
        original, modified_loops, modified_matrix = modify_hsv_image(
            image_path, 
            hue_shift, 
            value_exp, 
            save_path="output_image.jpg",
            print_values=True  # Enable printing of values
        )
        
        # Show the results
        show_results(original, modified_loops, modified_matrix)
        

        
        # Compare performance with images of different sizes
        # This is just an example; you would need to provide actual image paths
        # compare_performance(["small.jpg", "medium.jpg", "large.jpg"])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    """
    @brief Script entry point.
    
    @details Executes the main function and handles any uncaught exceptions
             that may occur during execution.
    
    @exception Exception All exceptions are caught and their messages printed
    """
    main()