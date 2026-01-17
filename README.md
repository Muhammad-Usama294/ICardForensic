# 🆔 ICardForensic - AI-Powered ID Card Intelligence System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF.svg)](https://github.com/ultralytics/ultralytics)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An intelligent computer vision application that automatically extracts information from Pakistani CNIC (Computerized National Identity Card) cards using state-of-the-art AI technologies. This system combines YOLOv8 for precise object detection and EasyOCR for accurate text recognition, all wrapped in an intuitive Streamlit web interface.

## ✨ Features

- **🤖 AI-Powered Detection**: YOLOv8 model for detecting ID card fields with high accuracy
- **📝 OCR Text Extraction**: EasyOCR for reading text from detected regions
- **🖥️ Interactive Web Interface**: Streamlit-based GUI with real-time preview
- **🎨 Image Enhancement**: Adjustable contrast, brightness, and sharpness controls
- **🔍 Field Detection**: Extracts Name, CNIC Number, and Father's Name
- **📊 Extraction History**: Logs all extracted data with timestamps
- **📦 Visual Annotations**: Displays bounding boxes on detected fields
- **⚡ Pre-trained Model**: Includes custom-trained YOLOv8 model (`best.pt`)
- **💾 Data Export**: Download extracted data as CSV
- **⚙️ Configurable**: Adjustable confidence thresholds and preprocessing options

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Streamlit** | Web UI and interactive interface |
| **YOLOv8** (Ultralytics) | Object detection for field localization |
| **EasyOCR** | Optical character recognition |
| **OpenCV** (cv2) | Image processing and manipulation |
| **PIL** (Pillow) | Image enhancement operations |
| **PyTorch** | Deep learning framework (via YOLOv8) |
| **NumPy** | Numerical operations |
| **Pandas** | Data handling and CSV export |
| **Python 3.x** | Core programming language |

## 📁 Project Structure

```
ICardForensic/
├── app.py                      # Main Streamlit application
├── best.pt                     # Trained YOLOv8 model (52 MB)
├── extraction_log.txt          # History of extracted data
├── cards.v1i.yolov8/          # Training dataset
│   ├── data.yaml              # Dataset configuration
│   ├── README.dataset.txt     # Dataset information
│   ├── README.roboflow.txt    # Roboflow export details
│   ├── train/                 # Training images and labels
│   └── valid/                 # Validation images and labels
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## 🎯 Model Information

### YOLOv8 Model Details

- **Model File**: `best.pt` (52 MB)
- **Architecture**: YOLOv8 (You Only Look Once v8)
- **Classes Detected**: 3 classes
  - `name`: Cardholder's name
  - `number`: CNIC number (13-digit format: XXXXX-XXXXXXX-X)
  - `fname`: Father's name
- **Training Dataset**: 43 images from Roboflow
- **Dataset Source**: [Roboflow Universe - cards-rzpvy](https://universe.roboflow.com/kraken00/cards-rzpvy)
- **License**: CC BY 4.0
- **Input Resolution**: 641x400
- **Preprocessing**: Resized to 641x400 (stretched)

## 📦 Installation & Setup

### Prerequisites

```bash
Python 3.8 or higher
Webcam or image files for ID card scanning
```

### Step-by-Step Installation

#### Option 1: Using Requirements File (Recommended)

```bash
# Clone the repository
git clone https://github.com/Muhammad-Usama294/ICardForensic.git
cd ICardForensic

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

#### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/Muhammad-Usama294/ICardForensic.git
cd ICardForensic

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies one by one
pip install streamlit>=1.28.0
pip install ultralytics>=8.0.0
pip install easyocr>=1.7.0
pip install opencv-python>=4.8.0
pip install numpy>=1.24.0
pip install pandas>=2.0.0
pip install pillow>=10.0.0
```

## 🚀 Usage Guide

### Running the Application

```bash
streamlit run app.py
```

This will open the application in your default web browser at `http://localhost:8501`

### Step-by-Step Usage

1. **📤 Upload ID Card Image**:
   - Click "Browse files" or drag & drop your ID card image
   - Supported formats: JPG, JPEG, PNG

2. **⚙️ Adjust Image Enhancement** (Optional):
   - Use sidebar sliders to adjust:
     - **Contrast** (0.5 - 2.0): Enhance image contrast
     - **Brightness** (0.5 - 2.0): Adjust brightness levels
     - **Sharpness** (0.0 - 3.0): Sharpen image details
   - Adjust **Confidence Threshold** (0.1 - 0.9): Detection sensitivity

3. **🖼️ View Processed Image**:
   - Compare original vs enhanced image side-by-side
   - Preview your adjustments in real-time

4. **🚀 Extract Information**:
   - Click "🚀 EXECUTE PIPELINE" button
   - AI model detects and extracts fields
   - Progress bar shows pipeline stages:
     - Phase 1: YOLOv8 Detection
     - Phase 2: Cropping Regions
     - Phase 3: OCR Reading

5. **📊 Review Results**:
   - View extracted data in structured format:
     - Name
     - CNIC Number
     - Father's Name
   - See bounding boxes on detected regions
   - Review individual cropped segments with OCR text
   - Download results as CSV

6. **📝 Check History**:
   - Navigate to "History Logs" tab
   - View all past extractions with timestamps
   - Stored in `extraction_log.txt`

## 🔧 How It Works

### Detection Pipeline

```
1. Image Upload      →  User uploads ID card image
2. Pre-processing    →  Optional contrast/brightness/sharpness enhancement
3. YOLO Detection    →  YOLOv8 model detects name, number, fname regions
4. Region Extraction →  Bounding boxes cropped from image
5. OCR Processing    →  EasyOCR extracts text from each region
6. Post-processing   →  Clean and format extracted text
7. Display Results   →  Show structured data with visual annotations
8. Logging          →  Save to extraction_log.txt with timestamp
```

### Code Architecture

- **Model Loading**: Cached with `@st.cache_resource` for performance optimization
- **Image Enhancement**: PIL ImageEnhance for manual adjustments
- **Detection**: YOLOv8 inference on enhanced image
- **OCR**: EasyOCR reader with English language support
- **Logging**: Timestamped entries in text file for audit trail

### Technical Flow

```python
# 1. Load Models (Cached)
model = YOLO('best.pt')
reader = easyocr.Reader(['en'])

# 2. Enhance Image
enhanced_img = apply_enhancements(image, contrast, brightness, sharpness)

# 3. Detect Fields
results = model(enhanced_img, conf=conf_threshold)

# 4. Extract Text
for box in results.boxes:
    crop = image[y1:y2, x1:x2]
    text = reader.readtext(crop)
    
# 5. Save Results
save_to_history(data, filename)
```

## 🪪 Supported ID Cards

### Currently Optimized For:

- **Pakistani CNIC** (Computerized National Identity Card)
  - Format: 13-digit (XXXXX-XXXXXXX-X)
  - Fields: Name, CNIC Number, Father's Name

### Extensible To:

With additional training data, the system can be adapted for:
- 🛂 Passport information extraction
- 🚗 Driving license data extraction
- 🎫 Other government-issued ID cards
- 🏢 Employee ID cards
- 🎓 Student ID cards

## 📄 Sample Output

### Example Extraction

```
[2025-12-21 18:03:13] SOURCE: id_card.jpg
----------------------------------------
name: Sundal Shamim
number: 37406-6558377-8
fname: Hazrat Ali
========================================
```

### CSV Export Format

| name | number | fname |
|------|--------|-------|
| Sundal Shamim | 37406-6558377-8 | Hazrat Ali |

## ⚙️ Configuration & Customization

### Modify Detection Classes

Edit `cards.v1i.yolov8/data.yaml`:

```yaml
nc: 3
names: ['fname', 'name', 'number']

roboflow:
  workspace: kraken00
  project: cards-rzpvy
  version: 1
  license: CC BY 4.0
  url: https://universe.roboflow.com/kraken00/cards-rzpvy/dataset/1
```

### Adjust OCR Settings

In `app.py`, modify line 50:

```python
# Add Urdu language support and enable GPU
reader = easyocr.Reader(['en', 'ur'], gpu=True)
```

### Change Detection Model

Replace `best.pt` with your custom-trained YOLOv8 model:

```python
model = YOLO('path/to/your/model.pt')
```

### Adjust UI Configuration

Modify page settings in `app.py` (lines 11-16):

```python
st.set_page_config(
    page_title="ID Intelligence System",
    page_icon="🆔",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

## 🎓 Training Your Own Model

### Using Roboflow & Ultralytics

1. **Collect ID Card Images**: Gather diverse samples
2. **Annotate Fields**: Label name, number, fname regions
3. **Export in YOLOv8 Format**: Use Roboflow export feature
4. **Train Model**:

```python
from ultralytics import YOLO

# Load base model
model = YOLO('yolov8n.pt')

# Train on your dataset
results = model.train(
    data='cards.v1i.yolov8/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    name='id_card_detector'
)

# Export best model
model.export(format='pt')
```

5. **Replace Model**: Copy trained model to `best.pt`

### Training Tips

- **Dataset Size**: Minimum 100+ images recommended
- **Augmentation**: Use rotation, flip, brightness variations
- **Validation Split**: 80/20 train/validation ratio
- **Epochs**: Start with 50-100 epochs
- **Batch Size**: Adjust based on GPU memory

## ⚡ Performance Optimization

### Speed Improvements

```python
# 1. Enable GPU for YOLO (requires CUDA-enabled PyTorch)
model = YOLO('best.pt')
results = model(image, device='cuda')

# 2. Enable GPU for OCR
reader = easyocr.Reader(['en'], gpu=True)

# 3. Reduce image resolution
image = cv2.resize(image, (640, 400))

# 4. Use YOLOv8n (nano) for faster inference
model = YOLO('yolov8n.pt')
```

### Accuracy Improvements

- **Increase Training Dataset**: 500+ images for production
- **Data Augmentation**: Simulate various lighting/angles
- **Fine-tune Hyperparameters**: Learning rate, batch size
- **Adjust Detection Threshold**: Lower for recall, higher for precision
- **Image Preprocessing**: Enhance contrast before detection
- **Post-processing**: Validate format (e.g., CNIC: XXXXX-XXXXXXX-X)

## 🛠️ Troubleshooting

### Model Not Loading

**Problem**: `Model not found! Check 'best.pt'`

**Solutions**:
- Ensure `best.pt` is in the root directory
- Check file size (should be ~52 MB)
- Re-download model if corrupted
- Verify file permissions

### OCR Not Working

**Problem**: No text detected or incorrect text

**Solutions**:
```bash
# Reinstall EasyOCR
pip install --upgrade easyocr

# For Urdu support
reader = easyocr.Reader(['en', 'ur'])

# Enable GPU if available
reader = easyocr.Reader(['en'], gpu=True)
```

### Low Detection Accuracy

**Problem**: Fields not detected or wrong detections

**Solutions**:
- Ensure good lighting and clear image quality
- Use image enhancement sliders (increase contrast/sharpness)
- Lower confidence threshold in sidebar
- Check if ID card format matches training data
- Verify image is not blurry or damaged

### Streamlit Errors

**Problem**: Application crashes or errors

**Solutions**:
```bash
# Update Streamlit
pip install --upgrade streamlit

# Clear Streamlit cache
streamlit cache clear

# Run with debug mode
streamlit run app.py --logger.level=debug
```

### Memory Issues

**Problem**: Out of memory errors

**Solutions**:
- Reduce batch size in detection
- Resize images to smaller resolution
- Disable GPU if causing issues
- Close other applications

## 🔒 Security & Privacy Considerations

⚠️ **Important Security Notice**

This tool processes **sensitive personal information**. Please follow these guidelines:

- ✅ **Do NOT** store extracted data without user consent
- ✅ **Do NOT** share extracted information with third parties
- ✅ Implement **encryption** for stored logs
- ✅ Use **HTTPS** in production deployments
- ✅ Comply with data protection regulations (GDPR, PDPA, etc.)
- ✅ Add **user authentication** for production use
- ✅ **Sanitize and validate** all extracted data
- ✅ Implement **access controls** and audit logging
- ✅ **Delete** extraction logs periodically
- ✅ Add **watermarks** to processed images
- ✅ Implement **rate limiting** to prevent abuse
- ✅ Use **secure file upload** mechanisms

### Recommended Security Practices

```python
# 1. Encrypt extraction logs
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)

# 2. Add user authentication
import streamlit_authenticator as stauth

# 3. Validate extracted data
import re
def validate_cnic(cnic):
    pattern = r'^\d{5}-\d{7}-\d$'
    return re.match(pattern, cnic)
```

## 🚀 Future Enhancements

### Planned Features

- [ ] **Multi-language Support**: Add Urdu OCR for better accuracy
- [ ] **Batch Processing**: Process multiple ID cards at once
- [ ] **Database Integration**: Store extracted data in PostgreSQL/MongoDB
- [ ] **REST API**: API endpoints for integration with other systems
- [ ] **Mobile App**: Android/iOS app for on-the-go scanning
- [ ] **NADRA Verification**: Cross-check with NADRA database (with authorization)
- [ ] **Additional Fields**: Extract DOB, address, expiry date, issue date
- [ ] **Document Classification**: Automatically detect ID card type
- [ ] **Face Detection**: Extract and verify photograph from ID card
- [ ] **Tamper Detection**: Identify forged or modified ID cards
- [ ] **QR Code Reading**: Extract data from QR codes on modern CNICs
- [ ] **Multi-sided Scanning**: Process both front and back of ID card
- [ ] **OCR Confidence Scoring**: Display confidence for each field
- [ ] **Auto-correction**: Suggest corrections for common OCR errors
- [ ] **Export Formats**: PDF, Excel, JSON export options

### Potential Integrations

- 🏦 Banking KYC systems
- 🏨 Hotel check-in systems
- 🏥 Hospital registration
- 🎫 Event management
- 🚗 Car rental verification

## 📊 Dataset Information

- **Source**: [Roboflow Universe](https://universe.roboflow.com/kraken00/cards-rzpvy)
- **Project**: cards-rzpvy
- **Version**: v1
- **Images**: 43 training images
- **Annotations**: YOLOv8 format
- **Classes**: 3 (fname, name, number)
- **Preprocessing**: Resized to 641x400 (stretched)
- **Augmentation**: None applied
- **License**: CC BY 4.0
- **Export Date**: December 16, 2023
- **URL**: https://universe.roboflow.com/kraken00/cards-rzpvy/dataset/1

### Dataset Statistics

| Split | Images |
|-------|--------|
| Train | 43 |
| Valid | TBD |
| Test | TBD |

## ⚠️ Known Issues

- **Mouse/Keyboard Navigation**: Limited navigation in Streamlit UI
- **Language Support**: Currently limited to English OCR (Urdu can be added)
- **Image Quality**: Requires clear, well-lit images for best results
- **Damaged Cards**: May struggle with damaged, worn, or faded ID cards
- **Curved Cards**: Works best with flat, non-reflective surfaces
- **Font Variations**: May have reduced accuracy with unusual fonts
- **Handwritten Text**: Not optimized for handwritten information

## 🤝 Contributing

Contributions are welcome! Here are areas where you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Areas for Improvement

- 🌍 Add support for more ID card types (international)
- 🔤 Improve OCR accuracy with Urdu text support
- 🧪 Add unit tests and integration tests
- 🐳 Create Docker container for easy deployment
- 🎨 Enhance UI/UX design with better styling
- 📊 Add export to CSV/Excel/PDF functionality
- 📱 Develop mobile application version
- 🔍 Implement advanced tamper detection
- 🌐 Add internationalization (i18n) support
- 📈 Create analytics dashboard for extraction statistics

### Contribution Guidelines

- Follow PEP 8 style guidelines for Python code
- Write clear commit messages
- Add documentation for new features
- Test your changes thoroughly
- Update README if adding new features

## 📜 License

This project uses multiple licenses:

- **Code**: Consider adding an open-source license (MIT recommended)
- **Dataset**: CC BY 4.0 (Roboflow dataset)
- **YOLOv8**: AGPL-3.0 (Ultralytics)

**Note**: When using or modifying this project, respect all applicable licenses, especially the CC BY 4.0 license for the dataset.

### Recommended License (MIT)

```
MIT License

Copyright (c) 2025 Muhammad Usama

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

## 👨‍💻 Authors & Credits

### Developer
- **Muhammad Usama** - *Initial work and development* - [@Muhammad-Usama294](https://github.com/Muhammad-Usama294)

### Dataset
- **Roboflow Community** - Dataset provider (kraken00)
- **License**: CC BY 4.0
- **Source**: [cards-rzpvy](https://universe.roboflow.com/kraken00/cards-rzpvy)

### Frameworks & Libraries
- **YOLOv8** - [Ultralytics](https://github.com/ultralytics/ultralytics)
- **OCR** - [EasyOCR by JaidedAI](https://github.com/JaidedAI/EasyOCR)

## 🙏 Acknowledgments

Special thanks to:

- **[Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)**: For providing state-of-the-art object detection models
- **[EasyOCR](https://github.com/JaidedAI/EasyOCR)**: For robust and easy-to-use text recognition
- **[Streamlit](https://streamlit.io/)**: For enabling rapid web application development
- **[Roboflow](https://roboflow.com/)**: For dataset management, annotation tools, and hosting
- **[OpenCV](https://opencv.org/)**: For comprehensive computer vision tools
- **Pakistani AI Community**: For inspiration and support

## 📞 Support & Contact

- 🐛 **Report Bugs**: [Open an issue](https://github.com/Muhammad-Usama294/ICardForensic/issues)
- 💡 **Feature Requests**: [Submit a request](https://github.com/Muhammad-Usama294/ICardForensic/issues)
- 📧 **Contact**: Open an issue or reach out via GitHub

## ⭐ Star History

If you find this project useful, please consider giving it a star ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ by Muhammad Usama**

**Powered by YOLOv8 🤖 | EasyOCR 📝 | Streamlit 🚀**

[⬆ Back to Top](#-icardforensic---ai-powered-id-card-intelligence-system)

</div>
