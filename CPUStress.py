import multiprocessing
import time
import signal

class CPUStressTester:
    def __init__(self):
        '''Initializes the CPU stress tester.'''
        self.stop_event = multiprocessing.Event()
        self.processes = []

    @staticmethod
    def worker(stop_event):
        '''Worker function that calculates prime numbers until the stop event is set.'''
        while not stop_event.is_set():
            CPUStressTester.calculate_primes(10000000)

    @staticmethod
    def calculate_primes(upper_limit):
        '''Calculates prime numbers up to the specified upper limit.'''
        primes = []
        for num in range(2, upper_limit):
            is_prime = True
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        return primes

    @staticmethod
    def update_stopwatch(start_time, stop_event):
        '''Displays the elapsed time since the start of the CPU stress test'''
        while not stop_event.is_set():
            elapsed_time = time.time() - start_time
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            print(f"\rElapsed time: {int(hours):02}:{int(minutes):02}:{int(seconds):02}", end="")
            time.sleep(1)

    def signal_handler(self, sig, frame):
        '''Signal handler that stops the CPU stress test when Ctrl+C is pressed.'''
        self.stop_event.set()

    def cpu_stress_test(self):
        '''Performs a CPU stress test until interrupted by the user, utilizing hyperthreading (SMT).'''
        num_logical_cores = multiprocessing.cpu_count()
        start_time = time.time()

        stopwatch_process = multiprocessing.Process(target=CPUStressTester.update_stopwatch, args=(start_time, self.stop_event))
        processes = [multiprocessing.Process(target=CPUStressTester.worker, args=(self.stop_event,)) for _ in range(num_logical_cores)]

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        try:
            stopwatch_process.start()
            for p in processes:
                p.start()
            print("Stressing the CPU...")
            print("Press Ctrl+C to stop the CPU stress test...")

            while not self.stop_event.is_set():
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping the stress test...")

        finally:
            self.stop_event.set()
            stopwatch_process.terminate()
            stopwatch_process.join()
            for p in processes:
                p.terminate()
                p.join()

if __name__ == "__main__":
    tester = CPUStressTester()
    tester.cpu_stress_test()
