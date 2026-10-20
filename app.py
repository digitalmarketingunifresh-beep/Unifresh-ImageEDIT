"""Product Main Image Tool — Streamlit app.

Turn one uploaded product photo into a clean 1:1 white-background image.
"""
from io import BytesIO

import streamlit as st
from PIL import Image, ImageChops, ImageFilter
from rembg import remove


CANVAS = 2000


def trim_transparent(im: Image.Image) -> Image.Image:
    alpha = im.getchannel("A")
    bbox = alpha.getbbox()
    return im.crop(bbox) if bbox else im


def make_main_image(source: Image.Image, coverage: int, shadow: bool) -> Image.Image:
    """Remove the background and centre the detected subject on an RGB white square."""
    source = source.convert("RGBA")
    cutout = remove(source).convert("RGBA")
    product = trim_transparent(cutout)
    if product.width == 0 or product.height == 0:
        raise ValueError("No product could be detected. Please try a clearer photo.")

    maximum = int(CANVAS * coverage / 100)
    scale = min(maximum / product.width, maximum / product.height)
    size = (max(1, round(product.width * scale)), max(1, round(product.height * scale)))
    product = product.resize(size, Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (CANVAS, CANVAS), (255, 255, 255, 255))
    x = (CANVAS - product.width) // 2
    y = (CANVAS - product.height) // 2

    if shadow:
        alpha = product.getchannel("A")
        drop = Image.new("RGBA", product.size, (70, 70, 70, 0))
        drop.putalpha(alpha.point(lambda a: int(a * 0.16)).filter(ImageFilter.GaussianBlur(20)))
        canvas.alpha_composite(drop, (x, y + max(12, product.height // 70)))

    canvas.alpha_composite(product, (x, y))
    return canvas.convert("RGB")


st.set_page_config(page_title="Product Main Image Tool", page_icon="🛍️", layout="centered")
st.title("Product Main Image Tool")
st.caption("Upload one raw product image and download a clean 1:1 white-background main image.")

with st.expander("Output rules", expanded=True):
    st.markdown("- One uploaded product only — no generated props, duplicate packs or extra logos\n- Pure white 1:1 background (2000 × 2000 px)\n- Product stays centred and fills the frame neatly\n- Existing artwork or logo printed on your own packaging is preserved")

upload = st.file_uploader("Upload raw product image", type=["png", "jpg", "jpeg", "webp"])
coverage = st.slider("Product size in frame", min_value=70, max_value=90, value=84, help="84–85% works well for Amazon main images.")
shadow = st.toggle("Soft contact shadow", value=True)

if upload:
    source = Image.open(upload)
    st.image(source, caption="Uploaded image", use_container_width=True)
    if st.button("Create main image", type="primary"):
        with st.spinner("Removing background and preparing the image..."):
            try:
                result = make_main_image(source, coverage, shadow)
                stream = BytesIO()
                result.save(stream, format="JPEG", quality=95, subsampling=0)
                st.session_state["result"] = stream.getvalue()
            except Exception as error:
                st.error(f"Could not process this image: {error}")

if st.session_state.get("result"):
    st.image(st.session_state["result"], caption="Ready main image", use_container_width=True)
    st.download_button("Download JPG (2000 × 2000)", st.session_state["result"], "product_main_image.jpg", "image/jpeg", type="primary")

st.divider()
st.caption("Tip: Use a sharp, well-lit photo where the product is clearly separated from the background. Check the final image before uploading to Amazon.")
