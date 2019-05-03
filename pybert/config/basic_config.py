#encoding:utf-8
from os import path
import multiprocessing
from pathlib import Path
"""Note:
pytorch BERT 模型包含三个文件：模型、vocab.txt, bert_config.json, 有两种加载方式：
（1）在线下载。这种方式下，模型和vocab会通过url的方式下载，只需将bert_model设置为 "bert_model=bert-base-chinese"
     另外，还需要设置cache_dir路径，用来存储下载的文件。
（2）先下载好文件。下载好的文件是tensorflow的ckpt格式的，首先要利用convert_tf_checkpoint_to_pytorch转换成pytorch格式存储
     这种方式是通过本地文件夹直接加载的，要注意这时的文件命名方式。首先指定bert_model=存储模型的文件夹
     第二，将vocab.txt和bert_config.json放入该目录下，并在配置文件中指定VOCAB_FILE路径。当然vocab.txt可以不和模型放在一起，
     但是bert_config.json文件必须和模型文件在一起。具体可见源代码file_utils
"""
## pybert 가 path 설정
BASE_DIR = Path('/Users/kim-woojeong/PycharmProjects/Bert-Multi-Label-Text-Classification/pybert')

## dataset 받아서, dataset/raw 폴더에 엑셀 형식으로 train과 test 넣기

configs = {

    'task':'multi label',
    'data':{
        'raw_data_path': BASE_DIR / 'dataset/raw/train.csv',  # 총 데이터, 일반적으로 train과 test를 함께..
        'train_file_path': BASE_DIR / 'dataset/processed/train.tsv',
        'valid_file_path': BASE_DIR / 'dataset/processed/valid.tsv',
        'test_file_path': BASE_DIR / 'dataset/raw/test.csv'
    },
    'output':{
        'log_dir': BASE_DIR / 'output/log', # 模型运行日志
        'writer_dir': BASE_DIR / "output/TSboard",# TSboard 정보 저장 경로
        'figure_dir': BASE_DIR / "output/figure", # 图形保存路径
        'checkpoint_dir': BASE_DIR / "output/checkpoints",# 模型保存路径
        'cache_dir': BASE_DIR / 'model/',
        'result': BASE_DIR / "output/result",
    },
    'pretrained':{
        "bert":{
            'vocab_path': BASE_DIR / 'model/pretrain/uncased_L-12_H-768_A-12/vocab.txt',
            'tf_checkpoint_path': BASE_DIR / 'model/pretrain/uncased_L-12_H-768_A-12/bert_model.ckpt',
            'bert_config_file': BASE_DIR / 'model/pretrain/uncased_L-12_H-768_A-12/bert_config.json',
            'pytorch_model_path': BASE_DIR / 'model/pretrain/pytorch_pretrain/pytorch_model.bin',
            'bert_model_dir': BASE_DIR / 'model/pretrain/pytorch_pretrain',
        },
        'embedding':{}
    },
    'train':{
        'valid_size': 0.2,
        'max_seq_len': 256,
        'do_lower_case':True,
        'batch_size': 100,#24,  # how many samples to process at once
        'epochs': 6,  # number of epochs to train
        'start_epoch': 1,
        'warmup_proportion': 0.1,# Proportion of training to perform linear learning rate warmup for. E.g., 0.1 = 10%% of training.
        'gradient_accumulation_steps': 1,# Number of updates steps to accumulate before performing a backward/update pass.
        'learning_rate': 2e-5,
        'n_gpu': [1,0], # GPU个数,如果只写一个数字，则表示gpu标号从0开始，并且默认使用gpu:0作为controller,
                       # 如果以列表形式表示，即[1,3,5],则我们默认list[0]作为controller
        'num_workers': multiprocessing.cpu_count(), # 线程个数
        'weight_decay': 1e-5,
        'seed':2018,
        'resume':False,
    },
    'predict':{
        'batch_size':400
    },
    'callbacks':{
        'lr_patience': 5, # number of epochs with no improvement after which learning rate will be reduced.
        'mode': 'min',    # one of {min, max}
        'monitor': 'valid_loss',  # 计算指标
        'early_patience': 20,   # early_stopping
        'save_best_only': True, # 是否保存最好模型
        'save_checkpoint_freq': 10 # 保存模型频率，当save_best_only为False时候，指定才有作用
    },
    'label2id' : { # 标签映射
        "toxic": 0,
        "severe_toxic": 1,
        "obscene": 2,
        "threat": 3,
        "insult": 4,
        "identity_hate": 5
    },
    'model':{
        'arch':'bert'
    }
}