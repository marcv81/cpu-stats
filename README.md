# CPU stats

`cpu_stats.py` outputs CPU stats in InfluxDB line protocol format. It integrates nicely with the Telegraf `execd` input plugin.

## Output

A sample follows.

    cpu_freq,name=cpu0 value=800352000
    cpu_power,name=package-0 value=6.869896

- The unit of `cpu_freq` is hertz (Hz).
- The unit of `cpu_power` is watt (W).

## Installation

Copy `rapl_init.sh` to `/usr/local/bin/rapl_init.sh`.

Create `/etc/udev/rules.d/99-rapl.rules`.

    SUBSYSTEM=="powercap", RUN+="/usr/local/bin/rapl_init.sh"

Copy `cpu_stats.py` to `/usr/local/bin`.

Create `/etc/telegraf/telegraf.d/cpu_stats.conf` with the following contents.

    [[inputs.execd]]
      command = ["cpu_stats.py"]
      signal = "STDIN"
      data_format = "influx"

Reboot.
