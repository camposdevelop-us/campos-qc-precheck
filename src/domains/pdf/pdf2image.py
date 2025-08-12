import os
import shutil
import tempfile
from typing import Optional, List
from pdf2image import convert_from_path
from flask import current_app


class PDF2ImageConverter(object):
    def __init__(
        self,
        poppler_path: Optional[str] = None,
        dpi: int = 400,
        output_folder: Optional[str] = None,
        fmt: str = "png",
        thread_count: int = 1,
    ):
        """Initialize the converter with optional configuration.
        :param poppler_path: Path to poppler binaries. If None, tries to auto-detect or use environment variable.
        :param dpi: Resolution of the output images.
        :param output_folder: Folder to save images. If None, uses a temporary directory.
        :param fmt: Output image format (e.g., 'png', 'jpeg').
        :param thread_count: Number of threads for parallel conversion.
        """
        self.poppler_path = poppler_path or os.getenv("POPPLER_PATH", None) or current_app.config['POPPLER_PATH']
        self.dpi = dpi
        self.output_folder = output_folder or tempfile.mkdtemp()
        self.fmt = fmt
        self.thread_count = thread_count
        self._validate_poppler()

    def _validate_poppler(self):
        """Validate that Poppler is available either in PATH or via poppler_path."""
        if not shutil.which("pdftoppm") and not self.poppler_path:
            raise EnvironmentError(
                "Poppler not found. Please install it and set the poppler_path or add it to your system PATH."
            )

    def convert(
        self,
        pdf_path: str,
        first_page: Optional[int] = None,
        last_page: Optional[int] = None,
    ) -> List[str]:
        """Convert PDF to images.
        :param pdf_path: Path to the PDF file.
        :param first_page: First page to convert.
        :param last_page: Last page to convert.
        :return: List of image file paths.
        """
        try:
            image_paths = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                output_folder=self.output_folder,
                fmt=self.fmt,
                thread_count=self.thread_count,
                first_page=first_page,
                last_page=last_page,
                paths_only=True,
                poppler_path=self.poppler_path,
            )
            return image_paths
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF to images: {e}")
