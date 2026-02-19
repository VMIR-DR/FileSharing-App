import os
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import File


def Selectfile(request):
    return request.FILES.get('file')


def Checkfile(uploaded):
    if not uploaded:
        return False, 'No file provided.'
    
    name = uploaded.name
    ext = os.path.splitext(name)[1].lower()
    
    # (دینک دودحم دیتساوخ رگا) دنوسپ یسررب لاثم:
    # allowed_ext = {'.jpg', '.png', '.pdf', '.txt'}
    # if ext not in allowed_ext:
    #     return False, 'File type not allowed.'
    
    # هزادنا یسررب (زاین تروص رد ؛لاعفریغ uncomment دینک):
    # max_size = 50 * 1024 * 1024  # 50 MB
    # if uploaded.size > max_size:
    #     return False, 'File too large.'
    
    return True, ''


@require_POST
def Savefile(request):
    uploaded = Selectfile(request)
    ok, msg = Checkfile(uploaded)
    
    if not ok:
        return JsonResponse({'ok': False, 'error': msg})
    
    title = request.POST.get('title', '')
    file_name = uploaded.name
    fmt = file_name.split('.')[-1] if '.' in file_name else ''
    
    instance = File(
        format=fmt,
        file_name=file_name,
        file_address=uploaded,
        file_size=uploaded.size,
        title=title
    )
    instance.save()
    
    return JsonResponse({'ok': True, 'url': instance.file_address.url, 'id': instance.id})


def Downloadfile(request, pk):
    obj = get_object_or_404(File, pk=pk)
    file_path = obj.file_address.path
    
    if not os.path.exists(file_path):
        raise Http404('File not found on disk')
    
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=obj.file_name)


@require_POST
def Deletefile(request, pk):
    obj = get_object_or_404(File, pk=pk)
    
    try:
        obj.file_address.delete(save=False)
    except Exception:
        pass
    
    obj.delete()
    return JsonResponse({'ok': True})


def Showlines(request):
    objs = File.objects.all().order_by('-created_at')
    data = []
    
    for o in objs:
        data.append({
            'id': o.id,
            'title': o.title,
            'file_name': o.file_name,
            'url': o.file_address.url,
            'size': o.file_size,
            'format': o.format,
        })
    
    return JsonResponse({'files': data})


def home(request):
    return render(request, 'home.html')


def upload_page(request):
    return render(request, 'uploadpage.html')


def download_page(request):
    return render(request, 'downloadpage.html')
