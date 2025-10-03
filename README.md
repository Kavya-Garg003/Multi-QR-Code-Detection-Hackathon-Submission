# 📌 Multi-QR Code Detection – Hackathon Submission

This repository contains code for the **Multi-QR Code Recognition Challenge**.
The task is to **detect all QR codes** on medicine pack images, and optionally **decode + classify** them.

---

## 📂 Repository Structure

```
multiqr-hackathon/
│
├── README.md                 # Setup & usage instructions
├── requirements.txt          # Dependencies
├── train.py                  # Training script
├── infer.py                  # Inference (images → JSON output)
├── evaluate.py               # Simple evaluation (optional)
├── hyp_qr.yaml               # Hyperparameters + augmentations
│
├── data/                     # Placeholder (dataset not committed)
│   └── demo_images/          # Small sample for demo
│
├── outputs/                  
│   ├── submission_detection_1.json   # Stage 1 submission
│   └── submission_decoding_2.json    # Stage 2 (bonus)
│
└── src/                      # Core code, utils, loaders
    ├── models/
    ├── datasets/
    ├── utils/
    └── __init__.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/multiqr-hackathon.git
cd multiqr-hackathon
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
ultralytics==8.3.0
opencv-python
numpy
pyyaml
```

---

## 📦 Dataset Preparation

1. **Upload dataset to Google Drive or local path**.
   Structure must be YOLO-format:

```
datasets/qr/
   ├── images/
   │    ├── train/
   │    └── val/          # optional (can reuse train if no val set)
   └── labels/
        ├── train/
        └── val/
   └── data.yaml
```

2. **Example `data.yaml`**:

```yaml
train: /content/drive/MyDrive/QR_dataset/datasets/qr/images/train
val: /content/drive/MyDrive/QR_dataset/datasets/qr/images/val

nc: 1
names: ["qr"]
```

If no validation split is available, point both `train` and `val` to the same folder, or set `val=False` in training.

---

## 🚀 Training

Run the training script:

```bash
python train.py \
  --data /content/drive/MyDrive/QR_dataset/datasets/qr/data.yaml \
  --model yolov8m.pt \
  --epochs 100 \
  --imgsz 960 \
  --batch 8 \
  --hyp hyp_qr.yaml
```

This will save results to:

```
/content/runs/detect/qr_detector_aug/
```

Inside you’ll find:

* `weights/best.pt` (final checkpoint)
* `results.png` (training curves)
* `results.csv` (raw metrics)

---

## 🔍 Inference

Run detection + decoding:

```bash
python infer.py \
  --weights /content/runs/detect/qr_detector_aug/weights/best.pt \
  --input data/demo_images \
  --output outputs
```

This generates:

* `outputs/submission_detection_1.json` ✅ (Stage 1)
* `outputs/submission_decoding_2.json` ✅ (Stage 2 bonus)

Format example:

```json
[
  {
    "image_id": "img001.jpg",
    "qrs": [
      {"bbox": [10, 20, 100, 150], "value": "B12345", "type": "batch"},
      {"bbox": [200, 50, 300, 180], "value": "MFR56789", "type": "manufacturer"}
    ]
  }
]
```

---

## 📊 Evaluation (optional)

You can quickly check how many QRs were detected:

```bash
python evaluate.py --pred outputs/submission_detection_1.json
```

---

## 📌 Notes

* The solution is **fully runnable & reproducible**.
* No external APIs are used.
* Supports augmentation, tilted/blurred/occluded QR codes.
* Efficient inference → lighter/faster models rank higher.

---

## 🏆 Submission Checklist

* [x] `submission_detection_1.json` (Stage 1)
* [x] `submission_decoding_2.json` (Stage 2, bonus)
* [x] Complete runnable repo with `README.md`, `train.py`, `infer.py`, `evaluate.py`
* [x] Instructions for dataset, training, inference

---

