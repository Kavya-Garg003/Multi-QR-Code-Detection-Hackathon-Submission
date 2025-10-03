import argparse
from ultralytics import YOLO

def main(args):
    model = YOLO(args.model)

    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        name=args.name,
        project=args.project,
        hyp=args.hyp
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="Path to data.yaml")
    parser.add_argument("--model", type=str, default="yolov8s.pt", help="YOLO base model")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=960)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--name", type=str, default="qr_detector_aug")
    parser.add_argument("--project", type=str, default="runs/detect")
    parser.add_argument("--hyp", type=str, default="hyp_qr.yaml")
    args = parser.parse_args()
    main(args)
