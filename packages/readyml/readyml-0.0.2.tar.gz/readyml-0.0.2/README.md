# ReadyML - Easy and Ready Machine Learning.

ReadyML makes trained Machine Learning models ready to consume with minimum effort.

## Available Models

### Image Classification

#### Model: NASNetLarge

**Class:** readyml.imageclassification.NASNetLarge

**Reference:** [Learning Transferable Architectures for Scalable Image Recognition (CVPR 2018)](https://arxiv.org/abs/1707.07012)

**Example of use:**
```
from readyml import imageclassification as fic
import PIL
import PIL.Image as Image

image_pil = Image.open("./images/brad.jpg")

nasnetlarge = fic.NASNetLarge()
results = nasnetlarge.infer(image_pil)
print(results)
```
