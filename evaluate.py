import argparse, json

def evaluate(pred_json):
    with open(pred_json, "r") as f:
        preds = json.load(f)

    total_imgs = len(preds)
    total_qrs = sum(len(p["qrs"]) for p in preds)

    print(f"Evaluated {total_imgs} images")
    print(f"Detected {total_qrs} QR codes total")
    print(f"Avg QRs per image: {total_qrs/total_imgs:.2f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred", type=str, required=True)
    args = parser.parse_args()
    evaluate(args.pred)
