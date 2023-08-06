import os
from functools import reduce
from typing import Any, List
from ....utils.format_output import format_output, dict_format
import numpy as np
import onnxruntime as rt
from ...abc import BatchAlgorithm
from ....auto_config import get_provider
from ....data import load
from ....utils import DictExtraction
from transformers import BertTokenizerFast

labels = reduce(lambda x, y: x+y, [[f"{kd}-{l}" for kd in ('B','I','O')] for l in ('SEG',)])
class BertCWS(BatchAlgorithm):
    """基于BERT的分词算法

    Args:
        device (str): 运行模型设备的名称，例如："cuda:1"，"cpu"。
        batch_size (int): 模型单次推理最大的batch size，默认会根据硬件资源自动设置。
        num_preprocess (int): 预处理函数进程数，默认为一个自动设置的不超过4的值。
        num_postprocess (int): 后处理函数进程数，默认为一个自动设置的不超过4的值。
        max_queue_size (int): 最大调用队列长度，默认为1024.
        multiprocessing_context: 多进程上下文，默认优先使用"fork"方式。
    
    :Name: bert

    **示例**

    .. code-block:: python

        oknlp.cws.get_by_name("bert", device="cpu")
    """

    def __init__(self, dictionary = [], device = None, *args, **kwargs):

        self.keyword_processor=DictExtraction(case_sensitive = False)

        self.keyword_processor.add_keywords_from_list(dictionary)
        provider, provider_op, fp16_mode, batch_size = get_provider(device)
        self.sent_split = True
        if not fp16_mode:
            model_path = load('cws.bert','fp32')
        else:
            model_path = load('cws.bert','fp16')
        self.config = {
            "model_path": model_path,
            "provider": provider,
            "provider_option": provider_op,
            "tokenizer": BertTokenizerFast.from_pretrained("bert-base-chinese"),
        }
        if "batch_size" not in kwargs:
            kwargs["batch_size"] = batch_size
        super().__init__(*args, **kwargs)

    # @staticmethod
    # def segment(self, sents : List[Any], max_length = 128):
    #     sents, is_end = split_text_list(sents, max_length)
    #     return merge_result(results, is_end)

    def init_preprocess(self):
        self.tokenizer = self.config["tokenizer"]

    def preprocess(self, x, *args, **kwargs):
        tokens = self.tokenizer.tokenize(x)
        sx = self.tokenizer.convert_tokens_to_ids(['[CLS]'] + tokens + ['[SEP]']) 
        return x, sx

    def postprocess(self, x, *args, **kwargs):
        segmentation = [x[0][j[1]:j[2] + 1] for j in format_output(x[1], labels + ['O']) if x[0][j[1]:j[2] + 1]]
        return dict_format(segmentation, self.keyword_processor.extract_dictwords(x[0]))

    def init_inference(self):
        sess_options = rt.SessionOptions()
        sess_options.graph_optimization_level = rt.GraphOptimizationLevel.ORT_ENABLE_ALL
        if hasattr(os, "sched_getaffinity") and len(os.sched_getaffinity(0)) < os.cpu_count():
            sess_options.intra_op_num_threads = 1
            sess_options.inter_op_num_threads = 1
        self.sess = rt.InferenceSession(
            os.path.join(self.config['model_path'],'model.onnx'),
            sess_options, 
            providers=self.config['provider'], 
            provider_options=self.config["provider_option"])
        self.input_name = self.sess.get_inputs()[0].name
        self.att_name = self.sess.get_inputs()[1].name 
        self.label_name = self.sess.get_outputs()[0].name

    def pack_batch(self, batch):
        
        max_len = max([len(i[1]) for i in batch])
        input_array = np.zeros((len(batch), max_len), dtype=np.int32)
        att_array = np.zeros((len(batch), max_len), dtype=np.int32)

        new_batch = []
        for i, (sent, tokens) in enumerate(batch):
            input_array[i, :len(tokens)] = tokens
            att_array[i, :len(tokens)] = 1

            new_batch.append((sent, len(tokens)))
        
        input_feed = {self.input_name: input_array, self.att_name: att_array}
        return new_batch, input_feed

    def inference(self, batch):
        sent_list, input_feed = batch
        pred_onx = self.sess.run([self.label_name],input_feed)[0]

        pred_onx = [
            (sent, pred[:length])
            for pred, (sent, length) in zip(pred_onx, sent_list)
        ]
        return pred_onx