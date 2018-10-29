from django.http import HttpResponse
from django.shortcuts import render

def home(request):
	return render(request, "home.html")

def contact(request):
	return render(request, "contact.html")

def count(request):
	if request.method == 'GET':
		print("inside get")
		word_count = 0
	elif request.method == 'POST':
		print("inside post")
		text = request.POST['text']
		word_count = len(text.split())
	return render(request, "count.html", {'count':word_count})

def stockprofile(request):
	data = {}
	if request.method == 'GET':
		print("inside get")
		data['valid'] = 'get'
	elif request.method == 'POST':
		print("inside post")
		if(request.POST['ticker_symbol'] and request.POST['allotment'] \
		and request.POST['final_share_price'] and request.POST['sell_commission'] \
		and request.POST['initial_share_price'] and request.POST['buy_commission'] \
		and request.POST['capital_gain_tax_rate']):
			data['valid'] = True
			ticker_symbol = request.POST['ticker_symbol'] or  ''
			allotment = int(request.POST['allotment']) or 0
			final_share_price = int(request.POST['final_share_price']) or 0
			sell_commission = int(request.POST['sell_commission']) or 0
			initial_share_price = int(request.POST['initial_share_price']) or 0
			buy_commission = int(request.POST['buy_commission']) or 0
			capital_gain_tax_rate = int(request.POST['capital_gain_tax_rate']) or 0

			# calculate report

			# Proceeds (Allotment x Final share price)
			proceeds = (allotment * final_share_price)

			# Cost (Allotment x Initial Share Price + commissions + Tax on Capital Gain)
			initial_investment = (allotment * initial_share_price)
			total_commission = (buy_commission + sell_commission)
			final_outcome = (allotment * final_share_price)
			total_cost = (final_outcome - (initial_investment + total_commission))
			tax_on_capital_gain = total_cost * (capital_gain_tax_rate/100.0)
			cost = initial_investment + total_commission + tax_on_capital_gain

			# Net Profit (in dollars)
			net_profit = (final_outcome - (initial_investment + total_commission + tax_on_capital_gain))

			# Return on investment (in %)
			rate_of_interest = net_profit / cost * 100.0

			# Break even price (in dollars)
			break_even_price = (initial_investment + total_commission) / (allotment / 1.0)


			# print report
			result = {}
			result["proceeds"] = "$" + str(proceeds)
			result["costs"] = "$" + str(cost)
			result['total_purchase_price'] =str(allotment)+"x $"+str(initial_share_price)+" = "+str(initial_investment)
			result["buy_commission"]= str(buy_commission)
			result["sell_commission"] = str(sell_commission)
			result["tax_on_capital_gain"] = str(capital_gain_tax_rate)+"% of $" \
				+str(total_cost)+" = " \
				+str(tax_on_capital_gain)

			result["net_profit"] = "$" + str(net_profit)
			result["return_on_investment"] = "{0:.2f}".format(rate_of_interest) + "%"
			result["break_even_price"] = "$"+str(break_even_price)
			data['result'] = result
		else:
			data['valid'] = False
	if data['valid'] == True:
		return render(request, "result.html", {'data':data})
	else:
		return render(request, "stockprofile.html", {'data':data})
