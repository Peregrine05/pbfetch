import pbfetch.parse_funcs.parse_uptime as uptime
import pbfetch.parse_funcs.parse_os as pos
import pbfetch.parse_funcs.parse_temp as temp
import pbfetch.parse_funcs.parse_cpu as cpu
import pbfetch.parse_funcs.parse_mem as mem
import platform, socket, psutil, os, subprocess, time


def stats():
    # constant for checking cpu usage (in seconds)
    DELAY = 0.3



    ################################
    #####         STATS        #####
    ################################



    stat_hostname = f"{os.getlogin()}@{socket.gethostname()}"
    stat_os = pos.parse_os()
    # stat_arch = platform.machine()
    stat_kernel = platform.release()
    stat_version = platform.version()
    stat_uptime = uptime.parse_uptime()
    stat_cpu_percent = f"{round(psutil.cpu_percent(DELAY))}%"
    stat_cpu_temp = f"{temp.parse_temp()}°c" 
    stat_cpu_name = cpu.parse_cpu()
    # TODO: parse memory usage from /proc/meminfo
    ram_total, ram_used = mem.parse_mem()
    stat_arch = (
        "x86_64" if (
            os.path.isfile("/lib/ld-linux-x86-64.so.2")
        ) else "x86"
    )
    stat_ram = str(
        f"{round(ram_used/1000)}/"
        f"{round(ram_total/1000)}"
        " MB"
    ) if ram_total and ram_used else None
    stat_packages = f"{len(
        str(
            subprocess.check_output(["pacman", "-Q"])
        ).split(" ")
    )} (pacman)"
    statvfs = os.statvfs("/")
    total_disk_size_in_bytes = statvfs.f_frsize * statvfs.f_blocks
    total_disk_size_in_gb = round(
        total_disk_size_in_bytes / (1024.0 ** 2)
    )
    disk_free_space_gb = round(
        statvfs.f_frsize * statvfs.f_bfree / (1024.0 ** 2)
    )
    total_disk_size_used = total_disk_size_in_gb - disk_free_space_gb
    stat_disk_total_and_used = (
        f"{total_disk_size_used}/{total_disk_size_in_gb} MB"
    )

    # init stats using keywords for configuration in .conf
    stats = {
        "$HOST": stat_hostname,
        "$SYS": stat_os,
        "$ARCH": stat_arch,
        "$KER": stat_kernel,
        "$MEM": stat_ram,
        "$UP": stat_uptime,
        "$PAC": stat_packages,
        "$TEM": stat_cpu_temp,
        "$%": stat_cpu_percent,
        "$CPU": stat_cpu_name,
        "$DISK": stat_disk_total_and_used,
    }



        ################################
        #####     END OF STATS     #####
        ################################



    return stats
