import atexit
from apscheduler.schedulers.background import BackgroundScheduler


def start_task(supernode_addr=""):
    if supernode_addr == "":
        return

    def check_alive_nodes():
        import requests

        try:
            requests.get(
                f"http://{supernode_addr}/api/supernode/xxx",
            )
            print("[+] requested supernode to run liveness check")
        except Exception as e:
            print("[.] failed to request supernode to run liveness check", e)

    sched = BackgroundScheduler()
    sched.add_job(
        func=check_alive_nodes,
        trigger="interval",
        seconds=5,
    )
    sched.start()
    atexit.register(lambda: sched.shutdown())
