import json
import pprint
import unirest
from secrets import *

BASE_URL  = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices"

class SkyScanMySky(object):

	base_url  = None
	rapid_key = None

	"""SkyScanMySky implement the RapidAPI wrapper around SkyScanner API"""
	def __init__(self, base_url, rapid_key):

		super(SkyScanMySky, self).__init__()

		self.base_url  = base_url
		self.rapid_key = rapid_key

	def create_session(self, country, currency, locale, origin_place, destination_place,
		departure_date, return_date = None, adults = 1, cabin_class = "economy", children = 0,
		infants = 0, include_carriers = None, exclude_carriers = None, group_pricing = "false"):

		"""create_session function create a live flight search session to poll for results

		Args:
			country: (required, str) The market country your user is in. Example: IR
			currency: (required, str) The currency you want the prices in. Example: EUR
			locale: (required, str) The locale you want the results in (ISO locale). Example: en-US
			origin_place: (required, str) The origin place (see places). Example: MUC-sky
			destination_place: (required, str) The destination place (see places). Example: DUB-sky
			departure_date: (required, str) The outbound date. Format "yyyy-mm-dd".

			return_date: (str) The return date. Format "yyyy-mm-dd". Use empty string for oneway trip. Default None
			adults: (int) Number of adults (16+ years). Must be between 1 and 8. Default 1
			cabin_class: (str) The cabin class. Can be "economy", "premiumeconomy", "business", "first". Default "economy"
			children: (int) Number of children (1-16 years). Can be between 0 and 8. Default 0
			infants: (int) Number of infants (under 12 months). Can be between 0 and 8. Default 0
			include_carriers: (str) Only return results from those carriers. Comma-separated list of carrier ids. Default None
			exclude_carriers: (str) Filter out results from those carriers. Comma-separated list of carrier ids. Default None
			group_pricing: (str) If set to true, prices will be obtained for the whole passenger group and
				if set to false it will be obtained for one adult. Default false

		Returns:
			The return value is a unirest response object with location set in headers field

		"""

		url = "{}/pricing/v1.0".format(self.base_url)

		params = {
			"country": country,
			"currency": currency,
			"locale": locale,
			"originPlace": origin_place,
			"destinationPlace": destination_place,
			"outboundDate": departure_date,
			"adults": adults,
			"cabinClass": cabin_class,
			"children": 0,
			"infants": 0,
			"groupPricing": group_pricing
		}

		if return_date != None:
			params["inboundDate"] = return_date

		if include_carriers != None:
			params["includeCarriers"] = include_carriers

		if exclude_carriers != None:
			params["excludeCarriers"] = exclude_carriers

		response = unirest.post(url,
			headers={
				"X-RapidAPI-Key": self.rapid_key,
				"Content-Type": "application/x-www-form-urlencoded"
			},
			params = params
		)

		return response

	def poll_results(self, session_key, sort_type = None, sort_order = "desc", duration = None, include_carriers = None,
		exclude_carriers = None, origin_airports = None, destination_airports = None, stops = "0",
		outbound_depart_time = None, outbound_depart_start_time = None, outbound_depart_end_time = None,
		outbound_arrive_start_time = None, outbound_arrive_end_time = None, inbound_depart_time = None,
		inbound_depart_start_time = None, inbound_depart_end_time = None, inbound_arrive_start_time = None,
		inbound_arrive_end_time = None, page_index = 0, page_size = 10):

		"""poll_results function poll for results over a session create with create_session

		Args:
			session_key: (required, str) The session key received in the Location Header when creating the session.

			sort_type: (str) The parameter to sort results on. Can be carrier, duration, outboundarrivetime,
				outbounddeparttime, inboundarrivetime, inbounddeparttime, price. Default None
			sort_order: (str) The sort order. "asc" or "desc". Default "desc"
			duration: (int) Filter for maximum duration in minutes. Integer between 0 and 1800. Default None
			include_carriers: (str) Only return results from those carriers. Comma-separated list of carrier ids. Default None
			exclude_carriers: (str) Filter out results from those carriers. Comma-separated list of carrier ids. Default None
			origin_airports: (str) Origin airports to filter on. List of airport codes delimited by ";". Default None
			destination_airports: (str) Destination airports to filter on. List of airport codes delimited by ";". Default None
			stops: (str) Filter by number of stops. 0: direct flights only 1: flights with one stop only.
				To show all flights do not use (only supports values 0 and 1). Default 0
			outbound_depart_time: (str) Filter for outbound departure time by time period of the day (i.e. morning, afternoon, evening).
				List of day time period delimited by ";"" (acceptable values are M, A, E). Default None
			outbound_depart_start_time: (str) Filter for start of range for outbound departure time. Format "hh:mm". Default None
			outbound_depart_end_time: (str) Filter for end of range for outbound departure time. Format "hh:mm". Default None
			outbound_arrive_start_time: (str) Filter for start of range for outbound arrival time. Format "hh:mm". Default None
			outbound_arrive_end_time: (str) Filter for end of range for outbound arrival time. Format "hh:mm". Default None
			inbound_depart_time: (str) Filter for inbound departure time by time period of the day (i.e. morning, afternoon, evening).
				List of day time period delimited by ";"" (acceptable values are M, A, E). Default None
			inbound_depart_start_time: (str) Filter for start of range for inbound departure time. Format "hh:mm". Default None
			inbound_depart_end_time: (str) Filter for start of range for inbound departure time. Format "hh:mm". Default None
			inbound_arrive_start_time: (str) Filter for start of range for inbound departure time. Format "hh:mm". Default None
			inbound_arrive_end_tim: (str) Filter for end of range for inbound arrival time. Format "hh:mm". Default None
			page_index: (int) The desired page number. Leave empty for no pagination. Default 0
			page_size: (int) The number of itineraries per page. Defaults to 10 if not specified. Default 10

		Returns:
			The return value is a unirest response object with location set in headers field

		"""

		url = "{}/pricing/uk2/v1.0/{}".format(self.base_url, session_key)
		if sort_type != None:
			url += "\\?sortType={}".format(sort_type)
		if sort_order != None:
		    url += "\\?sortOrder={}".format(sort_order)
		if duration != None:
		    url += "\\?duration={}".format(duration)
		if include_carriers != None:
		    url += "\\?includeCarriers={}".format(include_carriers)
		if exclude_carriers != None:
		    url += "\\?excludeCarriers={}".format(exclude_carriers)
		if origin_airports != None:
		    url += "\\?originAirports={}".format(origin_airports)
		if destination_airports != None:
		    url += "\\?destinationAirports={}".format(destination_airports)
		if stops == "0":
		    url += "\\?stops={}".format(stops)
		if outbound_depart_time != None:
		    url += "\\?outboundDepartTime={}".format(outbound_depart_time)
		if outbound_depart_start_time != None:
		    url += "\\?outboundDepartStartTime={}".format(outbound_depart_start_time)
		if outbound_depart_end_time != None:
		    url += "\\?outboundDepartEndTime={}".format(outbound_depart_end_time)
		if outbound_arrive_start_time != None:
		    url += "\\?outboundArriveStartTime={}".format(outbound_arrive_start_time)
		if outbound_arrive_end_time != None:
		    url += "\\?outboundArriveEndTime={}".format(outbound_arrive_end_time)
		if inbound_depart_time != None:
		    url += "\\?inboundDepartTime={}".format(inbound_depart_time)
		if inbound_depart_start_time != None:
		    url += "\\?inboundDepartStartTime={}".format(inbound_depart_start_time)
		if inbound_depart_end_time != None:
		    url += "\\?inboundDepartEndTime={}".format(inbound_depart_end_time)
		if inbound_arrive_start_time != None:
		    url += "\\?inboundArriveStartTime={}".format(inbound_arrive_start_time)
		if inbound_arrive_end_time != None:
		    url += "\\?inboundArriveEndTime={}".format(inbound_arrive_end_time)
		if page_index != 0:
		    url += "\\?pageIndex={}".format(page_index)
		if page_size != 1:
		    url += "\\?pageSize={}".format(page_size)

		response = unirest.get(url,
			headers = {
				"X-RapidAPI-Key": self.rapid_key
			}
		)

		return response

	def list_places(self, country, currency, locale, query):

		url = "{}/autosuggest/v1.0/{}/{}/{}/?query={}".format(self.base_url, country, currency, locale, query)

		response = unirest.get(url,
			headers={
				"X-RapidAPI-Key": self.rapid_key
			}
		)

		return response

	def browser_quotes(self, country, currency, locale, origin_place, destination_place, departure_date, return_date = None):

		url = "{}/browsequotes/v1.0/{}/{}/{}/{}/{}/{}".format(self.base_url, country, currency, locale, origin_place, destination_place, departure_date)
		if return_date != None:
			url += "\\?inboundpartialdate={}".format(return_date)

		response = unirest.get(url,
			headers={
				"X-RapidAPI-Key": self.rapid_key
			}
		)

		return response

	def browser_routes(self, country, currency, locale, origin_place, destination_place, departure_date, return_date = None):

		url = "{}/browseroutes/v1.0/{}/{}/{}/{}/{}/{}".format(self.base_url, country, currency, locale, origin_place, destination_place, departure_date)
		if return_date != None:
			url += "\\?inboundpartialdate={}".format(return_date)

		response = unirest.get(url,
			headers={
				"X-RapidAPI-Key": self.rapid_key
			}
		)

		return response

	def browser_dates(self, country, currency, locale, origin_place, destination_place, departure_date, return_date = None):

		url = "{}/browsedates/v1.0/{}/{}/{}/{}/{}/{}".format(self.base_url, country, currency, locale, origin_place, destination_place, departure_date)
		if return_date != None:
			url += "\\?inboundpartialdate={}".format(return_date)

		response = unirest.get(url,
			headers={
				"X-RapidAPI-Key": self.rapid_key
			}
		)

		return response

	def list_markets(self, country):

		url = "{}/reference/v1.0/countries/{}".format(self.base_url, country)

		response = unirest.get(url,
			headers={
				"X-RapidAPI-Key": self.rapid_key
			}
		)

		return response

	def curriencies(self):

		url = "{}/reference/v1.0/currencies".format(self.base_url)

		response = unirest.get(url,
			headers={
				"X-RapidAPI-Key": self.rapid_key
			}
		)

		return response

if __name__ == '__main__':

	ssms = SkyScanMySky(BASE_URL, RAPID_KEY)

	# places = ssms.list_places('IR', 'EUR', 'en-US', 'Dublin').body
	# pprint.pprint(places)

	# quotes = ssms.browser_quotes('IR', 'EUR', 'en-US', 'DUB-sky', 'MUC-sky', '2019-01-24', '2019-01-27').body
	# pprint.pprint(quotes)

	# routes = ssms.browser_routes('IR', 'EUR', 'en-US', 'DUB-sky', 'MUC-sky', '2019-01-24', '2019-01-27').body
	# pprint.pprint(routes)

	# dates = ssms.browser_dates('IR', 'EUR', 'en-US', 'DUB-sky', 'FRA-sky', '2019-03-15', '2019-03-18').body
	# pprint.pprint(dates)

	# markets = ssms.list_markets('en-US').body
	# pprint.pprint(markets)

	curriencies = ssms.curriencies().body
	pprint.pprint(curriencies)

	# session = ssms.create_session('IR', 'EUR', 'en-US', 'MUC-sky', 'DUB-sky', '2019-01-24', '2019-01-27').headers.headers
	# session_key = session[3].split("/")[-1].replace("\r\n", "")
	# results = ssms.poll_results(session_key).body
	# print json.dumps(results)









