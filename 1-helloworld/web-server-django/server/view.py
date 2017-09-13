from django.http import HttpResponse


cmd = '0'

def write(req):
    global cmd
    cmd = req.GET['cmd']
    return HttpResponse(cmd)

def getcmd(req):
    return HttpResponse(cmd)


