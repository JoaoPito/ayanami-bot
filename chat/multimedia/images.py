import base64


def load_using_base64(image_path):
    with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')