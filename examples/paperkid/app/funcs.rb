class Wallet
    attr_reader :cash 
    def initialize(amount)
      @cash = amount
    end
    def withdraw(amount)
       @cash -= amount
       amount
    end
  end

class Customer
  def initialize(wallet)
    @wallet = wallet
  end
  def pay(amount)
    @wallet.withdraw(amount)
  end
end
