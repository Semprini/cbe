# -*- mode: ruby -*-
# vi: set ft=ruby :

# Different VM images can be used by changing this variable, e.g. 'cdaf/WindowsServerCore'
if ENV['OVERRIDE_IMAGE']
  OVERRIDE_IMAGE = ENV['OVERRIDE_IMAGE']
else
  OVERRIDE_IMAGE = 'cdaf/WindowsServerStandard'
end

# If this environment variable is set, RAM and CPU allocations for virtual machines are increase by this factor, so must be an integer
if ENV['SCALE_FACTOR']
  scale = ENV['SCALE_FACTOR'].to_i
else
  scale = 1
end
vRAM = 1024 * scale
vCPU = scale

Vagrant.configure(2) do |allhosts|

  allhosts.vm.define 'cbe' do |cbe|
    cbe.vm.box = "#{OVERRIDE_IMAGE}"
    cbe.vm.hostname = 'cbe' # In Hyper-V this is automatically addressable from the host as cbe.mshome.net
    cbe.vm.provision 'shell', inline: 'Get-ScheduledTask -TaskName ServerManager | Disable-ScheduledTask -Verbose'

    # Generic provisioning, used for both in-situ and containers
    cbe.vm.provision 'shell', path: '.\.cdaf\imageBuild\bootstrapPython.ps1', args: 'c:\vagrant\cbe'

    # In-situ provisioning
    cbe.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\mkdir.ps1 C:\cbe $env:COMPUTERNAME\vagrant'
    cbe.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\base.ps1 "nssm"'
    cbe.vm.provision 'shell', inline: 'nssm install cbe python manage.py runserver 0.0.0.0:8000'
    cbe.vm.provision 'shell', inline: 'nssm set cbe AppDirectory C:\cbe'
    cbe.vm.provision 'shell', inline: 'nssm set cbe AppStdout C:\\cbe\\cbe.log'
    cbe.vm.provision 'shell', inline: 'nssm set cbe AppStderr C:\\cbe\\cbe.log'

    # Oracle VirtualBox, cannot use 172.0.0.0/8 range, as that is allocated to Windows Container network
    cbe.vm.provider 'virtualbox' do |virtualbox, override|
      virtualbox.gui = false
      virtualbox.memory = "#{vRAM}"
      virtualbox.cpus = "#{vCPU}"
      if ENV['SYNCED_FOLDER']
        override.vm.synced_folder "#{ENV['SYNCED_FOLDER']}", '/.provision'
      end
      override.vm.network 'private_network', ip: '172.16.17.90'
      override.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\addHOSTS.ps1 172.16.17.90 cbe.mshome.net'
    end
    
    # Microsoft Hyper-V does not support port forwarding: vagrant up target --provider hyperv
    cbe.vm.provider 'hyperv' do |hyperv, override|
      hyperv.memory = "#{vRAM}"
      hyperv.cpus = "#{vCPU}"
      override.vm.synced_folder ".", "/vagrant", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
      if ENV['SYNCED_FOLDER']
        override.vm.synced_folder "#{ENV['SYNCED_FOLDER']}", "/.provision", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
      end
    end
  end

  allhosts.vm.define 'build' do |build|
    build.vm.box = "#{OVERRIDE_IMAGE}"
    build.vm.provision 'shell', inline: 'Get-ScheduledTask -TaskName ServerManager | Disable-ScheduledTask -Verbose'

    build.vm.provision 'shell', path: './.cdaf/bootstrapAgent.ps1', args: 'C:\vagrant\cbe'

    # Vagrant specific for WinRM
    build.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\CredSSP.ps1 client'
    build.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\trustedHosts.ps1 *'
    build.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\setenv.ps1 CDAF_DELIVERY VAGRANT Machine'
    build.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\setenv.ps1 CDAF_PS_USERNAME vagrant'
    build.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\setenv.ps1 CDAF_PS_USERPASS vagrant'

    # Oracle VirtualBox, relaxed configuration for Desktop environment
    build.vm.provider 'virtualbox' do |virtualbox, override|
      virtualbox.gui = false
      virtualbox.memory = "#{vRAM}"
      virtualbox.cpus = "#{vCPU}"
      override.vm.network 'private_network', ip: '172.16.17.100'
      override.vm.provision 'shell', inline: '& $env:CDAF_AUTOMATION_ROOT\provisioning\addHOSTS.ps1 172.16.17.90 cbe.mshome.net'
      override.vm.provision 'shell', inline: 'cd C:\vagrant ; & $env:CDAF_AUTOMATION_ROOT\cdEmulate', privileged: false
    end

    # Set environment variable VAGRANT_DEFAULT_PROVIDER to 'hyperv'
    build.vm.provider 'hyperv' do |hyperv, override|
      hyperv.memory = "#{vRAM}"
      hyperv.cpus = "#{vCPU}"
      override.vm.hostname = 'build'
      override.vm.synced_folder ".", "/vagrant", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
      override.vm.provision 'shell', inline: 'cd C:\vagrant ; & $env:CDAF_AUTOMATION_ROOT\cdEmulate', privileged: false
    end
  end

end