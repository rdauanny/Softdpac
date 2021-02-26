
import subprocess

class SubCommandFailed(Exception):
    def __init__(self, cmd, out, err, ret):
        if isinstance(cmd, list):
            self.cmd = ' '.join(cmd)
        else:
            self.cmd = cmd
        self.out = out
        self.err = err
        self.ret = ret
        super(SubCommandFailed, self).__init__(self.__str__())

    def __str__(self):
        return 'Sub-command [{}] failed with return code [{}]\nstderr:\n\n{}\nstdout:\n\n{}'.format(self.cmd, self.ret, self.err, self.out)


# This function is used to run commands through a subprocess and catch results
def run_cmd(cmd, raiseExcept=True, shell = True, cmdinput=None, timeout=None, debug=False):
    if debug:
        print('cmd = [{}]'.format(cmd))
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, executable='/bin/bash')
    out, err = process.communicate(cmdinput)# timeout not supported by Azure Devops , timeout=timeout)
    if raiseExcept and process.returncode != 0:
        raise SubCommandFailed(cmd, out, err, process.returncode)
    if debug:
        print('code=[{}] stdout = [{}], stderr=[{}]'.format(process.returncode, out, err))

    return out, process.returncode

# This function is added for docker logs commands, as the result is mapped to stderr
def run_cmd_docker_logs(cmd, shell = True, cmdinput=None, debug=False):
    if debug:
        print('cmd = [{}]'.format(cmd))
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, executable='/bin/bash')
    out, err = process.communicate(cmdinput)
    if debug:
        print('code=[{}] stdout = [{}], stderr=[{}]'.format(process.returncode, out, err))

    return err, 0