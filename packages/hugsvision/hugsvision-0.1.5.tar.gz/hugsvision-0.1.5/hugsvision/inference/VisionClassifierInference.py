from transformers import ViTFeatureExtractor, ViTForImageClassification, pipeline
from PIL import Image

class VisionClassifierInference:
    
  """
  🤗 Constructor for the image classifier trainer
  """
  def __init__(self, model_path: str, resolution=128):
    
    print("Load model from: " + model_path)
    self.feature_extractor = ViTFeatureExtractor.from_pretrained(model_path)
    self.model = ViTForImageClassification.from_pretrained(model_path)
    print("Model loaded!")
    
    self.resolution = resolution

  def predict(self, img_path: str):

    # Load the image
    image_array = Image.open(img_path)

    # Change resolution to 128x128
    image_array.thumbnail((self.resolution,self.resolution))

    # Transform the image
    encoding = self.feature_extractor(images=image_array, return_tensors="pt")

    # Predict and get the corresponding label identifier
    pred = self.model(encoding['pixel_values'])

    # Get label index
    predicted_class_idx = pred.logits.argmax(-1).tolist()[0]

    # Get string label from index
    label = self.model.config.id2label[predicted_class_idx]
    
    # print(pred.logits)
    
    return label
