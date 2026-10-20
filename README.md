# Product Main Image Tool

A small Streamlit tool that converts one raw product photo into a centred 2000 × 2000 pixel JPG with a white background.

## Run on your computer

```bash
cd product_main_image_tool
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Put it online for free

1. Create a new GitHub repository and upload the three files in this folder.
2. Go to [Streamlit Community Cloud](https://share.streamlit.io/), sign in, and select **Create app**.
3. Select the repository and set the main file path to `product_main_image_tool/app.py`.
4. Deploy. Streamlit will give you a private/shareable web link.

The first upload can take a little longer because the image background-removal model is downloaded once.
