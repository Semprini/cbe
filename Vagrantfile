# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

Vagrant.configure(2) do |config|
  
  # If this environment variable is set, then the location defined will be used for media
  # [Environment]::SetEnvironmentVariable('SYNCED_FOLDER', 'E:\.provision', 'Machine')
  if ENV['SYNCED_FOLDER']
    provision = ENV['SYNCED_FOLDER']
  else
    provision = '../.provision'
  end

  # Performance multiplier, i.e increase depending on resources available to host, example of host with more that 4GB RAM available and 4 Virtual CPUs
  # [Environment]::SetEnvironmentVariable('PERFORMANCE_MULTIPLIER', '4', 'Machine')
  if ENV['PERFORMANCE_MULTIPLIER']
    multiplier = ENV['PERFORMANCE_MULTIPLIER'].to_i
  else
    multiplier = 1
  end
  ram = 1024 * multiplier
    
  config.vm.box = 'cdaf/WindowsServerDocker'
  config.vm.box_check_update = false
  config.vm.guest = :windows
  config.vm.communicator = 'winrm'
  config.vm.boot_timeout = 600 # 10 minutes
  config.winrm.timeout =   1800 # 30 minutes
  config.winrm.retry_limit = 10
  config.winrm.username = "vagrant" # Making defaults explicit
  config.winrm.password = "vagrant" # Making defaults explicit
  config.vm.graceful_halt_timeout = 180 # 3 minutes
  config.vm.provision 'shell', path: './automation/remote/capabilities.ps1'
    
  # Oracle VirtualBox, cannot use 172.0.0.0/8 range, as that is allocated to Windows Container network
  config.vm.provider 'virtualbox' do |virtualbox, override|
    virtualbox.gui = false
    virtualbox.memory = "#{ram}"
    virtualbox.cpus = "#{multiplier}"
    override.vm.synced_folder "#{provision}", '/.provision'
    override.vm.network 'private_network', ip: '10.10.8.101'
    override.vm.network 'forwarded_port', guest: 3389, host: 13389 # Remote Desktop
    override.vm.network 'forwarded_port', guest: 5985, host: 15985 # WinRM HTTP
    override.vm.network 'forwarded_port', guest: 5986, host: 15986 # WinRM HTTPS
    override.vm.network 'forwarded_port', guest: 8079, host: 8079 # WinRM HTTPS
    override.vm.network 'forwarded_port', guest: 8000, host: 8000 # WinRM HTTPS
    override.vm.provision 'shell', path: './automation/provisioning/setenv.ps1', args: 'environmentDelivery VAGRANT Machine'
    override.vm.provision 'shell', path: './automation/provisioning/CDAF.ps1'
    override.vm.provision 'shell', path: './automation/provisioning/CDAF.ps1' # Execute twice to verify rebuild works
  end
  
  # Microsoft Hyper-V does not support NAT or setting hostname: vagrant up target --provider hyperv
  config.vm.provider 'hyperv' do |hyperv, override|
    hyperv.memory = "#{ram}"
    hyperv.cpus = "#{multiplier}"
    hyperv.ip_address_timeout = 240 # 4 minutes to report IP
    override.vm.synced_folder ".", "/vagrant", type: "smb", smb_host: "#{ENV['COMPUTERNAME']}", smb_username: "#{ENV['USER_NAME']}", smb_password: "#{ENV['USER_PASS']}"
    override.vm.provision 'shell', path: './automation/provisioning/setenv.ps1', args: 'environmentDelivery VAGRANT Machine'
    override.vm.provision 'shell', inline: 'dir c:\vagrant'
  end
end