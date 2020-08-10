import yaml
import os 
import sys
import socket
import subprocess
import paramiko


MY_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = os.path.abspath(os.path.join(MY_DIR, '../'))
RUNTIME_DIR = os.path.join(WORK_DIR, 'runtime')
sys.path.append(os.path.join(WORK_DIR, 'python3/lib/python3.6/site-packages'))


def check_root():
    username ,home = os.environ.get('USER'), os.environ.get('HOME')

    if username !='root' or home != '/root':
        return False
    else:
        return True

def monkey_sudo(password, cmd ,sudo_need_password=False):
    monkey_cmd = 'echo {}|sudo -S {}'.format(password, cmd) if sudo_need_password else 'sudo {}'.format(cmd)

    return monkey_cmd




def run_cmd(cmd , timeout=60):
    print_fun = lambda x: print(x,file=sys.stderr)

    p = subprocess.Popen(
        cmd,
        shell=True,
        universal_newlines = True,
        stdout = subprocess.PIPE,
        stderr= subprocess.PIPE
        )
    
    try:
        (stdout,stderr) = p.communicate(cmd, timeout=timeout)
    except subprocess.TimeoutExpired:
        print('run cmd TIMEOUT')
        p.kill()
        (stdout,stderr) = p.communicate()
    
    ret = p.returncode
    res = {'ret': ret, 'stdout': stdout, 'stderr': stderr}
    return res

class SSHCLIENT(object):
    def __init__(
        self, host, port = 22, user = 'root', password = None, key_filename = None, encoding='utf8', timeout = 21, debug =False
    ):
        self.host = host
        self.user = user
        self.encoding = encoding

        if not key_filename and user != 'root':
            key_filename = '/home/{}/.ssh/id_rsa'.format(user)
            
            if not os.path.exists(key_filename):
                key_filename= None
        
        self.params = {
            'hostname': host,
            'port': port,
            'username': user,
            'password': password,
            'key_filename': key_filename,
            'timeout': timeout,
        }

        if debug:
            logger_dir = '{}/debug-paramiko'.format(RUNTIME_DIR)
            if not os.path.exists(logger_dir):
                os.makedirs(logger_dir, exist_ok=True)
            paramiko.util.log_to_file('{}/{}.log'.format(logger_dir, host))

        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        self.is_connected = False

    def __del__(self):
        try:
            self.client.close()
        except Exception as e:
            pass
    
    def connect(self):
        if self.is_connected:
            return True
        try:
            self.client.connect(**self.params)
            self.is_connected = True
        except socket.timeout:
            raise Exception('Connect timeout: The Server may be not allow to connect')

    def invoke_shell(self):
        self.is_connected = True
        return self.client.invoke_shell(term='linux')

    def run_cmd(self, cmd, timeout=1800):
        self.connect()

        stdin_fd, stdout_fd, stderr_fd = self.client.exec_command(cmd, timeout=timeout, get_pty=True)
        ret = stdout_fd.channel.recv_exit_status()
        stdout, stderr = stdout_fd.read().decode(self.encoding), stderr_fd.read().decode(self.encoding)
        return {'ret': ret, 'stdout': stdout, 'stderr': stderr}


    def check_paramiko(self, cmd ='echo "hello world"'):
        res = self.run_cmd(cmd)
        if res['ret']=='0':
            return True,res
        else:
            return False,res


            

def parse_conf(conf_file):
    if not os.path.exists(conf_file):
        raise Exception ('{}: not exists.'.format(conf_file))
    required_keys = ['ips','username','password','ssh_port','data_disk_path']
    list_type_keys = ['ips','data_disk_path']

    with open(conf_file,'r',encoding="utf-8") as f:
        try:
            conf = yaml.load(f.read(), Loader=yaml.FullLoader)
        except yaml.parser.ParserError or yaml.scanner.ScannerError as reason:
            raise Exception("{}:yaml parse error ':'\n {}".format(conf_file,reason.problem_mark))
        
    for k in required_keys:
        if k not in conf.keys():
            raise Exception("{} not in {}".format(k,conf_file))
        if conf[k] is None:
            raise Exception("invalid conf:{} should not be None".format(k))

#rint(parse_conf("config.yaml"))

    
