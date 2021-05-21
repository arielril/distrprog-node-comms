import atexit
from apscheduler.schedulers.background import BackgroundScheduler


def start_task(supernode_port):
    def check_alive_nodes():
        import requests

        try:
            requests.get(
                f'http://localhost:{supernode_port}/api/supernode/xxx',
            )
            print('[+] requested supernode to run liveness check')
        except:
            print('[.] failed to request supernode to run liveness check')

    sched = BackgroundScheduler()
    sched.add_job(
        func=check_alive_nodes,
        trigger='interval',
        seconds=5,
    )
    sched.start()
    atexit.register(lambda: sched.shutdown())
