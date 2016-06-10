配置新网站
需要安装的包Required packages:

    nginx
    Python 3
    Git
    pip
    virtualenv

eg, on Ubuntu:

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

配置Nginx虚拟主机 Nginx Virtual Host config

    参考 nginx.template.conf
    把 SITENAME 替换成所需的域名, 例如, staging.my-domain.com

gunicorn Job:

    参考 gunicorn-init.d.template.conf
    把 SITENAME 替换成所需的域名, staging.my-domain.com

文件夹结构 Folder structure:

    假如有用户账户,家目录为 /home/username

    /home/username 
    └── sites    
        └── SITENAME   
        ├── database    
        ├── source    
        ├── static   
         └── virtualenv
