import scipy.stats
import numpy as np
import matplotlib.pyplot as plt


N = scipy.stats.norm.cdf
N_prime = scipy.stats.norm.pdf


#create class for the classic European option without dividends
class BlackScholes_Euro:
	def __init__(self, call_put, S, K, r, t, sigma):
		self.call_put = call_put
		self.S = S
		self.K = K
		self.r = r
		self.t = t
		self.sigma = sigma
		self.d1 = (np.log(self.S / self.K) + (self.r + self.sigma ** 2 / 2) * self.t) / (self.sigma * np.sqrt(self.t))
		self.d2 = self.d1 - self.sigma * np.sqrt(self.t)

	def Price(self):
		if self.call_put == "c":
			return N(self.d1) * self.S - N(self.d2) * self.K * np.exp(-self.r * self.t)
		elif self.call_put=="p":
			return N(-self.d2) * self.K * np.exp(-self.r * self.t) - N(-self.d1) * self.S
		else:
			return "Please specify whether call/put!"

	def delta(self):
		if self.call_put == "c":
			return N(self.d1)
		elif self.call_put == "p":
			return N(self.d1) - 1
		else:
			return "Please specify whether call/put!"

	def gamma(self):
		if self.call_put != "c" or self.call_put != "p":
			return N_prime(self.d1) / (self.S * self.sigma * np.sqrt(self.t))
		else:
			return "Please specify whether call/put!"

	def vega(self):
		if self.call_put != "c" or self.call_put != "p":
			return self.S * N_prime(self.d1) / (self.sigma * np.sqrt(self.t))
		else:
			return "Please specify whether call/put!"

	def theta(self):
		if self.call_put=="c":
			return -(self.S*N_prime(self.d1)*self.sigma)/(2*np.sqrt(self.t)) - self.r*self.K*np.exp(-(self.r*self.t))*N(self.d2)
		elif self.call_put=="p":
			return -(self.S * N_prime(self.d1) * self.sigma) / (2 * np.sqrt(self.t)) + self.r * self.K * np.exp(-(self.r * self.t)) * N(-self.d2)
		else:
			return "Please specify whether call/put!"

	def rho(self):
		if self.call_put=="c":
			return self.K*self.t*np.exp(-self.r*self.t)*N(self.d2)
		elif self.call_put=="p":
			return -self.K*self.t*np.exp(-self.r*self.t)*N(self.d2)

	def plot_greeks(self,greek,changed_param,start=None,end=None):
		# Generate the end points for the param that we want to vary (default set to 0 and 2 times the stock price)
		#parameters that can be varied (S, K, r, t)
		if start is None:
			start=0.001
		if end is None:
			if changed_param=="S":
				end=self.S*2
			elif changed_param=="K":
				end=self.K*2
			elif changed_param=="r":
				end=self.r*2
			elif changed_param=="t":
				end=self.t*2
			elif changed_param=="sigma":
				end=self.sigma*2

		#generate the range for the parameter that we want to vary
		changed_param_range = np.linspace(start, end,200)

		# create new options for values in the range desired
		if changed_param == "S":
			opt_range=[BlackScholes_Euro(self.call_put,i,self.K,self.r,self.t,self.sigma) for i in changed_param_range]
		elif changed_param == "K":
			opt_range=[BlackScholes_Euro(self.call_put,self.S,i,self.r,self.t,self.sigma) for i in changed_param_range]
		elif changed_param == "r":
			opt_range=[BlackScholes_Euro(self.call_put,self.S,self.K,i,self.t,self.sigma) for i in changed_param_range]
		elif changed_param == "t":
			opt_range=[BlackScholes_Euro(self.call_put,self.S,self.K,self.r,i,self.sigma) for i in changed_param_range]
		elif changed_param == "sigma":
			opt_range=[BlackScholes_Euro(self.call_put,self.S,self.K,self.r,self.t,i) for i in changed_param_range]

		#calculate the desired for all the options
		greek_range=[getattr(i,greek)() for i in opt_range]

		plt.plot(changed_param_range,greek_range)
		plt.xlabel(changed_param)
		plt.ylabel(greek)
		plt.title(f"{greek} vs {changed_param}")

		#set grid
		plt.grid("True")

		# Add text box with parameters
		parameters = f"Call/Put: {self.call_put}\nS: {self.S}\nK: {self.K}\nr: {self.r}\nt: {self.t}\nsigma: {self.sigma}"
		plt.text(0.05, 0.05, parameters, transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
		plt.show()


# Example usage
call_put = "c"
S = 100
K = 100
r = 0.05
t = 1
sigma = 0.2
plot_start=0
plot_end=400

option=BlackScholes_Euro(call_put, S, K, r, t, sigma)
option.plot_greeks("delta","S")
option.plot_greeks("delta","K")


class BlackScholes_forward:
	def __init__(self, S, K, r, t):
		self.S = S
		self.K = K
		self.r = r
		self.t = t

	def Price(self):
		return self.S-self.K*np.exp(-self.r*self.t)

	def delta(self):
		return 1

	def gamma(self):
		return 0

	def theta(self):
		return -self.r*self.K*np.exp(-self.r*self.t)

	def rho(self):
		return -self.K*self.t * np.exp(-self.r * self.t)

	def plot_greeks(self, greek, changed_param, start=None, end=None):
		# Generate the end points for the param that we want to vary (default set to 0 and 2 times the stock price)
		# parameters that can be varied (S, K, r, t)
		if start is None:
			start = 0.001
		if end is None:
			if changed_param == "S":
				end = self.S * 2
			elif changed_param == "K":
				end = self.K * 2
			elif changed_param == "r":
				end = self.r * 2
			elif changed_param == "t":
				end = self.t * 2

		# generate the range for the parameter that we want to vary
		changed_param_range = np.linspace(start, end, 200)

		# create new options for values in the range desired
		if changed_param == "S":
			opt_range = [BlackScholes_forward(i, self.K, self.r, self.t) for i in changed_param_range]
		elif changed_param == "K":
			opt_range = [BlackScholes_forward(self.S, i, self.r, self.t) for i in changed_param_range]
		elif changed_param == "r":
			opt_range = [BlackScholes_forward(self.S, self.K, i, self.t) for i in changed_param_range]
		elif changed_param == "t":
			opt_range = [BlackScholes_forward(self.S, self.K, self.r, i) for i in changed_param_range]

		# calculate the desired for all the options
		greek_range = [getattr(i, greek)() for i in opt_range]

		plt.plot(changed_param_range, greek_range)
		plt.xlabel(changed_param)
		plt.ylabel(greek)
		plt.title(f"{greek} vs {changed_param}")

		# set grid
		plt.grid("True")

		# Add text box with parameters
		parameters = f"S: {self.S}\nK: {self.K}\nr: {self.r}\nt: {self.t}"
		plt.text(0.05, 0.05, parameters, transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
		plt.show()

S = 100
K = 100
r = 0.05
t = 1
forward=BlackScholes_forward(S,K,r,t)
forward.plot_greeks("delta","S")

class BlackScholes_Euro:
	def __init__(self, call_put, S, K, r, t, sigma):
		self.call_put = call_put
		self.S = S
		self.K = K
		self.r = r
		self.t = t
		self.sigma = sigma
		self.d1 = (np.log(self.S / self.K) + (self.r + self.sigma ** 2 / 2) * self.t) / (self.sigma * np.sqrt(self.t))
		self.d2 = self.d1 - self.sigma * np.sqrt(self.t)

	def Price(self):
		if self.call_put == "c":
			return N(self.d1) * self.S - N(self.d2) * self.K * np.exp(-self.r * self.t)
		elif self.call_put=="p":
			return N(-self.d2) * self.K * np.exp(-self.r * self.t) - N(-self.d1) * self.S
		else:
			return "Please specify whether call/put!"

	def delta(self):
		if self.call_put == "c":
			return N(self.d1)
		elif self.call_put == "p":
			return N(self.d1) - 1
		else:
			return "Please specify whether call/put!"

	def gamma(self):
		if self.call_put != "c" or self.call_put != "p":
			return N_prime(self.d1) / (self.S * self.sigma * np.sqrt(self.t))
		else:
			return "Please specify whether call/put!"

	def vega(self):
		if self.call_put != "c" or self.call_put != "p":
			return self.S * N_prime(self.d1) / (self.sigma * np.sqrt(self.t))
		else:
			return "Please specify whether call/put!"

	def theta(self):
		if self.call_put=="c":
			return -(self.S*N_prime(self.d1)*self.sigma)/(2*np.sqrt(self.t)) - self.r*self.K*np.exp(-(self.r*self.t))*N(self.d2)
		elif self.call_put=="p":
			return -(self.S * N_prime(self.d1) * self.sigma) / (2 * np.sqrt(self.t)) + self.r * self.K * np.exp(-(self.r * self.t)) * N(-self.d2)
		else:
			return "Please specify whether call/put!"

	def rho(self):
		if self.call_put=="c":
			return self.K*self.t*np.exp(-self.r*self.t)*N(self.d2)
		elif self.call_put=="p":
			return -self.K*self.t*np.exp(-self.r*self.t)*N(self.d2)

	def plot_greeks(self,greek,changed_param,start=None,end=None):
		# Generate the end points for the param that we want to vary (default set to 0 and 2 times the stock price)
		#parameters that can be varied (S, K, r, t)
		if start is None:
			start=0.001
		if end is None:
			if changed_param=="S":
				end=self.S*2
			elif changed_param=="K":
				end=self.K*2
			elif changed_param=="r":
				end=self.r*2
			elif changed_param=="t":
				end=self.t*2
			elif changed_param=="sigma":
				end=self.sigma*2

		#generate the range for the parameter that we want to vary
		changed_param_range = np.linspace(start, end,200)

		# create new options for values in the range desired
		if changed_param == "S":
			opt_range=[BlackScholes_Euro(self.call_put,i,self.K,self.r,self.t,self.sigma) for i in changed_param_range]
		elif changed_param == "K":
			opt_range=[BlackScholes_Euro(self.call_put,self.S,i,self.r,self.t,self.sigma) for i in changed_param_range]
		elif changed_param == "r":
			opt_range=[BlackScholes_Euro(self.call_put,self.S,self.K,i,self.t,self.sigma) for i in changed_param_range]
		elif changed_param == "t":
			opt_range=[BlackScholes_Euro(self.call_put,self.S,self.K,self.r,i,self.sigma) for i in changed_param_range]
		elif changed_param == "sigma":
			opt_range=[BlackScholes_Euro(self.call_put,self.S,self.K,self.r,self.t,i) for i in changed_param_range]

		#calculate the desired for all the options
		greek_range=[getattr(i,greek)() for i in opt_range]

		plt.plot(changed_param_range,greek_range)
		plt.xlabel(changed_param)
		plt.ylabel(greek)
		plt.title(f"{greek} vs {changed_param}")

		#set grid
		plt.grid("True")

		# Add text box with parameters
		parameters = f"Call/Put: {self.call_put}\nS: {self.S}\nK: {self.K}\nr: {self.r}\nt: {self.t}\nsigma: {self.sigma}"
		plt.text(0.05, 0.05, parameters, transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.5))
		plt.show()


