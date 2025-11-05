import SwiftUI

struct ContentView: View {
    @State private var investmentAmount: String = "1000"
    @State private var riskLevel: Double = 50
    @State private var targetROI: Double = 10
    @State private var timeframe: String = "1M"
    @State private var botStatus: String = "Not Running"

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Investment")) {
                    TextField("Amount (USD)", text: $investmentAmount)
                        .keyboardType(.decimalPad)
                }

                Section(header: Text("Risk Level")) {
                    Slider(value: $riskLevel, in: 0...100, step: 1)
                    Text("\(Int(riskLevel))%")
                }

                Section(header: Text("Target ROI")) {
                    Slider(value: $targetROI, in: 1...200, step: 1)
                    Text("\(Int(targetROI))%")
                }

                Section(header: Text("Timeframe")) {
                    TextField("Timeframe", text: $timeframe)
                }

                Section(header: Text("Actions")) {
                    Button(action: startBot) {
                        Text("Start Trading Bot")
                    }
                    Button(action: stopBot) {
                        Text("Stop Trading Bot")
                    }
                }

                Section(header: Text("Dashboard")) {
                    NavigationLink(destination: DashboardView()) {
                        Text("View Live Dashboard")
                    }
                }

                Section(header: Text("Simulation")) {
                    NavigationLink(destination: BacktestView()) {
                        Text("Run Backtest")
                    }
                }

                Section(header: Text("Status")) {
                    Text(botStatus)
                }
            }
            .navigationTitle("Trading Bot")
            .onAppear(perform: fetchStatus)
        }
    }

    func startBot() {
        let parameters: [String: Any] = [
            "investmentAmount": Double(investmentAmount) ?? 0,
            "riskLevel": riskLevel,
            "targetROI": targetROI,
            "timeframe": timeframe
        ]

        NetworkManager.shared.startBot(parameters: parameters) { result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    self.botStatus = "Running"
                case .failure(let error):
                    self.botStatus = "Error: \(error.localizedDescription)"
                }
            }
        }
    }

    func stopBot() {
        NetworkManager.shared.stopBot { result in
            DispatchQueue.main.async {
                switch result {
                case .success:
                    self.botStatus = "Stopped"
                case .failure(let error):
                    self.botStatus = "Error: \(error.localizedDescription)"
                }
            }
        }
    }

    func fetchStatus() {
        NetworkManager.shared.getStatus { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let status):
                    self.botStatus = status["running"] as? Bool ?? false ? "Running" : "Not Running"
                case .failure(let error):
                    self.botStatus = "Error: \(error.localizedDescription)"
                }
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
