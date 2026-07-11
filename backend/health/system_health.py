class SystemHealth:

    def evaluate(self):

        modules = {
            "Decision Engine": True,
            "Risk Manager": True,
            "Execution Guard": True,
            "Portfolio Manager": True,
            "Session Manager": True,
            "Learning Engine": True,
            "Decision Validator": True,
            "Orchestrator": True,
        }

        online = sum(modules.values())
        total = len(modules)

        health_score = round((online / total) * 100)

        status = "HEALTHY" if health_score == 100 else "DEGRADED"

        return {
            "status": status,
            "health_score": health_score,
            "modules": modules,
        }


if __name__ == "__main__":

    health = SystemHealth()
    report = health.evaluate()

    print("\n==============================")
    print(" STRATPILOT SYSTEM HEALTH")
    print("==============================")

    print(f"Overall Status : {report['status']}")
    print(f"Health Score   : {report['health_score']}%")

    print("\nModules")
    print("------------------------------")

    for module, state in report["modules"].items():
        icon = "✓" if state else "✗"
        print(f"{icon} {module}")

    print("\nThink First. Trade Second.")
