from vision.vision_module import VisionModule


def main():
    vision = VisionModule("resources/models/custom_cnn_model.tflite")

    results = vision.analyze_image("resources/images/hoarda.jpeg")

    print("\nRezultate Vision:")

    for result in results:
        print(f"Fata {result['index']}:")
        print("  Box:", result["box"])
        print("  Emotie:", result["emotion"])
        print(f"  Incredere: {result['confidence']:.2%}")

    print("\nImaginea finala a fost salvata in resources/images/result_emotions.jpg")


if __name__ == "__main__":
    main()