"""Simple module for getting amount of memory used by a specified user's
processes on a UNIX system.
It uses UNIX ps utility to get the memory usage for a specified username and
pipe it to awk for summing up per application memory usage and return the total
Python's Popen() from subprocess module is used for spawning ps and awk.

"""

import subprocess


class MemoryMonitor(object):

    def usage(self):
        """Return int containing memory used by user's processes."""
        command = "ps -o rss | awk '{sum+=$1} END {print sum}'"
        self.process = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE)
        self.stdout_list = self.process.communicate()[0].split('\n')
        return int(self.stdout_list[0])
