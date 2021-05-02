from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Stock
from .forms import StockForm

# https://iexcloud.io/docs/api/#introduction


def home(request):
	import requests
	import json

	
	#TODO: compare ticker entered by user with list of all known tickers
	# an return the most similar ticker that is known to exist
	if request.method == 'POST':
		ticker = request.POST['ticker']
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_144c5829de204a7e84434c9927448a72")
		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
			return render(request, 'home.html', {'api': api})
	else:
		return render(request, 'home.html', {'ticker': "Enter a Ticker Symbol Above..."})




	return render(request, 'home.html', {'api': api})

def about(request):
	return render(request, 'about.html', {})



def portfolio(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock has been succesfully added"))
			return redirect('portfolio')
	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_144c5829de204a7e84434c9927448a72")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."
		return render(request, 'portfolio.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk = stock_id)
	item.delete()
	messages.success(request, ("Succesfully Removed"))
	return redirect('portfolio')

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})