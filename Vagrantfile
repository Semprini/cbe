r# -*- mode: ruby -*-
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

Vagrant.configure(2) do |config|
  config.vm.box = "#{vagrantBox}"
  config.vm.box_check_update = false
  config.vm.guest = :windows
  config.vm.communicator = 'winrm'
  config.vm.boot_timeout = 600 # 10 minutes
  config.winrm.timeout =   1800 # 30 minutes
  config.winrm.retry_limit = 10
  config.winrm.username = "vagrant" # Making defaults explicit
  config.winrm.password = "vagrant" # Making defaults explicit
  config.vm.graceful_halt_timeout = 180 # 3 minutes
  config.vm.provision 'shell', path: './automation-solution/bootstrapAgent.ps1'
  config.vm.provision 'shell', path: './automation/remote/capabilities.ps1'
    
  # Oracle VirtualBox, cannot use 172.0.0.0/8 range, as that is allocated to Windows Container network
  config.vm.provider 'virtualbox' do |virtualbox, override|
    virtualbox.gui = false
    virtualbox.memory = "#{vRAM}"
    virtualbox.cpus = "#{vCPU}"
    override.vm.synced_folder "#{synchedFolder}", '/.provision'
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
    hyperv.memory = "#{vRAM}"
    hyperv.cpus = "#{vCPU}"
    hyperv.ip_address_timeout = 240 # 4 minutes to report IP
    override.vm.synced_folder ".", "/vagrant", type: "smb", smb_host: "#{ENV['COMPUTERNAME']}", smb_username: "#{ENV['USER_NAME']}", smb_password: "#{ENV['USER_PASS']}"
    override.vm.provision 'shell', path: './automation/provisioning/setenv.ps1', args: 'environmentDelivery VAGRANT Machine'
    override.vm.provision 'shell', inline: 'dir c:\vagrant'
  end
end