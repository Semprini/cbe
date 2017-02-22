# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

# Zip Package creation requires PowerShell v3 or above and .NET 4.5 or above.

Vagrant.configure(2) do |allhosts|

  allhosts.vm.define 'target' do |target|
    target.vm.box = 'mwrock/Windows2016'
    target.vm.communicator = 'winrm'
    target.vm.provision 'shell', path: './automation/remote/capabilities.ps1'
    # Oracle VirtualBox, relaxed configuration for Desktop environment
    target.vm.provision 'shell', path: './automation/provisioning/mkdir.ps1', args: 'C:\deploy'
    target.vm.provider 'virtualbox' do |virtualbox, override|
      virtualbox.gui = false
      override.vm.network 'private_network', ip: '172.16.17.103'
      override.vm.network 'forwarded_port', guest: 3389, host: 33389 # Remote Desktop
      override.vm.network 'forwarded_port', guest: 5985, host: 35985 # WinRM HTTP
      override.vm.network 'forwarded_port', guest: 5986, host: 33986 # WinRM HTTPS
      override.vm.network 'forwarded_port', guest:   80, host: 30080
      override.vm.network 'forwarded_port', guest:  443, host: 30443
      override.vm.provision 'shell', path: './automation/provisioning/CredSSP.ps1', args: 'client'
      override.vm.provision 'shell', path: './automation/provisioning/CredSSP.ps1', args: 'server'
    end
  end

  allhosts.vm.define 'build' do |build|
    build.vm.box = 'mwrock/Windows2016'
    build.vm.communicator = 'winrm'
    build.vm.provision 'shell', path: './automation/remote/capabilities.ps1'
    # Oracle VirtualBox, relaxed configuration for Desktop environment
    build.vm.provider 'virtualbox' do |virtualbox, override|
      virtualbox.gui = false
      override.vm.network 'private_network', ip: '172.16.17.101'
      override.vm.network 'forwarded_port', guest: 3389, host: 13389 # Remote Desktop
      override.vm.network 'forwarded_port', guest: 5985, host: 15985 # WinRM HTTP
      override.vm.network 'forwarded_port', guest: 5986, host: 15986 # WinRM HTTPS
      override.vm.provision 'shell', path: './automation/provisioning/addHOSTS.ps1', args: '172.16.17.103 target.sky.net'
      override.vm.provision 'shell', path: './automation/provisioning/trustedHosts.ps1', args: 'target.sky.net'
      override.vm.provision 'shell', path: './automation/provisioning/setenv.ps1', args: 'environmentDelivery VAGRANT Machine'
      override.vm.provision 'shell', path: './automation/provisioning/CDAF_Desktop_Certificate.ps1'
      override.vm.provision 'shell', path: './automation/provisioning/CredSSP.ps1', args: 'server'
      override.vm.provision 'shell', path: './automation/provisioning/CredSSP.ps1', args: 'client'
      override.vm.provision 'shell', path: './automation/provisioning/CDAF.ps1'
    end
  end

end