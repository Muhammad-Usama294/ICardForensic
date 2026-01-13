import streamlit as st
from ultralytics import YOLO
import easyocr
import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
from datetime import datetime

# --- 1. PAGE CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="ID Intelligence System",
    page_icon="🆔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS 
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        height: 50px;
        font-size: 20px;
        border-radius: 10px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZATION (CACHED) ---
@st.cache_resource
def load_models():
    """Load models once to improve performance"""
    try:
        # Load YOLO Model
        model = YOLO('best.pt')
        # Load OCR Reader (English)
        reader = easyocr.Reader(['en'], gpu=False)
        return model, reader
    except Exception as e:
        return None, None

model, reader = load_models()

# --- 3. UTILITY FUNCTIONS ---
def apply_enhancements(image, contrast, brightness, sharpness):
    """Apply Image Processing techniques manually"""
    # Convert to PIL for enhancement tools
    pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    
    # Apply enhancements
    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(contrast)
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(brightness)
    if sharpness != 1.0:
        enhancer = ImageEnhance.Sharpness(pil_img)
        pil_img = enhancer.enhance(sharpness)
        
    # Convert back to OpenCV format
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def save_to_history(data_dict, image_name):
    """Save formatted data to a log file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("extraction_log.txt", "a") as f:
        f.write(f"[{timestamp}] SOURCE: {image_name}\n")
        f.write("-" * 40 + "\n")
        for k, v in data_dict.items():
            f.write(f"{k}: {v}\n")
        f.write("=" * 40 + "\n\n")

# --- 4. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/id-card.png", width=150)
    st.title("⚙️ Control Panel")
    
    st.markdown("### 1. Pre-processing")
    st.info("Improve image quality before AI detection.")
    contrast = st.slider("Contrast", 0.5, 2.0, 1.0, 0.1)
    brightness = st.slider("Brightness", 0.5, 2.0, 1.0, 0.1)
    sharpness = st.slider("Sharpness", 0.0, 3.0, 1.0, 0.1)
    
    st.markdown("### 2. Model Config")
    conf_thres = st.slider("Confidence Threshold", 0.1, 0.9, 0.25, 0.05)
    
    st.markdown("---")
    st.caption("NeuroScan System v2.0 | Powered by YOLOv8")

# --- 5. MAIN APPLICATION LAYOUT ---
st.title("🆔 NeuroScan: Intelligent Document Digitization")
st.markdown("Automated pipeline for **Detection**, **Enhancement**, and **Text Extraction**.")

# Tabs for better organization
tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "📊 Live Analysis", "📝 History Logs"])

with tab1:
    uploaded_file = st.file_uploader("Upload Identity Document (JPG, PNG)", type=['jpg', 'jpeg', 'png'])

    if uploaded_file is not None:
        # Load Image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        raw_image = cv2.imdecode(file_bytes, 1)
        
        # Apply Sidebar Enhancements
        processed_image = apply_enhancements(raw_image, contrast, brightness, sharpness)

        # Layout: Original vs Processed
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Input")
            st.image(raw_image, channels="BGR", use_container_width=True)
        with col2:
            st.subheader("Enhanced Input")
            st.image(processed_image, channels="BGR", use_container_width=True)
            st.caption(f"Contrast: {contrast} | Sharpness: {sharpness}")

        # The "Magic" Button
        if st.button("🚀 EXECUTE PIPELINE", type="primary"):
            if model is None:
                st.error("Model not found! Check 'best.pt'")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Step 1: Detection
                status_text.text("Phase 1: Running YOLOv8 Detection...")
                results = model(processed_image, conf=conf_thres)
                progress_bar.progress(40)
                
                extracted_data = {}
                annotated_img = processed_image.copy()
                crop_images = []

                # Step 2: Processing Detections
                status_text.text("Phase 2: Cropping Regions of Interest...")
                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls_id = int(box.cls[0])
                        label = model.names[cls_id]
                        conf = float(box.conf[0])

                        # Draw Bounding Box
                        cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(annotated_img, f"{label} {conf:.2f}", (x1, y1 - 10), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        # Crop
                        crop = processed_image[y1:y2, x1:x2]
                        
                        # Phase 3: OCR
                        status_text.text(f"Phase 3: OCR Reading on {label}...")
                        ocr_result = reader.readtext(crop, detail=0)
                        text_content = " ".join(ocr_result).strip()
                        
                        if text_content:
                            extracted_data[label] = text_content
                            crop_images.append((label, crop, text_content))
                
                progress_bar.progress(100)
                status_text.success("Pipeline Completed Successfully!")

                # --- RESULT DISPLAY IN TAB 2 ---
                with tab2:
                    st.divider()
                    st.subheader("🔍 Detection Results")
                    st.image(annotated_img, channels="BGR", use_container_width=True, caption="YOLOv8 Detection Map")
                    
                    st.subheader("📝 Extracted Data Fields")
                    if extracted_data:
                        # Display nicely formatted metrics
                        cols = st.columns(len(extracted_data))
                        for idx, (key, value) in enumerate(extracted_data.items()):
                            with cols[idx]:
                                st.markdown(f"""
                                <div class="metric-card">
                                    <h3>{key.upper()}</h3>
                                    <p style="font-size:18px; color:#333;">{value}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        # Save Data
                        save_to_history(extracted_data, uploaded_file.name)
                        
                        # Download Button
                        df = pd.DataFrame([extracted_data])
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Data as CSV",
                            data=csv,
                            file_name='extracted_data.csv',
                            mime='text/csv',
                        )
                    else:
                        st.warning("No text detected. Try adjusting Contrast or Sharpness.")
                    
                    # Show Crops
                    if crop_images:
                        st.write("---")
                        st.write("**Verified Segments:**")
                        c_cols = st.columns(len(crop_images))
                        for idx, (lbl, crp, txt) in enumerate(crop_images):
                            with c_cols[idx]:
                                st.image(crp, channels="BGR", caption=f"{lbl}")
                                st.code(txt)

# Tab 3: History
with tab3:
    st.header("📂 Extraction Logs")
    if st.button("Refresh Logs"):
        try:
            with open("extraction_log.txt", "r") as f:
                st.text_area("Log File Content", f.read(), height=400)
        except FileNotFoundError:
            st.info("No logs found yet.")