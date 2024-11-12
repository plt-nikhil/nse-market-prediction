from django.urls import reverse
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import SectorSerializer
import json
import datetime
import os
from rest_framework import generics
from django.shortcuts import render
import json
import requests
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .serializers import GainersMoversSerializer, GainersDetailsSerializer, LoserDetailsSerializer, IndexSerializer, ScreenerCMOTSSerializer, IndexHeatmapResponseSerializer,  StockSectorDataSerializer, GetAllStcokSerializer, GetAllStockDetailSerializer, ProfitAndLossSerializer, BalanceSheetSerializer, QuaterlySerializer, HoldingSerializer


def coming_soon(request):
    return render(request, 'coming_soon.html')


class GainersMoversView(APIView):
    def get(self, request):
            url = 'https://portal.tradebrains.in/api/index/NIFTY/movers/'
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an exception for HTTP errors
                data = response.json()

                # Validate and serialize the data
                serializer = GainersMoversSerializer(data=data)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            except requests.RequestException as e:
                return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
class GainersView(APIView):
    def get(self, request, index):
        page = request.query_params.get('page', '1')
        per_page = request.query_params.get('per_page', '25000')
        by = request.query_params.get('by', 'change')
        ascending = request.query_params.get('ascending', 'false')
        
        url = f'https://portal.tradebrains.in/api/index/{index}/movers/gainers'
        params = {
            'page': page,
            'per_page': per_page,
            'by': by,
            'ascending': ascending
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            if 'results' not in data:
                data = {'results': [data]}
            
            # Validate and serialize the data
            serializer = GainersDetailsSerializer(data=data['results'], many=True)
            if serializer.is_valid():
                return Response({
                    'count': len(serializer.data),
                    'next': None,
                    'previous': None,
                    'results': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
class LosersView(APIView):
    def get(self, request, index):
        page = request.query_params.get('page', '1')
        per_page = request.query_params.get('per_page', '25000')
        by = request.query_params.get('by', 'change')
        ascending = request.query_params.get('ascending', 'false')
        
        url = f'https://portal.tradebrains.in/api/index/{index}/movers/losers'
        params = {
            'page': page,
            'per_page': per_page,
            'by': by,
            'ascending': ascending
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if 'results' not in data:
                data = {'results': [data]}
            
            # Validate and serialize the data
            serializer = LoserDetailsSerializer(data=data['results'], many=True)
            if serializer.is_valid():
                return Response({
                    'count': len(serializer.data),
                    'next': None,
                    'previous': None,
                    'results': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
       
class IndexListView(APIView):
    def get(self, request):
        url = 'https://portal.tradebrains.in/api/index/all'
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()

            # Filter out empty dictionaries and dictionaries with validation errors
            filtered_data = [item for item in data if item and (not item.get('symbol') or len(item['symbol']) <= 10)]
            
            # Validate and serialize the filtered data
            serializer = IndexSerializer(data=filtered_data, many=True, context={'request': request})
            serializer.is_valid(raise_exception=True)  # Raise exception if serialization fails

            return Response(serializer.data, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({'error': 'Error fetching data from external API'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ScreenerCMOTSView(APIView):
    def get(self, request, page):
        per_page = 25
            
        url = f'https://portal.tradebrains.in/api/screener-cmots/?page={page}&per_page={per_page}'
        payload = {"allFilters":[{"values":[0,2500000],"particular":"mcap","operator":"&"}],"selectedColumns":["mcap","pe","returns_1y","prev_close","dividend_yield"],"offset":0,"sortBy":"mcap","sortOrder":"DESC","industries":[],"indices":[],"sectors":[]}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            serializer = ScreenerCMOTSSerializer(data=data.get('results', []), many=True)
            serializer.is_valid()  # Perform validation (optional)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class IndexHeatmapView(APIView):
    def get(self, request, index):
        page = request.query_params.get('page', 1)
        per_page = request.query_params.get('per_page', 5000)
        filter_value = request.query_params.get('filter', '1D')  # Default to '1D' if not provided
        
        # Validate the filter value
        valid_filters = ['1D', '5D', '1Y', '5Y']
        if filter_value not in valid_filters:
            return Response({'error': 'Invalid filter value. Must be one of: 1D, 5D, 1Y, 5Y'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Define the URL for the external API
        url = f'https://portal.tradebrains.in/api/stocks/heatmap/{index}/'
        
        # Set up the query parameters
        params = {
            'page': page,
            'per_page': per_page,
            'filter': filter_value
        }

        try:
            # Send GET request to the external API with the parameters
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for non-2xx responses

            data = response.json()
            
            # Serialize the data using HeatmapResponseSerializer
            serializer = IndexHeatmapResponseSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


# ************************************************
# Get Sectore Name All


class SectorListView(APIView):
    def get(self, request):
        url = 'https://portal.tradebrains.in/api/company/sector-list/'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            print("Received data:", data)  # Add this line to debug

            # Validate and serialize the data
            serializer = SectorSerializer(data=data, many=True, context={'request': request})
            serializer.is_valid(raise_exception=True)  # Raise exception if serialization fails

            return Response(serializer.data, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            return Response({'error': 'Error fetching data from external API'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
# ************************************************

# Get All Stcok Name using Sector Vise
class StockSectoreDataView(generics.ListAPIView):

    serializer_class = StockSectorDataSerializer
    base_url = 'http://127.0.0.1:8000/api/stock/sector/'  # Your custom base URL

    def get_base_url(self):
        # Get the absolute URI for the current request
        absolute_url = self.request.build_absolute_uri()

        # Split the URL into segments
        segments = absolute_url.split('/')

        # Remove the last segment if it matches 'agro-chemicals'
        if segments[-2] == self.kwargs.get('name'):
            base_url = '/'.join(segments[:-2])
        else:
            base_url = absolute_url.rstrip('/')

        return base_url

    def get_absolute_url(self):
        return self.get_base_url() + reverse('your-url-name')

    def get_queryset(self):
        name = self.kwargs.get('name')  # Assuming 'name' is passed as a URL parameter
        page = self.request.query_params.get('page', 1)
        per_page = self.request.query_params.get('per_page', 15)
        
        url = f'https://portal.tradebrains.in/api/company/sector-data/{name}/'
        params = {'page': page, 'per_page': per_page}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            count = data['count']
            next_page = data['next']
            previous_page = data['previous']
            results = data['results']
            
            # Customize next and previous URLs
            if next_page:
                next_page = next_page.replace('https://portal.tradebrains.in/api/company/sector-data', self.get_base_url())
            if previous_page:
                previous_page = previous_page.replace('https://portal.tradebrains.in/api/company/sector-data', self.get_base_url())
            
            return {
                'count': count,
                'next': next_page,
                'previous': previous_page,
                'results': results
            }
        
        return {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)
    
# ====================================================================
#  Get All Stcok details And Create Slug All Stock

class AllStockNameView(APIView):
    def get(self, request):
        # per_page = 25
            
        url = f'https://portal.tradebrains.in/api/screener-cmots/?per_page=25000'
        payload = {"allFilters":[{"values":[0,2500000],"particular":"mcap","operator":"&"}],"selectedColumns":["mcap","pe","returns_1y","prev_close","dividend_yield"],"offset":0,"sortBy":"mcap","sortOrder":"DESC","industries":[],"indices":[],"sectors":[]}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            a = response.json()['results']

            d = []
            for i in a:
                if i['symbol'] == 0:
                    # print(i)
                    if i['scripcode'] == 0.0:
                        pass
                    else:
                        d.append({"slug":str(i['scripcode']).split('.')[0],"sector_name":i['sector_name'],"Company_name":i['short_name'],"industry_name":i['industry_name']})
                else:
                    d.append({"slug":i['symbol'],"sector_name":i['sector_name'],"Company_name":i['short_name'],"industry_name":i['industry_name']})

            # serializer = GetAllStcokSerializer(data=d, many=True)
            serializer = GetAllStcokSerializer(data=d, many=True, context={'request': request})
            serializer.is_valid()  # Perform validation (optional)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
# =======================================================
# Get All Stock Details Page 
class StockDetailsView(APIView):
    def get(self, request, index):

        
        # Define the URL for the external API
        
        url = f'https://portal.tradebrains.in/api/stock/{index}/'
        # Set up the query parameters

        try:
            # Send GET request to the external API with the parameters
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses

            data = response.json()
            # Serialize the data using HeatmapResponseSerializer
            serializer = GetAllStockDetailSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
# ======================================================================
# Get All Stock Heatmap 

class StockHeatmapView(APIView):
    def get(self, request, index):

        
        # Define the URL for the external API
        
        url = f'https://portal.tradebrains.in/api/company/stock/heatmap/{index}/'
        # Set up the query parameters

        try:
            # Send GET request to the external API with the parameters
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses

            data = response.json()
            # Serialize the data using HeatmapResponseSerializer
            return Response(data, status=status.HTTP_200_OK)
  
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
# ===========================================================
# Get Historical data

class StockHistoricalView(APIView):
    def get(self, request, index):

        
        # Define the URL for the external API
        
        url = f'https://portal.tradebrains.in/api/prices/historical-prices/{index}/?type=daily'
        # Set up the query parameters

        try:
            # Send GET request to the external API with the parameters
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses

            data = response.json()
            # Serialize the data using HeatmapResponseSerializer
            return Response(data, status=status.HTTP_200_OK)
  
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


# =========================================================================================
class ExchangeHolidayView(APIView):
    def get(self, request):

       
        current_year = datetime.datetime.now().year


        # Define the URL for the external API
        
        url = 'https://portal.tradebrains.in/api/company/exchange-holiday/{}/'.format(current_year)
        # Set up the query parameters

        try:
            # Send GET request to the external API with the parameters
            response = requests.get(url)
            response.raise_for_status()  # Raise exception for non-2xx responses

            data = response.json()
            # Serialize the data using HeatmapResponseSerializer
            return Response(data, status=status.HTTP_200_OK)
  
        except requests.RequestException as e:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

# =========================================================================================
# IPO API
class OPENDATEIPOView(APIView):


    def get_base_url(self):
        # Get the absolute URI for the current request
        absolute_url = self.request.build_absolute_uri()

        # Split the URL into segments
        segments = absolute_url.split('/')

        base_url = '/'.join(segments[:-1])

        return base_url

    def get(self, request):
        try:
            page = self.request.query_params.get('page', 1)
            per_page = self.request.query_params.get('per_page', 15)
            
            url = 'https://portal.tradebrains.in/api/ipos/ipo-data/open_data/'
            params = {'page': page, 'per_page': per_page}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                count = data['count']
                next_page = data['next']
                previous_page = data['previous']
                results = data['results']
                
                # Customize next and previous URLs
                if next_page:
                    next_page = next_page.replace('https://portal.tradebrains.in/api/ipos/ipo-data/closed_data', self.get_base_url())
                if previous_page:
                    previous_page = previous_page.replace('https://portal.tradebrains.in/api/ipos/ipo-data/closed_data', self.get_base_url())
                
                return Response({
                    'count': count,
                    'next': next_page,
                    'previous': previous_page,
                    'results': results
                }, status=status.HTTP_200_OK)
        except:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

class UpComingIPOView(APIView):
    def get_base_url(self):
        # Get the absolute URI for the current request
        absolute_url = self.request.build_absolute_uri()

        # Split the URL into segments
        segments = absolute_url.split('/')

        base_url = '/'.join(segments[:-1])

        return base_url

    def get(self, request):
        try:
            page = self.request.query_params.get('page', 1)
            per_page = self.request.query_params.get('per_page', 15)
            
            url = 'https://portal.tradebrains.in/api/ipos/ipo-data/upcoming_data/'
            params = {'page': page, 'per_page': per_page}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                count = data['count']
                next_page = data['next']
                previous_page = data['previous']
                results = data['results']
                
                # Customize next and previous URLs
                if next_page:
                    next_page = next_page.replace('https://portal.tradebrains.in/api/ipos/ipo-data/closed_data', self.get_base_url())
                if previous_page:
                    previous_page = previous_page.replace('https://portal.tradebrains.in/api/ipos/ipo-data/closed_data', self.get_base_url())
                
                return Response({
                    'count': count,
                    'next': next_page,
                    'previous': previous_page,
                    'results': results
                }, status=status.HTTP_200_OK)
        except:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

class CloseIPOView(APIView):
     
    def get_base_url(self):
        # Get the absolute URI for the current request
        absolute_url = self.request.build_absolute_uri()

        # Split the URL into segments
        segments = absolute_url.split('/')

        base_url = '/'.join(segments[:-1])

        return base_url

    def get(self, request):
        try:
            page = self.request.query_params.get('page', 1)
            per_page = self.request.query_params.get('per_page', 15)
            
            url = 'https://portal.tradebrains.in/api/ipos/ipo-data/closed_data/'
            params = {'page': page, 'per_page': per_page}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                count = data['count']
                next_page = data['next']
                previous_page = data['previous']
                results = data['results']
                
                # Customize next and previous URLs
                if next_page:
                    next_page = next_page.replace('https://portal.tradebrains.in/api/ipos/ipo-data/closed_data', self.get_base_url())
                if previous_page:
                    previous_page = previous_page.replace('https://portal.tradebrains.in/api/ipos/ipo-data/closed_data', self.get_base_url())
                
                return Response({
                    'count': count,
                    'next': next_page,
                    'previous': previous_page,
                    'results': results
                }, status=status.HTTP_200_OK)
        except:
            return Response({'error': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)



class ProfitAndLossView(APIView):
    def get(self, request, company_name, format=None):
        url = f"https://portal.tradebrains.in/api/company/profit-and-loss/{company_name}/consolidated/?years=10"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            serializer = ProfitAndLossSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Failed to fetch data from the external API'}, status=response.status_code)

class BalanceSheetView(APIView):
    def get(self, request, company_name, format=None):
        url = f"https://portal.tradebrains.in/api/company/balance-sheet/{company_name}/consolidated/?years=10"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            serializer = BalanceSheetSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Failed to fetch data from the external API'}, status=response.status_code)

class QuaterlyView(APIView):
    def get(self, request, company_name, format=None):
        url = f"https://portal.tradebrains.in/api/company/quaterly/{company_name}/consolidated/"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            serializer = QuaterlySerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Failed to fetch data from the external API'}, status=response.status_code)

class HoldingView(APIView):
    def get(self, request, company_name, format=None):
        url = f"https://portal.tradebrains.in/api/company/shareholding/consolidated/{company_name}/?quarters=2"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            formatted_data = {'stock': data}
            serializer = HoldingSerializer(data=formatted_data)
            if serializer.is_valid():
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Failed to fetch data from the external API'}, status=response.status_code)