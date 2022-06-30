require_relative '../funcs.rb'

describe 'PaperKid tests' do
    describe 'constructor' do
        it 'should instantiate' do
            expect{ pk = PaperKid.new }.not_to raise_error
        end
    end
    describe 'money collection' do
        it 'should call pay method of Customer' do
            pk = PaperKid.new
            customer_dbl = double("Customer")
            amount = 10
            expect(customer_dbl).to receive(:pay).with(amount).and_return(amount)
            pk.collect_money(customer_dbl, amount)
        end
        it 'should increment collected amount' do
            pk = PaperKid.new
            customer_dbl = double("Customer")
            amount = 10
            allow(customer_dbl).to receive(:pay).with(amount).and_return(amount)
            pk.collect_money(customer_dbl, amount)
            expect(pk.collected_amount).to eq(amount)
        end
    end
end