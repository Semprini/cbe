# -*- mode: ruby -*-
# vi: set ft=ruby :

#> vagrant plugin install vagrant-reload
require 'vagrant-reload'

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

# Zip Package creation requires PowerShell v3 or above and .NET 4.5 or above.

Vagrant.configure(2) do |allhosts|

  allhosts.vm.define 'host' do |host|
    host.vm.provision 'shell', path: './automation/remote/capabilities.ps1'
    host.vm.provision 'shell', path: './automation/provisioning/mkdir.ps1', args: 'C:\deploy'
    host.vm.provision 'shell', path: './automation/provisioning/mkdir.ps1', args: 'C:\deploy'
    host.vm.provision 'shell', path: './automation/provisioning/applyWindowsUpdates.ps1'
    host.vm.provision :reload
    host.vm.provision 'shell', path: './automation/provisioning/installDocker.ps1'
    host.vm.provision 'shell', path: './automation/provisioning/applyWindowsUpdates.ps1'
    host.vm.provision :reload
    
    host.vm.provider 'virtualbox' do |virtualbox, override|
      override.vm.box = 'mwrock/Windows2016'
      override.vm.boot_timeout = 600
      override.vm.communicator = 'winrm'
      virtualbox.gui = false
      override.vm.network 'private_network', ip: '172.16.17.101'
      override.vm.network 'forwarded_port', guest: 3389, host: 13389 # Remote Desktop
      override.vm.network 'forwarded_port', guest: 5985, host: 15985 # WinRM HTTP
      override.vm.network 'forwarded_port', guest: 5986, host: 15986 # WinRM HTTPS
      override.vm.provision 'shell', path: './automation/provisioning/setenv.ps1', args: 'environmentDelivery VAGRANT Machine'
      override.vm.provision 'shell', path: './automation/provisioning/CredSSP.ps1', args: 'server'
      override.vm.provision 'shell', path: './automation/provisioning/CredSSP.ps1', args: 'client'
      override.vm.provision 'shell', path: './automation/provisioning/CDAF.ps1'
      override.vm.provision 'shell', path: './automation/provisioning/CDAF.ps1'
    end
  end

end