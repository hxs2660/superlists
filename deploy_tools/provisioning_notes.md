1、配置用户账户
    sudo su
    useradd -m -s /bin/bash username #-m 家目录 -s 默认能使用bash
    usermod -a -G sudo username
    passwd username

2、配置新网站
    需要安装的包Required packages:
    sudo apt-get install nginx git python3 python3-pip openssh-server
    sudo pip3 install virtualenv

3、本地部署命令:
    fab deploy:host=username@sitename


4、配置Nginx虚拟主机 Nginx Virtual Host config

    sed "s/SITENAME/192.168.99.212/g" deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/192.168.99.212
    sudo ln -s ../sites-available/192.168.99.212 /etc/nginx/sites-enabled/192.168.99.212
    sudo service nginx reload

5、配置gunicorn Job:

    sed "s/SITENAME/192.168.99.212/g" deploy_tools/gunicorn-init.d-template.conf | sudo tee /etc/init.d/gunicorn-192.168.99.212 

    sudo chmod +x /etc/init.d/gunicorn-192.168.99.212
    sudo update-rc.d gunicorn-192.168.99.212 defaults


文件夹结构 Folder structure:

    假如有用户账户,家目录为 /home/username

    /home/username 
    └── sites    
        └── SITENAME   
        ├── database    
        ├── source    
        ├── static   
        └── virtualenv

