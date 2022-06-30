require_relative '../funcs.rb'

# use expect{...} when testing for errors and expect(...) for values
# (easy to forget)

describe 'Customer Tests' do
    describe 'constructor' do
        it 'should create a customer given a wallet' do
            wallet_double = double("Wallet")
            expect { customer = Customer.new(wallet_double) }.not_to raise_error
        end
    end

    describe 'paying up' do
        it 'should call withdraw in Wallet' do
            wallet_double = double("Wallet")
            amount = 20
            customer = Customer.new(wallet_double)
            expect(wallet_double).to receive(:withdraw).and_return(amount)
            customer.pay(amount)
        end
    end
end
