
import env_utils
import yaml
from env_utils import SSHCLIENT

def getParameters():
    with open("config.yaml",'r',encoding="utf-8") as f:
        try:
            conf = yaml.load(f.read(),Loader=yaml.FullLoader)
        except yaml.parser.ParserError or yaml.scanner.ScannerError as reason:
            raise Exception("{}:yaml parse error ':'\n{}}".format("config.yaml", reason.problem_mark))
    return conf


def check(config):
    for i in config['ips']:
        client=SSHCLIENT(host=i, password=config['password'])
        res=client.run_cmd(cmd= "free -g ")
        print(res['ret'])
        print(res['stdout'])


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('conf_file',help="see ./env.conf.example & ")
    parser.add_argument('-s',action='store_true',dest='skip',default=False,help='skip ysnc packages')
    
    disk_switch = parser.add_mutually_exclusive_group()
    disk_switch.add_argument(
        '--only_disks',action='store_true',dest='only_disks', default=False,help='only check disk'
    )
    disk_switch.add_argument('--no_disks', action='store_true',dest='no_disks',default=False,help='skip check disk')
    parser.add_argument(
        '--disk_thread', action='store', desk='disk_thread',default=1, choices=[str(i) for i in range(1, 7)],
        help='check n disks at the same time' 
    )
    parser.add_argument('--no_io',action='store_true', dest='no_io', default=False,help='skip check disk io')

    bw_switch = parser.add_mutually_exclusive_group()
    bw_switch.add_argument('--only_bw', action='store_true', dest='only_bw', default=False, help='only check bandwidth')
    bw_switch.add_argument('--no_bw',action='store_true',dest='no_bw',default=False, help='skip check bandwidth')





