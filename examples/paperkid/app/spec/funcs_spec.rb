require_relative '../funcs.rb'

# use expect{...} when testing for errors and expect(...) for values
# (easy to forget)

describe 'Wallet Tests' do
    describe 'constructor' do
        it 'should reject <0 money' do
            bad_amount = -100
            expect { Wallet.new(bad_amount) }.to raise_error(ArgumentError)
        end
    end
    describe 'getter setter' do
        it 'should have cash set by constructor' do
            amount = 20
            wallet = Wallet.new(amount)
            expect(wallet.cash).to eq(amount)
        end
        it 'should not have a cash setter method' do
            wallet = Wallet.new(10)
            expect{ wallet.cash = 100 }.to raise_error(NoMethodError)
        end
    end
    describe 'withdraw' do
        it 'should remove valid amount' do
            amount = 20
            amount_to_remove = 10
            wallet = Wallet.new(amount)
            expect{ wallet.withdraw(amount_to_remove) }.not_to raise_error
            expect(wallet.cash).to eq(amount - amount_to_remove)
        end
        it 'should not withdraw too much' do
            amount = 20
            wallet = Wallet.new(amount)
            expect{ wallet.withdraw(amount + 1) }.to raise_error(InsufficientFundsError)
            expect( wallet.cash ).to eq(amount)
        end
        it 'should not withdraw negative money' do
            amount = 20
            wallet = Wallet.new(amount)
            expect{ wallet.withdraw(-1 * amount) }.to raise_error(ArgumentError)
            expect( wallet.cash ).to eq(amount)
        end
    end
end
