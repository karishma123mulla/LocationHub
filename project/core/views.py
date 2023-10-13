from django.shortcuts import render
from core.models import LocationHub
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializer import T_Location_Serializer


@csrf_exempt
@api_view(['POST'])
def add_location(request):
    """
    API Endpoint for add location 
    """
    try:
        location_name=request.data.get('location_name', None)
        latitude=request.data.get('latitude',None)
        longitude=request.data.get('longitude',None)

        location_obj=LocationHub.objects.create(
            location_name=location_name,
            latitude=latitude,
            longitude=longitude
        )
        print(location_obj)
        return Response(
                {
                    "message": "Location created successfully."},
                    status=status.HTTP_200_OK,
                )
    except Exception as e:
        print(e)
        return Response(
            {
                "message": "Something went wrong Please try again later!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def weather_map_view(request):
    # Fetch all geolocations from the database
    try:
        geolocations = LocationHub.objects.all()
        print("geolocations",geolocations)
        
        # Initialize a list to store weather data for each geolocation
        weather_data = []

        # Fetch weather data for each geolocation and add it to the weather_data list
        for location in geolocations:
            location_name=location.location_name
            latitude = location.latitude
            longitude = location.longitude
            data = fetch_weather_data(latitude, longitude)  #function call
            
            if data:
                print("inside if")
                weather_data.append({
                    'location': location_name,
                    'longitude':longitude,
                    'latitude':latitude,
                    'temperature': data['temperature'],
                    'humidity': data['humidity'],
                })
        print(weather_data)

        return render(request, 'index.html', {'location_data': weather_data})
        
    except Exception as e:
        print(e)


def fetch_weather_data(latitude, longitude):
    print(latitude,longitude)
    headers = {'User-Agent': 'fetch_weather_data/1.0 (karishmapathan1327@gmail.com)'}
    base_url =  f'https://api.weather.gov/points/{latitude},{longitude}'
    # base_url =  'https://api.weather.gov/points/39.7456,-97.0892'
    response = requests.get(base_url, headers=headers)
    print(response)
    if response.status_code == 200:
        data = response.json()
        # Extract temperature and humidity data from the JSON response
        gridx = data['properties']['gridX']
        gridy = data['properties']['gridY']
        print("x",gridx)
        print("y",gridy)
        forecast_url =  f'https://api.weather.gov/gridpoints/TOP/{gridx},{gridy}/forecast'
        new_response = requests.get(forecast_url, headers=headers)
        print("new",new_response)
        if new_response.status_code == 200:
            new_data = new_response.json()
            # print("new data",new_data)
            temperature = new_data["properties"]["periods"][0]["temperature"]
            humidity = new_data["properties"]["periods"][0]["relativeHumidity"]["value"]
            print("temperature",temperature)
            print("humidity",humidity)
            return {'temperature': temperature, 'humidity': humidity}
        else:
            return None
    else:
        return None





@csrf_exempt
@api_view(['PUT'])
def update_location(request):
    """
    API Endpoint for updating location
    """
    try:

        location_id = request.data.get('id', None) 
        if not location_id:
            return Response({"message": "Please enter correct location_id."},status=status.HTTP_403_FORBIDDEN)
        
        location_name=request.data.get('location_name', None)
        latitude=request.data.get('latitude',None)
        longitude=request.data.get('longitude',None)

        location_obj = LocationHub.objects.filter(id = location_id)
        if not location_obj.exists():
            return Response({"message": "Location does not exists."},status=status.HTTP_404_NOT_FOUND)
            
        location_obj = location_obj.first()
            
        if location_name:
            location_obj.location_name = location_name

        if latitude:
            location_obj.latitude = latitude

        if longitude:
            location_obj.longitude=longitude

        location_obj.save()



        return Response(
                {
                    "message": "Location updated successfully."},
                    status=status.HTTP_200_OK,
                )
    except Exception as e:
        print(e)
        return Response(
            {
                "message": "Something went wrong Please try again later!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )




@csrf_exempt
@api_view(['DELETE'])
def deactivate_location(request):
    """
    API Endpoint for deactivating location
    """
    try:

        location_id = request.GET.get('id', None) 
        if not location_id:
            return Response({"message": "Please enter correct location_id."},status=status.HTTP_403_FORBIDDEN)
        
        location_obj = LocationHub.objects.filter(id = location_id)
        if not location_obj.exists():
            return Response({"message": "Location does not exists."},status=status.HTTP_404_NOT_FOUND)
            
        location_obj = location_obj.first()

        print(location_obj)

        # location_obj.status = "Inactive"
        # location_obj.save()

        location_obj.delete()



        return Response(
                {
                    "message": "Location deactivated successfully."},
                    status=status.HTTP_200_OK,
                )
    except Exception as e:
        print(e)
        return Response(
            {
                "message": "Something went wrong Please try again later!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )




@csrf_exempt
@api_view(['GET'])
def location_list(request):
    """
    API Endpoint for fetching location list 
    """
   
    try:
        location_obj = LocationHub.objects.all().exclude(status="Inactive")
        
        if not location_obj.exists():
            return Response(
            {
                "message": "Locations not found!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        location_list = T_Location_Serializer(location_obj, many=True)
        return Response({"location_list":location_list.data},status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response(
            {
                "message": "Something went wrong Please try again later!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

