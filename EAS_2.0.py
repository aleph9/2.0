import pyupbit
import time

access = "2T1KcUmPKdY6rx46YxTi5hLrlsZAfIaxBpYxIsrh"          
secret = "jxxNxxmkeIvXczCxybwUgInv3xlR7jenAaK20TJO"    

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


"""목표가 조회""" #3분봉 50개 중 최고가에서 -1.3%의 가격
def tar_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=50)
    tar = max(df['high']) - (max(df['high']) * k)
    return(tar)
# print("목표가 : ", tar_price("KRW-ETH", 0.0013))

"""현재가 조회"""
def cur_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
# print("현재가 : ", cur_price("KRW-ETH"))

"""잔고 조회"""
def get_balance(ticker): #KRW = 원화 / ETH = 잔고 
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0
# print("원화잔고 : ", get_balance("KRW"))

"""평균매수가 조회"""
def abp(ticker):
    return upbit.get_avg_buy_price(ticker)
    #abp("KRW-ETH")
# print("평균매수가 : ",abp("KRW-ETH"))

"""장 판단 기준가"""
def judge(ticker): # 60분봉 70개 기준 max+min 값 
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=70)
    j = max(df['high']) + min(df['low'])
    return(j)
# print(judge("KRW-ETH")/1.8)


"""자동매매 시작"""
while True:
    try:
        #매수 목표가 설정 (3분봉 50개 중 '최고가 * -1.3%원' )
        cur = cur_price("KRW-ETH")#현재가 
        j = judge("KRW-ETH")

        if cur >= j / 1.8:#상승장  (-1.4/0.8/-0.25) 
             
            if cur <= tar_price("KRW-ETH", 0.014):                    #현재가가 목표가(고점대비 -1.4%) 보다 작거나 같다면
                krw = get_balance("KRW")
                if krw > 6000:                                        #잔고가 6000원 이상 확인 후 
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)     #시장가로 매수 
            elif cur >= (abp("KRW-ETH")*0.008)+abp("KRW-ETH"):        #현재가가 매수평균가의 0.8% 수익 중이면 
                        eth = get_balance("ETH")                      
                        if eth > 0.001:                               #이더리움 잔고 조회 후 
                            upbit.sell_market_order("KRW-ETH", eth*1) #시장가로 전량 매도
            elif cur <= (abp("KRW-ETH")*-0.0025)+abp("KRW-ETH"):        #현재가가 매수평균가의 -0.25% 손해 중이면 
                        eth = get_balance("ETH")                       
                        if eth > 0.001:                               #이더리움 잔고 조회 후 
                            upbit.sell_market_order("KRW-ETH", eth*1) #시장가로 전량 매도 후 
                            time.sleep(2400)                           #40분 거래 정지 
        
        elif cur < j / 1.8:#하락장  (-2.5/0.3/-0.2)  
             
            if cur <= tar_price("KRW-ETH", 0.025):                    #현재가가 목표가(고점대비 -2.5%) 보다 작거나 같다면
                krw = get_balance("KRW")
                if krw > 6000:                                        #잔고가 6000원 이상 확인 후 
                    upbit.buy_market_order("KRW-ETH", krw*0.9995)     #시장가로 매수 
            elif cur >= (abp("KRW-ETH")*0.004)+abp("KRW-ETH"):        #현재가가 매수평균가의 0.4% 수익 중이면 
                        eth = get_balance("ETH")                      
                        if eth > 0.001:                               #이더리움 잔고 조회 후 
                            upbit.sell_market_order("KRW-ETH", eth*1) #시장가로 전량 매도
            elif cur <= (abp("KRW-ETH")*-0.002)+abp("KRW-ETH"):       #현재가가 매수평균가의 -0.2% 손해 중이면 
                        eth = get_balance("ETH")                       
                        if eth > 0.001:                               #이더리움 잔고 조회 후 
                            upbit.sell_market_order("KRW-ETH", eth*1) #시장가로 전량 매도 후 
                            time.sleep(2400)                          #40분 거래 정지       
        else:
            time.sleep(1)            
            
    except Exception as e:
        print(e)
        time.sleep(1)
