# Configuration for the database server
class config {
  import 'unix_user'
  import './credentials.pp'

  # Configure groups and users
  group {'db':
    ensure => present;
  'postgres':
    ensure => present;
  'frontend':
    ensure => present;
  }

  # Administrators
  unix_user {['raymond', 'ian', 'hcrute', 'aj']:
    groups  => ['db', 'frontend','sudo'],
    require => Group['db', 'frontend'],
  }

  # Create application users
  unix_user {'landingzone':
    groups   => ['db', 'postgres'],
    #password => $config::landingzone_pw,
    require  => Group['db'],
  }
  unix_user {'seadapi':
    groups  => ['db', 'postgres'],
    #password => $config::seadapi_pw,
    require => Group['db'],
  }
  unix_user {'seadssite':
    groups	=> ['frontend'],
    #password => $config::frontend_pw,
    require	=> Group['frontend'],
  }

  # Set up application directories
  file {'/home/seadapi/api':
    ensure  => directory,
    owner   => 'seadapi',
    group   => 'seadapi',
    require => User['seadapi'],
  }
  file {'/home/landingzone/landingzone':
    ensure  => directory,
    owner   => 'landingzone',
    group   => 'landingzone',
    require => User['landingzone'],
  }
  file {'/home/seadssite/seadssite':
	ensure	=> directory,
	owner	=> 'seadssite',
	group	=> 'seadssite',
	require => User['seadssite'],
  }

  # Set up init scripts
  file {'/etc/init.d/seadapi':
    source  => 'puppet:///modules/config/init.seadapi',
    mode    => '0774',
    owner   => 'root',
    group   => 'root',
    require => User['seadapi'],
  }
  service {'seadapi':
    ensure  => running,
    enable  => true,
    require => File['/etc/init.d/seadapi'],
  }
  file {'/etc/init.d/landingzone':
    source  => 'puppet:///modules/config/init.landingzone',
    mode    => '0774',
    owner   => 'root',
    group   => 'root',
    require => User['landingzone'],
  }
  service {'landingzone':
    ensure  => running,
    enable  => true,
    require => File['/etc/init.d/landingzone'],
  }
  file {'/etc/init.d/seadssite':
    source  => 'puppet:///modules/config/init.seadssite',
    mode    => '0774',
    owner   => 'root',
    group   => 'root',
    require => User['seadssite'],
  }
  service {'seadssite':
    ensure  => running,
    enable  => true,
    require => File['/etc/init.d/seadssite'],
  }

  #installs virtual environment for django
  if ! defined(Package['python-pip']) {
    package {'python-pip':
      ensure  => installed,
    }
  }

  #installs python with postgres interface
  package {['python3-pip',
  'libpq-dev']:
    ensure => present,
    before => Exec['psycopg2'],
  }

  exec {'psycopg2':
    command => 'pip3 install psycopg2',
  }
}
