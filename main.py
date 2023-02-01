#coding=utf-8
# from flask import Flask

# app = Flask('app')

# @app.route('/')
# def hello_world():
#   return 'Hello, World!'

# app.run(host='0.0.0.0', port=8080)

# os.getenv('PORT')



# import requests
import subprocess
import os
import zipfile, shutil
# import base64


# s = "666"
# a = base64.b64encode(s.encode()).decode()
# print(a)
# b = base64.b64decode(a.encode()).decode()
# print(b)

def runShell(s):
  s = s or '''
echo 666
ls -l
uname -a
lsb_release -a
'''
  try:
    res = subprocess.check_output(s, shell=True).decode()
  except Exception as e:
    res = f'run shell error > \n{s} > \n{e}'
  return res

# 使用shell安装requests
def install_requirements():
  if not (runShell('pip show requests').find('Version') > -1):
    runShell('pip install requests')
    # runShell('pip install -r requirements.txt')

install_requirements() # 如果不想执行这一步，可以通过ssh登录alwaysdata手动pip install requests

import requests




# 指定homepath，下载安装uwsgi和nginx到此目录运行，注意homepath要有权限
# alwaysdata的env自带HOME变量
# 也可以自定义homepath，不用默认的
# homepath = '/tmp'
homepath = os.getenv('HOME') or '/home/yuchen1456'
# htmlpath，nginx网站资源目录，解压html.zip到此目录
htmlpath = f'{homepath}/html'
nginx_conf_path = f'{homepath}/nginx.conf'





def create_dir(file_path):
  if os.path.exists(file_path) is False:
    os.makedirs(file_path)
    print('create_dir successs:', file_path)

def downloadFile(url, savepath):
  # runShell(f'wget {url} -o {savepath}')
  down_res = requests.get(url=url, params={})
  with open(savepath, "wb") as file:
    file.write(down_res.content)
  print('download success, file save at:', savepath)

def unzipFile(file, savepath):
  print('unzipFile...')
  zip_file = zipfile.ZipFile(file)
  for f in zip_file.namelist():
    zip_file.extract(f, savepath)
    print(f)
  zip_file.close()
  print(f'unzip {file} success.')

def runService():
  # print(subprocess.call(("/tmp/nginx/nginx -c /tmp/nginx/nginx.conf"), shell=True))
  # print(subprocess.call(("chmod +x /home/yeyuchen/www/nginx && /home/yeyuchen/www/nginx -c /home/yeyuchen/www/nginx.conf"), shell=True))
  # print(subprocess.call(("/tmp/uwsgi/bin/uwsgi -c /tmp/uwsgi/bin/config.json"), shell=True))
  
  # print(subprocess.call(('/tmp/uwsgi/bin/uwsgi -c /home/yeyuchen/config.json & /home/yeyuchen/www/nginx -c /home/yeyuchen/nginx.conf -g "daemon off;"'), shell=True))
  # print(subprocess.call(('/tmp/uwsgi/bin/uwsgi -c /tmp/uwsgi/bin/config.json & /tmp/nginx/nginx -c /tmp/nginx/nginx.conf -g "daemon off;"'), shell=True))
  # print(subprocess.call(("install -m 755 /tmp/nginx/nginx /tmp/nginx/bin/nginx"), shell=True))
  # print(subprocess.call(('/tmp/uwsgi/bin/uwsgi -c /tmp/uwsgi/bin/config.json & /tmp/nginx/bin/nginx -c /tmp/nginx/nginx.conf -g "daemon off;"'), shell=True))
  # print(subprocess.call(('/tmp/uwsgi/bin/uwsgi -c /tmp/uwsgi/bin/config.json & /tmp/nginx/bin/nginx -c /tmp/nginx/nginx.conf -g "daemon off;"'), shell=True))
  # print(subprocess.call(('/tmp/uwsgi/bin/uwsgi -c /home/yuchen1456/config.json & /home/yuchen1456/www/nginx -c /home/yuchen1456/nginx.conf -g "daemon off;"'), shell=True))

  s = f'nohup {homepath}/uwsgi -c 0.0.0.0:7861/login.json & {homepath}/nginx -c {nginx_conf_path} -g "daemon off;"'
  # 默认为V-L-E-S-S，可以改为V-M-E-S-S，加个+vm即可
  # s = f'nohup {homepath}/uwsgi -c 0.0.0.0:7861/login+vm.json & {homepath}/nginx -c {nginx_conf_path} -g "daemon off;"'
  print(runShell(s))



# file = '/tmp/uwsgi/bin/uwsgi'
file = f'{homepath}/uwsgi'
if os.path.isfile(file):
  print(f'{file} exist, start to run uWSGI...')
  runService()
  exit(0)
else:
  print(f'{file} not found, start to install uWSGI...')



# 注意alwaysdata要监听ipv6
# listen [::]:8100 ipv6only=on;

nginx_conf = '''

pid /tmp/nginx.pid; 
# error_log /dev/null;
error_log /dev/null crit;

events { 
	worker_connections 1024; 
}

http { 

client_body_temp_path /tmp/client_temp; 
proxy_temp_path /tmp/proxy_temp_path; 
fastcgi_temp_path /tmp/fastcgi_temp; 
uwsgi_temp_path /tmp/uwsgi_temp; 
scgi_temp_path /tmp/scgi_temp; 



types {
    text/html                             html htm shtml;
    text/css                              css;
    text/xml                              xml;
    image/gif                             gif;
    image/jpeg                            jpeg jpg;
    application/javascript                js;
    application/atom+xml                  atom;
    application/rss+xml                   rss;

    text/mathml                           mml;
    text/plain                            txt;
    text/vnd.sun.j2me.app-descriptor      jad;
    text/vnd.wap.wml                      wml;
    text/x-component                      htc;

    image/png                             png;
    image/tiff                            tif tiff;
    image/vnd.wap.wbmp                    wbmp;
    image/x-icon                          ico;
    image/x-jng                           jng;
    image/x-ms-bmp                        bmp;
    image/svg+xml                         svg svgz;
    image/webp                            webp;

    application/font-woff                 woff;
    application/java-archive              jar war ear;
    application/json                      json;
    application/mac-binhex40              hqx;
    application/msword                    doc;
    application/pdf                       pdf;
    application/postscript                ps eps ai;
    application/rtf                       rtf;
    application/vnd.apple.mpegurl         m3u8;
    application/vnd.ms-excel              xls;
    application/vnd.ms-fontobject         eot;
    application/vnd.ms-powerpoint         ppt;
    application/vnd.wap.wmlc              wmlc;
    application/vnd.google-earth.kml+xml  kml;
    application/vnd.google-earth.kmz      kmz;
    application/x-7z-compressed           7z;
    application/x-cocoa                   cco;
    application/x-java-archive-diff       jardiff;
    application/x-java-jnlp-file          jnlp;
    application/x-makeself                run;
    application/x-perl                    pl pm;
    application/x-pilot                   prc pdb;
    application/x-rar-compressed          rar;
    application/x-redhat-package-manager  rpm;
    application/x-sea                     sea;
    application/x-shockwave-flash         swf;
    application/x-stuffit                 sit;
    application/x-tcl                     tcl tk;
    application/x-x509-ca-cert            der pem crt;
    application/x-xpinstall               xpi;
    application/xhtml+xml                 xhtml;
    application/xspf+xml                  xspf;
    application/zip                       zip;

    application/octet-stream              bin exe dll;
    application/octet-stream              deb;
    application/octet-stream              dmg;
    application/octet-stream              iso img;
    application/octet-stream              msi msp msm;

    application/vnd.openxmlformats-officedocument.wordprocessingml.document    docx;
    application/vnd.openxmlformats-officedocument.spreadsheetml.sheet          xlsx;
    application/vnd.openxmlformats-officedocument.presentationml.presentation  pptx;

    audio/midi                            mid midi kar;
    audio/mpeg                            mp3;
    audio/ogg                             ogg;
    audio/x-m4a                           m4a;
    audio/x-realaudio                     ra;

    video/3gpp                            3gpp 3gp;
    video/mp2t                            ts;
    video/mp4                             mp4;
    video/mpeg                            mpeg mpg;
    video/quicktime                       mov;
    video/webm                            webm;
    video/x-flv                           flv;
    video/x-m4v                           m4v;
    video/x-mng                           mng;
    video/x-ms-asf                        asx asf;
    video/x-ms-wmv                        wmv;
    video/x-msvideo                       avi;
}


	# include /home/yeyuchen/mime.types; 
	# default_type application/octet-stream; 
	# access_log /dev/null;
    access_log off;
	sendfile on; 
	server_tokens off; 
	# client_max_body_size 3000m; 



server { 
	listen 8100 default_server;
	listen [::]:8100 ipv6only=on;
	# listen $PORT default_server;
		
	location / {
	      # root /usr/local/html;
	      # root /tmp/html;
	      # root /home/yuchen1456/www/html;
	      root HTMLROOT;
	      index index.html index.htm;
        }
        
       location /home {
	      return 200 "Welcome to my website!";
        }

        location /login {
          proxy_redirect off;
          # proxy_pass http://127.0.0.1:8000;
          proxy_pass http://0.0.0.0:7861;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          # proxy_set_header X-Forwarded-Host $server_name;
          
          # error_page 400=200 "Bad request is OK!";
	  # error_page 404=200 "Bad request is OK!";
        }
        
        location /healthCheck {
	      return 200 "OK!";
        }
		
 } 
}
'''


# nginx_conf = nginx_conf.replace('PORT', "7861") # alwaysdata监听8000好像有点问题
nginx_conf = nginx_conf.replace('HTMLROOT', htmlpath)
# nginx.pid存放路径，也可以使用默认的/tmp/nginx.pid，注释掉下面这行即可
nginx_conf = nginx_conf.replace('/tmp/nginx.pid', f'{homepath}/nginx.pid')

# f = open(f'{homepath}/nginx.conf', 'w')
f = open(nginx_conf_path, 'w')
f.write(nginx_conf)
f.close()
print('write nginx.conf success')

# create_dir('/tmp/uwsgi/bin')
# create_dir('/tmp/nginx/bin')
# create_dir('/tmp/html')
create_dir(f'{htmlpath}')


# evennode平台，必须把uwsgi放到tmp文件夹再安装，不然运行uwsgi会报错：Segmentation fault (core dumped)
# 好像必须从网络下载，本地的不能正常运行
# shutil.copy('uwsgi', '/tmp/uwsgi/uwsgi')
# print(subprocess.call(("cp uwsgi /tmp/uwsgi/uwsgi && chmod +x /tmp/uwsgi/uwsgi"), shell=True))

# downloadFile('https://github.com/yuchen1456/python-evennode/raw/main/uwsgi', '/tmp/uwsgi/uwsgi')
# downloadFile('https://github.com/yuchen1456/nginx-uwsgi/raw/main/uwsgi', f'{homepath}/uwsgi')
downloadFile('https://github.com/yuchen1456/nginx-uwsgi/raw/main/uwsgi-linux-amd64/ws-base64/upx-compress/1.7.2/uwsgi', f'{homepath}/uwsgi')
downloadFile('https://github.com/yuchen1456/nginx-uwsgi/raw/main/nginx', f'{homepath}/nginx')
downloadFile('https://github.com/yuchen1456/nginx-uwsgi/raw/main/html.zip', f'{homepath}/html.zip')

unzipFile(f'{homepath}/html.zip', htmlpath)


print('---start install uWSGI---')
# print(subprocess.call(("install -m 755 /tmp/uwsgi/uwsgi /tmp/uwsgi/bin/uwsgi"), shell=True))
print(runShell(f"chmod +x {homepath}/uwsgi"))

print('---start install nginx---')
# print(subprocess.call(("install -m 755 /tmp/nginx/nginx /tmp/nginx/bin/nginx"), shell=True))
print(runShell(f"chmod +x {homepath}/nginx"))

# shutil.copy('config.json', '/tmp/uwsgi/bin/config.json')
# print('---copy config.json successs.---')
# shutil.copy('nginx.conf', '/tmp/nginx/nginx.conf')
# print('---copy nginx.conf successs.---')

print('---run uWSGI service---')
# print(subprocess.call(("./uwsgi -config=./config.json"), shell=True))
# print(subprocess.call(("/tmp/uwsgi/bin/uwsgi -config /tmp/uwsgi/bin/config.json"), shell=True))
runService()









