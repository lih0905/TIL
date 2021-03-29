"""
파이썬 로그 함수 연습
왜 매번 해도 익숙해지지가 않냐
"""

import os
import time
import logging

from easydict import EasyDict as edict

def get_logger(args):
    log_path = os.path.join('ETC', args.log_path)
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
        
    train_instance_log_files = os.listdir(log_path)
    train_instance_count = len(train_instance_log_files)
    
    logging.basicConfig(
        filename=f'{log_path}/train_instance_{train_instance_count}_info.log', 
        filemode='w', 
        format="%(asctime)s | %(filename)15s | %(levelname)7s | %(funcName)10s | %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # 화면 출력 
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)7s | %(message)s","%Y-%m-%d %H:%M:%S")
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)    
    
    logger.info("-"*40)
    for arg in vars(args):
        logger.info(f"{arg}: {getattr(args, arg)}")
    logger.info("-"*40)
    
    return logger

if __name__ == '__main__':
    
    args = {'log_path':'logs', 'ckpt_path':'ckpt', 'model':'BART', 'epochs':5}
    args = edict(args)
    logger = get_logger(args)
        
    ckpt_path = os.path.join('ETC', args.ckpt_path)
    if not os.path.isdir(ckpt_path):
        os.mkdir(ckpt_path)
        
    
    for epoch in range(args.epochs):
        
        logger.info(f"TRAINING {epoch+1} epoch of {args.epochs} epochs.")    
        logger.debug("This is a degbug log.")
        
        filename = f'ckpt_{epoch+1}'
        text = f"This if a temporary text from {epoch+1} epoch."
        
        
        logger.info(f"Saved to {filename}.")
        with open(os.path.join(ckpt_path, filename), 'w') as f:
            f.write(text)    
        time.sleep(5)
        
    logger.info(f"END TRAINING")
        
        
"""
Screen Output
---------------------------
2021-03-28 08:35:57 |    INFO | ----------------------------------------
2021-03-28 08:35:57 |    INFO | log_path: logs
2021-03-28 08:35:57 |    INFO | ckpt_path: ckpt
2021-03-28 08:35:57 |    INFO | model: BART
2021-03-28 08:35:57 |    INFO | epochs: 5
2021-03-28 08:35:57 |    INFO | ----------------------------------------
2021-03-28 08:35:57 |    INFO | TRAINING 1 epoch of 5 epochs.
2021-03-28 08:35:57 |    INFO | Saved to ckpt_1.
2021-03-28 08:36:02 |    INFO | TRAINING 2 epoch of 5 epochs.
2021-03-28 08:36:02 |    INFO | Saved to ckpt_2.
2021-03-28 08:36:07 |    INFO | TRAINING 3 epoch of 5 epochs.
2021-03-28 08:36:07 |    INFO | Saved to ckpt_3.
2021-03-28 08:36:12 |    INFO | TRAINING 4 epoch of 5 epochs.
2021-03-28 08:36:12 |    INFO | Saved to ckpt_4.
2021-03-28 08:36:17 |    INFO | TRAINING 5 epoch of 5 epochs.
2021-03-28 08:36:17 |    INFO | Saved to ckpt_5.
2021-03-28 08:36:22 |    INFO | END TRAINING
"""
    