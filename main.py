import jinja2
import os


def render(filename, **kwargs):
    path = "ci-cd/config-tmpl"

    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(**kwargs)


def generate_online_conf(tmpl_filename):
    mysql = {'host': 'zzz.wul.ai', 'port': 3306, 'user': 'root', 'passwd': 'Laiye@2020'}
    online_config_path='ci-cd/online-config'
    if not os.path.exists(online_config_path):
        os.mkdir(online_config_path)
    res = render(tmpl_filename, **locals())
    online_conf = os.path.join(online_config_path, tmpl_filename)
    try:
        with open(online_conf, 'w') as f:
            f.write(res)
    except Exception as e:
        print(e)


if __name__ == '__main__':

    for file in os.listdir("ci-cd/config-tmpl"):
        generate_online_conf(file)
