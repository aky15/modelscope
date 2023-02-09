# Copyright (c) Alibaba, Inc. and its affiliates.
import unittest

from modelscope.hub.snapshot_download import snapshot_download
from modelscope.models import Model
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.pipelines.cv import ImageInpaintingSDV2Pipeline
from modelscope.utils.constant import Tasks
from modelscope.utils.demo_utils import DemoCompatibilityCheck
from modelscope.utils.test_utils import test_level


class ImageInpaintingSDV2Test(unittest.TestCase, DemoCompatibilityCheck):

    def setUp(self) -> None:
        self.task = Tasks.image_inpainting
        self.model_id = 'damo/cv_stable-diffusion-v2_image-inpainting_base'
        self.input_location = 'data/test/images/image_inpainting/image_inpainting_1.png'
        self.input_mask_location = 'data/test/images/image_inpainting/image_inpainting_mask_1.png'
        self.prompt = 'background'

        self.input = {
            'image': self.input_location,
            'mask': self.input_mask_location,
            'prompt': self.prompt
        }

    @unittest.skipUnless(test_level() >= 2, 'skip test in current test level')
    def test_run_by_direct_model_download(self):
        cache_path = snapshot_download(self.model_id)
        pipeline = ImageInpaintingSDV2Pipeline(cache_path)
        pipeline.group_key = self.task
        out_video_path = pipeline(input=self.input)[OutputKeys.OUTPUT_IMG]
        print('pipeline: the output image path is {}'.format(out_video_path))

    @unittest.skipUnless(test_level() >= 0, 'skip test in current test level')
    def test_run_with_model_from_modelhub(self):
        pipeline_ins = pipeline(
            task=Tasks.image_inpainting, model=self.model_id)
        out_video_path = pipeline_ins(input=self.input)[OutputKeys.OUTPUT_IMG]
        print('pipeline: the output image path is {}'.format(out_video_path))

    @unittest.skip('demo compatibility test is only enabled on a needed-basis')
    def test_demo_compatibility(self):
        self.compatibility_check()


if __name__ == '__main__':
    unittest.main()