import os, subprocess, socket, time
import cdsw


def run_scheduler(num_workers=1, cpu=1, memory=2):
    """
    Run a Dask Scheduler process in a CDSW worker.
    """
    scheduler_code = f"""!dask-scheduler \
        --host 0.0.0.0 \
        --dashboard-address 127.0.0.1:{os.environ['CDSW_READONLY_PORT']}"""
    dask_scheduler = cdsw.launch_workers(
        n=num_workers,
        cpu=cpu,
        memory=memory,
        code=scheduler_code,
    )
    scheduler_details = cdsw.await_workers(
      dask_scheduler, 
      wait_for_completion=False, 
      timeout_seconds=90
    )
    if scheduler_details['failures']:
        raise RuntimeError("dask-scheduler worker node failed to launch.")
        print(scheduler_details['failures'][0])
    return dask_scheduler

  
def get_scheduler_url(dask_scheduler):
    """
    Given a Dask Scheduler, identify its TCP url so Dask Workers can 
    communicate with it. 
    """
    scheduler_workers = cdsw.list_workers()
    scheduler_id = dask_scheduler[0]["id"]
    scheduler_ip = [
        worker["ip_address"] for worker in scheduler_workers if worker["id"] == scheduler_id
    ][0]

    return f"tcp://{scheduler_ip}:8786"
  

def run_dask_workers(scheduler_url, num_workers, cpu, memory, nvidia_gpu=0):
    """
    Launch num_workers CDSW workers as Dask Worker nodes.
    Assumes that the Dask Scheduler is running and available via 
    the scheduler_url.
    """
    workers = cdsw.launch_workers(
            n=num_workers, 
            cpu=cpu, 
            memory=memory, 
            nvidia_gpu=nvidia_gpu, 
            code=f"!dask-worker {scheduler_url}"
          )

    worker_details = cdsw.await_workers(workers, wait_for_completion=False)
    if worker_details['failures']:
        raise RuntimeError("dask worker nodes failed to launch.")
        print(worker_details['failures'])
    return workers


def run_dask_cluster(num_workers, cpu, memory, nvidia_gpu=0):
    """
    Runs a Dask Scheduler and the requested number of Dask Workers
    as CDSW workers via the Workers API. 
    """
    dask_scheduler = run_scheduler()
    scheduler_url = get_scheduler_url(dask_scheduler)
    dask_workers = run_dask_workers(
        scheduler_url=scheduler_url,
        num_workers=num_workers, 
        cpu=cpu, 
        memory=memory, 
        nvidia_gpu=nvidia_gpu, 
    )
    return {
        "scheduler": dask_scheduler,
        "workers": dask_workers,
        "scheduler_address": scheduler_url
        }