from django.db import models

from cbe.information_technology.models import Process, Component, ProcessFramework
from cbe.project.models import Project

def importapps(line):    
    appindex = 7
    for index, column in enumerate(line):
        if column == 'APPS':
            appindex = index
            break
            
    apps = []
    for column in line[appindex:]:
        name = column.strip('\n')#.replace(' ','_').replace('/','')
        app, created = Component.objects.get_or_create(name=name)
        apps.append( app )
    return (appindex,apps)

    
PROJECTINDEX = 5    
def importprojects(appindex,line):
    projects = []
    for column in line[PROJECTINDEX:appindex]:
        project, created = Project.objects.get_or_create(name=column)
        if not created:
            project.components.clear()
            project.processes.clear()
        projects.append(project)
    return projects
    
    
def reset(frameworkname):
    framework = ProcessFramework.objects.get(name=frameworkname)
    Process.objects.filter(framework=framework).delete()
    Component.objects.all().delete()
    Project.objects.all().delete()

    
processes = {}
def importprocess(framework, appindex, apps, projects, line):

    l = line[1].count('.')
    if line[1][-1]!="0":
        l+=1
    process, created = Process.objects.get_or_create(framework=framework,id=int(line[0]), hierarchy_id=line[1], level=l,name=line[4], friendly_name=line[3] )
            
    processes[line[1]] = process
    if len( line[1] ) > 2:
        pid = line[1][:-2]
        if pid in processes.keys():
            process.parent=processes[pid]
            process.save()
        elif pid+".0" in processes.keys() and pid+".0" != line[1]:
            process.parent=processes[pid+".0"]
            process.save()

    print( "Process: %s"%process )
    for index,column in enumerate(line[appindex:]):
        if column.lower()=="y":
            apps[index-appindex].processes.add( process )
            print( "    App: %d - %s"%(index-appindex,apps[index-appindex] ) )

    for index,column in enumerate(line[PROJECTINDEX:appindex]):
        if column.lower()=="y":
            projects[index].processes.add( process )
            projects[index].components.add(*process.components.all())
            print( "    Project: %d - %s"%(index,projects[index] ) )
        else:
            projects[index].processes.remove( process )            
            
                
def importtsv(frameworkname, filename):
    framework, created = ProcessFramework.objects.get_or_create(name=frameworkname)
    with open( filename ) as f:
        csv = f.readlines()
        
        appindex, apps=importapps(csv[1].split("\t"))
        projects=importprojects(appindex,csv[1].split("\t"))
        for line in csv[2:]:
            importprocess(framework, appindex, apps, projects, line.split("\t"))