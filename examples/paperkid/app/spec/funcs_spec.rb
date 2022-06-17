require_relative '../funcs.rb'

describe 'PaperKid tests' do
    describe 'constructor' do
        it 'should instantiate' do
            expect{ pk = PaperKid.new }.not_to raise_error
        end
    end
    describe 'money collection' do
        it 'should call pay method of Customer' do
            @pk = PaperKid.new
            @customer_dbl = double("Customer")
            expect(@customer_dbl).to receive(:pay).with(10).and_return(10)
            @pk.collect_money(@customer_dbl, 10)
        end
        it 'should increment collected amount' do
            @pk = PaperKid.new
            @customer_dbl = double("Customer")
            allow(@customer_dbl).to receive(:pay).with(10).and_return(10)
            @pk.collect_money(@customer_dbl, 10)
            expect(@pk.collected_amount).to eq(10)
        end
    end
end