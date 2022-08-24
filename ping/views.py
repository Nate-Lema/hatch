from django.shortcuts import render
from django.http import JsonResponse

def pingView(request):
	return JsonResponse({"success": True})
