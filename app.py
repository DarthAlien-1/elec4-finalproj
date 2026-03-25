import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="Image Processor")

st.title("DevOps x WebEngr: Image Processor")
st.write("Upload an image to apply custom automated filters.")

st.sidebar.header("⚙️ Filter Settings")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    filter_type = st.sidebar.selectbox("Select Filter Technique", 
        ["Original", "Thermal Vision", "Motion Blur", "Mirror Flip", "Solarize", "Channel Swap"])

    result_img = img.copy()

    if filter_type == "Thermal Vision":
        result_img = cv2.applyColorMap(img, cv2.COLORMAP_JET)
        
    elif filter_type == "Motion Blur":
        blur_amount = st.sidebar.slider("Blur Intensity", min_value=1, max_value=50, value=15)
        if blur_amount % 2 == 0:
            blur_amount += 1
            
        kernel = np.zeros((blur_amount, blur_amount))
        kernel[int((blur_amount-1)/2), :] = np.ones(blur_amount) / blur_amount
        result_img = cv2.filter2D(img, -1, kernel)
        
    elif filter_type == "Mirror Flip":
        result_img = cv2.flip(img, 1)
        
    elif filter_type == "Solarize":
        threshold = st.sidebar.slider("Invert Threshold", 0, 255, 128)
        mask = result_img > threshold
        result_img[mask] = 255 - result_img[mask]
        
    elif filter_type == "Channel Swap":
        result_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    original_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    if filter_type != "Channel Swap":
        result_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
    else:
        result_rgb = result_img

    # Display side-by-side
    col1, col2 = st.columns(2)
    with col1:
        st.header("Before")
        st.image(original_rgb, use_column_width=True)
    with col2:
        st.header("After")
        st.image(result_rgb, use_column_width=True)

    #  DOWNLOAD BUTTON LOGIC
    st.sidebar.markdown("---")
    
    is_success, buffer = cv2.imencode(".png", result_img)
    
    if is_success:
        file_name_format = f"{filter_type.lower().replace(' ', '_')}_image.png"
        
        st.sidebar.download_button(
            label="📥 Download Filtered Image",
            data=buffer.tobytes(),
            file_name=file_name_format,
            mime="image/png"
        )
