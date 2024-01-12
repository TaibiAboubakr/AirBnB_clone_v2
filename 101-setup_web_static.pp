# site.pp

package { 'nginx':
  ensure => installed,
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => Package['nginx'],
}

file { '/etc/nginx/sites-available/default':
  ensure  => file,
  mode    => '0644',
  content => template('nginx/default.erb'),
  require => Service['nginx'],
  notify  => Service['nginx'],
}

file { [ '/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test' ]:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => template('web_static/index.html.erb'),
  require => File['/data/web_static/releases/test'],
}

file { '/data/web_static/releases/test/404.html':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => 'Ceci n\'est pas une page',
  require => File['/data/web_static/releases/test'],
}

file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test',
  require => File['/data/web_static/releases/test/index.html'],
}

# nginx/default.erb
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0644',
  content => '
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /data/web_static/releases/test/;
    index index.html;

    location /redirect_me {
        return 301 http://localhost/new_page;
    }

    error_page 404 /404.html;
    location = /404.html {
        internal;
    }

    location /hbnb_static/ {
      alias /data/web_static/current/;
    }

    location / {
      add_header X-Served-By {$hostname};
    }',
}
}
