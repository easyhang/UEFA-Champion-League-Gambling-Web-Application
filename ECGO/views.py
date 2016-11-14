from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
import Gamble.models as g
import Gamble.forms as gg
# Create your views here.




def game(request):
    a = g.team.objects.filter(teamname="Juventus")
    return render(request, 'luck.html', {'doggy': a[0]})
    #a = g.team.objects.all()
    #return HttpResponse(a)


def index(request):
    if request.method == 'POST':

        form = gg.AddForm(request.POST)

        if form.is_valid():
            a = form.cleaned_data['a']
            print g.team.objects.all()
            for i in range(len(g.team.objects.all())):
                if str(a) in str(g.team.objects.all()[i]):
                    return HttpResponse(g.team.objects.all()[i])

    else:
        form = gg.AddForm()
    return render(request, 'index.html', {'form': form})