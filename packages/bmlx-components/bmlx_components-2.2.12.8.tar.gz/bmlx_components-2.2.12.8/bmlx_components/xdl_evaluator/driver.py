import os
import re
import logging
from typing import Dict, Text, Any
from bmlx.utils import artifact_utils, io_utils
from bmlx_components.proto import model_pb2
from bmlx_components.xdl_base.driver import XdlDriver
from bmlx.flow import Artifact, Channel, Pipeline, Component, DriverArgs
from bmlx.metadata import standard_artifacts
from bmlx.execution.execution import ExecutionInfo

CEPH_ARTIFACT_PATH_PATTERN = "ceph://([a-zA-Z0-9\-_\.\/]*)(exp_[0-9]+)/(run_[0-9]+)/([a-zA-Z0-9\-_\.]+)"
HDFS_ARTIFACT_PATH = "hdfs://bigo-rt/user/bmlx/artifacts"

# 将ceph路径重构成hdfs指定路径
def reconstruct_path(ceph_path: Text):
    ret = re.match(CEPH_ARTIFACT_PATH_PATTERN, ceph_path)
    if ret is None or ret.group(0) != ceph_path:
        raise RuntimeError(
            "Reconstruct path failed: input (%s) is not ceph_artifact_path" %
            ceph_path
        )

    output_path = os.path.join(
        HDFS_ARTIFACT_PATH,
        ret.group(2), ret.group(3), ret.group(4)
    )
    return output_path

class XdlEvaluatorDriver(XdlDriver):
    # override super method
    def _rewrite_launch_config(self, exec_properties):
        pass

    def _resolve_model_paths(self, input_dict, exec_properties):
        model_uri = ""
        if "model" in input_dict:
            if len(input_dict["model"]) > 0:
                model_uri = artifact_utils.get_single_uri(input_dict["model"])

        specific_model = exec_properties.get("specific_model", "")
        if specific_model:
            if (io_utils.exists(specific_model)
                or io_utils.exists(os.path.join(specific_model, "model.pbtxt"))
            ):
                logging.info("[specific_model] %s", specific_model)
                model_uri = specific_model
            else:
                logging.warning("model %s doesn't exist", specific_model)

        if not model_uri:
            return ("", "")

        if "model_file_pattern" not in exec_properties:
            raise RuntimeError("model file pattern must set")

        if model_uri.startswith("ceph://"):
            if io_utils.exists(os.path.join(model_uri, "model.pbtxt")):
                model_pb = io_utils.parse_pbtxt_file(
                    os.path.join(model_uri, "model.pbtxt"), model_pb2.Model()
                )
                model_uri = os.path.join(
                    model_pb.model_path, model_pb.model_version
                )

        model_bank_uri = self._get_model_bank_uri(
            model_uri, exec_properties["model_file_pattern"]
        )
        # eval 阶段内存优化，强制只加载phase0 的 embedding 数据
        # TDOO: find a better way to handle model bank uri for different job types
        model_bank_uri = (
            "*@" + model_bank_uri.split("@")[1]
        )

        if specific_model:
            return model_bank_uri, ""

        if exec_properties["is_local"]:
            return model_bank_uri, model_uri
        else:
            return model_bank_uri, exec_properties.get("model_uri_base", "")

    # override super method
    def pre_execution(
        self,
        input_dict: Dict[Text, Channel],
        output_dict: Dict[Text, Channel],
        exec_properties: Dict[Text, Any],
        pipeline: Pipeline,
        component: Component,
        driver_args: DriverArgs,
    ) -> ExecutionInfo:
        ret = super(XdlEvaluatorDriver, self).pre_execution(
            input_dict,
            output_dict,
            exec_properties,
            pipeline,
            component,
            driver_args,
        )

        def gen_artifact(type_name, uri):
            artifact = Artifact(type_name=type_name)
            artifact.meta.uri = uri
            artifact.meta.producer_component = component.id
            return artifact

        specific_samples = ret.exec_properties.get(
            "specific_samples",
            []
        )

        if specific_samples:
            logging.info("[specific_samples] %s", specific_samples)
            samples_selected = []
            for sample in specific_samples:
                if io_utils.exists(sample):
                    artifact = gen_artifact(
                        standard_artifacts.Samples.TYPE_NAME, sample,
                    )
                    samples_selected.append(artifact)
                else:
                    logging.warning("sample %s doesn't exist", sample)
            ret.input_dict["specific_samples"] = samples_selected

        output_uri = artifact_utils.get_single_uri(
            ret.output_dict["output"]
        )
        logging.info("[origin]output_uri is %s", output_uri)
        changed_output_uri = reconstruct_path(output_uri)
        ret.output_dict["output"][0].meta.uri = changed_output_uri
        changed_output_uri = artifact_utils.get_single_uri(
            ret.output_dict["output"]
        )
        logging.info("[changed]output_uri is %s", changed_output_uri)

        return ret