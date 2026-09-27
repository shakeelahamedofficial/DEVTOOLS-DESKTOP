import os
import io
from PySide6.QtGui import QImage, QPainter, QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QSize, Qt
from PIL import Image

def generate_from_svg():
    svg_path = "app/public/Dev.svg"
    
    renderer = QSvgRenderer(svg_path)
    
    # 1. Primary Application Icon (1024x1024)
    primary_size = 1024
    img_primary = QImage(primary_size, primary_size, QImage.Format_ARGB32_Premultiplied)
    img_primary.fill(Qt.transparent)
    
    painter = QPainter(img_primary)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()
    
    img_primary.save("app/public/icon_primary.png")
    
    # Sizes needed for ICO
    ico_sizes = [16, 24, 32, 48, 64, 128, 256]
    pil_images = []
    
    for size in ico_sizes:
        qimg = QImage(size, size, QImage.Format_ARGB32_Premultiplied)
        qimg.fill(Qt.transparent)
        
        p = QPainter(qimg)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        renderer.render(p)
        p.end()
        
        # Save QImage to memory buffer to load with PIL
        buffer = io.BytesIO()
        
        # QImage has save method to bytes? No, we use QByteArray
        # It's easier to just save to temp file and load
        temp_file = f"app/public/temp_{size}.png"
        qimg.save(temp_file)
        
        pil_images.append(Image.open(temp_file))
        
    pil_images[-1].save(
        "app/public/icon.ico",
        format="ICO",
        append_images=pil_images[:-1]
    )
    
    # cleanup temp files
    for p in pil_images:
        p.close()
    for size in ico_sizes:
        os.remove(f"app/public/temp_{size}.png")
        
    print("Logo updated from SVG.")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    generate_from_svg()
