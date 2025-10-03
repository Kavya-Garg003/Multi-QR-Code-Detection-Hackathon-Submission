import argparse, os, json, cv2
from ultralytics import YOLO

def classify_qr(value):
    if value.startswith("B"): return "batch"
    elif value.startswith("MFR"): return "manufacturer"
    return "other"

def expand_box(x1, y1, x2, y2, expand=10, W=640, H=640):
    """Expand box slightly for better decoding"""
    x1 = max(0, x1 - expand)
    y1 = max(0, y1 - expand)
    x2 = min(W, x2 + expand)
    y2 = min(H, y2 + expand)
    return x1, y1, x2, y2

def main(args):
    model = YOLO(args.weights)
    results = model.predict(args.input, conf=0.15, iou=0.6, save=False)

    detection_output, decoding_output = [], []
    for r in results:
        img_id = os.path.basename(r.path)
        img = cv2.imread(r.path)
        H, W = img.shape[:2]
        qrs_det, qrs_dec = [], []

        for box in r.boxes.xyxy.cpu().numpy():
            x1,y1,x2,y2 = map(int, box)
            qrs_det.append({"bbox":[x1,y1,x2,y2]})

            # expand crop slightly
            x1,y1,x2,y2 = expand_box(x1,y1,x2,y2, expand=15, W=W, H=H)
            crop = img[y1:y2, x1:x2]
            val, _, _ = cv2.QRCodeDetector().detectAndDecode(crop)

            if val:
                qrs_dec.append({"bbox":[x1,y1,x2,y2], "value":val, "type":classify_qr(val)})

        detection_output.append({"image_id": img_id, "qrs": qrs_det})
        decoding_output.append({"image_id": img_id, "qrs": qrs_dec})

    os.makedirs(args.output, exist_ok=True)
    with open(os.path.join(args.output, "submission_detection_1.json"), "w") as f:
        json.dump(detection_output, f, indent=2)

    with open(os.path.join(args.output, "submission_decoding_2.json"), "w") as f:
        json.dump(decoding_output, f, indent=2)

    print("✅ Inference complete. JSON saved to outputs/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", type=str, required=True)
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, default="outputs")
    args = parser.parse_args()
    main(args)
