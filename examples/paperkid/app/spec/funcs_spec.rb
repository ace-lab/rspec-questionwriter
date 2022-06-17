require_relative '../funcs.rb'

# use expect{...} when testing for errors and expect(...) for values
# (easy to forget)

describe 'Wallet Tests' do
    describe 'constructor' do
        it 'should reject <0 money' do
            expect { Wallet.new(-4) }.to raise_error(ArgumentError)
        end
    end
    describe 'getter setter' do
        before(:each) { @wallet = Wallet.new(20) }
        it 'should have cash set by constructor' do
            expect(@wallet.cash).to eq(20)
        end
        it 'should not have a cash setter method' do
            expect{ @wallet.cash = 100 }.to raise_error(NoMethodError)
        end
    end
    describe 'withdraw' do
        before(:each) { @wallet = Wallet.new(20) }
        it 'should remove valid amount' do
            expect{@wallet.withdraw(10)}.not_to raise_error
            expect(@wallet.cash).to eq(10)
        end
        it 'should not withdraw too much' do
            expect{ @wallet.withdraw(100) }.to raise_error(InsufficientFundsError)
            expect( @wallet.cash ).to eq(20)
        end
        it 'should not withdraw negative money' do
            expect{ @wallet.withdraw(-4) }.to raise_error(ArgumentError)
            expect( @wallet.cash ).to eq(20)
        end
    end
end

describe 'Customer Tests' do
    describe 'constructor' do
        it 'should create a customer given a wallet' do
            wallet_double = double("Wallet")
            expect { customer = Customer.new(wallet_double) }.not_to raise_error
        end
    end

    describe 'paying up' do
        # customer has a wallet, not cash.
        # we don't test the wallet here. hard to resist
        it 'should call withdraw in Wallet' do
            wallet_double = double("Wallet")
            @customer = Customer.new(wallet_double)
            expect(wallet_double).to receive(:withdraw)
            @customer.pay(20)
        end
    end
end

describe 'PaperKid tests' do
    describe 'constructor' do
        it 'should instantiate' do
            expect{ pk = PaperKid.new }.not_to raise_error
        end
    end
    describe 'money collection' do
        before(:each) do
            # @collected_money must be initialized to increment later
            @pk = PaperKid.new
            @customer_dbl = double("Customer")
        end
        it 'should call pay method of Customer' do
            # dbl must return or @collected_money increment fails
            expect(@customer_dbl).to receive(:pay).with(10).and_return(10)
            @pk.collect_money(@customer_dbl, 10)
        end
        it 'should increment collected amount' do
            allow(@customer_dbl).to receive(:pay).with(10).and_return(10)
            @pk.collect_money(@customer_dbl, 10)
            expect(@pk.collected_amount).to eq(10)
        end
    end
end