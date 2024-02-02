def pereklyuchatel(geocoder_request):
   geocoder_request = (geocoder_request + 1) % 3
   return geocoder_request