# Lint as: python3
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for config."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf  # pylint: disable=g-explicit-tensorflow-version-import
from tensorflow_model_analysis import config

from google.protobuf import text_format


class ConfigTest(tf.test.TestCase):

  def testUpdateConfigWithDefaultsNoModel(self):
    eval_config_pbtxt = """
      metrics_specs {
        metrics { class_name: "ExampleCount" }
      }
    """
    eval_config = text_format.Parse(eval_config_pbtxt, config.EvalConfig())

    expected_eval_config_pbtxt = """
      model_specs { name: "" }
      metrics_specs {
        metrics { class_name: "ExampleCount" }
        model_names: [""]
      }
    """
    expected_eval_config = text_format.Parse(expected_eval_config_pbtxt,
                                             config.EvalConfig())

    got_eval_config = config.update_eval_config_with_defaults(eval_config)
    self.assertProtoEquals(got_eval_config, expected_eval_config)

  def testUpdateConfigWithDefaultsEmtpyModelName(self):
    eval_config_pbtxt = """
      model_specs { name: "" }
      metrics_specs {
        metrics { class_name: "WeightedExampleCount" }
      }
    """
    eval_config = text_format.Parse(eval_config_pbtxt, config.EvalConfig())

    expected_eval_config_pbtxt = """
      model_specs { name: "" }
      metrics_specs {
        metrics { class_name: "WeightedExampleCount" }
        model_names: [""]
      }
    """
    expected_eval_config = text_format.Parse(expected_eval_config_pbtxt,
                                             config.EvalConfig())

    got_eval_config = config.update_eval_config_with_defaults(eval_config)
    self.assertProtoEquals(got_eval_config, expected_eval_config)

  def testUpdateConfigWithDefaultsSingleModel(self):
    eval_config_pbtxt = """
      model_specs { name: "model1" }
      metrics_specs {
        metrics { class_name: "WeightedExampleCount" }
      }
      metrics_specs {
        metrics { class_name: "MeanLabel" }
        model_names: ["model1"]
      }
    """
    eval_config = text_format.Parse(eval_config_pbtxt, config.EvalConfig())

    expected_eval_config_pbtxt = """
      model_specs { name: "" }
      metrics_specs {
        metrics { class_name: "WeightedExampleCount" }
        model_names: [""]
      }
      metrics_specs {
        metrics { class_name: "MeanLabel" }
        model_names: [""]
      }
    """
    expected_eval_config = text_format.Parse(expected_eval_config_pbtxt,
                                             config.EvalConfig())

    got_eval_config = config.update_eval_config_with_defaults(eval_config)
    self.assertProtoEquals(got_eval_config, expected_eval_config)

  def testUpdateConfigWithDefaultsMultiModel(self):
    eval_config_pbtxt = """
      model_specs { name: "model1" }
      model_specs { name: "model2" }
      metrics_specs {
        metrics { class_name: "WeightedExampleCount" }
      }
      metrics_specs {
        metrics { class_name: "MeanLabel" }
        model_names: ["model1"]
      }
    """
    eval_config = text_format.Parse(eval_config_pbtxt, config.EvalConfig())

    expected_eval_config_pbtxt = """
      model_specs { name: "model1" }
      model_specs { name: "model2" }
      metrics_specs {
        metrics { class_name: "WeightedExampleCount" }
        model_names: ["model1", "model2"]
      }
      metrics_specs {
        metrics { class_name: "MeanLabel" }
        model_names: ["model1"]
      }
    """
    expected_eval_config = text_format.Parse(expected_eval_config_pbtxt,
                                             config.EvalConfig())

    got_eval_config = config.update_eval_config_with_defaults(eval_config)
    self.assertProtoEquals(got_eval_config, expected_eval_config)

  def testUpdateConfigWithDefaultsBaselineModel(self):
    eval_config_pbtxt = """
      model_specs { name: "candidate" }
      model_specs { name: "baseline" is_baseline: true }
      metrics_specs {
        metrics { class_name: "WeightedExampleCount" }
      }
    """
    eval_config = text_format.Parse(eval_config_pbtxt, config.EvalConfig())

    expected_eval_config_pbtxt = """
      model_specs { name: "candidate" }
      model_specs { name: "baseline" is_baseline: true }
      metrics_specs {
        metrics { class_name: "WeightedExampleCount" }
        model_names: ["candidate", "baseline"]
      }
    """
    expected_eval_config = text_format.Parse(expected_eval_config_pbtxt,
                                             config.EvalConfig())

    got_eval_config = config.update_eval_config_with_defaults(eval_config)
    self.assertProtoEquals(got_eval_config, expected_eval_config)


if __name__ == '__main__':
  tf.test.main()
