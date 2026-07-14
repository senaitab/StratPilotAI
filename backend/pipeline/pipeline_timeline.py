from datetime import datetime, UTC


class PipelineTimeline:

    def __init__(self):

        self.started = datetime.now(UTC)

        self.events = []

    def record(self, stage):

        now = datetime.now(UTC)

        elapsed = (
            now - self.started
        ).total_seconds()

        self.events.append({

            "stage": stage,

            "timestamp": now.isoformat(),

            "elapsed": round(elapsed, 6)

        })

    def report(self):

        return self.events


if __name__ == "__main__":

    timeline = PipelineTimeline()

    timeline.record("Decision")

    timeline.record("Risk")

    timeline.record("Portfolio")

    timeline.record("Validation")

    timeline.record("Execution")

    print("\n================================")
    print(" STRATPILOT PIPELINE TIMELINE")
    print("================================")

    for event in timeline.report():

        print(

            f"{event['stage']:<15}"

            f"{event['elapsed']:>8} sec"

        )

    print("\nThink First. Trade Second.")
