"""High-level orchestration pipeline for the classifier."""
from __future__ import annotations

from ..config import constants, settings
from ..config.prompts import CLASSIFIER_SYSTEM_PROMPT
from ..ingestion.loader import CSVLoader
from ..ingestion.merger import DataMerger
from ..ingestion.validator import DataFrameValidator
from ..export.exporter import Exporter
from ..export.update_history import HistoryUpdater
from ..utils.logger import get_logger
from .ai_classifier import AIClassifier
from .category_assigner import CategoryAssigner
from .historical_matcher import HistoricalMatcher

logger = get_logger(__name__)


class Pipeline:
    def __init__(self) -> None:
        self.settings = settings.get_settings()
        self.loader = CSVLoader()
        self.validator = DataFrameValidator()
        self.merger = DataMerger()
        self.classifier = AIClassifier(model_path=self.settings.model_path)
        self.category_assigner = CategoryAssigner(default_category=constants.DEFAULT_CATEGORY)
        self.matcher = HistoricalMatcher()
        self.exporter = Exporter(self.settings.history_path)
        self.history_updater = HistoryUpdater(self.settings.history_path)

    def run(self, csv_paths: list[str]) -> None:
        logger.info("Starting pipeline", extra={"system_prompt": CLASSIFIER_SYSTEM_PROMPT})
        datasets = self.loader.load_many(csv_paths)
        merged = self.merger.merge(datasets)
        issues = self.validator.validate(merged)
        if issues:
            logger.warning("Validation issues detected", extra={"issues": issues})
        for _, row in merged.iterrows():
            text = row.get("texte", "")
            match = self.matcher.match(text)
            if match and match.score >= constants.HISTORY_MATCH_THRESHOLD:
                label = match.label
            else:
                result = self.classifier.predict(text)
                label = self.category_assigner.assign(result)
            self.history_updater.append(row.get("id"), label)
        self.exporter.save_latest(merged)
        logger.info("Pipeline finished")
