#!/usr/bin/env python3

import os
import sys
import time

CPU_DIR = "/sys/devices/system/cpu"
RAPL_DIR = "/sys/devices/virtual/powercap/intel-rapl"


def is_cpu(s):
    """Tests if a string represents a CPU device."""
    prefix = "cpu"
    if not s.startswith(prefix):
        return False
    for c in s[len(prefix) :]:
        if ord(c) < ord("0") or ord(c) > ord("9"):
            return False
    return True


def is_rapl(s):
    """Tests if a string represents a RAPL device."""
    prefix = "intel-rapl"
    if not s.startswith(prefix):
        return False
    for c in s[len(prefix) :]:
        if c != ":" and (ord(c) < ord("0") or ord(c) > ord("9")):
            return False
    return True


def read_cpu(cpu):
    """Reads the frequency of a CPU device."""
    filename = "%s/%s/cpufreq/scaling_cur_freq" % (CPU_DIR, cpu)
    with open(filename) as f:
        frequency = int(f.read())
    return frequency


def read_rapl(rapl):
    """Reads the energy of a RAPL device."""
    filename = "%s/%s/name" % (RAPL_DIR, rapl)
    with open(filename) as f:
        name = f.read().strip()
    filename = "%s/%s/energy_uj" % (RAPL_DIR, rapl)
    with open(filename) as f:
        energy = int(f.read())
    return name, energy


def iter_cpu():
    """Iterates over all the CPU frequencies."""
    try:
        for cpu in os.listdir(CPU_DIR):
            if not is_cpu(cpu):
                continue
            try:
                frequency = read_cpu(cpu)
                yield cpu, frequency
            except OSError:
                pass
    except OSError:
        pass


def iter_rapl():
    """Iterates over all the RAPL energies."""
    todo = []
    # Top-level Intel RAPL devices.
    try:
        for rapl in os.listdir(RAPL_DIR):
            if not is_rapl(rapl):
                continue
            todo.append(rapl)
    except OSError:
        pass
    while len(todo) > 0:
        rapl = todo.pop()
        try:
            name, energy = read_rapl(rapl)
            yield name, energy
        except OSError:
            pass
        # Nested Intel RAPL devices.
        try:
            for sub_rapl in os.listdir("%s/%s" % (RAPL_DIR, rapl)):
                if not is_rapl(sub_rapl):
                    continue
                todo.append("%s/%s" % (rapl, sub_rapl))
        except OSError:
            pass


def iter_frequency_stats():
    """Iterates over collections of CPU frequency stats."""
    while True:
        lines = []
        for cpu, frequency in iter_cpu():
            frequency *= 1000
            line = "cpu_freq,name=%s value=%d\n" % (cpu, frequency)
            lines.append(line)
        yield lines


def iter_power_stats():
    """Iterates over collections of RAPL power stats."""
    previous = {}
    while True:
        lines = []
        for name, energy_1 in iter_rapl():
            time_1 = time.monotonic()
            if name in previous:
                energy_0, time_0 = previous[name]
                # Use numerical differentiation to convert energy to power.
                power = (energy_1 - energy_0) / (time_1 - time_0) / 1e6
                if power >= 0:
                    line = "cpu_power,name=%s value=%f\n" % (name, power)
                    lines.append(line)
            previous[name] = energy_1, time_1
        yield lines


if __name__ == "__main__":
    frequency_stats = iter_frequency_stats()
    power_stats = iter_power_stats()
    while True:
        _ = sys.stdin.readline()
        lines = next(frequency_stats) + next(power_stats)
        sys.stdout.write("".join(lines))
        sys.stdout.flush()
