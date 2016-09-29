from django.shortcuts import render
from information.forms import ContactForm

# Create your views here.


def contact_page(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            form.send_email()
            return render(request, 'information/success.html')
    return render(request, 'information/contact.html', {'form': form})
