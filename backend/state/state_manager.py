from datetime import datetime
from state.system_state import SYSTEM_STATE


class StateManager:
    def update(self, key, value):
        SYSTEM_STATE[key] = value
        SYSTEM_STATE["timestamp"] = datetime.now().isoformat()

    def get(self, key):
        return SYSTEM_STATE.get(key)

    def snapshot(self):
        return SYSTEM_STATE.copy()


if __name__ == "__main__":
    manager = StateManager()

    manager.update("decision", "BUY")
    manager.update("risk", "APPROVED")
    manager.update("execution", "SAFE")

    print("=" * 35)
    print(" STRATPILOT SYSTEM STATE")
    print("=" * 35)

    for key, value in manager.snapshot().items():
        print(f"{key:12}: {value}")

    print("\nThink First. Trade Second.")
