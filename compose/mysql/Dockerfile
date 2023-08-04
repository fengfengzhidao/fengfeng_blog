FROM mysql:5.7

WORKDIR /opt
#RUN echo "character-set-server=utf8" >> /etc/mysql/mysql.conf.d/mysqld.cnf
#RUN service mysqld restart

COPY blog.sql /opt
COPY set.sh /opt
#RUN chmod +x /opt/set.sh
#RUN mysql -uroot -proot fengfeng_blog123 < /opt/blog.sql
# docker run --name mq -p 3307:3306 -e MYSQL_ROOT_PASSWORD=root -v ./compose/mysql/my.cnf:/etc/my.cnf  -itd mq
#ENTRYPOINT ["sh", "/opt/set.sh"]
# docker exec -it mq sh /opt/set.sh