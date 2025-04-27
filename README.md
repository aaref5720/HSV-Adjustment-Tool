
# Computer Vision - Assignment 1 (Group 3)  
**HSV Color Space Manipulation Tool**  
*Deggendorf Institute of Technology | Summer 2025*  

Submitted by: **Abdelrahman Mohamed & Ahmed Hassan**  
Instructor: **Prof. Marcus Barkowsky**  
Due: **April 27, 2025**

---

## Overview

This submission fulfills the requirements for Assignment 1 for Group 3.  
We implemented the HSV color space manipulation tool in **two different approaches**:

1. **StaticProgram.py** – a minimal command-line interface version that meets all assignment requirements using a clean and direct coding style.
2. **GUIProgram.py** – a more creative and user-friendly PyQt6 GUI, designed using **Qt Designer’s drag-and-drop interface** (`main_window.ui`). It provides interactive sliders and real-time previews for HSV editing.

---

## Highlights

- ✅ **RGB → HSV → RGB conversion** (OpenCV for RGB↔HSV, and custom HSV→RGB)
- ✅ **Hue rotation** (0–360°)
- ✅ **Value gamma correction** (0.5–4.0x)
- ✅ **Two HSV→RGB methods**:
  - Loop-based (classic)
  - Matrix-based (NumPy-optimized)
- ✅ **Performance benchmarking**
- ✅ **Interactive GUI** with real-time controls
- ✅ **Full Doxygen documentation**  
- ✅ **HTML Docs** generated for each module (`index.html`)

---

## File Structure

```plaintext
GROUP3_SUBMISSION/
├── GUI-Program/
│   ├── GUIProgram.py             # GUI implementation using PyQt6 (fully documented)
│   ├── main_window.ui            # Qt Designer file
│   ├── input_image.jpg           # Sample input image for testing
│   ├── Doxyfile                  # Doxygen configuration
│   └── docs/html/index.html      # HTML documentation for GUIProgram.py
├── Static-Program/
│   ├── StaticProgram.py          # CLI implementation (fully documented)
│   ├── input_image.jpg           # Sample input image for testing
│   ├── Doxyfile                  # Doxygen configuration
│   └── docs/html/index.html      # HTML documentation for StaticProgram.py
├── Presentation.pdf              # 5-slide summary presentation
├── Results/
│   ├── sample_output.jpg         # Example result image
│   └── performance.png           # Benchmarking graph
└── README.md                     # This file
```

---

## Installation

### Dependencies
```bash
# Base requirements (both implementations)
pip install opencv-python numpy matplotlib

# GUI-specific requirements
pip install PyQt6
```

### Verify Installation
```bash
python -c "import cv2, numpy, PyQt6"
```

---

## How to Run

### Option 1: Static Program (CLI)
```bash
python Static-Program/StaticProgram.py
```

- Loads `input_image.jpg`  
- Applies configurable **hue shift** and **value gamma correction**  
- Shows original vs. modified images in a pop-up window  
- ⚡ **Performance comparison** is printed in the **console**  

### Option 2: GUI Application
```bash
python GUI-Program/GUIProgram.py
```

- Upload an image  
- Adjust **Hue**, **Saturation**, and **Value (Gamma)** with sliders  
- Save using either **Matrix** or **Loop** method  
- 🧪 Use **Compare** button to benchmark both methods  

---

## Notes for Evaluation

- 📘 Both scripts are documented using **Doxygen-style comments**
- 🌐 HTML documentation is included under `docs/html/index.html` in both `GUI-Program/` and `Static-Program/`
- 🎨 The GUI layout was created using **Qt Designer’s drag-and-drop editor** (`main_window.ui`)
- ⚡ Performance comparison is displayed via **console** (StaticProgram) or in the **GUI** by pressing the **Compare Methods** button
- 🔬 All HSV transformations are reproducible, validated visually, and match OpenCV's internal conversions

---

## License

MIT License  
© 2025 Abdelrahman Mohamed & Ahmed Hassan  
*Submitted as coursework for Computer Vision – DIT Summer 2025*
