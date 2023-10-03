import os
from django.http import HttpResponse
from .resources.test2 import run
import threading
from  .resources.face_recogn import face_regn
from django.shortcuts import render
from .forms import ImageUploadForm
global thread
facestop = False
# myproject/myapp/views.py


def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            image = form.cleaned_data['image']
            handle_uploaded_image(name, image)
            path = 'home/resources/faces/representations_vggface.pkl'
            if os.path.isfile(path):
                os.remove(path)
            return render(request, 'upload_success.html')
    else:
        form = ImageUploadForm()
    return render(request, 'image_upload.html', {'form': form})

def handle_uploaded_image(name, image):
    file_name, file_extension = os.path.splitext(image.name)
    new_file_name = name + file_extension
    with open('home/resources/faces/' + new_file_name, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

def index(request):
    executor = ProgramExecutor()
    executor.stop()
    # if thread and thread.is_alive():
    #     # Terminate the thread
    #     thread.join()
    #     thread = None
    # thread = None
    return render(request, 'index.html')

class ProgramExecutor:
    def __init__(self):
        self.thread = None
        self.should_stop = False

    def start(self):
        if self.thread is None or not self.thread.is_alive():
            self.should_stop = False
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
            return True
        return False

    def stop(self):
        self.should_stop = True

    def _run(self):
        run()  # Run the `run()` function

def start(request):
    if ProgramExecutor().start():
        # return HttpResponse('Running the program')
        return render(request, 'running.html')
    else:
        return HttpResponse('Program already running')
def faceregn(request):
    thread  = threading.Thread(target=face_regn)
    thread.start()
    return render(request, 'running.html')
# def stop(request):
#     executor = ProgramExecutor()
#     executor.stop()
#     if executor.thread and executor.thread.is_alive():
#         executor.thread.join()
#     # return HttpResponse('Program stopped')
#     return render(request, 'index.html')
