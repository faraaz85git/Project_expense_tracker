import logging
import uuid

class Logger:
    def __init__(self,log_file:str, log_name:str):
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger=logging.getLogger(log_name)
        self.id=uuid.uuid1()
    def log(self,message,level='info'):
            log_pool= dict(
                debug=self.logger.debug,
                info=self.logger.info,
                warning=self.logger.warning,
                error=self.logger.error,
                critical=self.logger.critical
            )
            log_pool[level](f"{self.id} - {message}")


# logger=Logger("logger/Logs/logs.log","yo")
# logger.log("fsdfsdf","debug")