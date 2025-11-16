"""Input dataframe validation helpers."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ValidationIssue:
    column: str
    message: str


class DataFrameValidator:
    required_columns = ("id", "texte")

    def validate(self, df: pd.DataFrame) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for column in self.required_columns:
            if column not in df.columns:
                issues.append(ValidationIssue(column=column, message="missing"))
        return issues
