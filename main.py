from helper import *
import math, time

market = "SPXL"
live = True
#endDate = '2018-09-04' #end date resulting in a buy signal
#endDate = '2018-11-01' #end date resulting in a sell signal
woodDaily = getHistory("CUT")#[:endDate]
goldDaily = getHistory("IAU")#[:endDate]

#get current positions
api = getAPI()
positions = api.list_positions()
inMarket = False
marketPositions = 0
for position in positions:
    if position.symbol == market:
        marketPositions = position.qty

#get account info
account = api.get_account()
buying_power = float(account.buying_power)

#resample
fs = 'M'
woodMonthly = addReturnsColumn(woodDaily.resample(fs).last())
goldMonthly = addReturnsColumn(goldDaily.resample(fs).last())

#check if markets are open
marketIsOpen = api.get_clock().is_open

#trade
try:
    if(marketIsOpen):
        print("Markets are open")
        #check if it's the first trading day of the month
        if(woodDaily.index[-1].day < woodDaily.index[-2].day):
            print("It's the first of the month")
            #check if wood is beating gold or if gold is beating wood
            if(woodMonthly["Returns"].iloc[-2] > goldMonthly["Returns"].iloc[-2]):
                #buy or hold
                if(marketPositions > 0):
                    #hold SPY
                    push("Wood outperformed gold last month but we're already in the market. No trades were made.")
                else:
                    lastPrice = getCurrentPrice(api, market)
                    qty = str(math.floor(buying_power/lastPrice))
                    side = 'buy'
                    type = 'limit'
                    time_in_force = 'gtc'
                    limit_price = lastPrice*1.005
                    if (live):
                        order_id = api.submit_order(market, qty, side, type, time_in_force, limit_price).order_id
                        order = get_order(order_id)
                        filled = order.filled_qty
                        while(filled < qty):
                            filled = get_order(order_id).filled_qty
                            time.sleep(1)
                        avgPrice = order.filled_avg_price
                    else:
                        print([market, qty, side, type, time_in_force, limit_price])
                        avgPrice = lastPrice*1.0025
                    report = "Wood outperformed gold last month. Order filled for " + str(qty) + " shares of " + market + " at " + str(avgPrice) + ". "
                    report += "This is " + str(avgPrice*100/lastPrice) + " percent of the current price of " + market + " ."
                    push(report)
            else:
                #close positions
                if(marketPositions > 0):
                    #closing positions
                    lastPrice = getCurrentPrice(api, market)
                    qty = marketPositions
                    side = 'sell'
                    type = 'limit'
                    time_in_force = 'gtc'
                    limit_price = lastPrice*0.995
                    if (live):
                        order_id = api.submit_order(market, qty, side, type, time_in_force, limit_price).order_id
                        order = get_order(order_id)
                        filled = order.filled_qty
                        while(filled < qty):
                            filled = get_order(order_id).filled_qty
                            time.sleep(1)
                        avgPrice = order.filled_avg_price
                    else:
                        print([market, qty, side, type, time_in_force, limit_price])
                        avgPrice = lastPrice*0.9975
                    report =  "Gold outperformed wood last month so closing current long " + market + " position. Order filled for " + str(qty) + " shares of " + market + " at " + str(avgPrice) + ". "
                    report += "This is " + str(avgPrice*100/lastPrice) + " percent of the current price of " + market + " ."
                    push(report)
                else:
                    push("Gold outperformed wood last month but no " + market + " positions are currently held. No trades were made.")
        else:
            push("Not time to rebalance. Exiting...")
    else:
        push("Markets are closed. Exiting...")
except Exception as e:
    push(e)
