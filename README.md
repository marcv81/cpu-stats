# CPU stats

`cpu_stats.py` outputs CPU stats in InfluxDB line protocol format. It integrates nicely with the Telegraf `execd` input plugin.

## Output

A sample follows.

    cpu_freq,name=cpu0 value=800352000
    cpu_power,name=package-0 value=6.869896

- The unit of `cpu_freq` is hertz (Hz).
- The unit of `cpu_power` is watt (W).

## Installation

Copy `cpu_stats.py` to `/usr/local/bin`.

Add the following line to `/etc/sudoers.d/telegraf`.

    telegraf ALL=(root) NOPASSWD: /usr/local/bin/cpu_stats.py

Create `/etc/telegraf/telegraf.d/cpu_stats.conf` with the following contents.

    [[inputs.execd]]
      command = ["sudo", "cpu_stats.py"]
      signal = "STDIN"
      data_format = "influx"
