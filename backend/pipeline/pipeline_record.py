from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class PipelineRecord:

    pipeline_id: str = field(
        default_factory=lambda: f"TRD-{uuid4().hex[:8].upper()}"
    )

    created_at: datetime = field(default_factory=datetime.utcnow)

    completed_at: datetime | None = None

    status: str = "RUNNING"

    current_stage: str = "INITIALIZED"

    stages: dict = field(default_factory=dict)

    def update_stage(self, stage: str, data):

        self.current_stage = stage

        self.stages[stage] = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }

    def complete(self):

        self.completed_at = datetime.utcnow()

        self.status = "COMPLETE"

    def fail(self):

        self.completed_at = datetime.utcnow()

        self.status = "FAILED"

    @property
    def duration(self):

        end = self.completed_at or datetime.utcnow()

        return round(
            (end - self.created_at).total_seconds(),
            3
        )
