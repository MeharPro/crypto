import SwiftUI

struct BacktestView: View {
    @State private var symbol: String = "AAPL"
    @State private var startDate: Date = Calendar.current.date(byAdding: .year, value: -1, to: Date()) ?? Date()
    @State private var endDate: Date = Date()
    @State private var backtestResults: [String: Any]?
    @State private var isLoading = false
    @State private var errorMessage: String?

    var body: some View {
        Form {
            Section(header: Text("Parameters")) {
                TextField("Symbol", text: $symbol)
                DatePicker("Start Date", selection: $startDate, displayedComponents: .date)
                DatePicker("End Date", selection: $endDate, displayedComponents: .date)
            }

            Button(action: runBacktest) {
                if isLoading {
                    ProgressView()
                } else {
                    Text("Run Backtest")
                }
            }
            .disabled(isLoading)

            if let results = backtestResults {
                Section {
                    NavigationLink(destination: BacktestResultsView(results: results)) {
                        Text("View Results")
                    }
                }
            }

            if let error = errorMessage {
                Section {
                    Text(error).foregroundColor(.red)
                }
            }
        }
        .navigationTitle("Backtest")
    }

    func runBacktest() {
        isLoading = true
        errorMessage = nil

        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        let start = formatter.string(from: startDate)
        let end = formatter.string(from: endDate)

        let parameters: [String: Any] = [
            "symbol": symbol,
            "startDate": start,
            "endDate": end
        ]

        NetworkManager.shared.runBacktest(parameters: parameters) { result in
            DispatchQueue.main.async {
                isLoading = false
                switch result {
                case .success(let results):
                    self.backtestResults = results
                case .failure(let error):
                    self.errorMessage = "Error: \(error.localizedDescription)"
                }
            }
        }
    }
}

struct BacktestView_Previews: PreviewProvider {
    static var previews: some View {
        BacktestView()
    }
}
