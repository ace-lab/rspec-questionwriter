class Wallet
    attr_reader :cash
    def initialize(amount)
      @cash = amount
    end
    def withdraw(amount)
       @cash -= amount
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

class PaperKid
  attr_reader :collected_amount
  def initialize
    @collected_amount = 0
  end
  def collect_money(customer, due_amount)
    @collected_amount += customer.pay(due_amount)
  end
end