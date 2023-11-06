

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from yeelight import Bulb
import json
from django.shortcuts import redirect, render



from django.views.decorators.http import require_POST
from asgiref.sync import sync_to_async  # If needed to use synchronous code in async
import asyncio
from yeelight.aio import AsyncBulb

bulbs_ips = ["192.168.1.179", "192.168.1.175", "192.168.1.174", "192.168.1.173", "192.168.1.172"]

def home(request):
    return render(request, 'home.html', {})

def bulb_statuses_json(request):
    bulb_statuses = []
    for ip in bulbs_ips:
        try:
            bulb = Bulb(ip)
            properties = bulb.get_properties()
            properties['readable'] = {
                'ip': ip,
                'power': properties['power'],
                'bright': properties['bright'],
                'rgb': properties['rgb'] if 'rgb' in properties else 'N/A',
            }
            bulb_statuses.append(properties['readable'])
        except Exception as e:
            bulb_statuses.append({'ip': ip, 'error': str(e)})
    
    return JsonResponse({'bulbs': bulb_statuses})



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
            bulb.set_brightness(100)
            responses[ip] = 'success'
        except Exception as e:
            responses[ip] = str(e)
    
    return JsonResponse(responses)

@csrf_exempt  # Temporarily disable CSRF protection for this view
@require_POST  # Ensure that this view can only be called with POST method
async def set_brightness(request):
        responses = {}
        for ip in bulbs_ips:
         try:
            bulb = Bulb(ip)
            bulb.set_brightness(100)
            responses[ip] = 'success'
         except Exception as e:
            responses[ip] = str(e)

            return JsonResponse(responses)
