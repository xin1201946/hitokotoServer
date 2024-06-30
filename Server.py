import re
import time
import requests
from flask import Flask, request, jsonify, Response, render_template
import os
import json
import random
import logging

from theme.logo import LOGO
from Apps.preset import TOLOGO
from Apps.ServerAPPs import neofetch, Get_mechine_info, CommandDIC
import Storage

IP = '0.0.0.0'
server_name = 'CanFengServer'
PORT = 5000
app = Flask(server_name, static_folder='templates/')
Root_user = 'CanFeng'
Root_password = '1234567890qaz'
log_file_path = os.path.join('logs', 'app.log')

CommandObject = CommandDIC.CommandExecutor()
# 创建日志目录如果不存在
if not os.path.exists('logs'):
    os.makedirs('logs')

# 配置日志记录
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,  # 设置日志记录级别
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志记录格式
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.FileHandler(log_file_path, encoding="utf-8", mode="a")


@app.route('/', methods=['GET'])
def main_route():
    print(os.path)
    return render_template('index.html')


@app.route('/loginon', methods=['GET'])
def loginon():
    return render_template('login.html')


@app.route('/login', methods=['GET'])
def login_in():
    username = request.args.get('user', '')
    password = request.args.get('pass', '')
    if username == Root_user and password == Root_password:
        return render_template('dashboard.html')
    else:
        return 'Wrong Name OR Password'


@app.route('/hitokoto', methods=['GET'])
def hitokoto():
    try:
        # 获取请求参数

        type_param = request.args.get('type', 'a')
        charset = request.args.get('charset', 'utf-8')
        encode = request.args.get('encode', 'json')

        # 验证type参数是否合法
        if type_param < 'a' or type_param > 'i':
            return jsonify({'status': 'error', 'message': 'Invalid type parameter'}), 400

        # 构建文件路径
        file_path = os.path.join('DATA', f'{type_param}.json')

        # 验证文件是否存在
        if not os.path.exists(file_path):
            return jsonify({'status': 'error', 'message': 'File not found'}), 404

        # 读取JSON文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 从JSON数据中随机选取一条
        if not data:
            return jsonify({'status': 'error', 'message': 'No data found in file'}), 404
        selected_item = random.choice(data)

        # 根据encode参数决定返回格式
        if encode == 'json':
            response = jsonify(selected_item)
        elif encode == 'text':
            response = Response(selected_item['hitokoto'], mimetype='text/plain')
        else:
            return jsonify({'status': 'error', 'message': 'Invalid encode parameter'}), 400

        # 设置字符编码
        response.headers['Content-Type'] += f'; charset={charset}'
        return response
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/update', methods=['GET'])
def update():
    try:
        # 获取请求参数
        version = request.args.get('version', '1.0.393')

        # 验证type参数是否合法
        F_url = f'https://cdn.jsdelivr.net/gh/hitokoto-osc/sentences-bundle@{version}/sentences/'
        logging.info('请保持服务器网络畅通,正在尝试同步hitokoto数据')
        logging.info(f'即将更新的版本:{version}')
        for i in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
            D_URL = F_url + i + '.json'
            data = requests.get(D_URL)
            path = f'./DATA/{i}.json'
            with open(path, 'w', encoding='utf-8') as file:
                file.write(data.text)
            logging.info(f'正在更新 {path} ,Please Wait...')
        logging.info(f'DONE! ')
        return 'DONE!'
    except Exception as e:
        logging.error('无法更新:' + str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/help', methods=['GET'])
def help():
    return render_template('Help.html')


@app.route('/fonts', methods=['GET'])
def get_font():
    name = request.args.get('name', 'Smple_UNDERTALE')
    if os.path.exists(f'./templates/fonts/{name}.woff'):
        return app.send_static_file(f'fonts/{name}.woff')
    elif os.path.exists(f'./templates/fonts/{name}.otf'):
        return app.send_static_file(f'fonts/{name}.otf')
    elif os.path.exists(f'./templates/fonts/{name}.ttf'):
        return app.send_static_file(f'fonts/{name}.ttf')


@app.route('/PrivacyStatement', methods=['GET'])
def PrivacyStatement_route():
    return render_template('Privacy_Statement.html')


@app.route('/logs', methods=['GET'])
def get_logs():
    just_log = request.args.get('justlog', '')
    just_status = request.args.get('juststatus', '')
    web_reques = request.args.get('isweb', '')
    try:
        log_path = os.path.join('logs', 'app.log')
        if not os.path.exists(log_path):
            return jsonify({'status': 'error', 'message': 'Log file not found'}), 404

        # 读取日志文件内容
        with open(log_path, 'r', encoding='GBK') as log_file:
            log_content = log_file.read()

        # 移除终端控制字符
        clean_log_content = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', log_content)

        # 将日志按行分割
        log_lines = clean_log_content.split('\n')
        filtered_logs = [line for line in log_lines if '/logs?justlog=true&isweb=true' not in line]
        if just_log == 'true':
            if web_reques == 'true':
                return '<br>'.join(filtered_logs)
            return "\n".join(filtered_logs)
        elif just_status == 'true':
            return 'success', 200
        else:
            return jsonify({'status': 'success', 'logs': log_lines}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/clearlog', methods=['GET'])
def clear_log():
    with open('./logs/app.log', 'w', encoding='GBK') as f:
        f.write('')
    logging.info('Clear_log_DONE!')
    return 'Done', 200


@app.route('/poweroff', methods=['GET'])
def power_off():
    logging.info('=====SERVER Will try off in 5s')
    time.sleep(4)
    logging.info('=====SERVER OFF')
    time.sleep(1)
    os.kill(os.getpid(), 0)


@app.route('/Serverinfo', methods=['GET'])
def Serverinfo():
    return jsonify(Get_mechine_info.get_all())


@app.route('/DashBoardData', methods=['get'])
def submit_data():
    data = request.args.get('command')
    CommandObject.execute_command(data)


def cache_command(name, func, help=''):
    global CommandObject
    logging.info(f'-----Command ADD\n{name}->{help}')
    CommandObject.add_command(name, func)


def output_log(log):
    logging.info(log)


def local_commands():
    def clear():
        requests.get(f'http://{IP}:{PORT}/clearlog')

    cache_command('clear', clear, 'Clear Your logs.')

    def update():
        requests.get(f'http://{IP}:{PORT}/update')

    cache_command('update', update, 'Update Your Server_hitokoto.')

    def show_neofetch():
        system_info = neofetch.get_system_info()
        result = neofetch.print_system_info(system_info, 'WEB_SHELL_By_Canf')
        return result

    cache_command('neofetch', show_neofetch, 'Try Type this,and enjoy')


def main():
    logo = LOGO.get_logo(1)
    neirong = logo + f'''


    ServerName: {server_name}
    Storge:
    HitokotoServer [{Storage.get_all_size()}]
    |-> Apps [{Storage._getFileSize('./Apps')}]
          |-> OtherApps[{Storage._getFileSize('./Apps/OtherApps')}]
          |-> perset[{Storage._getFileSize('./Apps/preset')}]
          |-> ServerApps[{Storage._getFileSize('./Apps/ServerApps')}]
    |-> theme [{Storage._getFileSize('./theme')}]
    |-> DATA [{Storage.get_data_size()}]
    |-> Logs [{Storage.get_log_size()}]
    |-> Setting[{Storage._getFileSize('./Setting')}]
    |-> System [{Storage.get_system_size()}]
          |-> images[{Storage._getFileSize('./templates/images')}]
          |-> js[{Storage._getFileSize('./templates/js')}]
          |-> music[{Storage._getFileSize('./templates/music')}]
          |-> video[{Storage._getFileSize('./templates/video')}]
    '''
    print(neirong)
    logging.info(neirong)
    logging.info('=====SERVER START')
    TOLOGO.img_RGBcolor_ascii('./images/logo/logo.png')
    print('Start Server...')
    print(f"IP:{IP}\nServerHost: http://{IP}:{PORT}")
    local_commands()


if __name__ == '__main__':
    main()
    app.run(host=IP, port=PORT, debug=True)
