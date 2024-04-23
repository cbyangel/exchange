import logging
import logging.handlers
import os, errno, sys
import argparse 


class C_LOGGER:
    def __init__(self, params={}):
        
        name = params.get('name', 'default_logger')
        level = int(params.get('level', 1))
        log_dir = params.get('log_dir', None)
        
        
        # 로그 생성
        logger = logging.getLogger(name)

        # 로그의 출력 기준 설정
        # level = level * 10  # 0: NOTSET, 10: DEBUG, 20: INFO, 30: WARNING, 40: ERROR, 50: CRITICAL
        level = level * 10
        logger.setLevel(level)

        #log 출력 형식
        #self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(messages)s")
        self.formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)')
        self.logger = logger
        self.log_dir = log_dir
        

    def consoleHandler(self):
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
        
        

    def fileHandler(self, log_dir=None):
        
        log_file = 'sys.log'

        if log_dir is not None:
            self.log_dir = log_dir

        if(self.log_dir == None):
            raise ValueError('cannot be None of log_dir argument in file handler') 

        log_file = os.path.join(self.log_dir, log_file) # + '/' + name + '.log'
        file_max_bytes = 10 * 1024 * 1024

        try:
            if(sys.version_info.major==2):
                os.makedirs(self.log_dir)
            else:
                os.makedirs(self.log_dir, exist_ok=True)
        except OSError as e:
            if e.errno == errno.EEXIST and os.path.isdir(self.log_dir):
                pass
            else:
                raise
        
        try:
            handler = logging.handlers.RotatingFileHandler(filename=log_file, maxBytes=file_max_bytes, backupCount=100)
        except Exception as e:
            raise

        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def getLogger(self):
        return self.logger
        
        
    
if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser(description='logger')    
    parser.add_argument('--name', help='name')    
    parser.add_argument('--level', help='level')    
    parser.add_argument('--log_dir', help='log_dir')    
    args = parser.parse_args()
    
   
    c_logger = C_LOGGER({'name': args.name, 'level': args.level, 'log_dir': args.log_dir})
    c_logger.fileHandler(args.log_dir)
    
    logger = c_logger.getLogger()
    
    logger.info("start logger")
    
        