
import sys
import pathlib
import shutil
import functools
from hashlib import md5
import json
import os
from time import time
from typing import Optional, Tuple
from urllib.parse import urlparse
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import io
import yaml
from email import encoders
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
import urllib

try:
    import jinja2
except ImportError:
    os.system(f'{sys.executable} -m pip install jinja2')
    import jinja2

default_encrypter = None
global_config = None
gist_token = None


proxy_config_file = os.path.join(os.path.expanduser("~"), '.libvmake', 'proxy')


def md5sum(str):
    m = md5()
    m.update(str.encode('utf-8'))
    return m.hexdigest()


class Encrypter(object):

    def __init__(self, key: str):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC

    def encrypt(self, text: str) -> bytes:
        _text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        length = 16
        count = len(_text)
        if count < length:
            add = (length - count)
            _text = _text + ('\0' * add).encode('utf-8')
        elif count > length:
            add = (length - (count % length))
            _text = _text + ('\0' * add).encode('utf-8')
        self.ciphertext = cryptor.encrypt(_text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text: bytes) -> str:
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return bytes.decode(plain_text).rstrip('\0')

def get_default_key()->str:
    _defaultKey = md5sum("2f7326ed-3182-4ea9-8b6f-872b491800c4")
    key_file = os.path.join(os.path.expanduser("~"), '.libvmake', 'default.key')
    os.makedirs(os.path.dirname(key_file), exist_ok=True)
    if not os.path.exists(key_file):
        key = input("int the default encrypt key: ").strip()
        with open(key_file, mode='w', encoding='utf-8') as f:
            _key = (key + _defaultKey)[0:32]
            f.write(_key)
            return _key
    else:
        with open(key_file, mode='r', encoding='utf-8') as f:
            _key = f.read().strip()
            if len(_key) != 32:
                raise Exception("invalid default key")
            return _key


def get_default_encrypter():
    global default_encrypter
    if default_encrypter is None:
        default_encrypter = Encrypter(get_default_key())
    return default_encrypter


def private(f):
    """标记函数为私有，仅适用于开发者本人的系统配置
    """
    @functools.wraps(f)
    def func(*args, **kwargs):
        return f(*args, **kwargs)
    return func


@private
def _get_gist_token():
    defaultEncrypter = get_default_encrypter()
    token_file = os.path.join(os.path.expanduser("~"), '.libvmake', 'auth', 'token')
    if not os.path.exists(token_file):
        while True:
            _token = input("Input the github gist token: ").strip()
            if _token is None or _token.strip() == '':
                print("error: invalid gist token, please reinput")
            try:
                global_config = _get_global_config(_token)
                if global_config is not None:
                    os.makedirs(os.path.dirname(token_file), exist_ok=True)
                    with open(token_file, 'wb') as f:
                        f.write(defaultEncrypter.encrypt(_token))
                    return _token
            except Exception as e:
                print(f"error: invalid gist token, please reinput: {e}")
    else:
        with open(token_file, 'rb') as f:
            token = defaultEncrypter.decrypt(f.read())
            return token


@private
def get_gist_token():
    global gist_token
    if gist_token is None:
        gist_token = _get_gist_token()
    return gist_token


@private
def get_gist_config(gist_token, gist_id, gist_filename) -> str:
    from .libvmake import get_github_gist
    str_client_config = get_github_gist(gist_token, gist_id, gist_filename)
    return str_client_config


@private
def _get_global_config(gist_token=None) -> dict:
    if gist_token is None:
        gist_token = get_gist_token()
        if gist_token is None:
            raise Exception('can not get valid gist token')
    from .settings import settings
    client_config = get_gist_config(gist_token, settings['gist_config']['gist_id'], settings['gist_config']['gist_filename'])
    stringIO = io.StringIO(client_config)
    return yaml.load(stringIO)['config']


@private
def get_global_config() -> dict:
    global global_config
    if global_config is None:
        gist_token = get_gist_token()
        global_config = _get_global_config(gist_token)
    return global_config


@private
def get_google_drive_config():
    return get_global_config()['service']['googledrive']


@private
def get_google_drive_token() -> dict:
    googledrive_config = get_google_drive_config()
    return json.loads(get_gist_config(gist_token, googledrive_config['gist_id'], googledrive_config['gist_file']))


@private
def get_ss_config():
    """get ss config from global config which store in gist

    Returns:
        dict: ss configuration, eg: {
            enabled
            host
            port
            password
            method
        }
    """
    return get_global_config()['proxy']['ss']


@private
def get_qiniu_config()->dict:
    """get qiniu config from global config which store in gist

    Returns:
        dict: qiniu configuration, eg: {
            access_key
            secret_key
            default_bucket
            default_domain
            default_schema
        }
    """ 
    return get_global_config()['service']['qiniu']


@private
def get_aliyun_config():
    """get aliyun config from global config which store in gist

    Returns:
        dict: aliyun configuration, eg: {
            access_key
            secret_key
        }
    """
    return get_global_config()['service']['aliyun']

def get_proxy_from_config() -> Tuple[Optional[str], Optional[list]]:
    curdir = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
    config_yml = os.path.join(curdir, 'config.yml')
    if os.path.exists(config_yml):
        _config = yaml.load(config_yml)
        config = _config.get("config")
        if config is not None and config.__contains__("proxy"):
            proxy = config.get('proxy') if config.get('proxy') is not None else (config.get('http_proxy') if config.get('http_proxy') is not None else config.get('https_proxy'))
            noproxy = config.get('noproxy', '')
            if noproxy is None:
                return proxy, []
            elif type(noproxy) == str:
                return proxy, [x.strip() for x in noproxy.split(",") if x.strip() != '']
            elif type(noproxy) == list:
                return proxy, noproxy
            else:
                raise Exception("invalid proxy config") 

    if os.path.exists(proxy_config_file):
        with open(proxy_config_file, 'r', encoding='utf-8') as f:
            config = json.loads(f.read())
            return config['proxy'], config.get('noproxy', [])
    else:
        proxy = input("Input the http proxy(empty for none proxy): ").strip()
        noproxy = input("Input the no proxy url (seperated by ','): ").strip()
        save_proxy(proxy, noproxy)
        return proxy, [x.strip() for x in noproxy.split(",") if x.strip() != ""]

def save_proxy(proxy: Optional[str], noproxy):
    if proxy is None:
        proxy = ""

    if noproxy is None:
        noproxy = []

    _noproxy = []

    if type(noproxy) == str:
        _noproxy = [x.strip() for x in noproxy.split(",") if x.strip() != ""]
    elif type(noproxy) == list:
        _noproxy = noproxy
        
    os.makedirs(os.path.dirname(proxy_config_file), exist_ok=True)
    with open(proxy_config_file, 'w', encoding='utf-8') as f:
        proxy_settings = {
            "proxy": proxy.strip(),
            "noproxy": _noproxy
        }
        print(f"save proxy settings to {proxy_config_file}: {proxy_settings}")
        f.write(json.dumps(proxy_settings))

def set_proxy_from_config():
    proxy, noproxy = get_proxy_from_config()
    set_proxy(proxy, noproxy)


def unset_proxy():
    try:
        del os.environ['HTTP_PROXY']
    except:
        pass
    try:
        del os.environ['HTTPS_PROXY']
    except:
        pass
    try:
        del os.environ['NO_PROXY']
    except:
        pass

def set_proxy(proxy: Optional[str], noproxy:Optional[list] = None) -> None:
    if proxy is None or proxy.strip() == "":
        proxy = ""
    else:
        try:
            urlparse(proxy)
        except:
            raise Exception('invalid proxy url')
    
    if proxy == "":
        unset_proxy()
    else:
        os.environ['HTTP_PROXY'] = proxy
        os.environ['HTTPS_PROXY'] = proxy
        _noproxy = [] if noproxy is None else noproxy
        os.environ["NO_PROXY"] = ",".join(_noproxy)


def send_mail(
        sender: str,
        smtp_server: str,
        smtp_server_port: int,
        smtp_username: str,
        smtp_password: str,
        receivers: list,
        title: str,
        content: str,
        content_type='plain',
        cc_emails: list = None,
        bcc_emails: list = None,
        attaches: dict = None) -> Optional[dict]:
    """[summary]

    Args:
        sender (str): sender's email address
        smtp_server (str): smtp server host
        smtp_server_port (int): smtp server port
        smtp_username (str): smtp server username
        smtp_password (str): smtp server password
        receivers (list): receivers' email address list
        title (str): email's title
        content (str): email's content 
        content_type (str, optional): the email's content type, maybe plain or html. Defaults to 'plain'.
        cc_emails (list, optional): cc email address. Defaults to None.
        bcc_emails (list, optional): bcc email address. Defaults to None.
        attaches (dict, optional): attach files, eg: {"custom_file": "file.txt"}. Defaults to None.

    Returns:
        dict: The address that failed to send and the reason, eg: { "three@three.org" : ( 550 ,"User unknown" ) }
    """

    to_addrs = receivers
    message = MIMEMultipart("alternative")
    message["Subject"] = title
    message["From"] = sender
    message["To"] = receivers
    if cc_emails is not None and len(cc_emails) > 0:
        message["Cc"] = ",".join(cc_emails)
        to_addrs.extend(cc_emails)
    if bcc_emails is not None and len(bcc_emails) > 0:
        message["Bcc"] = ",".join(bcc_emails)
        to_addrs.extend(bcc_emails)

    message.attach(MIMEText(content, content_type))

    if attaches is not None:
        for filename, attach in attaches.items():
            with open(attach, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

                # Encode file in ASCII characters to send by email
                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )
                message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_server_port, context=context) as server:
        # server.starttls(context=context)
        server.login(smtp_username, smtp_password)
        result = server.sendmail(sender, to_addrs, message.as_string())
        return result


# content_type: plain / html
# eg: send_mail({stmp_server, stmp_server_port, stmp_username, stmp_password, stmp_email}, "yuhuan@seadee.com.cn",
#   "<html><body><h3>消息</h3><br /><p>测试服务器出错, 请处理</p></body></html>",
#   content_type="html", cc_emails=['uforgetmenot@yuhuans.cn'],
#   bcc_emails=['yuhuan@seadee.com.cn'], attaches= {filename: file}
# )
def send_mail(smtp: dict, receiver_email, title:str, content: str, content_type='plain', 
        cc_emails: list=None, bcc_emails: list=None, attaches: dict = None):
        
    # print("send mail to :" + receiver_email)
    # print("title: " + title)
    # print("content: " + content)
    # print("content_type: " + content_type)
    # print("cc_emails:")
    # print(cc_emails)
    # print("bcc_emails:")
    # print(bcc_emails)
    # print("attaches:")
    # print(attaches)

    to_addrs = [receiver_email]
    message = MIMEMultipart("alternative")
    message["Subject"] = title
    message["From"] = smtp['stmp_email']
    message["To"] = receiver_email
    if cc_emails is not None and len(cc_emails) > 0 :
        message["Cc"] = ",".join(cc_emails)
        to_addrs.extend(cc_emails)
    if bcc_emails is not None and len(bcc_emails) > 0:
        message["Bcc"] = ",".join(bcc_emails)
        to_addrs.extend(bcc_emails)

    message.attach(MIMEText(content, content_type))

    if attaches is not None:
        for filename, attach in attaches.items():
            with open(attach, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

                # Encode file in ASCII characters to send by email
                encoders.encode_base64(part)

                # Add header as key/value pair to attachment part
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={filename}",
                )
                message.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp['smtp_server'], smtp['smtp_server_port'], context=context) as server:
        # server.starttls(context=context)
        server.login(smtp['smtp_username'], smtp['smtp_password'])
        result = server.sendmail(smtp['sender_email'], to_addrs, message.as_string())
        return result



def copy_template(src, dest, context, encoding="utf-8"):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(src, 'r', encoding=encoding) as f:
        jinja2.Template(f.read()).stream(
            context=context).dump(dest, encoding=encoding)
        return True


def copy_templates(src_dir, dest_dir, context, encoding="utf-8"):
    for root, _, files in os.walk(src_dir):
        for _file in files:
            file = os.path.join(root, _file)
            relative_file = pathlib.Path(file).relative_to(src_dir)
            dest_file = os.path.join(dest_dir, relative_file)
            copy_template(file, dest_file, context=context, encoding=encoding)


def copy_files(src_dir, dest_dir):
    for root, _, files in os.walk(src_dir):
        for _file in files:
            file = os.path.join(root, _file)
            relative_file = pathlib.Path(file).relative_to(src_dir)
            dest_file = os.path.join(dest_dir, relative_file)
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy(file, dest_file)
