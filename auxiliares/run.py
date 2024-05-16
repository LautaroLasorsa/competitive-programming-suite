#!/usr/bin/python3
# encoding: utf-8
'''MIT License

Copyright (c) 2017 Martin Villagra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import sys
import os
import subprocess
import resource
import signal
from tempfile import NamedTemporaryFile

assert sys.version_info >= (3, )

class Result (object):
    def __init__(self, running_time = None):
        if running_time is not None:
            self.running_time = running_time

def run_solution(com_fn, par_fn, input_fn,
                 output_fn = None,
                 reference_fn = None, 
                 time_limit = 2, checker = None): #,
                 #mem_limit = 1024,
                 #file_limit = 512):
    if reference_fn is None:
        if output_fn is None:
            output_fn = '/dev/null'
    else:
        assert output_fn is None
        output_file = NamedTemporaryFile(delete = False)
        output_fn = output_file.name

    pid = os.fork()
    if pid == 0:
        resource.setrlimit(resource.RLIMIT_CPU, (time_limit+1, time_limit + 1))
        with open(input_fn, 'r') as in_file:
            os.dup2(in_file.fileno(), 0)
        with open(output_fn, 'w') as out_file:
            os.dup2(out_file.fileno(), 1)
        #~ with open('/dev/null', 'w') as err_file:
            #~ os.dup2(err_file.fileno(), 2)
        if (len(par_fn) == 0):
            os.execv(com_fn, [com_fn])
        else:
            os.execvp(com_fn, [com_fn] + par_fn)
    (pid, status, rusage) = os.wait4(pid, 0)
    result = Result(running_time = rusage.ru_utime)
    result.pts = 0.0

    if result.running_time > time_limit:
        result.status = 'TLE'
    elif status != 0:
        result.status = 'RE'
        result.detail = 'failed' + str(status)
        if os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGSEGV:
            result.detail = 'SIGSEGV'
        elif os.WIFSIGNALED(status) and os.WTERMSIG(status) == signal.SIGABRT:
            result.detail = 'SIGABRT'
    elif reference_fn:
        if checker is None:
            with open(os.devnull, "w") as ignorar:
                if subprocess.call(['diff', reference_fn, output_fn],
                                stdout = ignorar,
                                stderr = ignorar) == 0:
                    result.status = 'AC'
                    result.pts = 1.0
                else:
                    result.status = 'WA'
        else:
            with open(os.devnull, "w") as ignorar:
                p = subprocess.Popen([checker, input_fn, reference_fn, output_fn], stdout=subprocess.PIPE, stderr=None)
                output, _ = p.communicate()
                if p.returncode==0:
                    result.pts = float(output)
                    result.status = 'AC' if result.pts == 1.0 else ("PA" if result.pts>0 else 'WA')
                else:
                    result.status = 'WA'
    else:
        result.status = 'OK'
        result.pts = 1.0

    if reference_fn:
        os.remove(output_fn)
    return result
