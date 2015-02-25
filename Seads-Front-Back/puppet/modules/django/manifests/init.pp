# Install django and requirements for seadssite user
class django {
  # Install python-pip package
  if ! defined (Package['python-pip']) {
    package {'python-pip':
      ensure  => installed,
      require => User['seadssite'],
    }
  }

  # May need to fix, this is a laundrylist of python reqs for the frontend
  exec {'frontend-requirements':
    command => 'pip install virtualenv && \
pip install Django && pip install Flask && pip install Flask-Admin && \
pip install Flask-HTTPAuth && pip install Flask-SQLAlchemy && \
pip install Jinja2 && pip install MarkupSafe && pip install SQLAlchemy && \
pip install WTForms && pip install Werkzeug && pip install Django && \
pip install django-bootstrap3 && pip install docopt && pip install itsdangerous && \
pip install python-dateutil && pip install sandman && pip install six && \
pip install wsgiref',
    require => Package['python-pip'],
  }
}
