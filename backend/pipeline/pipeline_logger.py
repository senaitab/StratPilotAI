from datetime import datetime, UTC
from pathlib import Path


class PipelineLogger:

    def __init__(self, log_file="pipeline/pipeline.log"):
        self.log_path = Path(log_file)

        # Create parent directory if it doesn't exist
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, pipeline_id: str, stage: str, message: str):

        timestamp = datetime.now(UTC).isoformat()

        entry = (
            f"[{timestamp}] "
            f"[{pipeline_id}] "
            f"[{stage}] "
            f"{message}\n"
        )

        with open(self.log_path, "a", encoding="utf-8") as file:
            file.write(entry)

        return entry


if __name__ == "__main__":

    logger = PipelineLogger()

    pipeline = "TRD-DEMO1234"

    logger.log(pipeline, "Decision", "BUY")
    logger.log(pipeline, "Risk", "APPROVED")
    logger.log(pipeline, "Portfolio", "ALLOW")
    logger.log(pipeline, "Validation", "PASS")

    print("\n================================")
    print(" STRATPILOT PIPELINE LOGGER")
    print("================================")
    print("Pipeline log written successfully.")
    print("Log File : pipeline/pipeline.log")
    print("\nThink First. Trade Second.")
