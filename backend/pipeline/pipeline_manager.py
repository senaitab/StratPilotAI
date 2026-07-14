from pipeline.pipeline_record import PipelineRecord
from pipeline.pipeline_logger import PipelineLogger
from pipeline.pipeline_timeline import PipelineTimeline


class PipelineManager:

    def __init__(self):

        self.record = PipelineRecord()
        self.logger = PipelineLogger()
        self.timeline = PipelineTimeline()

    def update(self, stage: str, data: dict):

        self.record.update_stage(stage, data)

        self.timeline.record(stage)

        self.logger.log(
            self.record.pipeline_id,
            stage,
            str(data)
        )

    def complete(self):

        self.record.complete()

        return {
            "pipeline": self.record,
            "timeline": self.timeline.report()
        }


if __name__ == "__main__":

    manager = PipelineManager()

    manager.update("Decision", {"decision": "BUY"})
    manager.update("Risk", {"status": "APPROVED"})
    manager.update("Portfolio", {"status": "ALLOW"})
    manager.update("Validation", {"status": "PASS"})
    manager.update("Execution", {"status": "ORDER_SENT"})

    manager.complete()

    print("\n================================")
    print(" STRATPILOT PIPELINE MANAGER")
    print("================================")

    print("Pipeline:", manager.record.pipeline_id)
    print("Status  :", manager.record.status)

    print("\nTimeline")

    for event in manager.timeline.report():

        print(
            f"{event['stage']:<15}"
            f"{event['elapsed']:>8} sec"
        )

    print("\nThink First. Trade Second.")
