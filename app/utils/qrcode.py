import qrcode

from app.utils.app_utils.common_utils import uuid_getter


def create_qrcode(url: str):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    img = qr.make_image(fill_color="black", back_color="white")
    file_path = f"/images/qrcodes/{uuid_getter()}.png"
    file_name = f"assets/{file_path}"
    img.save(file_name, format="PNG")
    return file_path
