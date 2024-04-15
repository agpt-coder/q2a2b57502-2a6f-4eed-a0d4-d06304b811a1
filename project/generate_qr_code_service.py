import base64
from io import BytesIO
from typing import Optional

import qrcode
from pydantic import BaseModel


class GenerateQRCodeResponse(BaseModel):
    """
    This model outlines the response structure for a QR code generation request, including any metadata and the QR code image itself.
    """

    success: bool
    message: Optional[str] = None
    qr_code_image: str


def generate_qr_code(
    content: str,
    size: str,
    encoding: Optional[str] = None,
    error_correction: Optional[str] = None,
    border: Optional[int] = None,
) -> GenerateQRCodeResponse:
    """
    Generates a QR code based on specified data and customization options.

    Args:
        content (str): The content to be encoded into the QR code. This could be a URL, text, or any other data valid for QR encoding.
        size (str): The size of the QR code to be generated, typically specified in pixels (e.g., "250x250").
        encoding (Optional[str]): The encoding type for the QR code content, such as "UTF-8" for text or "binary" for more complex data formats. Not used directly in qrcode generation in this context but listed for potential future use.
        error_correction (Optional[str]): The level of error correction to be applied, which affects the QR code's resilience to damage. Valid options include "L", "M", "Q", "H" corresponding to low, medium, quartile, and high, respectively.
        border (Optional[int]): The width of the border to be added around the QR code, typically specified in units of the QR code's smallest square.

    Returns:
        GenerateQRCodeResponse: This model outlines the response structure for a QR code generation request, including any metadata and the QR code image itself.
    """
    try:
        qr_factory = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M
            if error_correction is None
            else getattr(
                qrcode.constants,
                f"ERROR_CORRECT_{error_correction}",
                qrcode.constants.ERROR_CORRECT_M,
            ),
            box_size=min([int(dim) for dim in size.split("x")]) // 10,
            border=border if border else 4,
        )  # TODO(autogpt): "QRCode" is not a known member of module "qrcode". reportAttributeAccessIssue
        #   Found documentation for the module:
        #    The error message you are encountering, """"QRCode" is not a known member of module "qrcode". reportAttributeAccessIssue"", suggests that the program is unable to recognize "QRCode" as a valid attribute or member of the "qrcode" module. Based on the provided documentation for the "qrcode" module, the correct way to use the "QRCode" class is shown below:
        #
        #   ```python
        #   import qrcode
        #   qr = qrcode.QRCode(
        #       version=1,
        #       error_correction=qrcode.constants.ERROR_CORRECT_L,
        #       box_size=10,
        #       border=4,
        #   )
        #   qr.add_data('Some data')
        #   qr.make(fit=True)
        #
        #   img = qr.make_image(fill_color="black", back_color="white")
        #   ```
        #
        #   This indicates that the "QRCode" class is indeed a valid member of the "qrcode" module and demonstrates how to correctly instantiate and use it. The error might arise due to several reasons such as:
        #
        #   - The "qrcode" module is not correctly installed or imported.
        #   - There is a version mismatch or an environment issue where a different version of the "qrcode" module is being accessed that does not have the "QRCode" class.
        #   - Typographical error in the name of the "QRCode" class upon usage.
        #
        #   To fix this error:
        #
        #   1. Ensure that you have correctly installed the "qrcode" package, which supports QRCode generation, using pip:
        #
        #   ```shell
        #   pip install qrcode[pil]
        #   ```
        #
        #   2. Verify that your import statement correctly imports the "qrcode" module:
        #
        #   ```python
        #   import qrcode
        #   ```
        #
        #   3. Use the QRCode class as demonstrated in the documentation provided.
        qr_factory.add_data(content)
        qr_factory.make(fit=True)
        img = qr_factory.make_image(fill_color="black", back_color="white")
        byte_io = BytesIO()
        img.save(byte_io, format="PNG")
        qr_code_base64 = base64.b64encode(byte_io.getvalue()).decode("utf-8")
        return GenerateQRCodeResponse(success=True, qr_code_image=qr_code_base64)
    except Exception as ex:
        return GenerateQRCodeResponse(
            success=False, message=str(ex), qr_code_image=None
        )
