class InsufficientFundsError < StandardError
end

class Wallet
    attr_reader :cash
    def initialize(amount)
      raise ArgumentError if amount < 0
      @cash = amount
    end
    def withdraw(amount)
      raise InsufficientFundsError if amount > @cash
      raise ArgumentError if amount < 0
      @cash -= amount
      return amount
    end
  end


  