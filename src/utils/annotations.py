import cv2, os
from pyzbar.pyzbar import decode as pyzbar_decode
from .conversions import convert_bbox

def auto_annotate(image_dir, label_dir, min_size=30):
    """Auto-generate YOLO txt annotations using Pyzbar + OpenCV QRCodeDetector"""
    os.makedirs(label_dir, exist_ok=True)
    qr_detector = cv2.QRCodeDetector()

    for img_name in os.listdir(image_dir):
        img_path = os.path.join(image_dir, img_name)
        img = cv2.imread(img_path)
        if img is None: continue
        H, W = img.shape[:2]
        boxes = []

        # Pyzbar
        for obj in pyzbar_decode(img):
            x, y, bw, bh = obj.rect
            if bw > min_size and bh > min_size:
                boxes.append([x, y, x+bw, y+bh])

        # OpenCV QR Detector
        _, _, points, _ = qr_detector.detectAndDecodeMulti(img)
        if points is not None:
            for p in points.astype(int):
                x_min, y_min = p[:,0].min(), p[:,1].min()
                x_max, y_max = p[:,0].max(), p[:,1].max()
                if (x_max-x_min) > min_size and (y_max-y_min) > min_size:
                    boxes.append([x_min, y_min, x_max, y_max])

        # Save YOLO labels
        if boxes:
            txt_name = os.path.splitext(img_name)[0] + ".txt"
            with open(os.path.join(label_dir, txt_name), "w") as f:
                for (x1,y1,x2,y2) in boxes:
                    x_c,y_c,w,h = convert_bbox((W,H), [x1,y1,x2,y2])
                    f.write(f"0 {x_c} {y_c} {w} {h}\n")
