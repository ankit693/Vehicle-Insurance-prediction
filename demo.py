# from src.logger import configure_logger
# import logging

# # Log messages at all levels
# logging.debug("This is a DEBUG message — useful for developers.")
# logging.info("This is an INFO message — general information.")
# logging.warning("This is a WARNING message — something to watch out for.")
# logging.error("This is an ERROR message — something went wrong.")
# logging.critical("This is a CRITICAL message — serious failure!")


from src.pipline.training_pipeline import TrainPipeline

pipline = TrainPipeline()
pipline.run_pipeline()
