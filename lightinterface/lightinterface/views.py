

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from yeelight import Bulb
import json
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

bulbs_ips = ["192.168.1.179", "192.168.1.175", "192.168.1.174", "192.168.1.173", "192.168.1.172"]


def turn_on_lights(request):
    for ip in bulbs_ips:
        bulb = Bulb(ip)
        bulb.turn_on()
    return JsonResponse({'status': 'all on'})

def turn_off_lights(request):
    for ip in bulbs_ips:
        bulb = Bulb(ip)
        bulb.turn_off()
    return JsonResponse({'status': 'all off'})

@csrf_exempt
def set_color(request):
    data = json.loads(request.body)
    color = data['color']

    # Convert the hex color to RGB
    r, g, b = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    responses = {}
    for ip in bulbs_ips:
        try:
            bulb = Bulb(ip)
            bulb.set_rgb(r, g, b)
            responses[ip] = 'success'
        except Exception as e:
            responses[ip] = str(e)
    
    return JsonResponse(responses)