import collections
import dataclasses
import statistics
from typing import Any, Tuple, Optional
import json
import pykka
import psutil
from datetime import timezone, datetime
import math

import time
import queue
import threading

from retriever_research.config import Config
from retriever_research.ticker import Ticker


# CPU usage - detailed
# CPU usage - average
# available memory
# network throughput up
# network throughput down
# disk io
# disk read throughput
# disk write throughput
#

UNIT_MAP = dict(
    cpu_avg="%",
    free_mem="GB",
    net_sent="Gbit/s",
    net_recv="Gbit/s",
    disk_read="MB/s",
    disk_write="MB/s",
    disk_iops="#",
    proc_mem="MB",
    proc_count="#",
)

def humanize_float(num): return "{0:,.4f}".format(num)
h=humanize_float

GIGA = 1_000_000_000

class Profiler:
    def __init__(self, file_loc="retriever.profile", interval=0.1):
        self.file_loc = file_loc
        self.interval = interval
        self.profile_writer_ref = None  # type: Optional[pykka.ActorRef]
        self.profiler_ref = None  # type: Optional[pykka.ActorRef]
        self.profiler_ticker = None  # type: Optional[Ticker]
        self.start_time = None  # type: Optional[float]
        self.end_time = None  # type: Optional[float]

    def start(self):
        self.profile_writer_ref = ProfileWriteActor.start(file_loc=self.file_loc)
        self.profiler_ref = ProfilerActor.start(writer_ref=self.profile_writer_ref)
        self.profiler_ticker = ProfilerTicker(profiler_actor_ref=self.profiler_ref, interval=self.interval)
        self.profiler_ticker.start()
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()
        self.profiler_ticker.stop()
        self.profiler_ticker.join()

        self.profiler_ref.stop(block=True)
        self.profile_writer_ref.stop(block=True)

    def summarize_profile(self):
        if self.start_time and self.end_time:
            print(f"Duration: {h(self.end_time - self.start_time)} sec")

        profiles = collections.defaultdict(lambda: [])
        with open(self.file_loc, 'r') as f:
            for line in f:
                profile_event = json.loads(line)
                for measurement_name, measurement_val in profile_event.items():
                    if measurement_name == "timestamp":
                        continue
                    profiles[measurement_name].append(measurement_val)

        for measurement_name, timeseries in profiles.items():
            # print(timeseries)
            avg_val = statistics.mean(timeseries)
            max_val = max(timeseries)
            min_val = min(timeseries)
            median_val = statistics.median(timeseries)

            print("------------------------")
            print(f"Profile Summary - {measurement_name} ({UNIT_MAP[measurement_name]})")
            # print(f"Num Datapoints={len(timeseries)}")
            print(f"avg: {h(avg_val)}")
            print(f"max: {h(max_val)}")
            print(f"min: {h(min_val)}")
            print(f"median: {h(median_val)}")
            print(f"first: {h(timeseries[0])}")
            # print(f"p90: {h(calculate_percentile(timeseries, 90))}")
            # print(f"p80: {h(calculate_percentile(timeseries, 80))}")
            # # print(f"p70: {h(calculate_percentile(timeseries, 70))}")
            # print(f"p60: {h(calculate_percentile(timeseries, 60))}")
            # print(f"median: {h(median_val)}")
            # print(f"p40: {h(calculate_percentile(timeseries, 40))}")
            # # print(f"p30: {h(calculate_percentile(timeseries, 30))}")
            # print(f"p20: {h(calculate_percentile(timeseries, 20))}")
            # print(f"p10: {h(calculate_percentile(timeseries, 10))}")
            print()


def calculate_percentile(timeseries, percentile):
    n = len(timeseries)
    p = n * percentile / 100
    if p.is_integer():
        return sorted(timeseries)[int(p)]
    else:
        return sorted(timeseries)[int(math.ceil(p)) - 1]


"""
- SimpleCpuUtilization = Measured in percent
- FreeMemory = Measured in Gigabytes
- NetworkSentThroughput = Measured in Gigabit/s
- NetworkRecvThroughput = Measured in Gigabit/s
- DiskIops
- DiskReadThroughput = Measured in Megabytes/second
- DiskWriteThroughput = Measured in Megabytes/second
- ProcessMemoryUsed = Measured in Megabytes  (includes memory used by subprocesses)
- ProcessCount
"""
class ProfilerActor(pykka.ThreadingActor):
    def __init__(self, writer_ref: pykka.ActorRef):
        super().__init__()
        self.writer_ref = writer_ref
        self.is_first_datapoint = True

    def on_start(self) -> None:
        self.net_throughput_tracker = NetThroughputCollector()
        self.disk_throughput_tracker = DiskReadWriteRateCollector()

    def on_receive(self, message: Any) -> Any:
        timestamp = datetime.now(timezone.utc)

        cpu_avg = SimpleCpuUtilCollector.sample()
        free_mem = FreeMemoryCollector.sample()
        net_sent, net_recv = self.net_throughput_tracker.sample()
        disk_read, disk_write, disk_iops = self.disk_throughput_tracker.sample()
        proc_mem, proc_count = ProcInfoCollector.sample()

        # Skip first datapoint
        if self.is_first_datapoint:
            self.is_first_datapoint = False
            return

        profile_event = ProfileEvent(
            timestamp=timestamp,
            cpu_avg=cpu_avg,
            free_mem=free_mem,
            net_sent=net_sent,
            net_recv=net_recv,
            disk_read=disk_read,
            disk_write=disk_write,
            disk_iops=disk_iops,
            proc_mem=proc_mem,
            proc_count=proc_count
        )

        self.writer_ref.tell(profile_event)




class ProfileWriteActor(pykka.ThreadingActor):
    def __init__(self, file_loc):
        super().__init__()
        self.file_loc = file_loc

    def on_start(self) -> None:
        self.profile_fileobj = open(self.file_loc, "w")

    def on_receive(self, msg: Any) -> Any:
        assert isinstance(msg, ProfileEvent), f"Incorrect message type received, {type(msg)}"
        data = dict(
            timestamp=msg.timestamp.isoformat(),
            cpu_avg=msg.cpu_avg,
            free_mem=msg.free_mem,
            net_sent=msg.net_sent,
            net_recv=msg.net_recv,
            disk_read=msg.disk_read,
            disk_write=msg.disk_write,
            disk_iops=msg.disk_iops,
            proc_mem=msg.proc_mem,
            proc_count=msg.proc_count
        )
        as_str = json.dumps(data)
        self.profile_fileobj.write(f"{as_str}\n")

    def on_stop(self):
        self.profile_fileobj.close()

    def on_failure(self, *args):
        print(f"ProfileWriteActor failed, {args[0]}, {args[1]}")
        self.profile_fileobj.close()

@dataclasses.dataclass
class ProfileEvent:
    timestamp: datetime
    cpu_avg: float
    free_mem: float
    net_sent: float
    net_recv: float
    disk_read: float
    disk_write: float
    disk_iops: float
    proc_mem: float
    proc_count: float

class ThroughputTracker:
    def __init__(self, name: str, multiplier: float = 1.0):
        self.name = name
        self.multiplier = multiplier  # Adjust output unit
        self.last_measured_time = time.time()
        self.last_measured_val = 0.0

    def add_measurement(self, new_val: float, log=False) -> float:
        """
        Add a new value and return the throughput since the last measurement. The Measurement from
        the first call to add() is meaningless since the starting value is arbitrarily set to 0.
        """
        now = time.time()
        timestamp = datetime.fromtimestamp(now, timezone.utc)
        dur = (now - self.last_measured_time)
        delta = (new_val - self.last_measured_val)
        old_last_measured_val = self.last_measured_val

        val_per_sec = (new_val - self.last_measured_val) / (now - self.last_measured_time)
        self.last_measured_time = now
        self.last_measured_val = new_val
        throughput = val_per_sec * self.multiplier
        if log:
            print(new_val, old_last_measured_val, dur, delta, throughput)
        return throughput


class SimpleCpuUtilCollector:
    @staticmethod
    def sample() -> float:
        return psutil.cpu_percent()


class FreeMemoryCollector:
    @staticmethod
    def sample() -> float:
        free_mem_bytes = psutil.virtual_memory().available
        return free_mem_bytes / GIGA


class ProcInfoCollector:
    @staticmethod
    def sample() -> Tuple[float, int]:
        # Returns memory_used, proc_count
        this_process = psutil.Process()
        proc_count = 1
        proc_mem_used = this_process.memory_info().rss
        for child in this_process.children(recursive=True):
            try:
                proc_count += 1
                proc_mem_used += child.memory_info().rss
            except psutil.NoSuchProcess:
                pass
        return proc_mem_used / Config.MEGA, proc_count


class NetThroughputCollector:
    def __init__(self) -> None:
        self.sent_throughput = ThroughputTracker("Network Sent (Gbit/s)", multiplier=8 / GIGA)
        self.recv_throughput = ThroughputTracker("Network Recv (Gbit/s)", multiplier=8 / GIGA)

        # Discard initial batch that is meaningless
        net = psutil.net_io_counters()
        self.sent_throughput.add_measurement(net.bytes_sent)
        self.recv_throughput.add_measurement(net.bytes_recv)

    def sample(self) -> Tuple[float, float]:
        net = psutil.net_io_counters()
        sent = self.sent_throughput.add_measurement(net.bytes_sent)
        recv = self.recv_throughput.add_measurement(net.bytes_recv)
        return sent, recv


class DiskReadWriteRateCollector:
    def __init__(self) -> None:
        self.read_throughput_tracker = ThroughputTracker("Disk Read (Megabytes/s)", multiplier=1/Config.MEGA)
        self.write_throughput_tracker = ThroughputTracker("Disk Write (Megabytes/s)", multiplier=1/Config.MEGA)
        self.iops = ThroughputTracker("Disk IOPS")

        # Discard initial batch that is meaningless
        disk = psutil.disk_io_counters()
        self.read_throughput_tracker.add_measurement(disk.read_bytes)
        self.write_throughput_tracker.add_measurement(disk.write_bytes)
        self.iops.add_measurement(disk.read_count + disk.write_count)

    def sample(self) -> Tuple[float, float, float]:
        """Return tuple of (Read, Write, IOPS) values"""
        disk = psutil.disk_io_counters()

        read_throughput = self.read_throughput_tracker.add_measurement(disk.read_bytes)
        write_throughput = self.write_throughput_tracker.add_measurement(disk.write_bytes)
        iops = self.iops.add_measurement(disk.read_count + disk.write_count, log=False)
        # print(disk.read_count + disk.write_count, iops)
        return read_throughput, write_throughput, iops


class ProfilerTick:
    pass


class ProfilerTicker(Ticker):
    def __init__(self, profiler_actor_ref: pykka.ActorRef, interval=1.0) -> None:
        self.shutdown_queue = queue.Queue()
        self.interval = interval
        self.profiler_actor_ref = profiler_actor_ref
        super().__init__(interval=interval)

    def execute(self):
        self.profiler_actor_ref.tell(ProfilerTick())


if __name__ == '__main__':
    prof = Profiler(interval=0.1)
    prof.start()

    from retriever_research.retriever import Retriever
    ret = Retriever()
    # ret.launch(s3_bucket="quilt-ml", s3_prefix="cv/coco2017/annotations/captions_", s3_region="us-east-1")
    ret.launch(s3_bucket="quilt-ml", s3_prefix="cv/coco2017/annotations/captions_train2017.json", s3_region="us-east-1")
    # ret.launch(s3_bucket="quilt-ml", s3_prefix="cv/coco2017/train2017/000000000025.jpg", s3_region="us-east-1")
    ret.get_output()

    prof.end()
    prof.summarize_profile()


