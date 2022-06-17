class InsufficientFundsError < StandardError
end

class Wallet
    attr_reader :cash # not attr_accessor
      # need a way to add money for Wallet tests
    def initialize(amount)
      raise ArgumentError if amount <= 0
      @cash = amount
    end
    def withdraw(amount)
       raise InsufficientFundsError if amount > @cash
       raise ArgumentError if amount <= 0
       @cash -= amount
       amount
    end
  end

class Customer
  # no # attr_accessor :wallet
  def initialize(wallet)
    @wallet = wallet
  end
  # behavior delegation
  def pay(amount)
    @wallet.withdraw(amount)
  end
end

class PaperKid
  attr_reader :collected_amount
  def initialize
    @collected_amount = 0
  end
  def collect_money(customer, due_amount)
    @collected_amount += customer.pay(due_amount)
  end
end