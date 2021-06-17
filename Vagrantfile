# -*- mode: ruby -*-
# vi: set ft=ruby :

# Different VM images can be used by changing this variable, e.g. 'cdaf/WindowsServerCore'
if ENV['OVERRIDE_IMAGE']
  OVERRIDE_IMAGE = ENV['OVERRIDE_IMAGE']
else
  OVERRIDE_IMAGE = 'cdaf/WindowsServerStandard'
end

Vagrant.configure(2) do |allhosts|

  allhosts.vm.define 'build' do |build|
    build.vm.box = "#{OVERRIDE_IMAGE}"
    build.vm.provision 'shell', inline: 'Get-ScheduledTask -TaskName ServerManager | Disable-ScheduledTask -Verbose'

    build.vm.provision 'shell', path: '.\.cdaf\bootstrapAgent.ps1', args: 'C:\vagrant\cbe'
    build.vm.provision 'shell', inline: "& addPath.ps1 C:\\vagrant\\automation"

    # Oracle VirtualBox, relaxed configuration for Desktop environment
    build.vm.provider 'virtualbox' do |virtualbox, override|
      override.vm.network 'private_network', ip: '172.16.17.100'
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.100 build.mshome.net"
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.101 cbe.mshome.net"
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.102 test.mshome.net"
      override.vm.provision 'shell', inline: "cd /vagrant ; ci ; exit $LASTEXITCODE"
    end

    # Set environment variable VAGRANT_DEFAULT_PROVIDER to 'hyperv'
    build.vm.provider 'hyperv' do |hyperv, override|
      override.vm.hostname = 'build'
      override.vm.synced_folder ".", "/vagrant", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
      override.vm.provision 'shell', inline: "cd /vagrant ; ci ; exit $LASTEXITCODE"
    end
  end

  allhosts.vm.define 'cbe' do |cbe|
    cbe.vm.box = "#{OVERRIDE_IMAGE}"
    cbe.vm.hostname = 'cbe' # In Hyper-V this is automatically addressable from the host as cbe.mshome.net
    cbe.vm.provision 'shell', inline: 'Get-ScheduledTask -TaskName ServerManager | Disable-ScheduledTask -Verbose'

    # Generic provisioning, used for both in-situ and containers
    cbe.vm.provision 'shell', path: '.\.cdaf\imageBuild\bootstrapPython.ps1', args: 'c:\vagrant\cbe'

    # In-situ provisioning
    cbe.vm.provision 'shell', inline: '& mkdir.ps1 C:\\cbe $env:COMPUTERNAME\\vagrant'
    cbe.vm.provision 'shell', inline: '& base.ps1 "nssm"'
    cbe.vm.provision 'shell', inline: 'nssm install cbe python -u manage.py runserver 0.0.0.0:8000'
    cbe.vm.provision 'shell', inline: 'nssm set cbe AppDirectory C:\\cbe'
    cbe.vm.provision 'shell', inline: 'nssm set cbe AppStdout C:\\cbe\\cbe.log'
    cbe.vm.provision 'shell', inline: 'nssm set cbe AppStderr C:\\cbe\\cbe.log'
    cbe.vm.provision 'shell', inline: '& openFirewallPort.ps1 "8000"'

    # Oracle VirtualBox, cannot use 172.0.0.0/8 range, as that is allocated to Windows Container network
    cbe.vm.provider 'virtualbox' do |virtualbox, override|
      if ENV['SYNCED_FOLDER']
        override.vm.synced_folder "#{ENV['SYNCED_FOLDER']}", '/.provision'
      end
      override.vm.network 'private_network', ip: '172.16.17.101'
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.100 build.mshome.net"
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.101 cbe.mshome.net"
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.102 test.mshome.net"
      override.vm.provision 'shell', inline: 'cd /vagrant ; ./TasksLocal/delivery.bat VAGRANT.deploy ; exit $LASTEXITCODE'
    end

    # Microsoft Hyper-V does not support port forwarding: vagrant up target --provider hyperv
    cbe.vm.provider 'hyperv' do |hyperv, override|
      override.vm.synced_folder ".", "/vagrant", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
      if ENV['SYNCED_FOLDER']
        override.vm.synced_folder "#{ENV['SYNCED_FOLDER']}", "/.provision", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
      end
      override.vm.provision 'shell', inline: 'cd /vagrant ; ./TasksLocal/delivery.bat VAGRANT.deploy ; exit $LASTEXITCODE'
    end
  end

  allhosts.vm.define 'test' do |test|
    test.vm.box = "#{OVERRIDE_IMAGE}"
    test.vm.provision 'shell', inline: 'Get-ScheduledTask -TaskName ServerManager | Disable-ScheduledTask -Verbose'

    test.vm.provision 'shell', path: '.\compose\test\bootstrapTest.ps1'

    # Oracle VirtualBox, relaxed configuration for Desktop environment
    test.vm.provider 'virtualbox' do |virtualbox, override|
      override.vm.network 'private_network', ip: '172.16.17.102'
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.100 build.mshome.net"
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.101 cbe.mshome.net"
      override.vm.provision 'shell', inline: "& addHOSTS.ps1 172.16.17.102 test.mshome.net"
      override.vm.provision 'shell', inline: 'cd /vagrant ; ./TasksLocal/delivery.bat VAGRANT.test ; exit $LASTEXITCODE'
    end

    # Set environment variable VAGRANT_DEFAULT_PROVIDER to 'hyperv'
    test.vm.provider 'hyperv' do |hyperv, override|
      override.vm.hostname = 'test'
      override.vm.synced_folder ".", "/vagrant", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
      override.vm.provision 'shell', inline: 'cd /vagrant ; ./TasksLocal/delivery.bat VAGRANT.test ; exit $LASTEXITCODE'
    end
  end
end