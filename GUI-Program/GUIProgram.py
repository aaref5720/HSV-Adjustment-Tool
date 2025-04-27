# @file HSVAdjustmentApp.py
# @brief GUI application for HSV color space manipulation with performance comparison.
# @details This application provides a graphical interface for:
#          - Loading and manipulating images in HSV color space
#          - Real-time adjustment of Hue, Saturation, and Value channels
#          - Performance comparison between matrix and loop-based HSV-RGB conversion
#          - Saving processed images in various formats
# @author Abdelrahman Aref & Ahmed Hassan
# @date 2025
# @version 0.1
# @copyright 2025 Abdelrahman Aref & Ahmed Hassan
# @license MIT
#
# @section DESCRIPTION
# This application demonstrates real-time image processing using the HSV color space.
# It provides both matrix-based and loop-based implementations for color space
# conversion, allowing performance comparison between the two approaches.
#
# @section INSTALLATION
# Requirements:
#   - Python 3.8 or higher
#   - PyQt6 (>=6.0.0)
#   - OpenCV (>=4.0.0)
#   - NumPy (>=1.19.0)
#
# Installation steps:
#   1. pip install PyQt6>=6.0.0
#   2. pip install opencv-python>=4.0.0
#   3. pip install numpy>=1.19.0
#
# @section USAGE
# To run the application:
#   python HSVAdjustmentApp.py
#
# @section TROUBLESHOOTING
# Common issues:
#   1. UI file not found:
#      - Ensure 'main_window.ui' is in the same directory
#   2. Image loading fails:
#      - Check file permissions and format support
#   3. Performance issues:
#      - Reduce image size for better performance
#      - Use matrix-based conversion for large images
#
# @section EXAMPLES
# Basic usage:
#    app = QApplication(sys.argv)
#    window = HSVAdjustmentApp()
#    window.show()
#    sys.exit(app.exec())
#
# @todo
#    - Add batch processing capability
#    - Implement undo/redo functionality
#    - Add image histogram display
#    - Add support for additional color spaces
#    - Implement image preprocessing options
#
# @bug
#    - Large images may cause memory issues
#    - UI may freeze during heavy processing
#
# @note
#    - Matrix operations are significantly faster than loop-based operations
#    - Memory usage increases with image size
#    - GUI responsiveness depends on image size and processing method

# System imports
import sys
import os
import time

# Image processing imports
import cv2
import numpy as np

# GUI imports
from PyQt6.QtWidgets import (
    QApplication, 
    QWidget, 
    QFileDialog, 
    QMessageBox,
    QGraphicsScene, 
    QGraphicsPixmapItem
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6 import QtCore, uic


class HSVAdjustmentApp(QWidget):
    """Main application class for HSV image adjustment.
    
    @brief GUI application for HSV color space manipulation
    
    @details This class implements a GUI application that provides tools for:
             - Image loading and display
             - Real-time HSV adjustments
             - Conversion method comparison
             - Image saving capabilities
             The application uses OpenCV for image processing and PyQt6 for the GUI.
    
    @exception RuntimeError If GUI components fail to initialize
    @exception ImportError If required libraries are not available
    @see QWidget Base class providing GUI functionality
    """
    
    def __init__(self):
        """Initialize the HSV Adjustment application.
        
        @brief Set up the UI components and initialize application state
        
        @details Sets up the UI components, initializes variables, and connects signal handlers
        
        @exception FileNotFoundError If the UI file cannot be found
        @exception RuntimeError If UI components cannot be initialized
        @exception ImportError If required Qt modules cannot be loaded
        """
        super().__init__()
        
        ui_path = os.path.join(os.path.dirname(__file__), 'main_window.ui')
        if not os.path.exists(ui_path):
            raise FileNotFoundError(f"Cannot find UI file at: {ui_path}")
        
        uic.loadUi((ui_path), self)
        self.setWindowTitle("HSV Adjustment Tool")
        
        # Disable maximize button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint)
        
        # Initialize variables
        self.image_path = None
        self.original_image = None
        self.adjusted_image = None
        self.hsv_image = None
        self.current_hsv = None
        
        # Connect UI elements
        self.UploadButton.clicked.connect(self.load_image)
        self.SaveMatrixButton.clicked.connect(lambda: self.save_image('matrix'))
        self.SaveLoopButton.clicked.connect(lambda: self.save_image('loop'))
        self.CompareButton.clicked.connect(self.compare_methods)
        
        # Connect sliders
        self.HueSlider.valueChanged.connect(self.update_sliders_and_image)
        self.SaturatedSlider.valueChanged.connect(self.update_sliders_and_image)
        self.ValueSlider.valueChanged.connect(self.update_sliders_and_image)
        
        # Setup graphics scenes
        self.original_scene = QGraphicsScene()
        self.graphicsView.setScene(self.original_scene)
        
        self.adjusted_scene = QGraphicsScene()
        self.graphicsView_2.setScene(self.adjusted_scene)
        
        # Initialize slider labels
        self.update_slider_labels()

        # Set the fixed size of the graphics views to 256x170
        self.graphicsView.setFixedSize(256, 170)  
        self.graphicsView_2.setFixedSize(256, 170)


    def update_slider_labels(self):
        """Update the UI labels with current slider values.
        
        @brief Update numerical displays for HSV sliders
        
        @details Updates the text displays showing the current values of all HSV sliders
        
        @exception ValueError If slider values are invalid
        @see update_image For the actual image processing
        """
        self.HueValue.setText(str(self.HueSlider.value()))
        self.SaturationValue.setText(str(self.SaturatedSlider.value()))
        self.SaturationValue_2.setText(str(self.ValueSlider.value()))
    
    @pyqtSlot()
    def load_image(self):
        """Load an image file selected through a file dialog.
        
        @brief Load and initialize an image for HSV processing
        
        @details Opens a file dialog for image selection, loads the selected image,
                and initializes it for HSV processing
        
        @exception IOError If the image file cannot be read
        @exception cv2.error If OpenCV fails to process the image
        @exception MemoryError If image is too large to process
        @see show_images For display update
        """
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Image files (*.jpg *.jpeg *.png *.bmp)")
        if file_dialog.exec():
            self.image_path = file_dialog.selectedFiles()[0]
            if self.image_path:
                # Load and process the image
                self.original_image = cv2.imread(self.image_path)
                self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
                self.adjusted_image = self.original_image.copy()
                self.hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_RGB2HSV).astype(np.float32)
                self.current_hsv = self.hsv_image.copy()
                self.show_images()
    
    def update_sliders_and_image(self):
        """Handle slider value changes and update the image.
        
        @brief Update image processing based on slider changes
        
        @details Updates both the slider value labels and processes the image
                when any HSV slider value changes
        
        @exception ValueError If slider values are out of valid range
        @see update_image For the actual image processing
        """
        self.update_slider_labels()
        self.update_image()
    
    def update_image(self):
        """Process and update the displayed image based on current HSV settings.
        
        @brief Apply HSV adjustments and update display
        
        @details Applies the current HSV adjustments to the image and updates the display:
                - Hue shift (0-180 degrees)
                - Saturation multiplication (0-200%)
                - Value/brightness gamma adjustment (0-200%)
        
        @exception ValueError If adjustment values are out of valid range
        @exception RuntimeError If image processing fails
        @exception MemoryError If insufficient memory for processing
        @see hsv_to_rgb_matrix For the color space conversion
        @see show_images For the display update
        """
        if self.original_image is None:
            return
        
        hue_shift = self.HueSlider.value() / 2 # OpenCV uses 0-180 for hue
        saturation_factor = self.SaturatedSlider.value() / 100.0
        gamma = self.ValueSlider.value() / 100.0
        
        current_hsv = self.hsv_image.copy()
        current_hsv[:, :, 0] = (current_hsv[:, :, 0] + hue_shift) % 180  # OpenCV uses 0-180 for hue
        current_hsv[:, :, 1] = np.clip(current_hsv[:, :, 1] * saturation_factor, 0, 255)

        normalized_value = current_hsv[:, :, 2] / 255.0
        modified_value = np.power(normalized_value, gamma) * 255.0
        current_hsv[:, :, 2] = np.clip(modified_value, 0, 255)
        
        self.current_hsv = current_hsv
        self.adjusted_image = cv2.cvtColor(current_hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
        self.show_images()
    
    def show_images(self):
        """Display both original and adjusted images in the UI.
        
        @details Converts the numpy arrays to QImage format and displays them
                in their respective QGraphicsView widgets while maintaining aspect ratio.
        
        @exception ValueError If image data is invalid
        @exception RuntimeError If graphics view initialization fails
        """
        if self.original_image is None:
            return
        
        # Prepare original image for display
        orig_img = self.original_image.copy()
        orig_height, orig_width = orig_img.shape[:2]
        
        # Create QImage from numpy array (original)
        bytes_per_line = 3 * orig_width
        q_orig_img = QImage(orig_img.data, orig_width, orig_height, 
                          bytes_per_line, QImage.Format.Format_RGB888)
        
        # Clear scenes and add images
        self.original_scene.clear()
        pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(q_orig_img))
        self.original_scene.addItem(pixmap_item)
        self.graphicsView.fitInView(pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        
        # Prepare adjusted image for display
        adj_img = self.adjusted_image.copy()
        adj_height, adj_width = adj_img.shape[:2]
        
        # Create QImage from numpy array (adjusted)
        bytes_per_line = 3 * adj_width
        q_adj_img = QImage(adj_img.data, adj_width, adj_height, 
                         bytes_per_line, QImage.Format.Format_RGB888)
        
        self.adjusted_scene.clear()
        pixmap_item2 = QGraphicsPixmapItem(QPixmap.fromImage(q_adj_img))
        self.adjusted_scene.addItem(pixmap_item2)
        self.graphicsView_2.fitInView(pixmap_item2, Qt.AspectRatioMode.KeepAspectRatio)
    
    def resizeEvent(self, event):
        """Handle window resize events.
        
        @param event The resize event containing the window's new dimensions
        @details Ensures images are properly scaled when the window is resized
                while maintaining their aspect ratios.
        """
        super().resizeEvent(event)
        if hasattr(self, 'original_scene') and self.original_scene.items():
            self.graphicsView.fitInView(self.original_scene.items()[0], Qt.AspectRatioMode.KeepAspectRatio)
        if hasattr(self, 'adjusted_scene') and self.adjusted_scene.items():
            self.graphicsView_2.fitInView(self.adjusted_scene.items()[0], Qt.AspectRatioMode.KeepAspectRatio)
    
    def hsv_to_rgb_matrix(self, hsv_img):
        """Convert HSV to RGB using vectorized matrix operations.
        
        @brief Perform HSV to RGB conversion using optimized NumPy operations
        
        @param hsv_img Input HSV image in OpenCV format (H: 0-180, S/V: 0-255)
        @type hsv_img numpy.ndarray
        @return RGB image in uint8 format
        @rtype numpy.ndarray
        
        @details Performs color space conversion using NumPy's optimized operations.
                The conversion follows the standard HSV to RGB algorithm but vectorized
                for better performance
        
        @exception ValueError If input is not a 3-channel numpy array
        @exception TypeError If input array has incorrect data type
        @exception MemoryError If insufficient memory for processing
        @see hsv_to_rgb_loop For the alternative implementation
        """
        hsv_img = hsv_img.astype(np.float32)
        # Scale hue from OpenCV's 0-180 range to 0-360 degrees
        h, s, v = hsv_img[:, :, 0] * 2.0, hsv_img[:, :, 1], hsv_img[:, :, 2]
        h = h / 60.0
        s = s / 255.0
        v = v / 255.0
        c = v * s
        x = c * (1 - np.abs((h % 2) - 1))
        m = v - c
        
        # Initialize RGB with zeros
        rgb = np.zeros_like(hsv_img)
        
        # Create a zeros array for the third channel with proper dimensions
        zeros = np.zeros_like(c)
        
        # Apply the conversion for each hue region
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
        
        # Add the m value to each channel
        rgb[:, :, 0] += m
        rgb[:, :, 1] += m
        rgb[:, :, 2] += m
        
        return (rgb * 255).clip(0, 255).astype(np.uint8)
    
    def hsv_to_rgb_loop(self, hsv_img):
        """Convert HSV to RGB using pixel-by-pixel loop processing.
        
        @brief Perform HSV to RGB conversion using explicit loops
        
        @param hsv_img Input HSV image in OpenCV format (H: 0-180, S/V: 0-255)
        @type hsv_img numpy.ndarray
        @return RGB image in uint8 format
        @rtype numpy.ndarray
        
        @details This method processes each pixel individually, which is slower
                but may be more memory-efficient for very large images
        
        @exception ValueError If input is not a 3-channel numpy array
        @exception TypeError If input array has incorrect data type
        @exception MemoryError If insufficient memory for processing
        @see hsv_to_rgb_matrix For the optimized matrix implementation
        """
        hsv_img = hsv_img.astype(np.float32)
        height, width = hsv_img.shape[:2]
        rgb_img = np.zeros((height, width, 3), dtype=np.uint8)
        
        for i in range(height):
            for j in range(width):
                h, s, v = hsv_img[i, j]
                # Scale hue from OpenCV's 0-180 range to 0-360 degrees
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
    
    def save_image(self, method='matrix'):
        """Save the processed image using the specified conversion method.
        
        @brief Save the current image state to a file
        
        @param method Conversion method to use ('matrix' or 'loop')
        @type method str
        
        @details Displays a file dialog for saving the image and shows processing time.
                Supported formats: JPEG (.jpg), PNG (.png)
        
        @exception IOError If the file cannot be written
        @exception ValueError If the conversion method is invalid
        @exception MemoryError If insufficient memory for processing
        @see hsv_to_rgb_matrix For matrix-based conversion
        @see hsv_to_rgb_loop For loop-based conversion
        """
        if self.adjusted_image is None:
            QMessageBox.critical(self, "Error", "No image to save!")
            return
        
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "",
            "JPEG Files (*.jpg);;PNG Files (*.png)"
        )
        
        if not save_path:
            return
        
        start = time.time()
        if method == 'matrix':
            rgb_image = self.hsv_to_rgb_matrix(self.current_hsv)
        else:
            rgb_image = self.hsv_to_rgb_loop(self.current_hsv)
        
        cv2.imwrite(save_path, cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR))
        elapsed = time.time() - start
        
        QMessageBox.information(
            self,
            "Success",
            f"Saved using {method} method in {elapsed:.4f} sec"
        )
    
    def compare_methods(self):
        """Compare performance between matrix and loop-based conversion methods.
        
        @brief Benchmark different HSV to RGB conversion methods
        
        @details Tests both conversion methods on different image sizes:
                - 100x100 (small image)
                - 400x400 (medium image)
                - 800x800 (large image)
        
        @exception RuntimeError If comparison fails
        @exception MemoryError If insufficient memory for testing
        @exception ValueError If current image is invalid
        @see hsv_to_rgb_matrix For the matrix-based implementation
        @see hsv_to_rgb_loop For the loop-based implementation
        """
        if self.hsv_image is None:
            QMessageBox.critical(self, "Error", "No image loaded!")
            return
        
        sizes = [(100, 100), (400, 400), (800, 800)]
        results = []
        
        for size in sizes:
            test_hsv = cv2.resize(self.current_hsv, size)
            
            # Time matrix method
            start = time.time()
            _ = self.hsv_to_rgb_matrix(test_hsv)
            matrix_time = time.time() - start
            
            # Time loop method
            start = time.time()
            _ = self.hsv_to_rgb_loop(test_hsv)
            loop_time = time.time() - start
            
            speedup = loop_time / matrix_time
            results.append(f"{size[0]}x{size[1]}: Matrix={matrix_time:.4f}s, Loop={loop_time:.4f}s, Speedup={speedup:.2f}x")
        
        QMessageBox.information(
            self,
            "Performance Comparison",
            "\n".join(results)
        )

    def showEvent(self, event):
        """Handle the initial window show event.
        
        @brief Initialize graphics views on window display
        
        @param event The show event object
        @type event QShowEvent
        
        @details Ensures proper initialization and scaling of graphics views
                when the window is first displayed
        
        @exception RuntimeError If graphics views cannot be initialized
        @see resizeEvent For handling subsequent size changes
        """
        super().showEvent(event)
        # This ensures proper sizing of graphics views
        if hasattr(self, 'original_scene') and self.original_scene.items():
            self.graphicsView.fitInView(self.original_scene.items()[0], Qt.AspectRatioMode.KeepAspectRatio)
        if hasattr(self, 'adjusted_scene') and self.adjusted_scene.items():
            self.graphicsView_2.fitInView(self.adjusted_scene.items()[0], Qt.AspectRatioMode.KeepAspectRatio)

if __name__ == "__main__":
    """Application entry point.
    
    @brief Initialize and run the HSV Adjustment application
    
    @details Creates and runs the HSV Adjustment application with dark theme styling.
             Handles any uncaught exceptions during execution
    
    @exception RuntimeError If application fails to start
    @exception SystemExit On normal application termination
    """
    App = QApplication(sys.argv)
    App.setStyleSheet('''
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QPushButton {
            background-color: #9dc0f9;
            color: #2b2b2b;
            border: 1px solid #9dc0f9;
            border-radius: 8px;
            padding: 5px 12px;
        }
        QPushButton:hover {
            background-color: #9dc0f9;
        }
    ''')
    try:
        window = HSVAdjustmentApp()
        window.show()
        sys.exit(App.exec())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
        