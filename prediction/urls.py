from django.urls import path, include
from . import views
# from .views import SectorViewSet
from rest_framework.routers import DefaultRouter
from .views import coming_soon,GainersMoversView, GainersView, LosersView, IndexListView, ScreenerCMOTSView, IndexHeatmapView, StockSectoreDataView,SectorListView, AllStockNameView, StockDetailsView,StockHeatmapView, StockHistoricalView, ExchangeHolidayView, OPENDATEIPOView, UpComingIPOView, CloseIPOView, ProfitAndLossView, BalanceSheetView, QuaterlyView, HoldingView
router = DefaultRouter()


urlpatterns = [
    path('', views.coming_soon, name='coming_soon'),

    # Gainer & Movers Stock API
    path('api/gainer-movers/', GainersMoversView.as_view(), name='gainer-movers'),
    path('api/gainers/<str:index>/', GainersView.as_view(), name='gainers'),
    path('api/losers/<str:index>/', LosersView.as_view(), name='gainers'),
    
    path('api/screener-cmots/<int:page>/', ScreenerCMOTSView.as_view(), name='screener-cmots'),

    # Index Vise Data Get API
    path('api/index/all', IndexListView.as_view(), name='index-list'),
    path('api/indexheatmap/<str:index>/', IndexHeatmapView.as_view(), name='index-heatmap-view'),  # NIFTY & INDEX/All pass

    # Sector Vise Data API
    path('api/stock/sectors',SectorListView.as_view(), name='sector-all'),
    path('api/stock/sector/<str:name>/', StockSectoreDataView.as_view(), name='stock-data'),     # Get All Stcok Details from Sector Vise #miscellaneous
    
    # All Stock Data And Details Page & Heatmp & Historical Data
    path('api/stock', AllStockNameView.as_view(),name='demo'),
    path('api/stock/<str:index>/',StockDetailsView.as_view(),name='demodd'),
    path('api/stock/heatmap/<str:index>/', StockHeatmapView.as_view(), name="askdhsd"),
    path('api/stock/historical/<str:index>/',StockHistoricalView.as_view(), name="asadsd"),

    
    # Get Holiday List
    path('api/holidaylist/',ExchangeHolidayView.as_view(), name="Holiday List"),

    #Get IPO List
    path('api/ipo/open/', OPENDATEIPOView.as_view(), name='openipodate'),
    path('api/ipo/upcoming/', UpComingIPOView.as_view(), name="upcomingIPO"),
    path('api/ipo/close/', CloseIPOView.as_view(), name="Close IPO"),
    path('api/profit-and-loss/<str:company_name>/', ProfitAndLossView.as_view(), name='profit-and-loss'),
    path('api/balance-sheet/<str:company_name>/', BalanceSheetView.as_view(), name='profit-and-loss'),
    path('api/quaterly/<str:company_name>/', QuaterlyView.as_view(), name='profit-and-loss'),
    path('api/holding/<str:company_name>/', HoldingView.as_view(), name='profit-and-loss'),
]



# detials link add from home page ex:- sector page under add url from details page
