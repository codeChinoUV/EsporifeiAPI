
RUN sudo -u postgres createdb espotifei
RUN sudo -u postgres psql -c "CREATE USER espotifeiapi WITH PASSWORD '123456';"
RUN sudo -u postgres psql -c "GRANT ALL PRIVELEGES ON DATABASE espotifei TO espotifeiapi;"
