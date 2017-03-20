# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

# If this environment variable is set, then the location defined will be used for media
# [Environment]::SetEnvironmentVariable('SYNCED_FOLDER', 'E:\.provision', 'Machine')
if ENV['SYNCED_FOLDER']
  provision = ENV['SYNCED_FOLDER']
else
  provision = '../.provision'
end

Vagrant.configure(2) do |config|
  
  config.vm.box = 'WindowsDocker'
  config.vm.boot_timeout = 1200
  config.vm.guest = "windows"
  config.vm.communicator = 'winrm'
  config.winrm.timeout = 120
  config.winrm.retry_limit = 10
  config.vm.provision 'shell', path: './automation/remote/capabilities.ps1'
    
  config.vm.provider 'virtualbox' do |virtualbox, override|
    virtualbox.gui = false
    override.vm.synced_folder "#{provision}", "/.provision"
    override.vm.network 'private_network', ip: '10.10.8.101'
    override.vm.network 'forwarded_port', guest: 3389, host: 13389 # Remote Desktop
    override.vm.network 'forwarded_port', guest: 5985, host: 15985 # WinRM HTTP
    override.vm.network 'forwarded_port', guest: 5986, host: 15986 # WinRM HTTPS
    override.vm.provision 'shell', path: './automation/provisioning/setenv.ps1', args: 'environmentDelivery VAGRANT Machine'
    override.vm.provision 'shell', path: './automation/provisioning/CDAF.ps1'
    override.vm.provision 'shell', path: './automation/provisioning/CDAF.ps1'
  end
end