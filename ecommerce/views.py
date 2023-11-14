from django.shortcuts import render


def base(requset):
    return render(requset, "base.html")
