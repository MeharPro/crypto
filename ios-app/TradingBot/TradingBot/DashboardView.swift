import SwiftUI

struct DashboardView: View {
    @State private var portfolioValue: String = "Loading..."
    @State private var recentTrades: [String] = []

    let timer = Timer.publish(every: 5, on: .main, in: .common).autoconnect()

    var body: some View {
        VStack {
            Text("Portfolio Value: \(portfolioValue)")
                .font(.largeTitle)

            List(recentTrades, id: \.self) { trade in
                Text(trade)
            }
        }
        .onReceive(timer) { _ in
            fetchStatus()
        }
        .onAppear(perform: fetchStatus)
        .navigationTitle("Dashboard")
    }

    func fetchStatus() {
        NetworkManager.shared.getStatus { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let status):
                    if let value = status["portfolio_value"] as? Double {
                        self.portfolioValue = String(format: "$%.2f", value)
                    }
                    if let trades = status["recent_trades"] as? [String] {
                        self.recentTrades = trades
                    }
                case .failure(let error):
                    self.portfolioValue = "Error"
                    print(error.localizedDescription)
                }
            }
        }
    }
}

struct DashboardView_Previews: PreviewProvider {
    static var previews: some View {
        DashboardView()
    }
}
