# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Vertex AI sample for editing an image using a mask mode. The
    mask mode is used to automatically select the background, foreground (i.e.,
    the primary subject of the image), or an object based on segmentation class.
    Inpainting can insert the object or background designated by the prompt.
"""
import os

from vertexai.preview import vision_models

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


def edit_image_3_inpainting_insert_mask_mode(
    input_file: str,
    mask_mode: str,
    output_file: str,
    prompt: str,
) -> vision_models.ImageGenerationResponse:
    # [START generativeaionvertexai_imagen_edit_image_3_inpainting_insert_mask_mode]

    import vertexai
    from vertexai.preview.vision_models import Image, ImageGenerationModel, MaskReferenceImage, RawReferenceImage

    # TODO(developer): Update and un-comment below lines
    # PROJECT_ID = "your-project-id"
    # input_file = "input-image.png"
    # mask_mode = "background" # 'background', 'foreground', or 'semantic'
    # output_file = "output-image.png"
    # prompt = "" # The text prompt describing what you want to see inserted.

    vertexai.init(project=PROJECT_ID, location="us-central1")

    model = ImageGenerationModel.from_pretrained("imagen-3.0-capability-001")
    base_img = Image.load_from_file(location=input_file)
    base_ref_image = RawReferenceImage(image=base_img, reference_id=0)
    mask_ref_image = MaskReferenceImage(
        reference_id=1, image=None, mask_mode=mask_mode
    )

    images = model.edit_image(
        reference_images=[base_ref_image, mask_ref_image],
        prompt=prompt,
        edit_mode="inpainting-insert",
    )

    images[0].save(location=output_file, include_generation_parameters=False)

    # Optional. View the edited image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")
    # Example response:
    # Created output image using 1234567 bytes

    # [END generativeaionvertexai_imagen_edit_image_3_inpainting_insert_mask_mode]

    return images


if __name__ == "__main__":
    edit_image_3_inpainting_insert_mask_mode(
        input_file="../test_resources/woman.png",
        mask_mode="background",
        output_file="../test_resources/woman_at_beach.png",
        prompt="beach",
    )