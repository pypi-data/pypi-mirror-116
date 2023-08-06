import argparse
import logging
import logging.config
import random
import shutil
from importlib import import_module
from pathlib import Path

import tensorflow as tf
from azureml.core.run import Run

from constants import DEFAULT_CONFIG, REPO_DIR

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s: line %(lineno)d'))
logger.addHandler(handler)


def copy_dir(src: Path, tgt: Path, glob_pattern: str, should_touch_init: bool = False):
    logger.info("Creating temp folder")
    if tgt.exists():
        shutil.rmtree(tgt)
    tgt.mkdir(parents=True, exist_ok=True)
    if should_touch_init:
        (tgt / '__init__.py').touch(exist_ok=False)

    paths_to_copy = list(src.glob(glob_pattern))
    logger.info(f"Copying to {tgt} the following files: {str(paths_to_copy)}")
    for p in paths_to_copy:
        destpath = tgt / p.relative_to(src)
        destpath.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(p, destpath)


def is_offline_run(run: Run) -> bool:
    return run.id.startswith("OfflineRun")


# Get the current run.
RUN = Run.get_context()

from cgmml.common.evaluation.eval_utilities import (  # noqa: E402, F401
    is_ensemble_evaluation, is_multiartifact_evaluation)
from cgmml.common.evaluation.evaluation_classes import (  # noqa: E402, F401
    Evaluation, EnsembleEvaluation, MultiartifactEvaluation)
from cgmml.common.model_utils.run_initialization import OfflineRunInitializer, OnlineRunInitializer  # noqa: E402

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s - %(pathname)s: line %(lineno)d')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--qa_config_module", default=DEFAULT_CONFIG, help="Configuration file")
    args = parser.parse_args()
    qa_config_module = args.qa_config_module
    qa_config = import_module(qa_config_module)
else:
    qa_config_module = DEFAULT_CONFIG
    qa_config = import_module(qa_config_module)
logger.info('Using the following config: %s', qa_config_module)


MODEL_CONFIG = qa_config.MODEL_CONFIG
EVAL_CONFIG = qa_config.EVAL_CONFIG
DATA_CONFIG = qa_config.DATA_CONFIG
RESULT_CONFIG = qa_config.RESULT_CONFIG
FILTER_CONFIG = qa_config.FILTER_CONFIG if getattr(qa_config, 'FILTER_CONFIG', False) else None


if __name__ == "__main__":
    # Make experiment reproducible
    tf.random.set_seed(EVAL_CONFIG.SPLIT_SEED)
    random.seed(EVAL_CONFIG.SPLIT_SEED)

    if is_offline_run(RUN):
        OUTPUT_CSV_PATH = str(REPO_DIR / 'data' / RESULT_CONFIG.SAVE_PATH)
        initializer = OfflineRunInitializer(DATA_CONFIG, EVAL_CONFIG)
    else:
        OUTPUT_CSV_PATH = RESULT_CONFIG.SAVE_PATH
        initializer = OnlineRunInitializer(DATA_CONFIG, EVAL_CONFIG, RUN)

    if is_ensemble_evaluation(MODEL_CONFIG):
        MODEL_BASE_DIR = (REPO_DIR / 'data' / MODEL_CONFIG.EXPERIMENT_NAME) if is_offline_run(RUN) else Path('.')
        eval_class = EnsembleEvaluation
        descriptor = MODEL_CONFIG.EXPERIMENT_NAME
    else:
        MODEL_BASE_DIR = REPO_DIR / 'data' / MODEL_CONFIG.RUN_ID if is_offline_run(RUN) else Path('.')
        eval_class = MultiartifactEvaluation if is_multiartifact_evaluation(DATA_CONFIG) else Evaluation
        descriptor = MODEL_CONFIG.RUN_ID
    evaluation = eval_class(MODEL_CONFIG, DATA_CONFIG, MODEL_BASE_DIR, initializer.dataset_path)
    evaluation.get_the_model_path(initializer.workspace)

    # Get the QR-code paths
    qrcode_paths = evaluation.get_the_qr_code_path()
    if getattr(EVAL_CONFIG, 'DEBUG_RUN', False) and len(qrcode_paths) > EVAL_CONFIG.DEBUG_NUMBER_OF_SCAN:
        qrcode_paths = qrcode_paths[:EVAL_CONFIG.DEBUG_NUMBER_OF_SCAN]
        logger.info("Executing on %d qrcodes for FAST RUN", EVAL_CONFIG.DEBUG_NUMBER_OF_SCAN)

    dataset_evaluation, paths_belonging_to_predictions = evaluation.prepare_dataset(qrcode_paths, FILTER_CONFIG)
    prediction_array = evaluation.get_prediction_(evaluation.model_path_or_paths, dataset_evaluation)
    logger.info("Prediction made by model on the depthmaps...")
    logger.info(prediction_array)

    df = evaluation.prepare_dataframe(paths_belonging_to_predictions, prediction_array, RESULT_CONFIG)
    evaluation.evaluate(df, RESULT_CONFIG, EVAL_CONFIG, OUTPUT_CSV_PATH, descriptor)

    # Done.
    initializer.run.complete()
