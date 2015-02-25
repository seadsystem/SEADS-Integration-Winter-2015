Exec { path => ['/usr/local/sbin', '/usr/local/bin', '/usr/sbin', '/usr/bin', '/sbin', '/bin'] }

include 'config'
include 'postgres'
include 'go'
include 'django'
include 'deploy'

Class['config']
  -> Class['postgres']
  -> Class['go']
  -> Class['django']
  -> Class['deploy']
