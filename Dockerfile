FROM python:3.6-stretch

WORKDIR /cryptowatch

ADD . /cryptowatch/

ENV NGINX_VERSION=1.13.7-1~stretch NJS_VERSION=1.13.7.0.1.15-1~stretch NGINX_MAX_UPLOAD=0 LISTEN_PORT=80 UWSGI_INI=/cryptowatch/inf/uwsgi_app.ini

RUN set -x && \
    curl -sS "https://dl.yarnpkg.com/debian/pubkey.gpg" | apt-key add - && \
    curl -sL "https://deb.nodesource.com/setup_8.x" | bash - && \
    apt-get update -y && \
    apt-get install --no-install-recommends --no-install-suggests -y gnupg1 && \
	NGINX_GPGKEY=573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62; \
	found=''; \
	for server in \
		hkp://keyserver.ubuntu.com:80 \
		hkp://p80.pool.sks-keyservers.net:80 \
		pgp.mit.edu \
	; do \
		echo "Fetching GPG key $NGINX_GPGKEY from $server"; \
		apt-key adv --keyserver "$server" --keyserver-options timeout=10 --recv-keys "$NGINX_GPGKEY" && found=yes && break; \
    done; \
    apt-get remove --purge --auto-remove -y gnupg1 && rm -rf /var/lib/apt/lists/* && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    echo "deb http://nginx.org/packages/mainline/debian/ stretch nginx" >> /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get install -y --allow-unauthenticated \
    nodejs \
    yarn \
    bash \
    supervisor \
    nginx=${NGINX_VERSION} \
	nginx-module-xslt=${NGINX_VERSION} \
	nginx-module-geoip=${NGINX_VERSION} \
	nginx-module-image-filter=${NGINX_VERSION} \
	nginx-module-njs=${NJS_VERSION} && \
    pip install uwsgi && \
    mkdir -p /etc/uwsgi/ && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log && \
    echo "daemon off;" >> /etc/nginx/nginx.conf && \
    rm /etc/nginx/conf.d/default.conf && \
    mv /cryptowatch/inf/nginx.conf /etc/nginx/conf.d/ && \
    mv /cryptowatch/inf/uwsgi.ini /etc/uwsgi/ && \
    mv /cryptowatch/inf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf && \
    chmod +x /cryptowatch/inf/entrypoint.sh && \
    cd /cryptowatch && \
    bash bin/build.sh && \
    rm -rf node_modules && \
    apt-get purge -y nodejs yarn && \
    rm -rf /etc/apt/sources.list.d/yarn.list /etc/apt/sources.list.d/nodesource.list && \
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    apt-get clean -y

EXPOSE 80

ENTRYPOINT ["/cryptowatch/inf/entrypoint.sh"]
CMD ["/usr/bin/supervisord"]
