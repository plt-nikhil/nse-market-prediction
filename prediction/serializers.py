from rest_framework import serializers


# Gainner & Loser Stock List For First 5
class StockInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    close = serializers.FloatField()
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    volume = serializers.FloatField()
    change = serializers.FloatField()
    percent = serializers.FloatField()
    date = serializers.DateTimeField()
    symbol = serializers.CharField()
    comp_name = serializers.CharField()
    scripcode = serializers.IntegerField()
    prev_close = serializers.FloatField()
# Gainner & Loser Stock List For First 5
class GainersMoversSerializer(serializers.Serializer):
    name = serializers.CharField()
    total_count = serializers.IntegerField()
    losers_count = serializers.IntegerField()
    gainers_count = serializers.IntegerField()
    gainers = StockInfoSerializer(many=True)
    losers = StockInfoSerializer(many=True)
    exchange = serializers.CharField()
    volume_movers = StockInfoSerializer(many=True)

# Gainer Details Page Show all Stock
class PriceSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    open = serializers.FloatField()
    close = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    volume = serializers.FloatField()
    value = serializers.FloatField()
    Fincode = serializers.IntegerField()
# Gainer Details Page Show all Stock
class GainersDetailsSerializer(serializers.Serializer):
    close = serializers.FloatField()
    change = serializers.FloatField()
    percent = serializers.FloatField()
    comp_name = serializers.CharField()
    prev_close = serializers.FloatField()
    name = serializers.CharField()
    short_name = serializers.CharField()
    mcap_type = serializers.CharField()
    industry_name = serializers.CharField()
    symbol = serializers.CharField()
    prices = PriceSerializer(many=True)

#Loser Details Page Show all Stock
class LoserDetailsSerializer(serializers.Serializer):
    close = serializers.FloatField()
    change = serializers.FloatField()
    percent = serializers.FloatField()
    comp_name = serializers.CharField()
    prev_close = serializers.FloatField()
    name = serializers.CharField()
    short_name = serializers.CharField()
    mcap_type = serializers.CharField()
    industry_name = serializers.CharField()
    symbol = serializers.CharField()
    prices = PriceSerializer(many=True)

# Get All Index EX:- NIFTY, AUTO 
class IndexSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)  # Allow id to be missing
    symbol = serializers.CharField(max_length=10, required=False)  # Allow symbol to be missing
    name = serializers.CharField(max_length=100, required=False)  # Allow name to be missing
    exchange = serializers.CharField(max_length=10, required=False)  # Allow exchange to be missing
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        if request is not None and obj is not None:
            return request.build_absolute_uri(f'/api/indexheatmap/{obj["symbol"]}/')
        return None


# Screen Page get All Stock
class ScreenerCMOTSSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    co_code = serializers.IntegerField()
    scripcode = serializers.FloatField()
    short_name = serializers.CharField()
    industry_name = serializers.CharField()
    sector_name = serializers.CharField()
    nse_listed_flag = serializers.IntegerField()
    bse_listed_flag = serializers.IntegerField()
    nse_status = serializers.CharField()
    bse_status = serializers.CharField()
    name = serializers.CharField()
    returns_1y = serializers.FloatField()
    prev_close = serializers.FloatField()
    mcap = serializers.FloatField()
    pe = serializers.FloatField()
    dividend_yield = serializers.FloatField()
    FINCODE = serializers.IntegerField()
    company_id = serializers.FloatField()


#Index Heatmap Result
class IndexHeatmapResultSerializer(serializers.Serializer):
    index = serializers.IntegerField()
    curr_price = serializers.FloatField()
    symbol = serializers.CharField(max_length=100)
    per_change = serializers.FloatField()
    change = serializers.FloatField()
    comp_name = serializers.CharField(max_length=255)
#Index Heatmap Result
class IndexHeatmapResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    previous = serializers.URLField(allow_blank=True, allow_null=True, required=False)
    results = IndexHeatmapResultSerializer(many=True)


# *******************************************************************
# All Stock Get Sectore Name

class SectorSerializer(serializers.Serializer):
    sect_code = serializers.CharField()
    sect_name = serializers.CharField()
    slug = serializers.CharField()
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        request = self.context.get('request')
        if request is not None and obj is not None:
            return request.build_absolute_uri(f'/api/stock/sector/{obj["slug"]}/')
        return None

# *******************************************************************

# Get Stock Details using sector Vise

class StockSectorDataSerializer(serializers.Serializer):
    # count = serializers.IntegerField()
    # next = serializers.CharField(allow_null=True)
    # previous = serializers.CharField(allow_null=True)
    # results = serializers.ListField(child=serializers.DictField())
    id = serializers.IntegerField()
    company_id = serializers.IntegerField()
    close = serializers.FloatField()
    open = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    volume = serializers.FloatField()
    change = serializers.FloatField()
    per_change = serializers.FloatField()
    date = serializers.DateTimeField()
    symbol = serializers.CharField()
    company = serializers.CharField()
    scripcode = serializers.CharField()
    co_code = serializers.IntegerField()
    isin = serializers.CharField()
    prev_close = serializers.FloatField()
    mcap = serializers.FloatField()
    pe = serializers.FloatField()
    roe = serializers.FloatField()

# Get All Stcok Name And Create Slug 
class GetAllStcokSerializer(serializers.Serializer):
    slug = serializers.CharField()
    sector_name = serializers.CharField()
    Company_name = serializers.CharField()
    industry_name = serializers.CharField()

    stock_details = serializers.SerializerMethodField()
    stock_heatmap = serializers.SerializerMethodField()
    stock_historical = serializers.SerializerMethodField()
    def get_stock_details(self, obj):
        request = self.context.get('request')
        if request is not None and obj is not None:
            return request.build_absolute_uri(f'/api/stock/{obj["slug"]}/')
        return None
    def get_stock_heatmap(self, obj):
        request = self.context.get('request')
        if request is not None and obj is not None:
            return request.build_absolute_uri(f'/api/stock/heatmap/{obj["slug"]}/')
        return None
    def get_stock_historical(self, obj):
        request = self.context.get('request')
        if request is not None and obj is not None:
            return request.build_absolute_uri(f'/api/stock/historical/{obj["slug"]}/')
        return None



# Get All Stock Details Page
class GetAllStockDetailSerializer(serializers.Serializer):
    fincode = serializers.CharField(allow_null=True)
    scrip_code = serializers.CharField(allow_null=True)
    scrip_name = serializers.CharField(allow_null=True)
    scrip_group = serializers.CharField(allow_null=True)
    company_name = serializers.CharField(allow_null=True)
    ind_code = serializers.CharField(allow_null=True)
    hse_code = serializers.CharField(allow_null=True)
    symbol = serializers.CharField(allow_null=True)
    series = serializers.CharField(allow_null=True)
    isin = serializers.CharField(allow_null=True)
    sname = serializers.CharField(allow_null=True)
    rformat = serializers.CharField(allow_null=True)
    fformat = serializers.CharField(allow_null=True)
    chairman = serializers.CharField(allow_null=True)
    mdir = serializers.CharField(allow_null=True)
    cosec = serializers.CharField(allow_null=True)
    inc_month = serializers.CharField(allow_null=True)
    inc_year = serializers.CharField(allow_null=True)
    fv = serializers.CharField(allow_null=True)
    status = serializers.CharField(allow_null=True)
    sublisting = serializers.CharField(allow_null=True)
    flag = serializers.CharField(allow_null=True)


class ProfitAndLossSerializer(serializers.Serializer):
    type = serializers.CharField()
    stock = serializers.DictField(child=serializers.DictField())

class BalanceSheetSerializer(serializers.Serializer):
    type = serializers.CharField()
    stock = serializers.DictField(child=serializers.DictField())

class QuaterlySerializer(serializers.Serializer):
    type = serializers.CharField()
    stock = serializers.DictField(child=serializers.DictField())


class ShareHoldingSerializer(serializers.Serializer):
    fincode = serializers.IntegerField()
    promoters = serializers.FloatField(allow_null=True)
    share_holding_pledge = serializers.FloatField(allow_null=True)
    public = serializers.FloatField(allow_null=True)
    fii = serializers.FloatField(allow_null=True)
    total_dii = serializers.FloatField(allow_null=True)
    mf = serializers.FloatField(allow_null=True)
    insurance = serializers.FloatField(allow_null=True)
    fin_inst = serializers.FloatField(allow_null=True)
    others = serializers.FloatField(allow_null=True)
    year = serializers.IntegerField()

class HoldingSerializer(serializers.Serializer):
    stock = serializers.DictField(child=ShareHoldingSerializer())