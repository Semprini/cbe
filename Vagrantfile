# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.

# SMB credentials are those for the user executing vagrant commands, if domain user, use @ format
# [Environment]::SetEnvironmentVariable('VAGRANT_SMB_USER', 'username', 'User')
# [Environment]::SetEnvironmentVariable('VAGRANT_SMB_PASS', 'p4ssWord!', 'User')

# Different VM images can be used by changing this variable
# $env:OVERRIDE_IMAGE = 'cdaf/WindowsServerCore'
if ENV['OVERRIDE_IMAGE']
  vagrantBox = ENV['OVERRIDE_IMAGE']
else
  vagrantBox = 'cdaf/WindowsServerStandard'
end

# If this environment variable is set, RAM and CPU allocations for virtual machines are increase by this factor, so must be an integer
# [Environment]::SetEnvironmentVariable('SCALE_FACTOR', '2', 'Machine')
if ENV['SCALE_FACTOR']
  scale = ENV['SCALE_FACTOR'].to_i
else
  scale = 1
end
vRAM = 1024 * scale
vCPU = scale

# If this environment variable is set, then the location defined will be used for media
# [Environment]::SetEnvironmentVariable('SYNCED_FOLDER', 'E:\.provision', 'Machine')
if ENV['SYNCED_FOLDER']
  synchedFolder = ENV['SYNCED_FOLDER']
else
  synchedFolder = '../.provision'
end

Vagrant.configure(2) do |cbe|
  cbe.vm.box = "#{vagrantBox}"
  cbe.vm.provision 'shell', inline: 'Get-ScheduledTask -TaskName ServerManager | Disable-ScheduledTask -Verbose'
  cbe.vm.hostname = 'cbe' # In Hyper-V this is automatically addressable from the host as cbe.mshome.net
  cbe.vm.provision 'shell', path: './.cdaf/bootstrap.ps1'

  # Oracle VirtualBox, cannot use 172.0.0.0/8 range, as that is allocated to Windows Container network
  cbe.vm.provider 'virtualbox' do |virtualbox, override|
    virtualbox.gui = false
    virtualbox.memory = "#{vRAM}"
    virtualbox.cpus = "#{vCPU}"
    override.vm.synced_folder "#{synchedFolder}", '/.provision'
    override.vm.network 'private_network', ip: '10.10.8.101'
    override.vm.network 'forwarded_port', guest: 8000, host: 8000, auto_correct: true
    override.vm.provision 'shell', inline: 'cd c:/vagrant ; & $env:CDAF_AUTOMATION_ROOT/provisioning/addHOSTS.ps1 10.10.8.101 cbe.mshome.net'
    override.vm.provision 'shell', inline: 'cd c:/vagrant ; & $env:CDAF_AUTOMATION_ROOT/provisioning/CDAF.ps1', privileged: false
    override.vm.provision 'shell', inline: 'cd c:/vagrant ; & $env:CDAF_AUTOMATION_ROOT/provisioning/CDAF.ps1', privileged: false # Execute twice to verify rebuild works
  end
  
  # Microsoft Hyper-V does not support port forwarding: vagrant up target --provider hyperv
  cbe.vm.provider 'hyperv' do |hyperv, override|
    hyperv.memory = "#{vRAM}"
    hyperv.cpus = "#{vCPU}"
    override.vm.synced_folder ".", "/vagrant", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
    override.vm.synced_folder "#{synchedFolder}", "/.provision", type: "smb", smb_username: "#{ENV['VAGRANT_SMB_USER']}", smb_password: "#{ENV['VAGRANT_SMB_PASS']}"
    override.vm.provision 'shell', inline: 'cd c:/vagrant ; & $env:CDAF_AUTOMATION_ROOT/provisioning/CDAF.ps1', privileged: false
    override.vm.provision 'shell', inline: 'cd c:/vagrant ; & $env:CDAF_AUTOMATION_ROOT/provisioning/CDAF.ps1', privileged: false # Execute twice to verify rebuild works
  end
end