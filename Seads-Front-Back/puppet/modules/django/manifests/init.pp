# Install django and requirements for seadssite user
class django {
  # Install python-pip package
  package {'python-pip':
    ensure  => installed,
    require => User['seadssite'],
  }

  # Ensure go directory exists for landingzone user
  file {'gopath-dir':
    ensure  => directory,
    path    => '/home/landingzone/go',
    require => User['landingzone'],
  }

  # Install go pq bulk library
  exec {'go-pq':
    command => 'env GOPATH=/home/landingzone/go go get github.com/olt/libpq',
    require => Package['golang'],
  }
}

  #may need to fix, this is a laundrylist of reqs for frontend
  exec {'frontend-requirements':
    command => 'pip install virtualenv',
    command => 'pip install Django',
    command => 'pip install Flask',
    command => 'pip install Flask-Admin',
    command => 'pip install Flask-HTTPAuth',
    command => 'pip install Flask-SQLAlchemy',
    command => 'pip install Jinja2',
    command => 'pip install MarkupSafe',
    command => 'pip install SQLAlchemy',
    command => 'pip install WTForms',
    command => 'pip install Werkzeug',
    command => 'pip install Django',
    command => 'pip install django-bootstrap3',
    command => 'pip install docopt',
    command => 'pip install itsdangerous',
    command => 'pip install python-dateutil',
    command => 'pip install sandman',
    command => 'pip install six',
    command => 'pip install wsgiref',
  }
